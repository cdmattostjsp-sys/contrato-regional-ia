"""
Página do Copilot de Contrato
==============================
Assistente conversacional que responde EXCLUSIVAMENTE sobre o contrato carregado.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state, reset_chat_history, add_log
from agents.copilot_agent import processar_pergunta_copilot


def render_chat_message(role: str, content: str, timestamp: datetime):
    """Renderiza uma mensagem no chat"""
    if role == "user":
        icon = "👤"
        class_name = "user"
    else:
        icon = "🤖"
        class_name = "assistant"
    
    st.markdown(f"""
        <div class="chat-message {class_name}">
            <p><strong>{icon} {role.upper()}</strong> 
            <span style="font-size: 0.8rem; color: #666;">
            {timestamp.strftime('%H:%M:%S')}
            </span></p>
            <p>{content}</p>
        </div>
    """, unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="TJSP - Copiloto de Contrato",
        page_icon="💬",
        layout="wide"
    )
    
    apply_tjsp_styles()
    initialize_session_state()
    
    # Seleção interna de contrato
    from components.contrato_selector import render_contrato_selector
    from services.contract_service import get_todos_contratos
    if (
        not st.session_state.get("contrato_selecionado") 
        or st.session_state.get("modo_selecao_contrato")
    ):
        contratos = get_todos_contratos()
        selecionado = render_contrato_selector(
            contratos,
            titulo="Central de Consulta de Contratos",
            help_text="Selecione um contrato para usar o Copiloto.",
            key_prefix="copiloto"
        )
        if selecionado:
            st.session_state["contrato_selecionado"] = {"id": selecionado["id"], "numero": selecionado["numero"], "fornecedor": selecionado.get("fornecedor", "")}
            st.session_state["modo_selecao_contrato"] = False
            st.rerun()
        return
    contrato = st.session_state["contrato_selecionado"]
    # Faixa de contrato selecionado + botão trocar
    with st.container():
        col_a, col_b = st.columns([8,2])
        with col_a:
            st.success(f"Contrato selecionado: Nº {contrato.get('numero','')} — Fornecedor: {contrato.get('fornecedor','')}")
        with col_b:
            if st.button("Trocar contrato", key="copiloto_trocar_contrato"):
                st.session_state["modo_selecao_contrato"] = True
                st.rerun()
    
    # Cabeçalho
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #003366 0%, #0066CC 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem; color: white;">
            <h1>🤖 Copilot de Contrato</h1>
            <p style="font-size: 1.1rem; margin: 0.5rem 0;">
            Contexto: <strong>{contrato.get('numero', '(a preencher)')}</strong>
            </p>
                contrato = ensure_contrato_context(key_prefix="copiloto")
                if not contrato:
                    return
                render_context_bar(contrato, key_prefix="copiloto")
                render_module_banner("Contrato – Assistente (Copiloto)", contrato.get("objeto", ""))
    with col4:
        if st.button("📖 Como Proceder", use_container_width=True):
            st.switch_page("pages/04_📖_Como_Proceder.py")
    
    st.markdown("---")
    
    # Área de chat
    st.markdown("### 💬 Conversa")
    
    # Instruções
    with st.expander("ℹ️ Como usar o Copiloto"):
        st.info("""
        O Copiloto responde perguntas **exclusivamente sobre o contrato carregado**.
        
        **Exemplos de perguntas:**
        - Qual é o prazo de vigência do contrato?
        - Quem são os fiscais responsáveis?
        - Quais são as principais obrigações da contratada?
        - Existem pendências no contrato?
        - Qual é o valor total contratado?
        - Quais documentos estão anexados?
        """)
    
    # Exibe histórico de mensagens
    chat_container = st.container()
    
    with chat_container:
        if len(st.session_state.chat_history) == 0:
            st.info("👋 Olá! Sou o Copiloto de Contratos. Posso responder perguntas sobre o contrato selecionado. Como posso ajudar?")
        
        for msg in st.session_state.chat_history:
            render_chat_message(
                msg["role"],
                msg["content"],
                msg["timestamp"]
            )
    
    # Input do usuário
    with st.container():
        user_input = st.chat_input("Digite sua pergunta sobre o contrato...")
        
        if user_input:
            # Adiciona pergunta do usuário ao histórico
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now()
            })
            
            # Processa pergunta via agente
            resposta = processar_pergunta_copilot(
                pergunta=user_input,
                contrato=contrato
            )
            
            # Adiciona resposta ao histórico
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": resposta,
                "timestamp": datetime.now()
            })
            
            # Log
            add_log("INFO", f"Copiloto: Pergunta processada para contrato {contrato['id']}")
            
            # Rerun para atualizar interface
            st.rerun()


if __name__ == "__main__":
    main()
