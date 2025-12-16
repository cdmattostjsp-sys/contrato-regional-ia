"""
Página de Visualização de Contrato
===================================
Exibe detalhes completos de um contrato selecionado.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state
from services.contract_service import get_contrato_detalhes


def render_contrato_header(contrato: dict):
    """Renderiza cabeçalho do contrato"""
    status_colors = {
        "ativo": ("🟢", "#28A745"),
        "atencao": ("🟡", "#FFC107"),
        "critico": ("🔴", "#DC3545")
    }
    
    icon, color = status_colors.get(contrato.get("status", "ativo"), ("⚪", "#666"))
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #003366 0%, #0066CC 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem; color: white;">
            <h1>{icon} {contrato['numero']}</h1>
            <p style="font-size: 1.2rem; margin: 0.5rem 0;">{contrato['objeto']}</p>
            <p style="opacity: 0.9;"><strong>Fornecedor:</strong> {contrato['fornecedor']}</p>
        </div>
    """, unsafe_allow_html=True)


def render_contrato_detalhes(contrato: dict):
    """Renderiza detalhes do contrato em tabs"""
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Dados Gerais", "📜 Cláusulas", "📁 Documentos", "📊 Histórico"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💰 Informações Financeiras")
            st.info(f"""
            **Valor Total:** R$ {contrato['valor']:,.2f}  
            **Tipo:** {contrato['tipo']}  
            **Status:** {contrato['status'].upper()}
            """)
            
            st.markdown("### 📅 Vigência")
            st.info(f"""
            **Período:** {contrato['vigencia']}  
            **Última Atualização:** {contrato['ultima_atualizacao'].strftime('%d/%m/%Y %H:%M')}
            """)
        
        with col2:
            st.markdown("### 👥 Fiscalização")
            st.success(f"""
            **Fiscal Titular:** {contrato['fiscal_titular']}  
            **Fiscal Substituto:** {contrato['fiscal_substituto']}
            """)
            
            if "pendencias" in contrato and contrato["pendencias"]:
                st.markdown("### ⚠️ Pendências")
                for pendencia in contrato["pendencias"]:
                    st.warning(f"• {pendencia}")
    
    with tab2:
        st.markdown("### 📜 Cláusulas Principais")
        if "clausulas_principais" in contrato:
            for i, clausula in enumerate(contrato["clausulas_principais"], 1):
                with st.expander(f"Cláusula {i}"):
                    st.write(clausula)
        else:
            st.info("Cláusulas serão carregadas em breve.")
    
    with tab3:
        st.markdown("### 📁 Documentos do Contrato")
        if "documentos" in contrato:
            for doc in contrato["documentos"]:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"📄 **{doc['tipo']}**")
                with col2:
                    st.write(doc['data'])
                with col3:
                    st.write(f"✓ {doc['status']}")
                st.markdown("---")
        else:
            st.info("Documentos serão carregados em breve.")
    
    with tab4:
        st.markdown("### 📊 Histórico de Eventos")
        if "historico_eventos" in contrato:
            for evento in contrato["historico_eventos"]:
                st.markdown(f"""
                    <div class="contract-card">
                        <p><strong>{evento['data'].strftime('%d/%m/%Y %H:%M')}</strong></p>
                        <p>{evento['evento']}</p>
                        <p style="color: #666; font-size: 0.9rem;">Por: {evento['responsavel']}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Histórico será carregado em breve.")


def main():
    st.set_page_config(
        page_title="TJSP - Detalhes do Contrato",
        page_icon="📄",
        layout="wide"
    )
    
    apply_tjsp_styles()
    initialize_session_state()
    
    # Verifica se há contrato selecionado
    if not st.session_state.contrato_selecionado:
        st.warning("⚠️ Nenhum contrato selecionado. Retorne ao dashboard.")
        if st.button("🏠 Voltar ao Dashboard"):
            st.switch_page("app.py")
        return
    
    # Obtém detalhes completos do contrato
    contrato = get_contrato_detalhes(st.session_state.contrato_selecionado["id"])
    
    if not contrato:
        st.error("❌ Erro ao carregar detalhes do contrato.")
        return
    
    # Renderiza cabeçalho
    render_contrato_header(contrato)
    
    # Botões de ação
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Dashboard", use_container_width=True):
            st.switch_page("app.py")
    
    with col2:
        if st.button("🤖 Copilot", use_container_width=True):
            st.switch_page("pages/02_🤖_Copilot.py")
    
    with col3:
        if st.button("📝 Notificar", use_container_width=True):
            st.switch_page("pages/03_📝_Notificações.py")
    
    with col4:
        if st.button("📖 Como Proceder", use_container_width=True):
            st.switch_page("pages/04_📖_Como_Proceder.py")
    
    st.markdown("---")
    
    # Renderiza detalhes
    render_contrato_detalhes(contrato)


if __name__ == "__main__":
    main()
