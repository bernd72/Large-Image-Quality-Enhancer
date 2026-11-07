"""Insta360 X5 360-KI-Belichtungsoptimierer: reale, vortrainierte DPRNet-Inferenz.

Gewichte stammen nicht aus diesem Paket, sondern aus dem BSD-2-Clause-Projekt
https://github.com/raspberrypi/AI_enhance von Raspberry Pi Ltd. (2026).
Die Erzeugung der KI-Korrektur erfolgt EINMAL global auf einer verkleinerten
Kopie des 360-Panoramas; sie wird danach kachelfrei auf Originalpixel angewandt.
Keine Rekonstruktion fehlender Details; keine geometrischen Änderungen.
"""
from __future__ import annotations

import os
import sys
import time
import traceback
import tempfile
import queue
import threading
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageTk, ImageOps
from x5_denoise import MODEL_BASENAME, model_valid, download_models, load_session, denoise_rgb, denoise_full_export
from x5_batch import safe_export, result_path, eta_text

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ImportError:
    print('Tkinter fehlt in dieser Python-Installation.')
    raise


APP_TITLE = 'Insta360 X5 – Low-Light-KI DPRNet + SCUNet v3.3'
HERE = Path(__file__).resolve().parent
MODEL_SIZES = (512, 1024)
MODEL_URLS = {n: f'https://raw.githubusercontent.com/raspberrypi/AI_enhance/main/DPRNet_{n}.tflite'
              for n in MODEL_SIZES}
Image.MAX_IMAGE_PIXELS = None


def model_file(n: int) -> Path:
    return HERE / 'models' / f'DPRNet_{n}.tflite'


def validated_model(p: Path) -> bool:
    try:
        with p.open('rb') as f:
            header = f.read(8)
        return p.stat().st_size > 50000 and header[4:8] == b'TFL3'
    except OSError:
        return False


def download_model(n: int, report):
    """Download weights and verify TFLite header. Errors never masquerade as success."""
    dest = model_file(n)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if validated_model(dest):
        report(100, f'Vortrainiertes DPRNet-{n}-Modell bereits vorhanden')
        return dest
    tmp = dest.with_suffix('.download')
    req = urllib.request.Request(MODEL_URLS[n], headers={'User-Agent': 'Insta360-X5-KI/3.0'})
    try:
        with urllib.request.urlopen(req, timeout=50) as resp, tmp.open('wb') as out:
            total = int(resp.headers.get('Content-Length', '0'))
            read = 0
            while True:
                chunk = resp.read(256 * 1024)
                if not chunk:
                    break
                out.write(chunk)
                read += len(chunk)
                report(min(99, int(read / total * 100)) if total else 15,
                       f'KI-Modell herunterladen: {read / 1048576:.1f} MB')
        if not validated_model(tmp):
            raise RuntimeError('Heruntergeladene Datei ist kein gültiges TFLite-Modell.')
        tmp.replace(dest)
    finally:
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass
    report(100, f'Vortrainiertes DPRNet-{n}-Modell installiert')
    return dest


def extract_original_xmp_segments(jpg_path: Path):
    """Keep APP1 GPano/XMP segments, which Pillow does not always propagate."""
    segments = []
    with jpg_path.open('rb') as f:
        if f.read(2) != b'\xff\xd8':
            return []
        while True:
            sig = f.read(1)
            if not sig:
                break
            if sig != b'\xff':
                break
            marker = f.read(1)
            while marker == b'\xff':
                marker = f.read(1)
            if not marker or marker in (b'\xda', b'\xd9'):
                break
            if marker in [bytes([x]) for x in range(0xd0, 0xd8)]:
                continue
            n_bytes = f.read(2)
            if len(n_bytes) != 2:
                break
            n = int.from_bytes(n_bytes, 'big')
            if n < 2:
                break
            payload = f.read(n - 2)
            if marker == b'\xe1' and (payload.startswith(b'http://ns.adobe.com/xap/1.0/\x00') or
                                        payload.startswith(b'http://ns.adobe.com/xmp/extension/\x00') or
                                        b'GPano:' in payload):
                segments.append(b'\xff' + marker + n_bytes + payload)
    return segments


def insert_xmp(path: Path, xmp_segments):
    if not xmp_segments:
        return
    data = path.read_bytes()
    if data[:2] != b'\xff\xd8':
        return
    tmp = path.with_suffix('.xmp.tmp')
    tmp.write_bytes(data[:2] + b''.join(xmp_segments) + data[2:])
    tmp.replace(path)


def compute_gain_field(src: Image.Image, model_path: Path, strength: float, max_gain: float,
                       progress) -> np.ndarray:
    """Run REAL pretrained DPRNet on whole panorama (only once), at model input size.
    Return a smooth global RGB gain field. Full-resolution pixels are never inferred in tiles.
    """
    from ai_edge_litert.interpreter import Interpreter
    progress(5, 'Vortrainiertes KI-Modell laden')
    interp = Interpreter(model_path=str(model_path), num_threads=4)
    inp = interp.get_input_details()[0]
    shape = tuple(int(x) for x in inp['shape'])
    if len(shape) != 4 or shape[0] != 1 or shape[1] != 3:
        raise RuntimeError(f'Unerwartetes DPRNet-Eingabeformat: {shape} (erwartet [1,3,H,W])')
    h, w = shape[2], shape[3]
    if h not in MODEL_SIZES or w not in MODEL_SIZES:
        raise RuntimeError(f'Unerwartete Modellauflösung: {w} x {h}')
    if inp['dtype'] != np.float32:
        raise RuntimeError(f'Unerwarteter KI-Eingabedatentyp: {inp["dtype"]}')
    interp.allocate_tensors()
    progress(17, '360°-Gesamtbild als KI-Eingabe vorbereiten')
    small = np.asarray(src.convert('RGB').resize((w, h), Image.Resampling.BICUBIC), dtype=np.float32) / 255.0
    net_input = np.transpose(small, (2, 0, 1))[np.newaxis, ...].copy()
    interp.set_tensor(inp['index'], net_input)
    progress(32, 'Neuronale DPRNet-KI berechnet das Gesamtbild')
    interp.invoke()
    out_data = interp.get_tensor(interp.get_output_details()[0]['index'])
    if out_data.ndim != 4 or out_data.shape[0] != 1 or out_data.shape[1] != 3:
        raise RuntimeError(f'Unerwartetes KI-Ausgabeformat: {out_data.shape}')
    enhanced = np.transpose(out_data[0], (1, 2, 0))
    if enhanced.shape != small.shape:
        raise RuntimeError('KI-Ausgabe hat nicht die erwartete Bildgröße.')
    if not np.isfinite(enhanced).all():
        raise RuntimeError('KI-Modell lieferte ungültige Pixelwerte.')
    progress(63, 'Globale KI-Belichtungskorrektur berechnen')
    # Avoid extreme amplification in nearly-black JPEG pixels; full-res details stay original.
    # Smooth relative global illumination, 60% luminance gain, 40% channel-dependent gain.
    weights = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    orig_lum = np.sum(small * weights, axis=2, keepdims=True)
    enh_lum = np.sum(np.clip(enhanced, 0, 1.0) * weights, axis=2, keepdims=True)
    lum_ratio = np.maximum(enh_lum / (orig_lum + 0.025), 1.0)
    rgb_ratio = np.maximum(np.clip(enhanced, 0, 1.0) / (small + 0.025), 1.0)
    ratio = 0.75 * lum_ratio + 0.25 * rgb_ratio
    ratio = np.clip(ratio, 1.0, max_gain)
    ratio = 1.0 + strength * (ratio - 1.0)
    # Equirectangular 360° left/right edges join; force correction to be identical there.
    edge = max(12, round(w * 0.055))
    avg = (ratio[:, 0:1, :] + ratio[:, -1:, :]) * 0.5
    for j in range(edge):
        a = 1.0 - j / edge
        ratio[:, j:j+1, :] = ratio[:, j:j+1, :] * (1.0 - a) + avg * a
        ratio[:, -1-j:w-j, :] = ratio[:, -1-j:w-j, :] * (1.0 - a) + avg * a
    progress(100, 'Globale KI-Korrektur bereit')
    return ratio.astype(np.float32)


def transform_region(original: Image.Image, ratio: np.ndarray, box, extra_exposure=1.0, shadow_lift=0.0):
    """Apply one global gain field to genuine full-resolution pixels, without patch seams."""
    import cv2
    W, H = original.size
    x0, y0, x1, y1 = box
    nw = int(x1 - x0)
    nh = int(y1 - y0)
    gx = np.linspace(x0, x1 - 1, nw, dtype=np.float32) * (ratio.shape[1]-1) / max(W-1,1)
    gy = np.linspace(y0, y1 - 1, nh, dtype=np.float32) * (ratio.shape[0]-1) / max(H-1,1)
    mx = np.broadcast_to(gx, (nh,nw)).copy()
    my = np.broadcast_to(gy[:,None], (nh,nw)).copy()
    field = cv2.remap(ratio, mx, my, interpolation=cv2.INTER_LINEAR,
                      borderMode=cv2.BORDER_REPLICATE)
    src = np.asarray(original.crop(box).convert('RGB'), dtype=np.float32)
    # Prevent blown whites by tapering illumination boost for high-intensity pixels.
    protection = np.clip((255.0 - np.max(src,axis=2,keepdims=True))/110.0, 0.0, 1.0)
    effective = 1.0 + (field-1.0)*protection
    result = np.clip(src * effective * extra_exposure, 0, 255)
    # Global, seam-free shadow curve. 0=unchanged; 1=strong shadows.
    # Unlike multiplication, the curve makes near-black-but-nonzero values visible.
    # Blacks remain black; bright areas are smoothly protected.
    if shadow_lift > 0:
        pixels = result / 255.0
        lum = (0.2126*pixels[...,0] + 0.7152*pixels[...,1] +
               0.0722*pixels[...,2])[..., None]
        eps = 0.003
        gamma = 0.56
        curve = ((lum + eps)**gamma - eps**gamma) / ((1.0 + eps)**gamma - eps**gamma)
        # No abrupt threshold; preserve whites and highlights.
        dark_weight = np.maximum(0, 1.0 - 1.6*lum)**1.5
        lifted = lum + np.clip(shadow_lift, 0, 1) * np.maximum(curve-lum, 0) * dark_weight
        factor = np.where(lum > 0.0, lifted / np.maximum(lum, 1e-6), 1.0)
        pixels = np.clip(pixels * factor, 0, 1)
        result = pixels * 255.0
    return np.rint(result).astype(np.uint8)


def export_full(original_path: Path, ratio: np.ndarray, dest: Path, extra_exposure: float,
                progress, cancelled, shadow_lift=0.0):
    import gc
    with Image.open(original_path) as im:
        w, h = im.size
        if w / h != 2.0:
            raise RuntimeError(f'Das Bild hat kein 2:1-Seitenverhältnis: {w}x{h}')
        exif = im.info.get('exif')
        icc = im.info.get('icc_profile')
        xmp = extract_original_xmp_segments(original_path)
        tempdir = HERE / '_temp'
        tempdir.mkdir(exist_ok=True)
        mmap_file = tempdir / f'x5_output_{os.getpid()}.bin'
        try:
            mm = np.memmap(mmap_file, dtype=np.uint8, mode='w+', shape=(h,w,3))
            stripes = list(range(0,h,192))
            for i,y0 in enumerate(stripes):
                if cancelled():
                    raise InterruptedError('Export abgebrochen')
                y1=min(h,y0+192)
                mm[y0:y1] = transform_region(im,ratio,(0,y0,w,y1),extra_exposure,shadow_lift)
                progress(int(8+75*(i+1)/len(stripes)),
                         f'Originalpixel erhalten und KI-Korrektur übertragen: {i+1}/{len(stripes)}')
            mm.flush()
            progress(87,'JPG in voller Auflösung schreiben')
            options={'format':'JPEG','quality':95,'subsampling':0}
            if exif: options['exif'] = exif
            if icc: options['icc_profile'] = icc
            # Save to temp name so incomplete file is never presented as output.
            tmp_jpg=dest.with_name(dest.stem+'._unfertig.jpg')
            try:
                Image.fromarray(mm).save(tmp_jpg,**options)
                insert_xmp(tmp_jpg, xmp)
                tmp_jpg.replace(dest)
            finally:
                tmp_jpg.unlink(missing_ok=True)
            with Image.open(dest) as out:
                if out.size != (w,h):
                    raise RuntimeError('Exportprüfung fehlgeschlagen: Originalauflösung verloren')
            progress(100,f'Fertig: {dest.name} ({w}x{h})')
            del mm
        finally:
            try: del mm
            except NameError: pass
            gc.collect()
            try: mmap_file.unlink(missing_ok=True)
            except OSError: pass


def create_comparison(original: Image.Image,ratio:np.ndarray,center,extra_exposure,size=1600):
    w,h=original.size
    cw=min(size,w);ch=min(size,h)
    x0 = max(0,min(w-cw,int(center[0]*w)-cw//2))
    y0 = max(0,min(h-ch,int(center[1]*h)-ch//2))
    box=(x0,y0,x0+cw,y0+ch)
    before=original.crop(box).convert('RGB')
    after=Image.fromarray(transform_region(original,ratio,box,extra_exposure))
    comparison=Image.new('RGB',(2*cw,ch+60),(235,235,235))
    comparison.paste(before,(0,60));comparison.paste(after,(cw,60))
    d=ImageDraw.Draw(comparison)
    d.text((15,22),'VORHER – Original',fill=(0,0,0))
    d.text((cw+15,22),'NACHHER – vortrainiertes DPRNet',fill=(0,0,0))
    return comparison

class Gui:
    def __init__(self,root):
        self.root=root
        root.title(APP_TITLE)
        root.geometry('1100x795')
        root.minsize(760,590)
        self.file=None
        self.ratio=None
        self.center=(0.5,0.5)
        self.thumb=None
        self.tkthumb=None
        self.queue=queue.Queue()
        self.busy=False
        self.cancelled=False
        self.strength=tk.DoubleVar(value=0.40)
        self.maxgain=tk.DoubleVar(value=1.8)
        self.exposure=tk.DoubleVar(value=1.0)
        self.shadow_lift=tk.DoubleVar(value=0.60)
        self.size=tk.IntVar(value=1024)
        self.use_denoise=tk.BooleanVar(value=True)
        self.denoise_strength=tk.DoubleVar(value=0.60)
        self.detail_strength=tk.DoubleVar(value=0.08)
        self.preview_size=tk.IntVar(value=1024)
        self.status=tk.StringVar(value='Bitte ein JPG-Bild auswählen.')
        self.info=tk.StringVar(value='')
        self.eta=tk.StringVar(value='Restzeit: --')
        self.overwrite_original=tk.BooleanVar(value=False)
        self.job_start=None
        self._widgets()
        root.after(100,self._poll)

    def _widgets(self):
        # Die Hauptaktionen stehen bewusst OBERHALB der Panorama-Vorschau.
        # Sonst verschwinden sie auf Notebooks oder bei 125-150% Windows-Skalierung.
        # Scrollbare Hauptansicht: auf kleineren Windows-Displays bleiben auch
        # die Panorama-Vorschau und alle Optionen erreichbar.
        outer=ttk.Frame(self.root);outer.pack(fill='both',expand=True)
        self.main_canvas=tk.Canvas(outer,highlightthickness=0,borderwidth=0)
        main_scroll=ttk.Scrollbar(outer,orient='vertical',command=self.main_canvas.yview)
        self.main_canvas.configure(yscrollcommand=main_scroll.set)
        main_scroll.pack(side='right',fill='y')
        self.main_canvas.pack(side='left',fill='both',expand=True)
        frm=ttk.Frame(self.main_canvas,padding=9)
        self.main_window=self.main_canvas.create_window((0,0),window=frm,anchor='nw')
        frm.bind('<Configure>',lambda e:self.main_canvas.configure(scrollregion=self.main_canvas.bbox('all')))
        self.main_canvas.bind('<Configure>',lambda e:self.main_canvas.itemconfigure(self.main_window,width=e.width))
        self.root.bind('<MouseWheel>',lambda e:self.main_canvas.yview_scroll(-int(e.delta/120),'units'))
        self.root.bind('<Button-4>',lambda e:self.main_canvas.yview_scroll(-1,'units'))
        self.root.bind('<Button-5>',lambda e:self.main_canvas.yview_scroll(1,'units'))
        ttk.Label(frm,text='Insta360 X5 · Low-Light-KI · DPRNet + SCUNet',font=('Segoe UI',14,'bold')).pack(anchor='w')
        ttk.Label(frm,text='DPRNet fuer Helligkeit + SCUNet fuer Rauschen. Beide sind trainierte KI-Modelle.',foreground='#444').pack(anchor='w',pady=(1,5))

        row=ttk.Frame(frm);row.pack(fill='x',pady=(0,3))
        self.btn_file=ttk.Button(row,text='1. Original-JPG öffnen',command=self._pick_file)
        self.btn_file.pack(side='left',padx=(0,8))
        ttk.Label(row,textvariable=self.info).pack(side='left')

        opts=ttk.LabelFrame(frm,text='2. Vortrainiertes KI-Modell',padding=6);opts.pack(fill='x',pady=3)
        row2=ttk.Frame(opts);row2.pack(fill='x')
        for n in MODEL_SIZES:
            ttk.Radiobutton(row2,text=f'DPRNet {n}',variable=self.size,value=n).pack(side='left',padx=(0,7))
        self.btn_download=ttk.Button(row2,text='Modell herunterladen',command=self._download)
        self.btn_download.pack(side='left',padx=(3,7))
        ttk.Button(row2,text='Modelldatei auswählen',command=self._manual).pack(side='left')

        settings=ttk.LabelFrame(frm,text='3. KI-Belichtung + gezielte Schattenaufhellung',padding=6)
        settings.pack(fill='x',pady=3)
        for label,var,a,b in [('KI-Korrektur übernehmen',self.strength,0.2,1.0),
                              ('Maximale lokale Aufhellung',self.maxgain,1.2,5.0),
                              ('Zusätzliche Belichtung',self.exposure,1.0,1.6),
                              ('Schatten gezielt aufhellen',self.shadow_lift,0.0,1.0)]:
            line=ttk.Frame(settings);line.pack(fill='x',pady=1)
            ttk.Label(line,text=label,width=27).pack(side='left')
            ttk.Scale(line,from_=a,to=b,variable=var).pack(side='left',fill='x',expand=True,padx=5)
            ttk.Label(line,textvariable=var,width=18).pack(side='left')

        denoise=ttk.LabelFrame(frm,text='4. Zweites trainiertes KI-Modell: SCUNet (Rauschunterdrueckung)',padding=6)
        denoise.pack(fill='x',pady=3)
        line=ttk.Frame(denoise);line.pack(fill='x')
        ttk.Checkbutton(line,text='SCUNet bei Vergleich und Export anwenden',variable=self.use_denoise).pack(side='left',padx=(0,9))
        self.btn_scunet=ttk.Button(line,text='SCUNet herunterladen',command=self._download_scunet)
        self.btn_scunet.pack(side='left',padx=(0,7))
        ttk.Button(line,text='Modell-Dateien manuell waehlen',command=self._manual_scunet).pack(side='left')
        controls=ttk.Frame(denoise);controls.pack(fill='x')
        for label,var,a,b in [('KI-Entrauschung',self.denoise_strength,0.0,1.0),
                              ('Dezente Nachschaerfung',self.detail_strength,0.0,0.40)]:
            line=ttk.Frame(controls);line.pack(side='left',fill='x',expand=True,padx=(0,8))
            ttk.Label(line,text=label,width=23).pack(side='left')
            ttk.Scale(line,from_=a,to=b,variable=var).pack(side='left',fill='x',expand=True,padx=4)
            ttk.Label(line,textvariable=var,width=10).pack(side='left')
        hint=ttk.Frame(denoise);hint.pack(fill='x')
        ttk.Label(hint,text='Testgroesse (Originalpixel):').pack(side='left')
        ttk.Combobox(hint,textvariable=self.preview_size,values=(768,1024,1600),width=7,state='readonly').pack(side='left',padx=7)
        ttk.Label(hint,text='Tipp: erst 768 px testen; Vollbild mit SCUNet dauert auf CPU wesentlich laenger.',foreground='#555').pack(side='left')

        # Wichtig: immer vor dem dynamisch großen Canvas anzeigen.
        actions=ttk.LabelFrame(frm,text='5. KI-Optimierung STARTEN',padding=6)
        actions.pack(fill='x',pady=(6,3))
        self.btn_preview=ttk.Button(actions,text='KI-VERGLEICH STARTEN',command=self._comparison)
        self.btn_preview.pack(side='left',padx=(0,7))
        self.btn_export=ttk.Button(actions,text='GESAMTES 360°-BILD OPTIMIEREN',command=self._export)
        self.btn_export.pack(side='left',padx=(0,7))
        self.btn_batch=ttk.Button(actions,text='STAPELVERARBEITUNG ...',command=self._batch_dialog)
        self.btn_batch.pack(side='left',padx=(0,7))
        mode_row=ttk.Frame(actions);mode_row.pack(fill='x',pady=(5,0))
        ttk.Checkbutton(mode_row,
            text='Beim einzelnen Speichern Original-JPG ersetzen (mit Sicherungskopie)',
            variable=self.overwrite_original).pack(side='left')
        self.btn_cancel=ttk.Button(actions,text='Abbrechen',command=lambda:setattr(self,'cancelled',True),state='disabled')
        self.btn_cancel.pack(side='right',padx=(5,0))
        self.progress=ttk.Progressbar(frm,maximum=100)
        self.progress.pack(fill='x',pady=(4,2))
        ttk.Label(frm,textvariable=self.eta,foreground='#444').pack(anchor='w')
        ttk.Label(frm,textvariable=self.status,wraplength=980).pack(anchor='w',pady=(0,2))
        ttk.Label(frm,text='Erst Testbereich im Panorama anklicken, dann oben KI-VERGLEICH STARTEN.  Strg+P: Vergleich · Strg+E: Export',foreground='#555',wraplength=690).pack(anchor='w',pady=(0,3))

        imgframe=ttk.LabelFrame(frm,text='6. Gewuenschten Testbereich im 360°-Panorama anklicken',padding=5)
        imgframe.pack(fill='both',expand=True,pady=(1,0))
        self.preview=tk.Canvas(imgframe,background='#202020',highlightthickness=0,height=210)
        self.preview.pack(fill='both',expand=True)
        self.preview.bind('<Button-1>',self._click)
        self.preview.bind('<Configure>',lambda e:self._redraw())
        self.root.bind('<Control-p>',lambda e:self._comparison())
        self.root.bind('<Control-e>',lambda e:self._export())

    def _click(self,event):
        if not self.file or not self.tkthumb: return
        cw,ch=self.preview.winfo_width(),self.preview.winfo_height()
        tw,th=self.thumb.size
        sx=max(0,(cw-tw)//2); sy=max(0,(ch-th)//2)
        self.center=(max(0.0,min(1.0,(event.x-sx)/tw)),max(0.0,min(1.0,(event.y-sy)/th)))
        self._redraw()

    def _redraw(self):
        if self.thumb is None:return
        c=self.preview
        c.delete('all')
        cw=max(c.winfo_width(),1);ch=max(c.winfo_height(),1)
        tw,th=self.thumb.size
        sx=(cw-tw)//2; sy=(ch-th)//2
        self.tkthumb=ImageTk.PhotoImage(self.thumb)
        c.create_image(sx,sy,image=self.tkthumb,anchor='nw')
        x=sx+round(self.center[0]*tw); y=sy+round(self.center[1]*th)
        test_size=self.preview_size.get()
        rect_w=tw*test_size / max(self.full_dimensions[0],1)
        rect_h=th*test_size / max(self.full_dimensions[1],1)
        c.create_rectangle(x-rect_w/2,y-rect_h/2,x+rect_w/2,y+rect_h/2,outline='#00e5ff',width=2)
        c.create_line(x-9,y,x+9,y,fill='#00e5ff',width=2)
        c.create_line(x,y-9,x,y+9,fill='#00e5ff',width=2)

    def _pick_file(self):
        s=filedialog.askopenfilename(filetypes=[('JPG Bilder','*.jpg *.jpeg'),('Alle Dateien','*.*')])
        if not s:return
        self.file=Path(s)
        self.ratio=None
        with Image.open(s) as im:
            self.full_dimensions=im.size
            if im.width!=im.height*2:
                messagebox.showwarning('Kein 360°-Panorama','Das Bild hat nicht das für equirektanguläre 360°-Bilder typische 2:1-Format.')
            thumb=im.convert('RGB');thumb.thumbnail((955,390))
            self.thumb=thumb
        self.info.set(f'{self.file.name} · {self.full_dimensions[0]:,} × {self.full_dimensions[1]:,} Pixel')
        self.status.set('Original geladen. Nun Modell herunterladen und KI-Vergleich erzeugen.')
        self.root.after(100,self._redraw)

    def _progress(self,pct,msg):
        self.queue.put(('progress',pct,msg))

    def _run(self,fn):
        if self.busy:return
        self.busy=True;self.cancelled=False
        self.job_start=time.monotonic()
        self.eta.set('Restzeit: wird ermittelt ...')
        self.progress['value']=0
        for b in (self.btn_file,self.btn_preview,self.btn_export,self.btn_batch,self.btn_download,self.btn_scunet):b.configure(state='disabled')
        self.btn_cancel.configure(state='normal')
        def work():
            try:fn()
            except InterruptedError:
                self.queue.put(('cancelled', 'KI-Verarbeitung wurde abgebrochen. Vorhandene Originale bleiben erhalten.'))
            except Exception as exc:
                msg=f'{type(exc).__name__}: {exc}'
                self.queue.put(('error',msg,traceback.format_exc()))
            finally:self.queue.put(('end',))
        threading.Thread(target=work,daemon=True).start()

    def _poll(self):
        try:
            while True:
                x=self.queue.get_nowait()
                if x[0]=='progress':
                    self.progress['value']=x[1];self.status.set(x[2])
                    if self.job_start is not None:
                        elapsed=time.monotonic()-self.job_start
                        pct=float(x[1])
                        if pct >= 100:
                            self.eta.set('Restzeit: 0 Min.')
                        elif elapsed >= 8 and pct >= 2.5:
                            seconds=elapsed * (100.0 - pct) / max(pct, 1e-6)
                            self.eta.set(eta_text(seconds))
                elif x[0]=='error':
                    self.status.set('Fehler: '+x[1]); messagebox.showerror('KI-Verarbeitung fehlgeschlagen',x[1]+'\n\nFür Details siehe Terminalfenster.')
                    print(x[2],file=sys.stderr)
                elif x[0]=='done':
                    self.status.set(x[1]);messagebox.showinfo('Fertig',x[1])
                elif x[0]=='comparison':
                    self.status.set(x[1]); messagebox.showinfo('KI-Vergleich',x[1])
                elif x[0]=='cancelled':
                    self.status.set(x[1]);self.eta.set('Abgebrochen')
                    messagebox.showinfo('Abgebrochen',x[1])
                elif x[0]=='end':
                    self.busy=False;self.btn_cancel.configure(state='disabled')
                    self.job_start=None
                    for b in (self.btn_file,self.btn_preview,self.btn_export,self.btn_batch,self.btn_download,self.btn_scunet):b.configure(state='normal')
        except queue.Empty:pass
        self.root.after(120,self._poll)

    def _manual(self):
        n=int(self.size.get())
        s=filedialog.askopenfilename(title=f'DPRNet_{n}.tflite auswählen',filetypes=[('LiteRT Modell','*.tflite')])
        if not s:return
        if not validated_model(Path(s)):
            messagebox.showerror('Ungültiges Modell','Die Datei enthält kein gültiges TFLite-Modell.');return
        import shutil
        dest=model_file(n);dest.parent.mkdir(exist_ok=True);shutil.copy2(s,dest)
        self.status.set(f'Manuell hinzugefügtes KI-Modell: {dest.name}')

    def _download(self):
        n=int(self.size.get())
        self._run(lambda: (download_model(n,self._progress),self.queue.put(('done',f'DPRNet-{n} trainiertes KI-Modell ist installiert.'))))

    def _download_scunet(self):
        folder=HERE/'models'
        self._run(lambda: (download_models(folder,self._progress,lambda:self.cancelled),
                           self.queue.put(('done','SCUNet-ONNX-Modell vollstaendig installiert.'))))

    def _manual_scunet(self):
        src=filedialog.askopenfilename(title='scunet_color_real_psnr.onnx waehlen',
                                      filetypes=[('SCUNet ONNX','*.onnx')])
        if not src:return
        src=Path(src)
        if src.name!=MODEL_BASENAME or not model_valid(src.parent):
            messagebox.showerror('Modell unvollstaendig',
                'Bitte im selben Ordner BEIDE Dateien ablegen:\n'
                'scunet_color_real_psnr.onnx\nscunet_color_real_psnr.onnx.data')
            return
        import shutil
        dest=HERE/'models';dest.mkdir(exist_ok=True)
        if src.parent.resolve()!=dest.resolve():
            for basename in (MODEL_BASENAME, MODEL_BASENAME+'.data'):
                shutil.copy2(src.parent/basename,dest/basename)
        self.status.set('SCUNet-Modell aus den beiden Dateien uebernommen.')

    def _get_denoise(self, enabled):
        if not enabled:
            return None
        p=HERE/'models'/MODEL_BASENAME
        if not model_valid(p.parent):
            raise RuntimeError('SCUNet nicht installiert: Bitte auf SCUNet herunterladen klicken. '
                'Bei Proxy-407 beide Dateien ueber den Browser herunterladen und manuell waehlen.')
        self._progress(2,'SCUNet-KI (ONNX) laden')
        return load_session(p,threads=4)

    def _ratio_for_job(self,strength,maxgain,report=None,source=None):
        source=source or self.file
        if not source:raise RuntimeError('Bitte zuerst ein JPG auswählen.')
        n=int(self.size.get())
        p=model_file(n)
        if not validated_model(p):raise RuntimeError(f'KI-Modell DPRNet_{n}.tflite fehlt. Bitte zuerst herunterladen.')
        with Image.open(source) as im:
            return compute_gain_field(im,p,strength,maxgain,report or self._progress)

    def _comparison(self):
        if not self.file:
            messagebox.showwarning('Bild fehlt','Bitte zuerst ein JPG auswaehlen.');return
        strength,maxgain,exposure=float(self.strength.get()),float(self.maxgain.get()),float(self.exposure.get())
        shadow=float(self.shadow_lift.get())
        apply_scunet=bool(self.use_denoise.get())
        amount,sharp=float(self.denoise_strength.get()),float(self.detail_strength.get())
        size=int(self.preview_size.get())
        center=self.center
        def job():
            # First load both models, to catch model errors before any expensive work.
            session=self._get_denoise(apply_scunet)
            gain=self._ratio_for_job(strength,maxgain,lambda p,m:self._progress(int(p*0.64),m))
            with Image.open(self.file) as im:
                w,h=im.size
                cw,ch=min(size,w),min(size,h)
                x0=max(0,min(w-cw,int(center[0]*w)-cw//2))
                y0=max(0,min(h-ch,int(center[1]*h)-ch//2))
                box=(x0,y0,x0+cw,y0+ch)
                before=im.crop(box).convert('RGB')
                bright=transform_region(im,gain,box,exposure,shadow)
            if session is not None:
                enhanced=denoise_rgb(bright,session,amount,sharp,
                    lambda p,m:self._progress(65+int(p*0.34),m),lambda:self.cancelled)
                label='DPRNet + Schatten + SCUNet'
            else:
                enhanced=bright
                label='DPRNet + Schatten (ohne Entrauschung)'
            # Triptych when SCUNet is enabled: original, DPR only, DPR + denoiser.
            ncols=3 if session is not None else 2
            result=Image.new('RGB',(ncols*cw,ch+60),(236,236,236))
            result.paste(before,(0,60))
            result.paste(Image.fromarray(bright),(cw,60))
            if session is not None:
                result.paste(Image.fromarray(enhanced),(2*cw,60))
            d=ImageDraw.Draw(result)
            d.text((15,21),'1: ORIGINAL',fill=(0,0,0))
            d.text((cw+15,21),'2: DPRNet + SCHATTEN',fill=(0,0,0))
            if session is not None:
                d.text((2*cw+15,21),'3: DPRNet + SCUNet',fill=(0,0,0))
            dest=self.file.with_name(self.file.stem+'_DPRNet_SCUNet_Vergleich.jpg')
            result.save(dest,quality=95,subsampling=0)
            self._progress(100,'KI-Vergleich fertig')
            self.queue.put(('comparison',f'KI-Vergleich gespeichert:\n{dest}\n\nBei SCUNet: Original / nur DPRNet / DPRNet + SCUNet.'))
            if sys.platform=='win32':
                try:os.startfile(str(dest))
                except OSError:pass
        self._run(job)

    def _current_settings(self):
        """Read Tk variables only from the GUI thread."""
        return dict(strength=float(self.strength.get()), maxgain=float(self.maxgain.get()),
                    exposure=float(self.exposure.get()), shadow=float(self.shadow_lift.get()),
                    scunet=bool(self.use_denoise.get()),
                    amount=float(self.denoise_strength.get()), sharp=float(self.detail_strength.get()))

    def _render_one(self, src: Path, dest: Path, cfg: dict, session, report):
        """Full 360 export into a caller-supplied temporary destination."""
        ratio=self._ratio_for_job(cfg['strength'],cfg['maxgain'],
                                  lambda p,m:report(p*0.07,m), source=src)
        if self.cancelled:
            raise InterruptedError('Verarbeitung abgebrochen')
        def pmap(p,m):
            report(7 + 0.92*p,m)
        if session is None:
            export_full(src,ratio,dest,cfg['exposure'],pmap,
                        lambda:self.cancelled,cfg['shadow'])
        else:
            denoise_full_export(src,ratio,dest,cfg['exposure'],session,
                cfg['amount'],cfg['sharp'],transform_region,
                extract_original_xmp_segments,insert_xmp,HERE,
                pmap,lambda:self.cancelled,shadow_lift=cfg['shadow'])
        if self.cancelled:
            raise InterruptedError('Verarbeitung abgebrochen')

    def _export(self):
        if not self.file:
            messagebox.showwarning('Bild fehlt','Bitte zuerst ein JPG auswählen.');return
        src=self.file.resolve()
        overwrite=bool(self.overwrite_original.get())
        if overwrite:
            dest=src
            if not messagebox.askyesno('Original-JPG wirklich ersetzen?',
                'Die bearbeitete Datei ersetzt das Original-JPG.\n'
                'Vorher wird automatisch eine unveränderte Sicherungskopie erstellt.\n\n'
                'Original: '+str(src)+'\n\nFortfahren?',icon='warning'):
                return
        else:
            chosen=filedialog.asksaveasfilename(defaultextension='.jpg',
                initialfile=src.stem+'_DPRNet_SCUNet_KI.jpg',filetypes=[('JPG-Bild','*.jpg')])
            if not chosen:return
            dest=Path(chosen).resolve()
            if dest==src:
                if not messagebox.askyesno('Original-JPG ersetzen?',
                    'Du hast das Original als Speicherziel ausgewählt.\n'
                    'Soll es wirklich durch das KI-Bild ersetzt werden?\n'
                    'Eine Sicherungskopie wird automatisch angelegt.',icon='warning'):
                    return
                overwrite=True
            elif dest.exists() and not messagebox.askyesno('Vorhandenes Bild ersetzen?',
                f'Eine Datei mit dem Namen {dest.name} existiert bereits.\n\n'
                'Soll die vorhandene Ergebnisdatei überschrieben werden?',icon='warning'):
                return
        cfg=self._current_settings()
        if cfg['scunet'] and not messagebox.askyesno('Vollbild-KI auf CPU',
            'SCUNet kann bei 71 MP sehr lange benötigen.\n'
            'Hast du zuerst einen Testausschnitt geprüft und möchtest du jetzt exportieren?'):
            return
        def job():
            session=self._get_denoise(cfg['scunet'])
            self._progress(1,'KI-Export vorbereiten')
            backup=safe_export(src,dest,
                lambda temp:self._render_one(src,temp,cfg,session,self._progress),
                backup_original=True)
            note='\nUnverändertes Original gesichert unter:\n'+str(backup) if backup else ''
            self._progress(100,'Bild erfolgreich gespeichert')
            self.queue.put(('done',f'KI-Bild in Originalauflösung gespeichert:\n{dest}{note}'))
        self._run(job)

    def _batch_dialog(self):
        """Separate dialog keeps the existing single-image UI compact."""
        if self.busy:return
        d=tk.Toplevel(self.root)
        d.title('Stapelverarbeitung – mehrere Insta360 JPGs')
        d.geometry('760x565')
        d.minsize(600,470)
        d.transient(self.root)
        files=[]
        mode=tk.StringVar(value='new')
        backup=tk.BooleanVar(value=True)
        out_dir=tk.StringVar(value=str(self.file.parent if self.file else Path.home()))
        frm=ttk.Frame(d,padding=12);frm.pack(fill='both',expand=True)
        ttk.Label(frm,text='Stapelverarbeitung mit DPRNet + SCUNet',font=('Segoe UI',13,'bold')).pack(anchor='w')
        ttk.Label(frm,text='Alle gewählten JPGs werden mit denselben aktuellen KI-Einstellungen verarbeitet.',
                  wraplength=700).pack(anchor='w',pady=(2,8))
        lb_frame=ttk.Frame(frm);lb_frame.pack(fill='both',expand=True)
        lb=tk.Listbox(lb_frame,selectmode='extended',height=10)
        sb=ttk.Scrollbar(lb_frame,orient='vertical',command=lb.yview)
        lb.configure(yscrollcommand=sb.set)
        lb.pack(side='left',fill='both',expand=True);sb.pack(side='right',fill='y')
        count=tk.StringVar(value='0 Bilder ausgewählt')
        def refresh():
            lb.delete(0,'end')
            for f in files:lb.insert('end',str(f))
            count.set(f'{len(files)} Bilder ausgewählt')
        def add():
            new=filedialog.askopenfilenames(parent=d,title='JPG-Dateien zur Stapelverarbeitung',
                            filetypes=[('JPG-Bilder','*.jpg *.jpeg'),('Alle Dateien','*.*')])
            seen=set(files)
            for name in new:
                p=Path(name).resolve()
                if p not in seen and p.suffix.lower() in ('.jpg','.jpeg'):
                    files.append(p);seen.add(p)
            if files and not self.file:out_dir.set(str(files[0].parent))
            refresh()
        def remove():
            for i in reversed(lb.curselection()):del files[i]
            refresh()
        buttons=ttk.Frame(frm);buttons.pack(fill='x',pady=(6,8))
        ttk.Button(buttons,text='JPGs hinzufügen ...',command=add).pack(side='left',padx=(0,8))
        ttk.Button(buttons,text='Markierte entfernen',command=remove).pack(side='left',padx=(0,8))
        ttk.Button(buttons,text='Liste leeren',command=lambda:(files.clear(),refresh())).pack(side='left')
        ttk.Label(buttons,textvariable=count).pack(side='right')
        options=ttk.LabelFrame(frm,text='Speichern',padding=8);options.pack(fill='x',pady=(0,7))
        for label, val in [
            ('Neue Dateien mit Zusatz _DPRNet_SCUNet_KI erzeugen (empfohlen)', 'new'),
            ('Vorhandene KI-Ergebnisdateien ersetzen; Originale behalten', 'replace_results'),
            ('Original-JPGs direkt überschreiben (nur nach Sicherheitsabfrage)', 'replace_originals')]:
            ttk.Radiobutton(options,text=label,variable=mode,value=val).pack(anchor='w')
        backup_ck=ttk.Checkbutton(options,text='Vor Überschreiben der Originale unveränderte Sicherung anlegen (empfohlen)',
                                   variable=backup)
        backup_ck.pack(anchor='w',padx=18,pady=(2,0))
        dest_frame=ttk.Frame(options);dest_frame.pack(fill='x',pady=(5,0))
        ttk.Label(dest_frame,text='Ausgabeordner:').pack(side='left')
        out_entry=ttk.Entry(dest_frame,textvariable=out_dir)
        out_entry.pack(side='left',fill='x',expand=True,padx=7)
        def browse():
            p=filedialog.askdirectory(parent=d,title='Ausgabeordner wählen',initialdir=out_dir.get())
            if p:out_dir.set(p)
        out_button=ttk.Button(dest_frame,text='Durchsuchen ...',command=browse)
        out_button.pack(side='left')
        def change_mode(*_):
            orig=mode.get()=='replace_originals'
            out_entry.configure(state='disabled' if orig else 'normal')
            out_button.configure(state='disabled' if orig else 'normal')
            backup_ck.configure(state='normal' if orig else 'disabled')
        mode.trace_add('write',change_mode);change_mode()
        footer=ttk.Frame(frm);footer.pack(fill='x',pady=(4,0))
        ttk.Button(footer,text='Schließen',command=d.destroy).pack(side='right',padx=(8,0))
        def start():
            if not files:
                messagebox.showwarning('Keine Bilder','Bitte zuerst JPG-Dateien hinzufügen.',parent=d);return
            paths=list(files)
            selected_mode=mode.get()
            if selected_mode!='replace_originals' and not out_dir.get().strip():
                messagebox.showerror('Ausgabeordner fehlt','Bitte einen Ausgabeordner wählen.',parent=d);return
            folder=Path(out_dir.get()).resolve() if selected_mode!='replace_originals' else None
            if selected_mode=='replace_originals':
                confirm=messagebox.askyesno('Achtung: Originale überschreiben',
                    f'{len(paths)} ORIGINAL-JPG-Dateien werden nach erfolgreicher KI-Verarbeitung ersetzt.\n'
                    + ('Für jede Datei wird zuvor eine unveränderte Sicherung erstellt.\n' if backup.get()
                       else 'DU HAST DIE SICHERUNGSKOPIEN DEAKTIVIERT!\n')
                    +'\nMöchtest du wirklich fortfahren?',icon='warning',parent=d)
                if not confirm:return
            if selected_mode=='replace_results':
                existing=sum((folder / (p.stem+'_DPRNet_SCUNet_KI.jpg')).exists() for p in paths)
                if existing and not messagebox.askyesno('Vorhandene KI-Bilder ersetzen',
                    f'{existing} bereits vorhandene KI-Ergebnisdateien werden ersetzt. Fortfahren?',
                    icon='warning',parent=d):return
            d.destroy()
            self._batch_export(paths,selected_mode,folder,bool(backup.get()))
        ttk.Button(footer,text='STAPELVERARBEITUNG STARTEN',command=start).pack(side='right')
        refresh()

    def _batch_export(self, paths: list[Path], mode: str, folder: Path | None, backup: bool):
        cfg=self._current_settings()
        n=len(paths)
        def job():
            # File headers are enough; no full image decoded during planning.
            dimensions=[]
            for p in paths:
                with Image.open(p) as im:
                    dimensions.append(im.size)
            weights=[w*h for w,h in dimensions]
            total_weight=max(sum(weights),1)
            completed=0
            successful=[]
            failed=[]
            reserved=set()
            session=self._get_denoise(cfg['scunet'])
            for idx,(src,wh,weight) in enumerate(zip(paths,dimensions,weights)):
                if self.cancelled:
                    break
                def report(pct,msg,idx=idx,src=src,weight=weight,completed=completed):
                    # Report total *pixel-weighted* progress for realistic large-image ETAs.
                    fraction=(completed + weight*max(0,min(100,pct))/100)/total_weight
                    self._progress(100*fraction,f'Bild {idx+1}/{n} – {src.name}: {msg}')
                try:
                    if wh[0] != 2*wh[1]:
                        raise ValueError(f'Kein equirektanguläres 2:1-Panorama: {wh[0]}x{wh[1]}')
                    dest=result_path(src,folder if folder is not None else src.parent,mode,reserved)
                    if mode=='replace_results' and dest in reserved:
                        raise ValueError('Gleichnamige Bilder aus verschiedenen Ordnern: Bitte getrennt verarbeiten.')
                    reserved.add(dest)
                    report(0,'KI-Verarbeitung vorbereiten')
                    saved_backup=safe_export(src,dest,
                       lambda temp:self._render_one(src,temp,cfg,session,report),
                       backup_original=backup)
                    successful.append((str(dest),str(saved_backup) if saved_backup else ''))
                except InterruptedError:
                    self.cancelled=True
                    break
                except Exception as exc:
                    failed.append((src.name,str(exc)))
                    report(100,f'Fehler: {type(exc).__name__}: {exc}')
                finally:
                    completed+=weight
            count=len(successful)
            lines=[f'Stapellauf: {count} von {n} Bildern erfolgreich verarbeitet.']
            if mode=='replace_originals':
                lines.append('Originale ersetzt.'+(' Sicherungskopien angelegt.' if backup else ' OHNE Sicherungen.'))
            if failed:
                lines.append(f'{len(failed)} Fehler:')
                lines.extend(f'- {name}: {reason}' for name,reason in failed[:8])
                if len(failed)>8:lines.append(f'... und {len(failed)-8} weitere Fehler.')
            if self.cancelled:lines.append('Stapelverarbeitung vorzeitig abgebrochen.')
            self._progress(100 if not self.cancelled else 100*completed/total_weight,
                           f'Stapelverarbeitung: {count} erfolgreich, {len(failed)} fehlgeschlagen')
            self.queue.put(('done','\n'.join(lines)))
        self._run(job)


def main():
    root=tk.Tk();gui=Gui(root)
    root.mainloop()

if __name__=='__main__':main()
