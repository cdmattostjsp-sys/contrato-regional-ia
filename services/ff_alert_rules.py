"""
Regras de Alertas para Execução Físico-Financeira
==================================================
Define regras objetivas e parametrizáveis para geração de alertas
baseados nos registros de execution_financial_service.

GOVERNANÇA: Sistema aponta, gestor decide, histórico registra.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from services.execution_financial_service import listar_por_contrato

# ========================================
# PARÂMETROS CONFIGURÁVEIS
# ========================================
DIAS_ALERTA_ATESTE_PENDENTE = 5  # Dias após emissão da NF sem ateste
DIAS_ALERTA_PAGAMENTO_ATRASADO = 30  # Dias após ateste sem pagamento
DIAS_ALERTA_STATUS_PARADO = 15  # Dias sem mudança de status

# Status considerados "em fluxo" (não geram alerta de parado)
STATUS_FINAIS = ["Pago", "Cancelado", "Glosado"]


def compute_ff_alerts_for_contract(contrato_id: str) -> List[Dict]:
    """
    Calcula alertas de execução físico-financeira para um contrato.
    
    Regras implementadas:
    1. FF_CRITICO: Ateste pendente há mais de X dias
    2. FF_ATENCAO: Pagamento atrasado após ateste
    3. FF_ATENCAO: Status parado (sem evolução)
    4. FF_INFO: ISS retido inconsistente
    
    Args:
        contrato_id: ID do contrato a analisar
        
    Returns:
        Lista de alertas com estrutura compatível com alert_service
    """
    registros = listar_por_contrato(contrato_id)
    alertas = []
    hoje = datetime.now()
    
    for registro in registros:
        # Converte datas string para datetime
        nf_data_emissao = _parse_date(registro.get('nf_data_emissao'))
        data_ateste = _parse_date(registro.get('data_ateste'))
        created_at = _parse_datetime(registro.get('created_at'))
        
        nf_numero = registro.get('nf_numero', 'N/A')
        competencia = registro.get('competencia', 'N/A')
        status_fluxo = registro.get('status_fluxo', 'Desconhecido')
        
        # REGRA 1: Ateste pendente há mais de X dias
        if _is_ateste_pendente(status_fluxo):
            if nf_data_emissao:
                dias_pendente = (hoje - nf_data_emissao).days
                if dias_pendente > DIAS_ALERTA_ATESTE_PENDENTE:
                    alertas.append({
                        'id': f"FF_ATESTE_PEND_{contrato_id}_{nf_numero}",
                        'tipo': 'critico',
                        'categoria': 'Execução Físico-Financeira',
                        'titulo': f'Ateste pendente: NF {nf_numero}',
                        'descricao': f"Nota Fiscal {nf_numero} (competência {competencia}) aguarda ateste há {dias_pendente} dias.",
                        'contrato_id': contrato_id,
                        'contrato_numero': contrato_id,  # Será atualizado no upsert
                        'data_alerta': hoje,
                        'acao_sugerida': 'ateste_nf',
                        'metadados_ff': {
                            'nf_numero': nf_numero,
                            'competencia': competencia,
                            'dias_pendente': dias_pendente,
                            'regra': 'ATESTE_PENDENTE'
                        }
                    })
        
        # REGRA 2: Pagamento atrasado após ateste
        if _is_status_atestado(status_fluxo) and data_ateste:
            dias_apos_ateste = (hoje - data_ateste).days
            if dias_apos_ateste > DIAS_ALERTA_PAGAMENTO_ATRASADO:
                alertas.append({
                    'id': f"FF_PGTO_ATRAS_{contrato_id}_{nf_numero}",
                    'tipo': 'atencao',
                    'categoria': 'Execução Físico-Financeira',
                    'titulo': f'Pagamento atrasado: NF {nf_numero}',
                    'descricao': f"Nota Fiscal {nf_numero} foi atestada há {dias_apos_ateste} dias, mas pagamento não foi registrado.",
                    'contrato_id': contrato_id,
                    'contrato_numero': contrato_id,
                    'data_alerta': hoje,
                    'acao_sugerida': 'verificar_pagamento',
                    'metadados_ff': {
                        'nf_numero': nf_numero,
                        'competencia': competencia,
                        'dias_apos_ateste': dias_apos_ateste,
                        'data_ateste': str(data_ateste),
                        'regra': 'PAGAMENTO_ATRASADO'
                    }
                })
        
        # REGRA 3: Status parado (sem evolução)
        if not _is_status_final(status_fluxo) and created_at:
            dias_sem_evolucao = (hoje - created_at).days
            if dias_sem_evolucao > DIAS_ALERTA_STATUS_PARADO:
                alertas.append({
                    'id': f"FF_STATUS_PARADO_{contrato_id}_{nf_numero}",
                    'tipo': 'atencao',
                    'categoria': 'Execução Físico-Financeira',
                    'titulo': f'Status sem evolução: NF {nf_numero}',
                    'descricao': f"Nota Fiscal {nf_numero} está com status '{status_fluxo}' há {dias_sem_evolucao} dias sem evolução.",
                    'contrato_id': contrato_id,
                    'contrato_numero': contrato_id,
                    'data_alerta': hoje,
                    'acao_sugerida': 'verificar_status',
                    'metadados_ff': {
                        'nf_numero': nf_numero,
                        'competencia': competencia,
                        'status_atual': status_fluxo,
                        'dias_sem_evolucao': dias_sem_evolucao,
                        'regra': 'STATUS_PARADO'
                    }
                })
        
        # REGRA 4: ISS retido inconsistente (informativo)
        incidencia_iss = registro.get('incidencia_iss', False)
        iss_retido = registro.get('iss_retido', 0.0)
        
        if incidencia_iss and iss_retido == 0:
            alertas.append({
                'id': f"FF_ISS_INCONS_{contrato_id}_{nf_numero}",
                'tipo': 'info',
                'categoria': 'Execução Físico-Financeira',
                'titulo': f'ISS inconsistente: NF {nf_numero}',
                'descricao': f"Nota Fiscal {nf_numero} tem incidência de ISS, mas valor retido é zero. Verificar se é correto.",
                'contrato_id': contrato_id,
                'contrato_numero': contrato_id,
                'data_alerta': hoje,
                'acao_sugerida': 'verificar_iss',
                'metadados_ff': {
                    'nf_numero': nf_numero,
                    'competencia': competencia,
                    'incidencia_iss': incidencia_iss,
                    'iss_retido': iss_retido,
                    'regra': 'ISS_INCONSISTENTE'
                }
            })
    
    return alertas


# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Converte string YYYY-MM-DD para datetime."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except Exception:
        return None


def _parse_datetime(datetime_str: Optional[str]) -> Optional[datetime]:
    """Converte string YYYY-MM-DD HH:MM:SS para datetime."""
    if not datetime_str:
        return None
    try:
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    except Exception:
        return None


def _is_ateste_pendente(status: str) -> bool:
    """Verifica se status indica ateste pendente."""
    status_lower = status.lower()
    return any(termo in status_lower for termo in ['pendente', 'aguardando', 'a atestar'])


def _is_status_atestado(status: str) -> bool:
    """Verifica se status indica que já foi atestado."""
    status_lower = status.lower()
    return 'atestado' in status_lower and 'pendente' not in status_lower


def _is_status_final(status: str) -> bool:
    """Verifica se status é considerado final (não gera alerta de parado)."""
    return status in STATUS_FINAIS


def get_estatisticas_ff(contrato_id: str) -> Dict:
    """
    Retorna estatísticas de execução FF para um contrato.
    
    Args:
        contrato_id: ID do contrato
        
    Returns:
        Dicionário com estatísticas agregadas
    """
    registros = listar_por_contrato(contrato_id)
    
    stats = {
        'total_registros': len(registros),
        'total_atestados': 0,
        'total_pendentes': 0,
        'total_pagos': 0,
        'valor_total_bruto': 0.0,
        'valor_total_iss': 0.0,
        'registros_por_status': {}
    }
    
    for registro in registros:
        status = registro.get('status_fluxo', 'Desconhecido')
        
        # Contadores
        if _is_status_atestado(status):
            stats['total_atestados'] += 1
        elif _is_ateste_pendente(status):
            stats['total_pendentes'] += 1
        
        if _is_status_final(status) and 'pago' in status.lower():
            stats['total_pagos'] += 1
        
        # Valores
        stats['valor_total_bruto'] += registro.get('valor_bruto', 0.0)
        stats['valor_total_iss'] += registro.get('iss_retido', 0.0)
        
        # Agrupamento por status
        if status not in stats['registros_por_status']:
            stats['registros_por_status'][status] = 0
        stats['registros_por_status'][status] += 1
    
    return stats
