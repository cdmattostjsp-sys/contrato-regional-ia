import streamlit as st
from services.contract_service import get_todos_contratos
from components.contrato_selector import render_contrato_selector

def ensure_contrato_context(key_prefix: str) -> dict:
    """
    Garante que o contrato selecionado está presente e enriquecido com objeto.
    Se não houver, renderiza seletor e interrompe fluxo.
    """
    if (
        not st.session_state.get("contrato_selecionado")
        or st.session_state.get("modo_selecao_contrato")
    ):
        contratos = get_todos_contratos()
        selecionado = render_contrato_selector(
            contratos,
            titulo="Central de Consulta de Contratos",
            help_text="Selecione um contrato para continuar.",
            key_prefix=key_prefix
        )
        if selecionado:
            # Enriquecer com objeto e outros campos
            contrato = next((c for c in contratos if c.get("id") == selecionado["id"]), selecionado)
            st.session_state["contrato_selecionado"] = contrato
            st.session_state["modo_selecao_contrato"] = False
            st.rerun()
        return None
    contrato = st.session_state["contrato_selecionado"]
    # Enriquecer com objeto se faltar
    if not contrato.get("objeto"):
        contratos = get_todos_contratos()
        encontrado = next((c for c in contratos if c.get("id") == contrato.get("id") or c.get("numero") == contrato.get("numero")), None)
        if encontrado:
            contrato["objeto"] = encontrado.get("objeto", "")
            contrato["fornecedor"] = encontrado.get("fornecedor", contrato.get("fornecedor", ""))
            contrato["numero"] = encontrado.get("numero", contrato.get("numero", ""))
            contrato["unidade"] = encontrado.get("unidade", contrato.get("unidade", ""))
    return contrato

def render_context_bar(contrato: dict, key_prefix: str):
    """
    Renderiza barra verde de contexto do contrato selecionado + botão Trocar contrato.
    """
    col_a, col_b = st.columns([8,2])
    with col_a:
        st.markdown(f"<div style='background:#b9f6ca;padding:0.7rem 1.2rem;border-radius:8px;color:#222;font-weight:500;font-size:1.08rem;'>Contrato selecionado: Nº {contrato.get('numero','')} — Fornecedor: {contrato.get('fornecedor','')}</div>", unsafe_allow_html=True)
    with col_b:
        if st.button("Trocar contrato", key=f"{key_prefix}_trocar_contrato", use_container_width=True):
            st.session_state["modo_selecao_contrato"] = True
            st.rerun()

def render_module_banner(title: str, subtitle: str | None):
    """
    Renderiza banner azul institucional compacto, sem ícones/emoji.
    """
    st.markdown(f"""
        <div style="background:#003366;padding:1.1rem 1.6rem;border-radius:14px;width:100%;margin-bottom:16px;">
            <div style="font-size:1.25rem;font-weight:700;color:#fff;">{title}</div>
            {f'<div style="font-size:0.98rem;color:#e0e6ef;font-weight:400;margin-top:0.3rem;">{subtitle}</div>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)
