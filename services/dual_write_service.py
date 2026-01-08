"""
Serviço Dual Write: Sincronização automática entre alertas V1 e V2
Fase 3 - contrato-regional-ia
Autor: Copilot
Data: 08/01/2026
"""
import logging
from services import alert_service, alert_lifecycle_service
from typing import Dict, Any
from pathlib import Path

# Configuração de log dedicado
LOG_PATH = Path("logs/dual_write.log")
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def criar_alerta_dual(v1_alert_data: Dict[str, Any]) -> None:
    """
    Cria alerta V1 e replica no V2
    """
    try:
        # Criação no V1
        alerta_v1 = alert_service.criar_alerta(v1_alert_data)
        # Mapeamento para V2
        v2_data = mapear_v1_para_v2(alerta_v1)
        alerta_v2 = alert_lifecycle_service.criar_alerta_v2(v2_data)
        logging.info(f"DualWrite: alerta criado V1={alerta_v1['id']} V2={alerta_v2['id']}")
    except Exception as e:
        logging.error(f"Erro DualWrite criar_alerta_dual: {e}")

def atualizar_alerta_dual(v1_alert_id: str, changes: Dict[str, Any]) -> None:
    """
    Atualiza alerta V1 e sincroniza no V2
    """
    try:
        alert_service.atualizar_alerta(v1_alert_id, changes)
        v2_id = buscar_v2_por_v1(v1_alert_id)
        if v2_id:
            alert_lifecycle_service.atualizar_alerta_v2(v2_id, changes)
            logging.info(f"DualWrite: alerta atualizado V1={v1_alert_id} V2={v2_id}")
    except Exception as e:
        logging.error(f"Erro DualWrite atualizar_alerta_dual: {e}")

def sincronizar_acao_dual(v1_action_data: Dict[str, Any]) -> None:
    """
    Sincroniza ação administrativa V1 para V2
    """
    try:
        alert_service.registrar_acao(v1_action_data)
        v2_id = buscar_v2_por_v1(v1_action_data['alerta_id'])
        if v2_id:
            alert_lifecycle_service.registrar_acao_v2(v2_id, v1_action_data)
            logging.info(f"DualWrite: ação sincronizada V1={v1_action_data['id']} V2={v2_id}")
    except Exception as e:
        logging.error(f"Erro DualWrite sincronizar_acao_dual: {e}")

def mapear_v1_para_v2(alerta_v1: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mapeia campos do alerta V1 para V2
    """
    # Exemplo de mapeamento básico
    return {
        'contrato_id': alerta_v1.get('contrato_id'),
        'titulo': alerta_v1.get('titulo'),
        'descricao': alerta_v1.get('descricao'),
        'prazo': alerta_v1.get('prazo'),
        'responsavel': alerta_v1.get('responsavel'),
        # ... outros campos conforme necessário
    }

def buscar_v2_por_v1(v1_alert_id: str) -> str:
    """
    Busca o id do alerta V2 correspondente ao V1
    """
    # Implementação depende do modelo de dados
    # Exemplo: consulta por campo de referência cruzada
    return ""  # TODO: Implementar busca real

# TODO: Adicionar funções de rollback e auditoria
