import streamlit as st
from services.contract_service import get_todos_contratos
from services.tag_service import get_tag_service

def filtrar_contratos(
    contratos,
    busca=None,
    filtro_num_contrato=None,
    filtro_num_processo=None,
    filtro_fornecedor=None,
    filtro_fiscal=None,
    filtro_tags=None,
    filtro_status=None,
    filtro_tipo=None
):
    """Aplica filtros e busca sobre lista de contratos."""
    contratos_filtrados = contratos
    # Filtro por busca geral (palavra-chave)
    if busca and busca.strip():
        termo_busca = busca.lower().strip()
        contratos_filtrados = [
            c for c in contratos_filtrados
            if termo_busca in c.get('numero', '').lower()
            or termo_busca in c.get('objeto', '').lower()
            or termo_busca in c.get('fornecedor', '').lower()
            or termo_busca in str(c.get('id', '')).lower()
        ]
    if filtro_num_contrato and filtro_num_contrato.strip():
        termo_contrato = filtro_num_contrato.lower().strip()
        contratos_filtrados = [
            c for c in contratos_filtrados
            if termo_contrato in c.get('numero', '').lower()
        ]
    if filtro_num_processo and filtro_num_processo.strip():
        termo_processo = filtro_num_processo.lower().strip()
        contratos_filtrados = [
            c for c in contratos_filtrados
            if termo_processo in c.get('numero', '').lower()
        ]
    if filtro_fornecedor and filtro_fornecedor != "Todos":
        contratos_filtrados = [
            c for c in contratos_filtrados
            if c.get('fornecedor') == filtro_fornecedor
        ]
    if filtro_fiscal and filtro_fiscal != "Todos":
        contratos_filtrados = [
            c for c in contratos_filtrados
            if c.get('fiscal_titular') == filtro_fiscal
        ]
    if filtro_tags:
        tag_service = get_tag_service()
        contratos_filtrados = [
            c for c in contratos_filtrados
            if any(tag_id in [t['id'] for t in tag_service.obter_tags_do_contrato(c['id'])] 
                   for tag_id in filtro_tags)
        ]
    if filtro_status and filtro_status != "Todos":
        status_map = {
            "Ativos": "ativo",
            "Atenção": "atencao",
            "Crítico": "critico"
        }
        status_busca = status_map.get(filtro_status)
        if status_busca:
            contratos_filtrados = [c for c in contratos_filtrados if c.get('status') == status_busca]
    if filtro_tipo and filtro_tipo != "Todos":
        contratos_filtrados = [c for c in contratos_filtrados if c.get('tipo') == filtro_tipo]
    return contratos_filtrados

def render_lista_contratos(contratos, abrir_callback=None):
    """Renderiza lista/tabela de contratos com botão Abrir."""
    if not contratos:
        st.warning("❌ Nenhum contrato encontrado com os filtros aplicados.")
        return
    for contrato in contratos:
        col1, col2 = st.columns([8,2])
        with col1:
            st.markdown(f"**{contrato.get('numero','')}** - {contrato.get('fornecedor','')}<br>**Objeto:** {contrato.get('objeto','')}", unsafe_allow_html=True)
        with col2:
            if st.button("📄 Abrir", key=f"abrir_{contrato['id']}"):
                if abrir_callback:
                    abrir_callback(contrato)
                else:
                    st.session_state['contrato_selecionado'] = contrato
                    st.rerun()
        st.markdown("---")
