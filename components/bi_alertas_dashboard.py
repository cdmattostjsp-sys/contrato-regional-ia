"""
Dashboard de BI - Alertas Contratuais
======================================
CICLO 5 - Visualização dos indicadores prospectivos

Autor: Copilot
Data: 09/01/2026

COMPONENTES:
- KPIs principais
- Gráficos de risco
- Análise de eficiência
- Previsão de rupturas
- Timeline de consumo
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import List, Dict

from services.bi_alertas_service import (
    calcular_risco_ruptura,
    calcular_consumo_silencioso,
    calcular_eficiencia_gestores,
    prever_rupturas,
    obter_kpis_dashboard,
    analisar_tendencia_temporal
)


# ========================================
# COMPONENTE 1: KPIs PRINCIPAIS
# ========================================

def render_kpis_principais(kpis: Dict):
    """Renderiza cards com KPIs principais"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="⛔ Contratos Risco Alto",
            value=kpis['contratos_risco_alto'],
            delta=f"-{kpis['contratos_ok']} OK",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="⚠️ Contratos Risco Médio",
            value=kpis['contratos_risco_medio'],
            delta=None
        )
    
    with col3:
        st.metric(
            label="⏱️ Consumo Excessivo",
            value=kpis['alertas_consumo_excessivo'],
            delta=f"{kpis['alertas_consumo_moderado']} moderado",
            delta_color="off"
        )
    
    with col4:
        st.metric(
            label="📊 Tempo Médio Resolução",
            value=f"{kpis['tempo_medio_resolucao_geral']:.1f} dias",
            delta=None
        )


# ========================================
# COMPONENTE 2: PREVISÃO DE RUPTURAS
# ========================================

def render_previsao_rupturas(previsoes: List[Dict]):
    """Renderiza tabela de previsão de rupturas"""
    
    st.subheader("📊 Previsão de Rupturas - Próximos Contratos em Risco")
    
    if not previsoes:
        st.success("✅ Nenhum contrato em risco identificado no momento")
        return
    
    # Converter para DataFrame
    df = pd.DataFrame(previsoes)
    
    # Configurar colunas
    df_display = df[[
        'contrato', 'objeto', 'data_fim', 
        'dias_nominais', 'tempo_real_restante', 
        'etapas_pendentes', 'status'
    ]].copy()
    
    df_display.columns = [
        'Contrato', 'Objeto', 'Data Fim',
        'Dias Nominais', 'Tempo Real', 
        'Etapas', 'Status'
    ]
    
    # Aplicar cores
    def colorir_linha(row):
        cor_map = {
            'red': 'background-color: #ffebee',
            'orange': 'background-color: #fff3e0',
            'yellow': 'background-color: #fffde7'
        }
        cor = df.loc[row.name, 'cor']
        return [cor_map.get(cor, '')] * len(row)
    
    styled_df = df_display.style.apply(colorir_linha, axis=1)
    
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Gráfico de barras
    st.markdown("### 📊 Visualização de Risco")
    
    fig = go.Figure()
    
    cores_mapa = {'urgente': 'red', 'alto': 'orange', 'medio': 'yellow', 'baixo': 'green'}
    
    fig.add_trace(go.Bar(
        x=df['contrato'][:10],
        y=df['tempo_real_restante'][:10],
        marker_color=[cores_mapa.get(r, 'gray') for r in df['nivel_risco'][:10]],
        text=df['tempo_real_restante'][:10],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Tempo Real: %{y} dias<extra></extra>'
    ))
    
    fig.update_layout(
        title="Tempo Real Restante (Dias) - Top 10 Contratos em Risco",
        xaxis_title="Contrato",
        yaxis_title="Dias",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ========================================
# COMPONENTE 3: EFICIÊNCIA POR GESTOR
# ========================================

def render_eficiencia_gestores(eficiencia: Dict[str, Dict]):
    """Renderiza análise de eficiência por gestor"""
    
    st.subheader("👥 Eficiência por Gestor")
    
    if not eficiencia:
        st.info("Sem dados de gestores disponíveis")
        return
    
    # Converter para DataFrame
    df = pd.DataFrame.from_dict(eficiencia, orient='index')
    df = df.reset_index().rename(columns={'index': 'Gestor'})
    
    # Ordenar por tempo médio
    df = df.sort_values('tempo_medio')
    
    # Tabela de métricas
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📊 Métricas Detalhadas")
        
        df_display = df[[
            'Gestor', 'total_alertas', 'resolvidos', 
            'tempo_medio', 'p50', 'p75', 
            'taxa_resolucao', 'classificacao'
        ]].copy()
        
        df_display.columns = [
            'Gestor', 'Total', 'Resolvidos',
            'Tempo Médio', 'P50', 'P75',
            'Taxa (%)', 'Classificação'
        ]
        
        st.dataframe(df_display, use_container_width=True, height=300)
    
    with col2:
        st.markdown("#### 🏆 Ranking")
        
        for idx, row in df.head(5).iterrows():
            posicao = idx + 1
            emoji = "🥇" if posicao == 1 else "🥈" if posicao == 2 else "🥉" if posicao == 3 else "🔹"
            
            st.markdown(f"""
            <div style='padding: 10px; margin: 5px 0; background-color: #f0f2f6; border-radius: 5px;'>
                <b>{emoji} {row['Gestor']}</b><br>
                <small>{row['tempo_medio']:.1f} dias | {row['resolvidos']} resolvidos</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Gráfico de comparação
    st.markdown("#### 📈 Comparação de Performance")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Tempo Médio',
        x=df['Gestor'],
        y=df['tempo_medio'],
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        name='P75',
        x=df['Gestor'],
        y=df['p75'],
        marker_color='orange'
    ))
    
    fig.update_layout(
        barmode='group',
        xaxis_title="Gestor",
        yaxis_title="Dias",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ========================================
# COMPONENTE 4: CONSUMO SILENCIOSO
# ========================================

def render_analise_consumo(alertas: List[Dict]):
    """Renderiza análise de consumo silencioso"""
    
    st.subheader("⏰ Análise de Consumo Silencioso de Prazo")
    
    # Calcular consumo para todos os alertas ativos
    from services.alert_lifecycle_service import ESTADO_RESOLVIDO, ESTADO_ENCERRADO
    
    alertas_ativos = [
        a for a in alertas 
        if a['estado'] not in [ESTADO_RESOLVIDO, ESTADO_ENCERRADO]
    ]
    
    if not alertas_ativos:
        st.success("✅ Nenhum alerta ativo no momento")
        return
    
    consumos = []
    for alerta in alertas_ativos:
        consumo = calcular_consumo_silencioso(alerta)
        consumos.append({
            'contrato': alerta.get('contrato_numero', 'N/A'),
            'titulo': alerta.get('titulo', '')[:50],
            'estado': alerta.get('estado'),
            'dias_criacao': consumo['dias_desde_criacao'],
            'tempo_esperado': consumo['tempo_esperado'],
            'consumo': consumo['consumo_silencioso'],
            'percentual': consumo['percentual_extra'],
            'status': consumo['status'],
            'severidade': consumo['severidade']
        })
    
    # Filtrar apenas os com consumo > 0
    consumos_significativos = [c for c in consumos if c['consumo'] > 0]
    
    if not consumos_significativos:
        st.success("✅ Todos os alertas estão dentro do prazo esperado")
        return
    
    # Ordenar por consumo
    consumos_significativos.sort(key=lambda x: x['consumo'], reverse=True)
    
    # Exibir top 10
    df = pd.DataFrame(consumos_significativos[:10])
    
    st.dataframe(
        df[['contrato', 'titulo', 'dias_criacao', 'tempo_esperado', 'consumo', 'percentual', 'status']],
        use_container_width=True,
        height=300
    )
    
    # Gráfico de pizza - distribuição de severidade
    col1, col2 = st.columns(2)
    
    with col1:
        severidade_count = pd.Series([c['severidade'] for c in consumos]).value_counts()
        
        fig = px.pie(
            values=severidade_count.values,
            names=severidade_count.index,
            title="Distribuição por Severidade",
            color_discrete_map={'normal': 'green', 'atencao': 'yellow', 'critico': 'red'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top 5 maiores consumos
        st.markdown("#### 🔝 Maiores Consumos")
        
        for c in consumos_significativos[:5]:
            st.markdown(f"""
            <div style='padding: 8px; margin: 5px 0; background-color: #fff3e0; border-left: 4px solid orange; border-radius: 3px;'>
                <b>{c['contrato']}</b>: +{c['consumo']} dias ({c['percentual']:.0f}% extra)
            </div>
            """, unsafe_allow_html=True)


# ========================================
# COMPONENTE 5: TENDÊNCIA TEMPORAL
# ========================================

def render_tendencia_temporal(alertas: List[Dict], dias: int = 30):
    """Renderiza análise de tendência temporal"""
    
    st.subheader(f"📈 Tendência - Últimos {dias} Dias")
    
    tendencia = analisar_tendencia_temporal(alertas, dias)
    
    # KPIs da tendência
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Alertas Criados",
            tendencia['total_criados'],
            f"{tendencia['media_criados_dia']:.1f}/dia"
        )
    
    with col2:
        st.metric(
            "Alertas Resolvidos",
            tendencia['total_resolvidos'],
            f"{tendencia['media_resolvidos_dia']:.1f}/dia"
        )
    
    with col3:
        saldo = tendencia['saldo']
        st.metric(
            "Saldo",
            saldo,
            delta="Backlog crescendo" if saldo > 0 else "Backlog reduzindo",
            delta_color="inverse" if saldo > 0 else "normal"
        )
    
    with col4:
        taxa = (tendencia['total_resolvidos'] / tendencia['total_criados'] * 100) if tendencia['total_criados'] > 0 else 0
        st.metric(
            "Taxa Resolução",
            f"{taxa:.1f}%"
        )
    
    # Gráfico de linha temporal
    if tendencia['por_dia']:
        df_temporal = pd.DataFrame([
            {
                'Data': data,
                'Criados': valores['criados'],
                'Resolvidos': valores['resolvidos']
            }
            for data, valores in tendencia['por_dia'].items()
        ])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_temporal['Data'],
            y=df_temporal['Criados'],
            mode='lines+markers',
            name='Criados',
            line=dict(color='red', width=2),
            marker=dict(size=6)
        ))
        
        fig.add_trace(go.Scatter(
            x=df_temporal['Data'],
            y=df_temporal['Resolvidos'],
            mode='lines+markers',
            name='Resolvidos',
            line=dict(color='green', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title="Evolução de Alertas - Criação vs Resolução",
            xaxis_title="Data",
            yaxis_title="Quantidade",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)


# ========================================
# DASHBOARD COMPLETO
# ========================================

def render_dashboard_bi_completo(contratos: List[Dict], alertas: List[Dict]):
    """
    Renderiza dashboard completo de BI
    
    Args:
        contratos: Lista de contratos
        alertas: Lista de alertas V2
    """
    
    st.title("📊 Business Intelligence - Alertas Contratuais")
    st.markdown("**Dashboard Prospectivo**: Da gestão reativa para preditiva")
    
    # Obter KPIs consolidados
    kpis = obter_kpis_dashboard(contratos, alertas)
    
    # Seção 1: KPIs Principais
    st.markdown("---")
    render_kpis_principais(kpis)
    
    # Seção 2: Previsão de Rupturas
    st.markdown("---")
    render_previsao_rupturas(kpis['previsoes_ruptura'])
    
    # Seção 3: Eficiência de Gestores
    st.markdown("---")
    render_eficiencia_gestores(kpis['eficiencia_gestores'])
    
    # Seção 4: Consumo Silencioso
    st.markdown("---")
    render_analise_consumo(alertas)
    
    # Seção 5: Tendência Temporal
    st.markdown("---")
    render_tendencia_temporal(alertas, dias=30)
    
    # Rodapé
    st.markdown("---")
    st.caption(f"📅 Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.caption("💡 **Dica**: Use os filtros acima para análises específicas por período ou categoria")
