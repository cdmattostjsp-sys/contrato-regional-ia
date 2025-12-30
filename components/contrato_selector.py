import streamlit as st
from services.contract_service import get_todos_contratos
from .contratos_ui import filtrar_contratos

def render_contrato_selector(
    contratos: list[dict],
    *,
    titulo: str = "Central de Consulta de Contratos",
    help_text: str = "Use a busca e filtros para localizar um contrato e selecionar.",
    key_prefix: str = "selector",
) -> dict | None:
    """
    Renderiza UI de busca + filtros + lista.
    Retorna o contrato selecionado (dict) ou None.
    """
    st.markdown(f"### {titulo}")
    st.info(help_text)
    busca = st.text_input("Buscar contrato", key=f"{key_prefix}_busca")
    with st.expander("Filtros Avançados"):
        col1, col2 = st.columns(2)
        with col1:
            filtro_status = st.selectbox("Status", ["Todos", "Ativos", "Atenção", "Crítico"], key=f"{key_prefix}_status")
            filtro_tipo = st.selectbox("Tipo", ["Todos", "Ordinário", "Extraordinário"], key=f"{key_prefix}_tipo")
        with col2:
            filtro_fornecedor = st.text_input("Fornecedor", key=f"{key_prefix}_fornecedor")
            filtro_num_contrato = st.text_input("Nº Contrato", key=f"{key_prefix}_num_contrato")
    contratos_filtrados = filtrar_contratos(
        contratos,
        busca=busca,
        filtro_num_contrato=filtro_num_contrato,
        filtro_fornecedor=filtro_fornecedor if filtro_fornecedor else None,
        filtro_status=filtro_status,
        filtro_tipo=filtro_tipo,
    )
    selecionado = None
    if not contratos_filtrados:
        st.warning("❌ Nenhum contrato encontrado com os filtros aplicados.")
    for contrato in contratos_filtrados:
        col1, col2 = st.columns([8,2])
        with col1:
            st.markdown(f"**{contrato.get('numero','')}** - {contrato.get('fornecedor','')}<br>**Objeto:** {contrato.get('objeto','')}", unsafe_allow_html=True)
        with col2:
            if st.button("Selecionar", key=f"{key_prefix}_select_{contrato['id']}"):
                selecionado = contrato
        st.markdown("---")
    return selecionado
