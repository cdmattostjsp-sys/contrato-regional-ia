"""
Serviço de indexação incremental da Biblioteca (SQLite + FTS5).
Cria índice local em .cache/biblioteca_index.sqlite
"""
import sqlite3
import os
from pathlib import Path
from services.pdf_text_extractor import extract_pdf_pages, compute_sha256, get_mtime_size
from services.document_service import listar_documentos_disponiveis
from datetime import datetime

CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)
INDEX_PATH = CACHE_DIR / "biblioteca_index.sqlite"

# --- Criação e manutenção do índice ---
def ensure_index():
    conn = sqlite3.connect(INDEX_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        doc_id INTEGER PRIMARY KEY,
        path TEXT UNIQUE,
        title TEXT,
        category TEXT,
        doc_type TEXT,
        sha256 TEXT,
        mtime_size TEXT,
        indexed_at TEXT,
        text_char_count INTEGER,
        is_scanned INTEGER
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS pages (
        doc_id INTEGER,
        page_no INTEGER,
        text TEXT,
        PRIMARY KEY (doc_id, page_no)
    )""")
    c.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS pages_fts USING fts5(doc_id, page_no, text)
    """)
    conn.commit()
    return conn

def scan_knowledge_folder():
    """Lista PDFs e metadados da knowledge/"""
    return listar_documentos_disponiveis()

def needs_reindex(conn, path, sha256, mtime_size):
    c = conn.cursor()
    c.execute("SELECT sha256, mtime_size FROM documents WHERE path=?", (path,))
    row = c.fetchone()
    if not row:
        return True
    return row[0] != sha256 or row[1] != mtime_size

def index_pdf(conn, doc_meta):
    path = doc_meta["caminho"]
    title = doc_meta["nome"]
    category = doc_meta.get("categoria", "Outros")
    doc_type = doc_meta.get("tipo", "Outro")
    sha256 = compute_sha256(path)
    mtime_size = get_mtime_size(path)
    pages, is_scanned, char_count = extract_pdf_pages(path)
    c = conn.cursor()
    # Remove antigo
    c.execute("DELETE FROM pages WHERE doc_id = (SELECT doc_id FROM documents WHERE path=?)", (path,))
    c.execute("DELETE FROM pages_fts WHERE doc_id IN (SELECT doc_id FROM documents WHERE path=?)", (path,))
    # Upsert documento
    c.execute("INSERT OR REPLACE INTO documents (path, title, category, doc_type, sha256, mtime_size, indexed_at, text_char_count, is_scanned) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ",
        (path, title, category, doc_type, sha256, mtime_size, datetime.now().isoformat(), char_count, int(is_scanned)))
    c.execute("SELECT doc_id FROM documents WHERE path=?", (path,))
    doc_id = c.fetchone()[0]
    for page in pages:
        c.execute("INSERT INTO pages (doc_id, page_no, text) VALUES (?, ?, ?)", (doc_id, page["page_no"], page["text"]))
        c.execute("INSERT INTO pages_fts (doc_id, page_no, text) VALUES (?, ?, ?)", (doc_id, page["page_no"], page["text"]))
    conn.commit()

def build_or_update_index():
    conn = ensure_index()
    docs = scan_knowledge_folder()
    for doc in docs:
        path = doc["caminho"]
        sha256 = compute_sha256(path)
        mtime_size = get_mtime_size(path)
        if needs_reindex(conn, path, sha256, mtime_size):
            index_pdf(conn, doc)
    conn.close()

def get_index_status():
    conn = ensure_index()
    c = conn.cursor()
    c.execute("SELECT COUNT(*), SUM(text_char_count), MAX(indexed_at) FROM documents")
    row = c.fetchone()
    c.execute("SELECT COUNT(*) FROM pages")
    n_pages = c.fetchone()[0]
    conn.close()
    return {
        "n_docs": row[0] or 0,
        "total_chars": row[1] or 0,
        "last_indexed": row[2],
        "n_pages": n_pages
    }
