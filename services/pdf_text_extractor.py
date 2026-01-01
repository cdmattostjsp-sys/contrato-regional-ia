"""
Extração de texto de PDFs por página usando PyMuPDF.
Detecta PDFs digitalizados (sem texto pesquisável).
"""
import fitz  # PyMuPDF
from typing import List, Tuple
import hashlib
import os

def extract_pdf_pages(path: str) -> Tuple[List[dict], bool, int]:
    """
    Extrai texto de cada página do PDF.
    Retorna lista de dicts: [{page_no, text}], flag is_scanned, total_chars
    """
    doc = fitz.open(path)
    pages = []
    total_chars = 0
    for i, page in enumerate(doc):
        text = page.get_text("text")
        pages.append({"page_no": i+1, "text": text})
        total_chars += len(text)
    is_scanned = total_chars < 200  # Heurística: PDF sem texto pesquisável
    return pages, is_scanned, total_chars

def compute_sha256(path: str) -> str:
    """Calcula hash SHA256 do arquivo para detectar mudanças."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def get_mtime_size(path: str) -> str:
    stat = os.stat(path)
    return f"{stat.st_mtime}-{stat.st_size}"
