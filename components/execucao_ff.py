"""
Componente de interface para Execução Físico-Financeira de contratos.
Blocos: KPIs, Medições, Pagamentos, Alertas.
"""
import streamlit as st
from services.ff_service import (
    get_baseline, set_baseline, get_etapas, add_etapa, get_medicoes, add_medicao, get_pagamentos, add_pagamento
)
from services.contract_service import get_todos_contratos
from services.history_service import log_event
from datetime import datetime

def render_bloco_execucao_fisico_financeira(contract_id):
    st.header("Execução Físico-Financeira")
    # 1. KPIs do contrato
    render_kpis(contract_id)
    st.divider()
    # 2. Medições
    render_medicoes(contract_id)
    st.divider()
    # 3. Pagamentos
    render_pagamentos(contract_id)
    st.divider()
    # 4. Alertas e Pendências
    render_alertas_ff(contract_id)

def render_kpis(contract_id):
    baseline = get_baseline(contract_id)
    medicoes = get_medicoes(contract_id)
    pagamentos = get_pagamentos(contract_id)
    # KPIs simplificados (implementação completa nos próximos passos)
    valor_total = baseline.get("valor_contratual_total", 0) if baseline else 0
    total_pago = sum(p.get("valor_pago", 0) for p in pagamentos if p.get("status") == "REALIZADO")
    percentual_financeiro = (total_pago / valor_total * 100) if valor_total else 0
    # Físico acumulado (simples)
    if medicoes:
        percentual_fisico = max(m.get("percentual_acumulado", 0) for m in medicoes)
    else:
        percentual_fisico = 0
    saldo = valor_total - total_pago
    descolamento = percentual_fisico - percentual_financeiro
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("% Físico acumulado", f"{percentual_fisico:.1f}%")
    col2.metric("% Financeiro realizado", f"{percentual_financeiro:.1f}%")
    col3.metric("Saldo contratual", f"R$ {saldo:,.2f}")
    col4.metric("Descolamento (pp)", f"{descolamento:.1f}")

def render_medicoes(contract_id):
    st.subheader("Medições (Físico)")
    medicoes = get_medicoes(contract_id)
    st.dataframe(medicoes)
    if st.button("Nova medição", key="btn_nova_medicao"):
        with st.form("form_nova_medicao", clear_on_submit=True):
            competencia = st.text_input("Competência (YYYY-MM)")
            etapa_id = st.text_input("Etapa (ID ou 'Geral')")
            percentual_no_periodo = st.number_input("% no período", 0.0, 100.0, 0.0)
            percentual_acumulado = st.number_input("% acumulado", 0.0, 100.0, 0.0)
            valor_medido = st.number_input("Valor medido (R$)", 0.0)
            data_medicao = st.date_input("Data da medição", value=datetime.today())
            ateste_status = st.selectbox("Status do ateste", ["PENDENTE", "ATESTADO"])
            responsavel_ateste = st.text_input("Responsável pelo ateste (opcional)")
            observacoes = st.text_area("Observações")
            evidencia_link = st.text_input("Evidência (link ou caminho, opcional)")
            submitted = st.form_submit_button("Salvar")
            if submitted:
                medicao = {
                    "medicao_id": f"{contract_id}_{competencia}_{etapa_id}_{datetime.now().timestamp()}",
                    "contract_id": contract_id,
                    "competencia": competencia,
                    "etapa_id": etapa_id,
                    "percentual_no_periodo": percentual_no_periodo,
                    "percentual_acumulado": percentual_acumulado,
                    "valor_medido": valor_medido,
                    "data_medicao": str(data_medicao),
                    "ateste_status": ateste_status,
                    "responsavel_ateste": responsavel_ateste,
                    "observacoes": observacoes,
                    "evidencia_link": evidencia_link
                }
                add_medicao(contract_id, medicao)
                log_event(contract_id, event_type="FF_MEDICAO_CRIADA", title="Medição criada", details=f"{competencia} - {etapa_id}", source="Execução Físico-Financeira")
                st.success("Medição salva!")

def render_pagamentos(contract_id):
    st.subheader("Pagamentos (Financeiro)")
    pagamentos = get_pagamentos(contract_id)
    st.dataframe(pagamentos)
    if st.button("Novo pagamento", key="btn_novo_pagamento"):
        with st.form("form_novo_pagamento", clear_on_submit=True):
            medicao_id = st.text_input("ID da Medição (opcional)")
            data_pagamento = st.date_input("Data do pagamento", value=datetime.today())
            valor_pago = st.number_input("Valor pago (R$)", 0.0)
            tipo = st.selectbox("Tipo", ["MEDICAO", "ADIANTAMENTO", "REAJUSTE", "RETENCAO", "GLOSA", "OUTRO"])
            referencia_nf = st.text_input("Referência NF (opcional)")
            referencia_ne_empenho = st.text_input("Referência NE/Empenho (opcional)")
            status = st.selectbox("Status", ["PREVISTO", "REALIZADO"])
            observacoes = st.text_area("Observações")
            submitted = st.form_submit_button("Salvar")
            if submitted:
                pagamento = {
                    "pagamento_id": f"{contract_id}_{tipo}_{datetime.now().timestamp()}",
                    "contract_id": contract_id,
                    "medicao_id": medicao_id,
                    "data_pagamento": str(data_pagamento),
                    "valor_pago": valor_pago,
                    "tipo": tipo,
                    "referencia_nf": referencia_nf,
                    "referencia_ne_empenho": referencia_ne_empenho,
                    "status": status,
                    "observacoes": observacoes
                }
                add_pagamento(contract_id, pagamento)
                log_event(contract_id, event_type="FF_PAGAMENTO_REGISTRADO", title="Pagamento registrado", details=f"{tipo} - R$ {valor_pago}", source="Execução Físico-Financeira")
                st.success("Pagamento salvo!")

def render_alertas_ff(contract_id):
    st.subheader("Alertas e Pendências")
    st.info("Regras de alerta e validação serão implementadas nos próximos passos.")
