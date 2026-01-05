import json
import os
from datetime import datetime
from typing import List, Dict, Optional

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/execution_financial_records.json')

# Modelo de registro
# {
#   "id": str,  # UUID
#   "contrato_id": str,
#   "nf_numero": str,
#   "nf_data_emissao": str (YYYY-MM-DD),
#   "competencia": str,
#   "valor_bruto": float,
#   "iss_retido": float,
#   "incidencia_iss": bool,
#   "municipio_iss": str,
#   "aliquota_iss": float,
#   "data_ateste": str (YYYY-MM-DD),
#   "responsavel": str,
#   "observacoes": str,
#   "status_fluxo": str,
#   "created_at": str (YYYY-MM-DD HH:MM:SS)
# }

def _load_records() -> List[Dict]:
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return []

def _save_records(records: List[Dict]):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def criar_registro(registro: Dict) -> Optional[str]:
    """Cria novo registro, impede duplicidade por contrato + NF."""
    records = _load_records()
    for r in records:
        if r['contrato_id'] == registro['contrato_id'] and r['nf_numero'] == registro['nf_numero']:
            return None  # Duplicidade
    registro['id'] = f"{registro['contrato_id']}_{registro['nf_numero']}"
    registro['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    records.append(registro)
    _save_records(records)
    return registro['id']

def listar_por_contrato(contrato_id: str) -> List[Dict]:
    records = _load_records()
    return [r for r in records if r['contrato_id'] == contrato_id]

def filtrar(periodo_ini: Optional[str], periodo_fim: Optional[str], status: Optional[str], contrato_id: Optional[str]=None) -> List[Dict]:
    records = _load_records()
    def _match(r):
        if contrato_id and r['contrato_id'] != contrato_id:
            return False
        if status and r['status_fluxo'] != status:
            return False
        if periodo_ini:
            if r['data_ateste'] < periodo_ini:
                return False
        if periodo_fim:
            if r['data_ateste'] > periodo_fim:
                return False
        return True
    return [r for r in records if _match(r)]

def atualizar_status(registro_id: str, novo_status: str) -> bool:
    """
    Atualiza status de um registro e registra evento no histórico.
    
    Args:
        registro_id: ID do registro
        novo_status: Novo status a aplicar
        
    Returns:
        True se atualizado com sucesso, False caso contrário
    """
    records = _load_records()
    for r in records:
        if r['id'] == registro_id:
            status_anterior = r['status_fluxo']
            r['status_fluxo'] = novo_status
            _save_records(records)
            
            # Registra evento no histórico
            try:
                from services.history_service import log_event
                from services.contract_service import get_todos_contratos
                
                contrato_id = r['contrato_id']
                contratos = get_todos_contratos()
                contrato = next((c for c in contratos if c['id'] == contrato_id), None)
                
                if contrato:
                    log_event(
                        contract=contrato,
                        event_type="FF_STATUS_ATUALIZADO",
                        title=f"Status atualizado: NF {r.get('nf_numero')}",
                        details=f"Status alterado de '{status_anterior}' para '{novo_status}'",
                        source="Execução Físico-Financeira",
                        actor="Sistema",
                        metadata={
                            'registro_id': registro_id,
                            'nf_numero': r.get('nf_numero'),
                            'competencia': r.get('competencia'),
                            'status_anterior': status_anterior,
                            'status_novo': novo_status,
                            'valor_bruto': r.get('valor_bruto')
                        }
                    )
            except Exception as e:
                print(f"Aviso: Não foi possível registrar evento no histórico: {e}")
            
            return True
    return False

def seed_registros():
    """Adiciona registros fictícios para testes."""
    from random import randint, choice
    contratos = ['PNCP_001', 'PNCP_002']
    status_list = ['Atestado', 'Encaminhado para pagamento', 'Pago']
    municipios = ['São Paulo', 'Campinas', 'Ribeirão Preto']
    for i in range(5):
        registro = {
            'contrato_id': choice(contratos),
            'nf_numero': f'NF-{1000+i}',
            'nf_data_emissao': f'2025-12-{randint(1,28):02d}',
            'competencia': f'Dez/2025',
            'valor_bruto': float(randint(10000,20000)),
            'iss_retido': float(randint(500,1500)),
            'incidencia_iss': True,
            'municipio_iss': choice(municipios),
            'aliquota_iss': 5.0,
            'data_ateste': f'2025-12-{randint(1,28):02d}',
            'responsavel': 'Fiscal Teste',
            'observacoes': 'Registro de teste',
            'status_fluxo': choice(status_list)
        }
        criar_registro(registro)
