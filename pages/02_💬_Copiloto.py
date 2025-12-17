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
            <h1>🤖 Copilot de Contrato</h1>
            <p style="font-size: 1.1rem; margin: 0.5rem 0;">
            Contexto: <strong>{contrato['numero']}</strong>
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
        if st.button("🗑️ Limpar Chat", use_container_width=True):
            reset_chat_history()
            st.rerun()
    
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
