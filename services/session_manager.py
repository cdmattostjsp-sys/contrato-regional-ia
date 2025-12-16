"""
Gerenciador de Session State
=============================
Gerencia o estado da sessão do aplicativo Streamlit.

Padrões:
- Variáveis terminadas em _campos_ai: dados estruturados para agentes
- Variáveis terminadas em _buffer: dados temporários/cache
"""

import streamlit as st
from datetime import datetime


def initialize_session_state():
    """
    Inicializa todas as variáveis de session state do aplicativo.
    Seguindo padrão institucional: *_campos_ai para dados estruturados, *_buffer para cache.
    """
    
    # ===== USUÁRIO E PERFIL =====
    if "usuario" not in st.session_state:
        st.session_state.usuario = "Coordenador Regional"
    
    if "perfil" not in st.session_state:
        st.session_state.perfil = "Fiscal de Contrato"
    
    if "raj" not in st.session_state:
        st.session_state.raj = "10.1"
    
    # ===== CONTRATO SELECIONADO =====
    if "contrato_selecionado" not in st.session_state:
        st.session_state.contrato_selecionado = None
    
    # ===== COPILOT / CHAT =====
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "copilot_buffer" not in st.session_state:
        st.session_state.copilot_buffer = ""
    
    if "contexto_campos_ai" not in st.session_state:
        st.session_state.contexto_campos_ai = {}
    
    # ===== NOTIFICAÇÕES =====
    if "notificacao_campos_ai" not in st.session_state:
        st.session_state.notificacao_campos_ai = {
            "tipo": "",
            "motivo": "",
            "prazo": "",
            "fundamentacao": "",
            "destinatario": ""
        }
    
    if "notificacao_buffer" not in st.session_state:
        st.session_state.notificacao_buffer = ""
    
    # ===== EXPORTS =====
    if "ultimo_export" not in st.session_state:
        st.session_state.ultimo_export = None
    
    # ===== LOGS =====
    if "logs_sistema" not in st.session_state:
        st.session_state.logs_sistema = []
    
    # ===== TIMESTAMP =====
    if "session_start" not in st.session_state:
        st.session_state.session_start = datetime.now()


def reset_chat_history():
    """Reseta o histórico do chat (copilot)"""
    st.session_state.chat_history = []
    st.session_state.copilot_buffer = ""


def reset_notificacao():
    """Reseta os campos de notificação"""
    st.session_state.notificacao_campos_ai = {
        "tipo": "",
        "motivo": "",
        "prazo": "",
        "fundamentacao": "",
        "destinatario": ""
    }
    st.session_state.notificacao_buffer = ""


def add_log(tipo: str, mensagem: str):
    """
    Adiciona um log ao sistema.
    
    Args:
        tipo: Tipo do log (INFO, WARNING, ERROR, SUCCESS)
        mensagem: Mensagem do log
    """
    log_entry = {
        "timestamp": datetime.now(),
        "tipo": tipo,
        "mensagem": mensagem,
        "usuario": st.session_state.get("usuario", "Desconhecido")
    }
    st.session_state.logs_sistema.append(log_entry)


def get_current_user_info():
    """
    Retorna informações do usuário atual.
    
    Returns:
        dict: Informações do usuário
    """
    return {
        "usuario": st.session_state.get("usuario", "Desconhecido"),
        "perfil": st.session_state.get("perfil", "Não definido"),
        "raj": st.session_state.get("raj", "N/A"),
        "session_start": st.session_state.get("session_start", datetime.now())
    }
