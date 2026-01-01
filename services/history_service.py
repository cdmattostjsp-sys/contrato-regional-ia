import os
import sqlite3
import json
from datetime import datetime
import streamlit as st

def get_db_path():
    # Prioriza st.secrets, senão usa data/history.db
    db_path = None
    try:
        db_path = st.secrets.get("HISTORY_DB_PATH", None)
    except Exception:
        pass
    if not db_path:
        os.makedirs("data", exist_ok=True)
        db_path = os.path.join("data", "history.db")
    return db_path

def init_history_db(db_path=None):
    db_path = db_path or get_db_path()
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS contract_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                contract_id TEXT,
                contract_numero TEXT,
                actor TEXT,
                source TEXT,
                event_type TEXT,
                title TEXT,
                details TEXT,
                metadata_json TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        st.warning(f"Não foi possível inicializar o banco de histórico: {e}")

def log_event(contract, event_type, title, details, source, actor="Sistema", metadata=None, db_path=None):
    db_path = db_path or get_db_path()
    init_history_db(db_path)
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO contract_history (
                timestamp, contract_id, contract_numero, actor, source, event_type, title, details, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            str(contract.get("id", "")),
            str(contract.get("numero", "")),
            actor,
            source,
            event_type,
            title,
            details,
            json.dumps(metadata or {})
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        st.warning(f"Não foi possível registrar evento no histórico: {e}")

def list_events(contract_id, date_from=None, date_to=None, event_type=None, source=None, limit=200, db_path=None):
    db_path = db_path or get_db_path()
    init_history_db(db_path)
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        query = "SELECT id, timestamp, contract_id, contract_numero, actor, source, event_type, title, details, metadata_json FROM contract_history WHERE contract_id = ?"
        params = [str(contract_id)]
        if date_from:
            query += " AND timestamp >= ?"
            params.append(date_from)
        if date_to:
            query += " AND timestamp <= ?"
            params.append(date_to)
        if event_type and event_type != "Todos":
            query += " AND event_type = ?"
            params.append(event_type)
        if source and source != "Todos":
            query += " AND source = ?"
            params.append(source)
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        c.execute(query, params)
        rows = c.fetchall()
        conn.close()
        events = []
        for row in rows:
            events.append({
                "id": row[0],
                "timestamp": row[1],
                "contract_id": row[2],
                "contract_numero": row[3],
                "actor": row[4],
                "source": row[5],
                "event_type": row[6],
                "title": row[7],
                "details": row[8],
                "metadata_json": row[9],
            })
        return events
    except Exception as e:
        st.warning(f"Não foi possível buscar eventos do histórico: {e}")
        return []

def get_event_types(contract_id, db_path=None):
    db_path = db_path or get_db_path()
    init_history_db(db_path)
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT DISTINCT event_type FROM contract_history WHERE contract_id = ?", (str(contract_id),))
        types = [row[0] for row in c.fetchall() if row[0]]
        conn.close()
        return types
    except Exception:
        return []

def get_sources(contract_id, db_path=None):
    db_path = db_path or get_db_path()
    init_history_db(db_path)
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT DISTINCT source FROM contract_history WHERE contract_id = ?", (str(contract_id),))
        sources = [row[0] for row in c.fetchall() if row[0]]
        conn.close()
        return sources
    except Exception:
        return []import os
import sqlite3
import json
from datetime import datetime
import streamlit as st

def get_db_path():
    # Prioriza st.secrets, senão usa data/history.db
    db_path = None
    try:
        db_path = st.secrets.get("HISTORY_DB_PATH", None)
    except Exception:
        pass
    if not db_path:
        os.makedirs("data", exist_ok=True)
        db_path = os.path.join("data", "history.db")
    return db_path

def init_history_db(db_path=None):
    db_path = db_path or get_db_path()
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS contract_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                contract_id TEXT,
                contract_numero TEXT,
                actor TEXT,
                source TEXT,
                event_type TEXT,
                title TEXT,
                details TEXT,
                metadata_json TEXT
            )
            """
        )
        conn.commit()
        conn.close()
    except Exception as e:
        st.warning(f"Não foi possível inicializar o histórico: {e}")

def log_event(contract, event_type, title, details, source, actor="Sistema", metadata=None, db_path=None):
    db_path = db_path or get_db_path()
    try:
        init_history_db(db_path)
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        timestamp = datetime.now().isoformat()
        contract_id = str(contract.get("id", ""))
        contract_numero = str(contract.get("numero", ""))
        metadata_json = json.dumps(metadata or {}, ensure_ascii=False)
        c.execute(
            """
            INSERT INTO contract_history (timestamp, contract_id, contract_numero, actor, source, event_type, title, details, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                contract_id,
                contract_numero,
                actor,
                source,
                event_type,
                title,
                details,
                metadata_json
            )
        )
        conn.commit()
        conn.close()
    except Exception as e:
        st.warning(f"Não foi possível registrar evento no histórico: {e}")

def list_events(contract_id, date_from=None, date_to=None, event_type=None, source=None, limit=200, db_path=None):
    db_path = db_path or get_db_path()
    try:
        init_history_db(db_path)
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        query = "SELECT id, timestamp, contract_id, contract_numero, actor, source, event_type, title, details, metadata_json FROM contract_history WHERE contract_id = ?"
        params = [str(contract_id)]
        if date_from:
            query += " AND timestamp >= ?"
            params.append(date_from)
        if date_to:
            query += " AND timestamp <= ?"
            params.append(date_to)
        if event_type and event_type != "Todos":
            query += " AND event_type = ?"
            params.append(event_type)
        if source and source != "Todos":
            query += " AND source = ?"
            params.append(source)
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        c.execute(query, params)
        rows = c.fetchall()
        conn.close()
        events = []
        for row in rows:
            events.append({
                "id": row[0],
                "timestamp": row[1],
                "contract_id": row[2],
                "contract_numero": row[3],
                "actor": row[4],
                "source": row[5],
                "event_type": row[6],
                "title": row[7],
                "details": row[8],
                "metadata_json": row[9],
            })
        return events
    except Exception as e:
        st.warning(f"Não foi possível buscar eventos do histórico: {e}")
        return []
