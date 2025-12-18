"""
Serviço de Alertas Contratuais
===============================
Gera e gerencia alertas automáticos baseados em regras de negócio.
"""

from datetime import datetime, timedelta
from typing import List, Dict


def calcular_alertas(contratos: List[Dict]) -> List[Dict]:
    """
    Calcula alertas automáticos para contratos.
    
    Args:
        contratos: Lista de contratos
        
    Returns:
        Lista de alertas ordenados por criticidade
    """
    alertas = []
    hoje = datetime.now()
    
    for contrato in contratos:
        # Verifica vigência
        data_fim = contrato.get('data_fim')
        if isinstance(data_fim, str):
            data_fim = datetime.fromisoformat(data_fim)
        
        if data_fim:
            dias_restantes = (data_fim - hoje).days
            
            # ALERTA CRÍTICO: Vigência < 60 dias
            if dias_restantes < 60 and dias_restantes >= 0:
                alertas.append({
                    'id': f"VIG_CRIT_{contrato['id']}",
                    'tipo': 'critico',
                    'categoria': 'Vigência',
                    'titulo': f'Vigência crítica: {dias_restantes} dias',
                    'descricao': f"Contrato {contrato['numero']} vence em {dias_restantes} dias. Providenciar prorrogação ou nova licitação urgentemente.",
                    'contrato_id': contrato['id'],
                    'contrato_numero': contrato['numero'],
                    'dias_restantes': dias_restantes,
                    'data_alerta': hoje,
                    'acao_sugerida': 'prorrogacao'
                })
            
            # ALERTA ATENÇÃO: Vigência 60-120 dias
            elif dias_restantes >= 60 and dias_restantes <= 120:
                alertas.append({
                    'id': f"VIG_ATEN_{contrato['id']}",
                    'tipo': 'atencao',
                    'categoria': 'Vigência',
                    'titulo': f'Vigência requer atenção: {dias_restantes} dias',
                    'descricao': f"Contrato {contrato['numero']} vence em {dias_restantes} dias. Planejar renovação ou nova contratação.",
                    'contrato_id': contrato['id'],
                    'contrato_numero': contrato['numero'],
                    'dias_restantes': dias_restantes,
                    'data_alerta': hoje,
                    'acao_sugerida': 'planejamento'
                })
            
            # ALERTA VENCIDO
            elif dias_restantes < 0:
                alertas.append({
                    'id': f"VIG_VENC_{contrato['id']}",
                    'tipo': 'critico',
                    'categoria': 'Vigência',
                    'titulo': f'Contrato VENCIDO há {abs(dias_restantes)} dias',
                    'descricao': f"Contrato {contrato['numero']} está VENCIDO. Verificar situação imediatamente.",
                    'contrato_id': contrato['id'],
                    'contrato_numero': contrato['numero'],
                    'dias_restantes': dias_restantes,
                    'data_alerta': hoje,
                    'acao_sugerida': 'verificacao'
                })
        
        # ALERTA STATUS CRÍTICO
        if contrato.get('status') == 'critico':
            alertas.append({
                'id': f"STATUS_CRIT_{contrato['id']}",
                'tipo': 'critico',
                'categoria': 'Status',
                'titulo': 'Contrato com status CRÍTICO',
                'descricao': f"Contrato {contrato['numero']} está marcado como crítico. Requer atenção imediata.",
                'contrato_id': contrato['id'],
                'contrato_numero': contrato['numero'],
                'data_alerta': hoje,
                'acao_sugerida': 'verificacao'
            })
        
        # ALERTA PENDÊNCIAS
        pendencias = contrato.get('pendencias', [])
        if pendencias:
            alertas.append({
                'id': f"PEND_{contrato['id']}",
                'tipo': 'atencao',
                'categoria': 'Pendências',
                'titulo': f'{len(pendencias)} pendência(s) identificada(s)',
                'descricao': f"Contrato {contrato['numero']}: {', '.join(pendencias[:2])}{'...' if len(pendencias) > 2 else ''}",
                'contrato_id': contrato['id'],
                'contrato_numero': contrato['numero'],
                'total_pendencias': len(pendencias),
                'data_alerta': hoje,
                'acao_sugerida': 'resolucao'
            })
        
        # ALERTA VALOR ALTO (> R$ 50M)
        valor = contrato.get('valor', 0)
        if valor > 50_000_000:
            alertas.append({
                'id': f"VALOR_ALTO_{contrato['id']}",
                'tipo': 'info',
                'categoria': 'Valor',
                'titulo': f'Contrato de alto valor: R$ {valor/1_000_000:.1f}M',
                'descricao': f"Contrato {contrato['numero']} possui valor elevado. Acompanhamento especial recomendado.",
                'contrato_id': contrato['id'],
                'contrato_numero': contrato['numero'],
                'valor': valor,
                'data_alerta': hoje,
                'acao_sugerida': 'acompanhamento'
            })
    
    # Ordena por criticidade e dias restantes
    prioridade = {'critico': 0, 'atencao': 1, 'info': 2}
    alertas.sort(key=lambda x: (prioridade.get(x['tipo'], 3), x.get('dias_restantes', 999)))
    
    return alertas


def get_alertas_por_tipo(alertas: List[Dict]) -> Dict[str, int]:
    """
    Conta alertas por tipo.
    
    Args:
        alertas: Lista de alertas
        
    Returns:
        Dicionário com contagens por tipo
    """
    contagens = {
        'critico': 0,
        'atencao': 0,
        'info': 0
    }
    
    for alerta in alertas:
        tipo = alerta.get('tipo', 'info')
        contagens[tipo] = contagens.get(tipo, 0) + 1
    
    return contagens


def get_alertas_por_categoria(alertas: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Agrupa alertas por categoria.
    
    Args:
        alertas: Lista de alertas
        
    Returns:
        Dicionário com alertas agrupados por categoria
    """
    agrupados = {}
    
    for alerta in alertas:
        categoria = alerta.get('categoria', 'Outros')
        if categoria not in agrupados:
            agrupados[categoria] = []
        agrupados[categoria].append(alerta)
    
    return agrupados
