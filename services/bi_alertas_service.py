"""
Serviço de Business Intelligence - Alertas Contratuais
=======================================================
CICLO 5 - BI Prospectivo: Da gestão reativa para preditiva

Autor: Copilot
Data: 09/01/2026

FUNCIONALIDADES:
- Risco real de ruptura (tempo nominal vs tempo histórico)
- Consumo silencioso de prazo
- Eficiência por gestor
- Previsão de rupturas
- Análise de gargalos
- Tendências temporais
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json
from collections import defaultdict
import statistics

# Imports internos
from services.alert_lifecycle_service import (
    listar_alertas_v2,
    ESTADO_NOVO,
    ESTADO_EM_ANALISE,
    ESTADO_PROVIDENCIA_EM_CURSO,
    ESTADO_AGUARDANDO_PRAZO,
    ESTADO_RESOLVIDO,
    ESTADO_ENCERRADO,
    ESTADO_ESCALONADO
)


# ========================================
# CONSTANTES E CONFIGURAÇÕES
# ========================================

# Tempos médios históricos por etapa (em dias) - P75
TEMPO_MEDIO_ANALISE = 5  # Tempo médio em análise
TEMPO_MEDIO_DECISAO = 3  # Tempo para tomar decisão
TEMPO_MEDIO_PROCESSO_PRORROGACAO = 45  # Tempo para processar prorrogação
TEMPO_MEDIO_PROCESSO_LICITACAO = 120  # Tempo para nova licitação
TEMPO_MEDIO_APROVACAO = 15  # Tempo de aprovação
TEMPO_MEDIO_FORMALIZACAO = 10  # Tempo de formalização

# Prazos de segurança (buffer)
BUFFER_SEGURANCA_CRITICO = 15  # 15 dias de buffer para críticos
BUFFER_SEGURANCA_NORMAL = 30  # 30 dias de buffer para normais

# Thresholds de performance
THRESHOLD_EFICIENCIA_BOA = 5  # <= 5 dias = eficiente
THRESHOLD_EFICIENCIA_MEDIA = 15  # <= 15 dias = média
# > 15 dias = baixa eficiência


# ========================================
# INDICADOR 1: RISCO REAL DE RUPTURA
# ========================================

def calcular_risco_ruptura(contrato: Dict, alertas: List[Dict]) -> Dict[str, any]:
    """
    Calcula o risco real de ruptura considerando tempo histórico necessário
    
    Lógica:
    - Tempo Nominal: Dias até o fim da vigência
    - Tempo Necessário: Soma dos tempos médios das etapas pendentes
    - Tempo Real Restante: Tempo Nominal - Tempo Necessário
    - Risco: Violação quando Tempo Real Restante < Janela de Segurança
    
    Args:
        contrato: Dados do contrato
        alertas: Lista de alertas relacionados
        
    Returns:
        Dicionário com análise de risco
    """
    hoje = datetime.now()
    data_fim = contrato.get('data_fim')
    
    if isinstance(data_fim, str):
        data_fim = datetime.fromisoformat(data_fim)
    
    if not data_fim:
        return {"risco": "indeterminado", "motivo": "Data de fim não informada"}
    
    # Tempo nominal restante
    dias_nominais = (data_fim - hoje).days
    
    # Identificar etapas pendentes
    alertas_ativos = [a for a in alertas if a['estado'] not in [ESTADO_RESOLVIDO, ESTADO_ENCERRADO]]
    
    # Calcular tempo necessário baseado em etapas
    tempo_necessario = 0
    etapas_pendentes = []
    
    for alerta in alertas_ativos:
        estado = alerta.get('estado')
        tipo = alerta.get('tipo')
        
        if estado == ESTADO_NOVO or estado == ESTADO_EM_ANALISE:
            tempo_necessario += TEMPO_MEDIO_ANALISE
            etapas_pendentes.append(f"Análise ({TEMPO_MEDIO_ANALISE}d)")
        
        if tipo == 'critico':
            # Alertas críticos geralmente requerem processo completo
            tempo_necessario += TEMPO_MEDIO_PROCESSO_PRORROGACAO
            tempo_necessario += TEMPO_MEDIO_APROVACAO
            tempo_necessario += TEMPO_MEDIO_FORMALIZACAO
            etapas_pendentes.extend([
                f"Processo prorrogação ({TEMPO_MEDIO_PROCESSO_PRORROGACAO}d)",
                f"Aprovação ({TEMPO_MEDIO_APROVACAO}d)",
                f"Formalização ({TEMPO_MEDIO_FORMALIZACAO}d)"
            ])
    
    # Se não há alertas ativos mas contrato está próximo do fim
    if not alertas_ativos and dias_nominais < 180:
        tempo_necessario = TEMPO_MEDIO_PROCESSO_PRORROGACAO + TEMPO_MEDIO_APROVACAO + TEMPO_MEDIO_FORMALIZACAO
        etapas_pendentes = ["Processo completo de renovação"]
    
    # Tempo real restante
    tempo_real_restante = dias_nominais - tempo_necessario
    
    # Janela de segurança
    janela_seguranca = BUFFER_SEGURANCA_CRITICO if len(alertas_ativos) > 0 else BUFFER_SEGURANCA_NORMAL
    
    # Determinar risco
    if tempo_real_restante < 0:
        nivel_risco = "urgente"
        status = "⛔ RUPTURA IMINENTE"
        cor = "red"
    elif tempo_real_restante < janela_seguranca:
        nivel_risco = "alto"
        status = "⚠️ JANELA DE SEGURANÇA VIOLADA"
        cor = "orange"
    elif tempo_real_restante < janela_seguranca * 2:
        nivel_risco = "medio"
        status = "⚡ ATENÇÃO NECESSÁRIA"
        cor = "yellow"
    else:
        nivel_risco = "baixo"
        status = "✅ DENTRO DA MARGEM"
        cor = "green"
    
    return {
        "contrato_id": contrato.get('id'),
        "contrato_numero": contrato.get('numero'),
        "dias_nominais": dias_nominais,
        "tempo_necessario": tempo_necessario,
        "tempo_real_restante": tempo_real_restante,
        "janela_seguranca": janela_seguranca,
        "nivel_risco": nivel_risco,
        "status": status,
        "cor": cor,
        "etapas_pendentes": etapas_pendentes,
        "margem_dias": tempo_real_restante - janela_seguranca,
        "percentual_consumido": round((tempo_necessario / dias_nominais * 100) if dias_nominais > 0 else 0, 1)
    }


# ========================================
# INDICADOR 2: CONSUMO SILENCIOSO DE PRAZO
# ========================================

def calcular_consumo_silencioso(alerta: Dict) -> Dict[str, any]:
    """
    Identifica tempo gasto além do esperado em cada estado
    
    Lógica:
    - Compara tempo real no estado vs tempo médio esperado
    - Identifica "consumo silencioso" (tempo perdido)
    - Alerta quando consumo é significativo
    
    Args:
        alerta: Alerta V2
        
    Returns:
        Análise de consumo silencioso
    """
    hoje = datetime.now()
    data_criacao = alerta.get('data_criacao')
    
    if isinstance(data_criacao, str):
        data_criacao = datetime.fromisoformat(data_criacao)
    
    dias_desde_criacao = (hoje - data_criacao).days
    estado_atual = alerta.get('estado')
    
    # Tempo esperado por estado
    tempo_esperado_map = {
        ESTADO_NOVO: 1,
        ESTADO_EM_ANALISE: TEMPO_MEDIO_ANALISE,
        ESTADO_PROVIDENCIA_EM_CURSO: 30,
        ESTADO_AGUARDANDO_PRAZO: 45,
        ESTADO_ESCALONADO: 3
    }
    
    tempo_esperado = tempo_esperado_map.get(estado_atual, 7)
    
    # Calcular consumo silencioso
    consumo_silencioso = max(0, dias_desde_criacao - tempo_esperado)
    percentual_extra = round((consumo_silencioso / tempo_esperado * 100) if tempo_esperado > 0 else 0, 1)
    
    # Determinar severidade
    if consumo_silencioso == 0:
        severidade = "normal"
        status = "✅ No prazo"
        cor = "green"
    elif consumo_silencioso <= tempo_esperado * 0.5:
        severidade = "atencao"
        status = "⚠️ Consumo moderado"
        cor = "yellow"
    else:
        severidade = "critico"
        status = "⛔ Consumo excessivo"
        cor = "red"
    
    return {
        "alerta_id": alerta.get('id'),
        "estado": estado_atual,
        "dias_desde_criacao": dias_desde_criacao,
        "tempo_esperado": tempo_esperado,
        "consumo_silencioso": consumo_silencioso,
        "percentual_extra": percentual_extra,
        "severidade": severidade,
        "status": status,
        "cor": cor
    }


# ========================================
# INDICADOR 3: EFICIÊNCIA POR GESTOR
# ========================================

def calcular_eficiencia_gestores(alertas: List[Dict]) -> Dict[str, Dict]:
    """
    Analisa eficiência de cada gestor na resolução de alertas
    
    Métricas:
    - Tempo médio de resolução
    - Percentis (P50, P75, P90)
    - Taxa de resolução
    - Alertas escalonados
    
    Args:
        alertas: Lista de alertas V2
        
    Returns:
        Dicionário com métricas por gestor
    """
    gestores_stats = defaultdict(lambda: {
        "total_alertas": 0,
        "resolvidos": 0,
        "escalonados": 0,
        "tempos_resolucao": [],
        "alertas_ativos": 0
    })
    
    hoje = datetime.now()
    
    for alerta in alertas:
        responsavel = alerta.get('responsavel', 'desconhecido')
        estado = alerta.get('estado')
        
        stats = gestores_stats[responsavel]
        stats["total_alertas"] += 1
        
        if estado == ESTADO_RESOLVIDO or estado == ESTADO_ENCERRADO:
            stats["resolvidos"] += 1
            
            # Calcular tempo de resolução
            data_criacao = alerta.get('data_criacao')
            data_atualizacao = alerta.get('data_ultima_atualizacao')
            
            if data_criacao and data_atualizacao:
                if isinstance(data_criacao, str):
                    data_criacao = datetime.fromisoformat(data_criacao)
                if isinstance(data_atualizacao, str):
                    data_atualizacao = datetime.fromisoformat(data_atualizacao)
                
                tempo_resolucao = (data_atualizacao - data_criacao).days
                stats["tempos_resolucao"].append(tempo_resolucao)
        
        elif estado == ESTADO_ESCALONADO:
            stats["escalonados"] += 1
        
        elif estado in [ESTADO_NOVO, ESTADO_EM_ANALISE, ESTADO_PROVIDENCIA_EM_CURSO]:
            stats["alertas_ativos"] += 1
    
    # Calcular métricas agregadas
    resultado = {}
    
    for gestor, stats in gestores_stats.items():
        tempos = stats["tempos_resolucao"]
        
        if tempos:
            tempo_medio = statistics.mean(tempos)
            p50 = statistics.median(tempos)
            p75 = statistics.quantiles(tempos, n=4)[2] if len(tempos) >= 4 else p50
            p90 = statistics.quantiles(tempos, n=10)[8] if len(tempos) >= 10 else p75
        else:
            tempo_medio = 0
            p50 = 0
            p75 = 0
            p90 = 0
        
        taxa_resolucao = round((stats["resolvidos"] / stats["total_alertas"] * 100) if stats["total_alertas"] > 0 else 0, 1)
        taxa_escalonamento = round((stats["escalonados"] / stats["total_alertas"] * 100) if stats["total_alertas"] > 0 else 0, 1)
        
        # Classificar eficiência
        if tempo_medio <= THRESHOLD_EFICIENCIA_BOA:
            classificacao = "🌟 Excelente"
            cor = "green"
        elif tempo_medio <= THRESHOLD_EFICIENCIA_MEDIA:
            classificacao = "✅ Boa"
            cor = "blue"
        else:
            classificacao = "⚠️ Requer atenção"
            cor = "orange"
        
        resultado[gestor] = {
            "total_alertas": stats["total_alertas"],
            "resolvidos": stats["resolvidos"],
            "escalonados": stats["escalonados"],
            "alertas_ativos": stats["alertas_ativos"],
            "taxa_resolucao": taxa_resolucao,
            "taxa_escalonamento": taxa_escalonamento,
            "tempo_medio": round(tempo_medio, 1),
            "p50": round(p50, 1),
            "p75": round(p75, 1),
            "p90": round(p90, 1),
            "classificacao": classificacao,
            "cor": cor
        }
    
    return resultado


# ========================================
# INDICADOR 4: PREVISÃO DE RUPTURAS
# ========================================

def prever_rupturas(contratos: List[Dict], alertas_por_contrato: Dict[str, List[Dict]]) -> List[Dict]:
    """
    Identifica contratos com alto risco de ruptura nos próximos N dias
    
    Args:
        contratos: Lista de contratos
        alertas_por_contrato: Mapa contrato_id -> lista de alertas
        
    Returns:
        Lista de contratos em risco, ordenados por urgência
    """
    previsoes = []
    hoje = datetime.now()
    
    for contrato in contratos:
        contrato_id = contrato.get('id')
        alertas = alertas_por_contrato.get(contrato_id, [])
        
        # Calcular risco
        risco = calcular_risco_ruptura(contrato, alertas)
        
        # Incluir apenas se risco médio ou superior
        if risco.get('nivel_risco') in ['medio', 'alto', 'urgente']:
            data_fim = contrato.get('data_fim')
            if isinstance(data_fim, str):
                data_fim = datetime.fromisoformat(data_fim)
            
            previsoes.append({
                "contrato": contrato.get('numero'),
                "objeto": contrato.get('objeto', '')[:60] + '...',
                "data_fim": data_fim.strftime('%d/%m/%Y') if data_fim else 'N/A',
                "dias_nominais": risco['dias_nominais'],
                "tempo_real_restante": risco['tempo_real_restante'],
                "nivel_risco": risco['nivel_risco'],
                "status": risco['status'],
                "cor": risco['cor'],
                "etapas_pendentes": len(risco['etapas_pendentes']),
                "urgencia_score": -risco['tempo_real_restante']  # Para ordenação
            })
    
    # Ordenar por urgência (menor tempo real restante primeiro)
    previsoes.sort(key=lambda x: x['urgencia_score'], reverse=True)
    
    return previsoes


# ========================================
# DASHBOARD: KPIs CONSOLIDADOS
# ========================================

def obter_kpis_dashboard(contratos: List[Dict], alertas: List[Dict]) -> Dict[str, any]:
    """
    Retorna KPIs consolidados para dashboard executivo
    
    Returns:
        Dicionário com KPIs principais
    """
    hoje = datetime.now()
    
    # Agrupar alertas por contrato
    alertas_por_contrato = defaultdict(list)
    for alerta in alertas:
        alertas_por_contrato[alerta.get('contrato_id')].append(alerta)
    
    # KPI 1: Contratos em risco
    contratos_risco_alto = []
    contratos_risco_medio = []
    contratos_ok = []
    
    for contrato in contratos:
        risco = calcular_risco_ruptura(contrato, alertas_por_contrato.get(contrato.get('id'), []))
        nivel = risco.get('nivel_risco')
        
        if nivel in ['urgente', 'alto']:
            contratos_risco_alto.append(contrato)
        elif nivel == 'medio':
            contratos_risco_medio.append(contrato)
        else:
            contratos_ok.append(contrato)
    
    # KPI 2: Alertas com consumo silencioso
    alertas_consumo_excessivo = []
    alertas_consumo_moderado = []
    
    for alerta in alertas:
        if alerta.get('estado') not in [ESTADO_RESOLVIDO, ESTADO_ENCERRADO]:
            consumo = calcular_consumo_silencioso(alerta)
            if consumo['severidade'] == 'critico':
                alertas_consumo_excessivo.append(alerta)
            elif consumo['severidade'] == 'atencao':
                alertas_consumo_moderado.append(alerta)
    
    # KPI 3: Eficiência geral
    eficiencia_gestores = calcular_eficiencia_gestores(alertas)
    tempos_validos = [g['tempo_medio'] for g in eficiencia_gestores.values() if g['tempo_medio'] > 0]
    tempo_medio_geral = statistics.mean(tempos_validos) if tempos_validos else 0
    
    # KPI 4: Previsões
    previsoes_ruptura = prever_rupturas(contratos, alertas_por_contrato)
    
    return {
        "total_contratos": len(contratos),
        "contratos_risco_alto": len(contratos_risco_alto),
        "contratos_risco_medio": len(contratos_risco_medio),
        "contratos_ok": len(contratos_ok),
        "alertas_consumo_excessivo": len(alertas_consumo_excessivo),
        "alertas_consumo_moderado": len(alertas_consumo_moderado),
        "tempo_medio_resolucao_geral": round(tempo_medio_geral, 1),
        "previsoes_ruptura": previsoes_ruptura[:10],  # Top 10
        "total_gestores": len(eficiencia_gestores),
        "eficiencia_gestores": eficiencia_gestores,
        "data_atualizacao": hoje.isoformat()
    }


# ========================================
# ANÁLISE TEMPORAL
# ========================================

def analisar_tendencia_temporal(alertas: List[Dict], dias: int = 30) -> Dict[str, any]:
    """
    Analisa tendências nos últimos N dias
    
    Args:
        alertas: Lista de alertas
        dias: Número de dias para análise
        
    Returns:
        Análise de tendências
    """
    hoje = datetime.now()
    data_inicio = hoje - timedelta(days=dias)
    
    # Filtrar alertas no período
    alertas_periodo = [
        a for a in alertas
        if datetime.fromisoformat(a['data_criacao']) >= data_inicio
    ]
    
    # Agrupar por dia
    por_dia = defaultdict(lambda: {"criados": 0, "resolvidos": 0})
    
    for alerta in alertas_periodo:
        data_criacao = datetime.fromisoformat(alerta['data_criacao']).date()
        por_dia[data_criacao]["criados"] += 1
        
        if alerta['estado'] in [ESTADO_RESOLVIDO, ESTADO_ENCERRADO]:
            data_resolucao = datetime.fromisoformat(alerta['data_ultima_atualizacao']).date()
            if data_resolucao >= data_inicio.date():
                por_dia[data_resolucao]["resolvidos"] += 1
    
    # Calcular médias
    total_criados = sum(d["criados"] for d in por_dia.values())
    total_resolvidos = sum(d["resolvidos"] for d in por_dia.values())
    
    media_criados_dia = round(total_criados / dias, 1) if dias > 0 else 0
    media_resolvidos_dia = round(total_resolvidos / dias, 1) if dias > 0 else 0
    
    return {
        "periodo_dias": dias,
        "total_criados": total_criados,
        "total_resolvidos": total_resolvidos,
        "media_criados_dia": media_criados_dia,
        "media_resolvidos_dia": media_resolvidos_dia,
        "saldo": total_criados - total_resolvidos,
        "por_dia": dict(sorted(por_dia.items()))
    }
