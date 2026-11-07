"""Sichere Ausgabe- und Zeitfunktionen fuer den Insta360-X5-Stapelmodus.

Wichtig: Ein Original wird niemals waehrend der Bildverarbeitung geoeffnet
und gleichzeitig veraendert. Erst nachdem eine vollstaendige, gepruefte
Ausgabe vorliegt, wird es optional atomar ersetzt.
"""
from __future__ import annotations

import math
import os
from pathlib import Path
import shutil
import tempfile
import time


def eta_text(seconds: float | None) -> str:
    """Rückgabe als Stunden und Minuten statt unlesbarer Sekundenzahlen."""
    if seconds is None or not math.isfinite(seconds) or seconds < 0:
        return 'Restzeit: wird ermittelt ...'
    if seconds < 60:
        return 'Restzeit: unter 1 Min.'
    mins = math.ceil(seconds / 60.0)
    hours, minutes = divmod(mins, 60)
    return (f'Restzeit: ca. {hours} Std. {minutes:02d} Min.' if hours
            else f'Restzeit: ca. {minutes} Min.')


def result_path(src: Path, out_dir: Path, mode: str,
                reserved: set[Path] | None = None) -> Path:
    """mode = new, replace_results oder replace_originals."""
    src = src.resolve()
    if mode == 'replace_originals':
        return src
    if mode not in ('new', 'replace_results'):
        raise ValueError(f'Unbekannter Speichermodus: {mode}')
    out_dir = out_dir.resolve()
    base = out_dir / f'{src.stem}_X5_Offline_KI.jpg'
    if base == src:
        raise ValueError('Ergebnisdatei darf nicht unbemerkt das Original ersetzen.')
    if mode == 'replace_results':
        return base
    reserved = reserved or set()
    if not base.exists() and base not in reserved:
        return base
    for idx in range(2, 100000):
        candidate = out_dir / f'{src.stem}_X5_Offline_KI_{idx}.jpg'
        if not candidate.exists() and candidate not in reserved and candidate != src:
            return candidate
    raise RuntimeError('Kein freier Ergebnis-Dateiname gefunden.')


def reserve_backup(src: Path) -> Path:
    stamp = time.strftime('%Y%m%d_%H%M%S')
    for num in range(1,100000):
        extra = '' if num == 1 else f'_{num}'
        name = f'{src.stem}_ORIGINAL_Sicherung_{stamp}{extra}{src.suffix}'
        p = src.with_name(name)
        if not p.exists():
            return p
    raise RuntimeError('Kein freier Sicherungsname gefunden.')


def safe_export(src: Path, dest: Path, render, *, backup_original: bool = True):
    """Render into a unique sibling tempfile and only afterwards replace dest.

    `render(tmp_path)` must write the finished JPG to the supplied temp path.
    The render method must close any original file handles before returning.
    Returns optional backup path. An exception leaves the original unchanged.
    """
    src = src.resolve()
    dest = dest.resolve()
    if not src.is_file():
        raise FileNotFoundError(src)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix='.x5_ki_unfertig_', suffix='.jpg', dir=dest.parent)
    os.close(fd)
    temp = Path(temp_name)
    backup = None
    try:
        temp.unlink(missing_ok=True)
        render(temp)
        if not temp.is_file() or temp.stat().st_size < 100:
            raise RuntimeError('Der KI-Export wurde nicht erfolgreich erstellt.')
        # Source already closed by render(). Back up the *unmodified* source.
        if src == dest and backup_original:
            backup = reserve_backup(src)
            shutil.copy2(src, backup)
            if not backup.is_file() or backup.stat().st_size != src.stat().st_size:
                raise RuntimeError('Sicherung des Originals fehlgeschlagen; es wird nicht ersetzt.')
        # Atomic when source/destination live on same volume (temp created as sibling).
        os.replace(temp, dest)
        return backup
    finally:
        temp.unlink(missing_ok=True)
