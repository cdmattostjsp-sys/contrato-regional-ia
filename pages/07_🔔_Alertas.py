"""
Página de Alertas Contratuais
==============================
Sistema automático de alertas baseado em regras de negócio.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state
from services.contract_service import get_todos_contratos
from services.alert_service import calcular_alertas, get_alertas_por_tipo, get_alertas_por_categoria


def render_alerta_card(alerta: dict):
    """Renderiza card de alerta individual"""
    
    # Define cores e ícones por tipo
    config_tipos = {
        'critico': {
            'cor': '#DC3545',
            'cor_bg': '#F8D7DA',
            'icone': '🔴',
            'label': 'CRÍTICO'
        },
        'atencao': {
            'cor': '#FFC107',
            'cor_bg': '#FFF3CD',
            'icone': '🟡',
            'label': 'ATENÇÃO'
        },
        'info': {
            'cor': '#17A2B8',
            'cor_bg': '#D1ECF1',
            'icone': '🔵',
            'label': 'INFO'
        }
    }
    
    config = config_tipos.get(alerta.get('tipo', 'info'), config_tipos['info'])
    
    # Extrai dados com escape de caracteres especiais
    titulo = str(alerta.get('titulo', 'Sem título')).replace("'", "&#39;").replace('"', '&quot;')
    descricao = str(alerta.get('descricao', 'Sem descrição')).replace("'", "&#39;").replace('"', '&quot;')
    contrato_numero = str(alerta.get('contrato_numero', 'N/A')).replace("'", "&#39;").replace('"', '&quot;')
    categoria = str(alerta.get('categoria', 'Geral')).replace("'", "&#39;").replace('"', '&quot;')
    data_alerta = alerta.get('data_alerta', datetime.now())
    data_formatada = data_alerta.strftime('%d/%m/%Y %H:%M') if isinstance(data_alerta, datetime) else str(data_alerta)
    
    html_card = f"""
        <div style="background: white; border-left: 5px solid {config['cor']}; 
                    padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div>
                    <span style="background: {config['cor']}; color: white; padding: 0.3rem 0.8rem;
                                border-radius: 15px; font-size: 0.75rem; font-weight: bold;">
                        {config['icone']} {config['label']}
                    </span>
                    <span style="background: #E9ECEF; color: #495057; padding: 0.3rem 0.8rem;
                                border-radius: 15px; font-size: 0.75rem; font-weight: bold; margin-left: 0.5rem;">
                        {categoria}
                    </span>
                </div>
                <span style="color: #6C757D; font-size: 0.85rem;">
                    {data_formatada}
                </span>
            </div>
            
            <h4 style="margin: 0 0 0.5rem 0; color: {config['cor']};">
                {titulo}
            </h4>
            
            <p style="margin: 0 0 1rem 0; color: #495057; line-height: 1.6;">
                {descricao}
            </p>
            
            <p style="margin: 0; color: #6C757D; font-size: 0.9rem;">
                <strong>Contrato:</strong> {contrato_numero}
            </p>
        </div>
    """
    
    st.markdown(html_card, unsafe_allow_html=True)
    
    # Botões de ação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Ver Contrato", key=f"ver_{alerta['id']}", use_container_width=True):
            # Busca contrato
            contratos = get_todos_contratos()
            contrato = next((c for c in contratos if c['id'] == alerta['contrato_id']), None)
            if contrato:
                st.session_state.contrato_selecionado = contrato
                st.switch_page("pages/01_📄_Contrato.py")
    
    with col2:
        if st.button("📝 Gerar Notificação", key=f"notif_{alerta['id']}", use_container_width=True):
            contratos = get_todos_contratos()
            contrato = next((c for c in contratos if c['id'] == alerta['contrato_id']), None)
            if contrato:
                st.session_state.contrato_selecionado = contrato
                st.switch_page("pages/03_📝_Notificações.py")
    
    with col3:
        if st.button("✅ Marcar Resolvido", key=f"resolve_{alerta['id']}", use_container_width=True):
            st.success("Funcionalidade em desenvolvimento")


def main():
    st.set_page_config(
        page_title="TJSP - Alertas Contratuais",
        page_icon="🔔",
        layout="wide"
    )
    
    apply_tjsp_styles()
    initialize_session_state()
    
    # Cabeçalho
    st.markdown("""
        <div class="tjsp-header">
            <h1>🔔 Alertas Contratuais</h1>
            <p class="tjsp-subtitle">Sistema Automático de Monitoramento e Alertas</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Botão de retorno
    if st.button("🏠 Voltar ao Dashboard", use_container_width=False):
        st.switch_page("Home.py")
    
    st.markdown("---")
    
    # Carrega contratos e calcula alertas
    with st.spinner("Calculando alertas..."):
        contratos = get_todos_contratos()
        alertas = calcular_alertas(contratos)
    
    # Estatísticas de alertas
    contagens = get_alertas_por_tipo(alertas)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🔴 Críticos",
            value=contagens['critico'],
            delta="Requer ação imediata",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="🟡 Atenção",
            value=contagens['atencao'],
            delta="Acompanhamento necessário"
        )
    
    with col3:
        st.metric(
            label="🔵 Informativos",
            value=contagens['info'],
            delta="Monitoramento"
        )
    
    with col4:
        st.metric(
            label="📊 Total de Alertas",
            value=len(alertas),
            delta=f"{len(contratos)} contratos"
        )
    
    st.markdown("---")
    
    # Filtros
    col_filtro1, col_filtro2, col_filtro3 = st.columns([2, 2, 1])
    
    with col_filtro1:
        filtro_tipo = st.selectbox(
            "Filtrar por Tipo",
            ["Todos", "🔴 Críticos", "🟡 Atenção", "🔵 Informativos"],
            key="filtro_tipo_alerta"
        )
    
    with col_filtro2:
        categorias_disponiveis = ["Todas"] + list(get_alertas_por_categoria(alertas).keys())
        filtro_categoria = st.selectbox(
            "Filtrar por Categoria",
            categorias_disponiveis,
            key="filtro_categoria_alerta"
        )
    
    with col_filtro3:
        st.write("")
        st.write("")
        if st.button("🔄 Atualizar", use_container_width=True):
            st.rerun()
    
    # Aplica filtros
    alertas_filtrados = alertas
    
    if filtro_tipo != "Todos":
        tipo_map = {
            "🔴 Críticos": "critico",
            "🟡 Atenção": "atencao",
            "🔵 Informativos": "info"
        }
        tipo_busca = tipo_map.get(filtro_tipo)
        if tipo_busca:
            alertas_filtrados = [a for a in alertas_filtrados if a.get('tipo') == tipo_busca]
    
    if filtro_categoria != "Todas":
        alertas_filtrados = [a for a in alertas_filtrados if a.get('categoria') == filtro_categoria]
    
    # Mostra resultados
    st.markdown("---")
    
    if not alertas_filtrados:
        st.success("✅ Nenhum alerta encontrado com os filtros aplicados!")
        st.balloons()
    else:
        if len(alertas_filtrados) != len(alertas):
            st.info(f"📊 Exibindo **{len(alertas_filtrados)}** de {len(alertas)} alertas")
        
        st.markdown("### 📋 Lista de Alertas")
        
        # Renderiza alertas
        for alerta in alertas_filtrados:
            render_alerta_card(alerta)
    
    # Rodapé informativo
    st.markdown("---")
    with st.expander("ℹ️ Como funcionam os alertas automáticos"):
        st.markdown("""
        ### 🤖 Sistema Automático de Alertas
        
        Os alertas são calculados automaticamente com base em regras de negócio:
        
        **🔴 Alertas Críticos:**
        - Vigência < 60 dias
        - Contratos vencidos
        - Status marcado como crítico
        
        **🟡 Alertas de Atenção:**
        - Vigência entre 60-120 dias
        - Contratos com pendências
        
        **🔵 Alertas Informativos:**
        - Contratos de alto valor (> R$ 50M)
        - Notificações gerais
        
        ### 📊 Ações Disponíveis
        
        Para cada alerta você pode:
        - **Ver Contrato**: Acessar detalhes completos
        - **Gerar Notificação**: Criar notificação com IA
        - **Marcar Resolvido**: Registrar resolução (em desenvolvimento)
        
        ### 🔄 Atualização
        
        Os alertas são recalculados a cada visualização da página ou ao clicar em "🔄 Atualizar".
        """)


if __name__ == "__main__":
    main()
