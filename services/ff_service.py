"""
Serviço para gerenciamento de Execução Físico-Financeira de contratos.
Persistência em JSON: data/execution_financial_records.json
"""
import json
from pathlib import Path
from datetime import datetime

DATA_PATH = Path("data/execution_financial_records.json")

# --- Funções utilitárias de persistência ---
def load_all_records():
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_all_records(records):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2, default=str)

# --- CRUD Baseline do Contrato ---
def get_baseline(contract_id):
    records = load_all_records()
    for rec in records:
        if rec.get("contract_id") == contract_id and rec.get("type") == "baseline":
            return rec
    return None

def set_baseline(contract_id, baseline_data):
    records = load_all_records()
    found = False
    for i, rec in enumerate(records):
        if rec.get("contract_id") == contract_id and rec.get("type") == "baseline":
            records[i].update(baseline_data)
            found = True
            break
    if not found:
        baseline_data["contract_id"] = contract_id
        baseline_data["type"] = "baseline"
        records.append(baseline_data)
    save_all_records(records)

# --- CRUD Etapas ---
def get_etapas(contract_id):
    records = load_all_records()
    return [r for r in records if r.get("contract_id") == contract_id and r.get("type") == "etapa"]

def add_etapa(contract_id, etapa_data):
    etapa_data["contract_id"] = contract_id
    etapa_data["type"] = "etapa"
    records = load_all_records()
    records.append(etapa_data)
    save_all_records(records)

def update_etapa(etapa_id, etapa_data):
    records = load_all_records()
    for i, rec in enumerate(records):
        if rec.get("etapa_id") == etapa_id and rec.get("type") == "etapa":
            records[i].update(etapa_data)
            break
    save_all_records(records)

def delete_etapa(etapa_id):
    records = load_all_records()
    records = [r for r in records if not (r.get("etapa_id") == etapa_id and r.get("type") == "etapa")]
    save_all_records(records)

# --- CRUD Medições ---
def get_medicoes(contract_id):
    records = load_all_records()
    return [r for r in records if r.get("contract_id") == contract_id and r.get("type") == "medicao"]

def add_medicao(contract_id, medicao_data):
    medicao_data["contract_id"] = contract_id
    medicao_data["type"] = "medicao"
    records = load_all_records()
    records.append(medicao_data)
    save_all_records(records)

def update_medicao(medicao_id, medicao_data):
    records = load_all_records()
    for i, rec in enumerate(records):
        if rec.get("medicao_id") == medicao_id and rec.get("type") == "medicao":
            records[i].update(medicao_data)
            break
    save_all_records(records)

def delete_medicao(medicao_id):
    records = load_all_records()
    records = [r for r in records if not (r.get("medicao_id") == medicao_id and r.get("type") == "medicao")]
    save_all_records(records)

# --- CRUD Pagamentos ---
def get_pagamentos(contract_id):
    records = load_all_records()
    return [r for r in records if r.get("contract_id") == contract_id and r.get("type") == "pagamento"]

def add_pagamento(contract_id, pagamento_data):
    pagamento_data["contract_id"] = contract_id
    pagamento_data["type"] = "pagamento"
    records = load_all_records()
    records.append(pagamento_data)
    save_all_records(records)

def update_pagamento(pagamento_id, pagamento_data):
    records = load_all_records()
    for i, rec in enumerate(records):
        if rec.get("pagamento_id") == pagamento_id and rec.get("type") == "pagamento":
            records[i].update(pagamento_data)
            break
    save_all_records(records)

def delete_pagamento(pagamento_id):
    records = load_all_records()
    records = [r for r in records if not (r.get("pagamento_id") == pagamento_id and r.get("type") == "pagamento")]
    save_all_records(records)

# --- Funções de cálculo de KPIs e alertas ---
# (A implementar nos próximos passos)
