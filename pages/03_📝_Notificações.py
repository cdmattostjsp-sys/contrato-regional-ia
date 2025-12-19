"""
Página de Geração de Notificações
==================================
Geração assistida de notificações contratuais por IA.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state, reset_notificacao, add_log
from agents.notificacao_agent import gerar_notificacao_contratual


def main():
    st.set_page_config(
        page_title="TJSP - Notificações Contratuais",
        page_icon="📝",
        layout="wide"
    )
    
    apply_tjsp_styles()
    initialize_session_state()
    
    # Verifica se há contrato selecionado
    if not st.session_state.contrato_selecionado:
        st.warning("⚠️ Nenhum contrato selecionado. Retorne ao dashboard.")
        if st.button("🏠 Voltar ao Dashboard"):
            st.switch_page("Home.py")
        return
    
    contrato = st.session_state.contrato_selecionado
    
    # Cabeçalho
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #003366 0%, #0066CC 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem; color: white;">
            <h1>📝 Geração de Notificações Contratuais</h1>
            <p style="font-size: 1.1rem; margin: 0.5rem 0;">
            Contrato: <strong>{contrato['numero']}</strong>
            </p>
            <p style="opacity: 0.9;">{contrato['objeto']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Botões de navegação
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Dashboard", use_container_width=True):
            st.switch_page("Home.py")
    
    with col2:
        if st.button("📄 Ver Contrato", use_container_width=True):
            st.switch_page("pages/01_📄_Contrato.py")
    
    with col3:
        if st.button("💬 Copiloto", use_container_width=True):
            st.switch_page("pages/02_💬_Copiloto.py")
    
    with col4:
        if st.button("📖 Como Proceder", use_container_width=True):
            st.switch_page("pages/04_📖_Como_Proceder.py")
    
    st.markdown("---")
    
    # Formulário de notificação
    col_form, col_preview = st.columns([1, 1])
    
    with col_form:
        st.markdown("### 📋 Dados da Notificação")
        # Mapeamento de tipos de notificação por categoria
        TIPOS_NOTIFICACAO = {
            "Gestor do Contrato": [
                "Notificação de Início de Vigência",
                "Notificação de Designação de Fiscais",
                "Notificação de Reajuste Contratual",
                "Notificação de Alteração Contratual (Aditamento)",
                "Notificação de Rescisão Contratual"
            ],
            "Fiscal do Contrato": [
                "Advertência",
                "Solicitação de Correção",
                "Solicitação de Documentação",
                "Comunicado de Irregularidade",
                "Notificação Prévia de Penalidade"
            ]
        }

        # Campo de seleção da categoria da notificação
        categoria_notificacao = st.selectbox(
            "Categoria da Notificação",
            list(TIPOS_NOTIFICACAO.keys())
        )

        # Campo de seleção do tipo de notificação, dinâmico conforme categoria
        tipo_notificacao = st.selectbox(
            "Tipo de Notificação",
            TIPOS_NOTIFICACAO[categoria_notificacao]
        )
        
        motivo = st.text_area(
            "Motivo da Notificação",
            placeholder="Descreva o motivo da notificação de forma clara e objetiva...",
            height=100,
            key="notif_motivo"
        )
        
        prazo = st.number_input(
            "Prazo para Resposta (dias úteis)",
            min_value=1,
            max_value=30,
            value=5,
            key="notif_prazo"
        )
        
        fundamentacao = st.text_area(
            "Fundamentação Legal (opcional)",
            placeholder="Ex: Cláusula 7ª do contrato, Lei 8.666/93, etc.",
            height=80,
            key="notif_fundamentacao"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🤖 Gerar com IA", type="primary", use_container_width=True):
                if not motivo:
                    st.error("⚠️ Por favor, descreva o motivo da notificação.")
                else:
                    with st.spinner("Gerando notificação..."):
                        # Prepara dados para o agente
                        st.session_state.notificacao_campos_ai = {
                            "tipo": tipo_notificacao,
                            "motivo": motivo,
                            "prazo": prazo,
                            "fundamentacao": fundamentacao,
                            "destinatario": contrato["fornecedor"]
                        }
                        
                        # Gera notificação
                        notificacao_gerada = gerar_notificacao_contratual(
                            contrato=contrato,
                            dados_notificacao=st.session_state.notificacao_campos_ai
                        )
                        
                        st.session_state.notificacao_buffer = notificacao_gerada
                        add_log("INFO", f"Notificação gerada para contrato {contrato['id']}")
                        st.rerun()
        
        with col_btn2:
            if st.button("🗑️ Limpar", use_container_width=True):
                reset_notificacao()
                st.rerun()
    
    with col_preview:
        st.markdown("### 👁️ Pré-visualização")
        
        if st.session_state.notificacao_buffer:
            st.markdown("""
                <div class="contract-card">
                    <div style="white-space: pre-wrap; font-family: 'Courier New', monospace; font-size: 0.9rem;">
            """, unsafe_allow_html=True)
            
            st.markdown(st.session_state.notificacao_buffer)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Botões de ação
            col_act1, col_act2, col_act3 = st.columns(3)
            
            with col_act1:
                if st.button("📥 Baixar DOCX", use_container_width=True):
                    st.info("Funcionalidade em desenvolvimento")
            
            with col_act2:
                if st.button("📧 Enviar", use_container_width=True):
                    st.info("Funcionalidade em desenvolvimento")
            
            with col_act3:
                if st.button("✏️ Editar", use_container_width=True):
                    st.info("Funcionalidade em desenvolvimento")
        else:
            st.info("""
            📝 A notificação gerada aparecerá aqui.
            
            Preencha os campos ao lado e clique em "Gerar com IA".
            """)


if __name__ == "__main__":
    main()
