import streamlit as st
import json
from services.history_service import list_events, get_event_types, get_sources
from datetime import datetime, timedelta

def render_bloco_historico(contrato):
    st.markdown("## Histórico do Contrato")
    if not contrato or not contrato.get("id"):
        st.info("Selecione um contrato para visualizar o histórico.")
        return
    contract_id = contrato["id"]
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        periodo_opcoes = ["7 dias", "30 dias", "90 dias", "Todos"]
        periodo = st.selectbox("Período", periodo_opcoes, index=1, key="hist_periodo")
    with col2:
        tipos = ["Todos"] + get_event_types(contract_id)
        tipo_evento = st.selectbox("Tipo de Evento", tipos, key="hist_tipo")
    with col3:
        sources = ["Todos"] + get_sources(contract_id)
        source = st.selectbox("Módulo", sources, key="hist_source")
    # Calcula datas
    date_from = None
    if periodo != "Todos":
        dias = int(periodo.split()[0])
        date_from = (datetime.now() - timedelta(days=dias)).isoformat()
    eventos = list_events(
        contract_id,
        date_from=date_from,
        event_type=tipo_evento,
        source=source,
        limit=200
    )
    if not eventos:
        st.info("Ainda não há eventos registrados para este contrato.")
        return
    for ev in eventos:
        with st.container():
            ts = datetime.fromisoformat(ev["timestamp"]).strftime("%d/%m/%Y %H:%M")
            st.markdown(f"**{ts} — {ev['title']}**")
            st.markdown(f"<span style='font-size:0.92em'>`{ev['event_type']}` | `{ev['source']}`</span>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-bottom:0.5em'>{ev['details']}</div>", unsafe_allow_html=True)
            with st.expander("Detalhes do evento"):
                try:
                    meta = json.loads(ev["metadata_json"] or "{}")
                    st.json(meta, expanded=False)
                except Exception:
                    st.text(ev["metadata_json"])
            st.markdown("---")import streamlit as st
import json
from services.history_service import list_events
from datetime import datetime, timedelta

def render_bloco_historico(contrato):
    st.markdown("## Histórico do Contrato")
    if not contrato or not contrato.get("id"):
        st.info("Selecione um contrato para visualizar o histórico.")
        return
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        periodo_opcoes = {
            "Últimos 7 dias": 7,
            "Últimos 30 dias": 30,
            "Últimos 90 dias": 90,
            "Todos": None
        }
        periodo_sel = st.selectbox("Período", list(periodo_opcoes.keys()), key="hist_periodo")
    with col2:
        tipo_sel = st.selectbox("Tipo de Evento", ["Todos", "NOTIFICACAO_GERADA", "NOTIFICACAO_EXPORTADA_DOCX", "CONTRATO_SELECIONADO"], key="hist_tipo")
    with col3:
        source_sel = st.selectbox("Módulo", ["Todos", "Notificações", "Contrato", "Copiloto"], key="hist_source")
    # Datas filtro
    date_from = None
    if periodo_opcoes[periodo_sel]:
        date_from = (datetime.now() - timedelta(days=periodo_opcoes[periodo_sel])).isoformat()
    # Busca eventos
    eventos = list_events(
        contrato_id=contrato["id"],
        date_from=date_from,
        event_type=tipo_sel,
        source=source_sel,
        limit=200
    )
    if not eventos:
        st.info("Ainda não há eventos registrados para este contrato.")
        return
    # Timeline
    for ev in eventos:
        with st.container():
            ts = datetime.fromisoformat(ev["timestamp"]).strftime("%d/%m/%Y %H:%M")
            st.markdown(f"**{ts} — {ev['title']}**")
            st.markdown(f"<span style='font-size:0.92em'>`{ev['event_type']}` | `{ev['source']}`</span>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-bottom:0.3em'>{ev['details']}</div>", unsafe_allow_html=True)
            meta = ev.get("metadata_json")
            if meta and meta != "{}":
                with st.expander("Detalhes do evento"):
                    try:
                        st.json(json.loads(meta), expanded=False)
                    except Exception:
                        st.text(meta)
            st.markdown("---")
