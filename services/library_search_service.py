"""
Serviço de busca textual na Biblioteca (SQLite + FTS5).
Retorna resultados com snippet, página, doc info.
"""
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional

INDEX_PATH = Path(".cache/biblioteca_index.sqlite")


def search_library(query: str, category: Optional[str] = None, doc_type: Optional[str] = None, limit: int = 10) -> List[Dict]:
    conn = sqlite3.connect(INDEX_PATH)
    c = conn.cursor()
    sql = """
    SELECT d.title, d.category, d.doc_type, d.is_scanned, p.page_no, snippet(pages_fts, 2, '<mark>', '</mark>', '...', 20) as snippet
    FROM pages_fts
    JOIN documents d ON d.doc_id = pages_fts.doc_id
    JOIN pages p ON p.doc_id = d.doc_id AND p.page_no = pages_fts.page_no
    WHERE pages_fts.text MATCH ?
    """
    params = [query]
    if category:
        sql += " AND d.category = ?"
        params.append(category)
    if doc_type:
        sql += " AND d.doc_type = ?"
        params.append(doc_type)
    sql += " ORDER BY rank LIMIT ?"
    params.append(limit)
    c.execute(sql, params)
    results = []
    for row in c.fetchall():
        results.append({
            "title": row[0],
            "category": row[1],
            "doc_type": row[2],
            "is_scanned": bool(row[3]),
            "page_no": row[4],
            "snippet": row[5]
        })
    conn.close()
    return results
