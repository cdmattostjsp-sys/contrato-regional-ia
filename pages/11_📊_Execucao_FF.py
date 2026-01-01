"""
Página de Execução Físico-Financeira
====================================
Acompanhamento físico-financeiro de contratos TJSP.
"""
import streamlit as st
from components.layout_header import render_context_bar, render_module_banner
from components.execucao_ff import render_bloco_execucao_fisico_financeira
from services.contract_service import get_todos_contratos
from services.session_manager import initialize_session_state

def main():
    st.set_page_config(
        page_title="Execução Físico-Financeira",
        page_icon="📊",
        layout="wide"
    )
    initialize_session_state()
    # Seleção de contrato
    contratos = get_todos_contratos()
    contrato = st.session_state.get("contrato_selecionado")
    if not contrato:
        st.warning("Selecione um contrato para acompanhar a execução físico-financeira.")
        return
    render_context_bar(contrato, key_prefix="ff")
    render_module_banner(
        title="Execução Físico-Financeira",
        subtitle=f"Contrato: {contrato.get('numero', '(a preencher)')} — {contrato.get('objeto', '(a preencher)')}"
    )
    render_bloco_execucao_fisico_financeira(contrato["id"])

if __name__ == "__main__":
    main()
