"""SCUNet-ONNX denoising for very large 360° images.

Weights: Heliosoph/scunet-onnx (Apache-2.0), ONNX export from
https://github.com/cszn/SCUNet. Both ONNX graph and .data weights required.

Uses REAL ONNX inference; never pretends to have neural output when unavailable.
Memory-bounded processing and smooth, normalized overlapping-tile blending.
"""
from __future__ import annotations

import gc
import os
from pathlib import Path
import urllib.request

import numpy as np
from PIL import Image

MODEL_BASENAME = 'scunet_color_real_psnr.onnx'
MODEL_URL_BASE = 'https://huggingface.co/Heliosoph/scunet-onnx/resolve/main/'
MODEL_FILES = (MODEL_BASENAME, MODEL_BASENAME + '.data')


def model_valid(folder: Path) -> bool:
    graph = folder / MODEL_FILES[0]
    weights = folder / MODEL_FILES[1]
    return (graph.is_file() and weights.is_file()
            and graph.stat().st_size > 100_000
            and weights.stat().st_size > 30_000_000)


def download_models(folder: Path, progress, cancelled=lambda: False) -> Path:
    """Download BOTH ONNX and external-data files; tolerate proxy failures explicitly."""
    folder.mkdir(parents=True, exist_ok=True)
    if model_valid(folder):
        progress(100, 'SCUNet-Modell bereits vorhanden')
        return folder / MODEL_BASENAME
    for index, basename in enumerate(MODEL_FILES):
        dest = folder / basename
        minimum = 100_000 if index == 0 else 30_000_000
        if dest.is_file() and dest.stat().st_size > minimum:
            continue
        tmp = folder / (basename + '.download')
        try:
            req = urllib.request.Request(MODEL_URL_BASE + basename + '?download=true',
                headers={'User-Agent': 'Mozilla/5.0 Insta360-Optimierer/3.1'})
            with urllib.request.urlopen(req, timeout=100) as resp, tmp.open('wb') as output:
                total = int(resp.headers.get('Content-Length', 0))
                count = 0
                while True:
                    if cancelled():
                        raise InterruptedError('Modell-Download abgebrochen')
                    chunk = resp.read(262144)
                    if not chunk:
                        break
                    output.write(chunk)
                    count += len(chunk)
                    frac = count / total if total else 0.3
                    progress(min(98, int((index + min(frac, 1)) * 50)),
                             f'SCUNet-Modelldatei {index+1}/2: {count / 1048576:.1f} MB geladen')
            if tmp.stat().st_size < minimum:
                raise RuntimeError(f'Zu kleine Modelldatei: {basename}')
            tmp.replace(dest)
        finally:
            tmp.unlink(missing_ok=True)
    if not model_valid(folder):
        raise RuntimeError('SCUNet-Modell unvollständig. Beide Dateien müssen im selben Ordner liegen.')
    progress(100, 'Trainiertes SCUNet-Modell heruntergeladen')
    return folder / MODEL_BASENAME


def load_session(model_path: Path, threads: int = 4):
    """Real pretrained RGB ONNX model, provided separately by author."""
    import onnxruntime as ort
    if not model_valid(model_path.parent):
        raise RuntimeError('SCUNet-Modell unvollständig; ONNX und ONNX.data werden benötigt.')
    opts = ort.SessionOptions()
    opts.intra_op_num_threads = max(1, threads)
    opts.inter_op_num_threads = 1
    opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    available=ort.get_available_providers()
    # Prefer hardware acceleration only if a DirectML runtime is already installed.
    providers=['DmlExecutionProvider','CPUExecutionProvider'] if 'DmlExecutionProvider' in available else ['CPUExecutionProvider']
    sess = ort.InferenceSession(str(model_path), sess_options=opts,providers=providers)
    inp = sess.get_inputs()[0]
    if len(inp.shape) != 4 or inp.shape[1] != 3:
        raise RuntimeError(f'SCUNet ONNX erwartet RGB NCHW, gefunden: {inp.shape}')
    return sess


def _cosine_weights(tile_size: int, overlap: int) -> np.ndarray:
    # Positive weights avoid NaNs at picture boundaries.
    ramp = np.arange(tile_size, dtype=np.float32)
    w = np.minimum(np.minimum((ramp + 1) / (overlap + 1),
                               (tile_size - ramp) / (overlap + 1)), 1.)
    return np.maximum(w, 1e-5)


def _reflect_indices(indices: np.ndarray, n: int) -> np.ndarray:
    if n <= 1:
        return np.zeros_like(indices)
    period = 2 * (n - 1)
    a = np.mod(indices, period)
    return np.where(a < n, a, period - a).astype(np.intp)


def denoise_rgb(rgb: np.ndarray, sess, strength: float, sharpen: float,
                progress=lambda pct,msg:None, cancelled=lambda:False,
                tile: int = 256, overlap: int = 64, wrap_horizontal: bool = False) -> np.ndarray:
    """Denoise RGB uint8 with real SCUNet ONNX, blended tile overlaps.

    Full panorama: horizontal input wraps only when wrap_horizontal=True.
    Cropped previews and vertical borders reflect. Output is feather-blended and restored to exact input dimensions.
    """
    import cv2
    if rgb.dtype != np.uint8 or rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError('RGB uint8 mit drei Kanälen erforderlich')
    if tile % 8 or not (0 < overlap < tile // 2):
        raise ValueError('Kachelgröße muss durch 8 teilbar sein; overlap < tile/2')
    h, w = rgb.shape[:2]
    if strength <= 0 and sharpen <= 0:
        return rgb.copy()
    step = tile - overlap
    xs = list(range(-overlap, w, step))
    ys = list(range(-overlap, h, step))
    total = len(xs) * len(ys)
    completed = 0
    taper = _cosine_weights(tile, overlap)
    weight2 = taper[:, None] * taper[None, :]
    accum = np.zeros((h, w, 3), dtype=np.float32)
    weights = np.zeros((h, w, 1), dtype=np.float32)
    input_name = sess.get_inputs()[0].name
    output_name = sess.get_outputs()[0].name
    for iy, y in enumerate(ys):
        yy = _reflect_indices(np.arange(y,y+tile,dtype=np.intp),h)
        # local indexes in returned crop
        out_y0, out_y1 = max(0,y), min(h,y+tile)
        out_ys = slice(out_y0-y,out_y1-y)
        for ix, x in enumerate(xs):
            if cancelled():
                raise InterruptedError('KI-Rauschunterdrückung abgebrochen')
            xs_idx=np.arange(x, x+tile, dtype=np.intp)
            xx = np.mod(xs_idx,w) if wrap_horizontal else _reflect_indices(xs_idx,w)
            patch = np.ascontiguousarray(rgb[yy[:, None],xx[None, :],:], dtype=np.float32) / 255.
            net_input = np.ascontiguousarray(patch.transpose(2,0,1)[None,...])
            net_output = sess.run([output_name], {input_name: net_input})[0]
            if net_output.shape != (1,3,tile,tile):
                raise RuntimeError(f'SCUNet-Ausgabeform falsch: {net_output.shape}')
            den = np.clip(net_output[0].transpose(1,2,0),0,1)*255.
            # ONNX inference may return a non-finite result; abort rather than export corrupt data.
            if not np.isfinite(den).all():
                raise RuntimeError('SCUNet gab ungültige Pixelwerte zurück')
            out_x0,out_x1=max(0,x),min(w,x+tile)
            out_xs=slice(out_x0-x,out_x1-x)
            patch_den = den[out_ys,out_xs]
            patch_original = rgb[out_y0:out_y1,out_x0:out_x1].astype(np.float32)
            mixed = patch_original*(1-strength)+patch_den*strength
            wa = weight2[out_ys,out_xs,None]
            accum[out_y0:out_y1,out_x0:out_x1] += mixed * wa
            weights[out_y0:out_y1,out_x0:out_x1] += wa
            completed += 1
            progress(round(100*completed/total), f'SCUNet-Kacheln: {completed}/{total}')
    cleaned = np.clip(accum / np.maximum(weights,1e-7),0,255)
    if sharpen > 0:
        soft = cv2.GaussianBlur(cleaned,(0,0),0.75,borderType=cv2.BORDER_REFLECT)
        cleaned = np.clip(cleaned + sharpen*(cleaned-soft),0,255)
    return np.rint(cleaned).astype(np.uint8)


def denoise_full_export(original_path: Path, ratio, dest: Path, exposure: float, session,
                        strength: float, sharpen: float, transform_region,
                        extract_xmp, insert_xmp, here:Path,
                        progress, cancelled, shadow_lift=0.0):
    """Bounded memory processing, overlapping vertical strips, original JPG size.

    Uses disk-based RGB memmap to avoid holding full 71 MP output in RAM.
    Overlapping strip halos and feathering prevent visible horizontal stripes.
    """
    with Image.open(original_path) as im:
        w,h = im.size
        exif, icc = im.info.get('exif'), im.info.get('icc_profile')
        xmp = extract_xmp(original_path)
        workdir = here / '_temp'
        workdir.mkdir(parents=True,exist_ok=True)
        mmap_path = workdir / f'x5_denoised_{os.getpid()}.raw'
        mm = None
        temp_jpg = dest.with_name(dest.stem+'._unfertig.jpg')
        try:
            mm = np.memmap(mmap_path,dtype=np.uint8,mode='w+',shape=(h,w,3))
            stripe_h, halo = 512, 96
            bands = list(range(0,h,stripe_h))
            prior_halo = None
            for ib, y0 in enumerate(bands):
                if cancelled():
                    raise InterruptedError('Export abgebrochen')
                y1 = min(h,y0+stripe_h)
                a,b = max(0,y0-halo), min(h,y1+halo)
                bright = transform_region(im,ratio,(0,a,w,b),exposure,shadow_lift)
                def prog(pct,msg):
                    progress(int(2+84*(ib+pct/100)/len(bands)),
                             f'Abschnitt {ib+1}/{len(bands)}: {msg}')
                filtered = denoise_rgb(bright,session,strength,sharpen,prog,cancelled,
                                       wrap_horizontal=(w == 2*h))
                start,end=y0-a,y1-a
                core = filtered[start:end].copy()
                if prior_halo is not None:
                    n=min(halo,len(prior_halo),len(core))
                    ramp=np.linspace(0,1,n,dtype=np.float32)[:,None,None]
                    core[:n] = np.clip(prior_halo[:n].astype(np.float32)*(1-ramp)
                                        +core[:n].astype(np.float32)*ramp,0,255).astype(np.uint8)
                mm[y0:y1] = core
                prior_halo = filtered[end:min(end+halo,filtered.shape[0])].copy()
                del bright,filtered,core
            mm.flush()
            progress(91,'JPG in voller Auflösung schreiben')
            opts=dict(format='JPEG',quality=95,subsampling=0)
            if exif: opts['exif']=exif
            if icc: opts['icc_profile']=icc
            Image.fromarray(mm).save(temp_jpg,**opts)
            insert_xmp(temp_jpg,xmp)
            with Image.open(temp_jpg) as check:
                if check.size != (w,h):
                    raise RuntimeError('Ausgabeauflösung konnte nicht bestätigt werden')
            temp_jpg.replace(dest)
            progress(100,f'Fertig: {dest.name}')
        finally:
            try:
                if mm is not None:
                    mm.flush()
                    del mm
            finally:
                gc.collect()
                mmap_path.unlink(missing_ok=True)
                temp_jpg.unlink(missing_ok=True)
