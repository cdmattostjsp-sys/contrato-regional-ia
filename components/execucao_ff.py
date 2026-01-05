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
        from ui.forms_help import help_prazo
        with st.form("form_nova_medicao", clear_on_submit=True):
            competencia = st.text_input(
                "Competência (YYYY-MM)",
                placeholder="Ex: 2025-01",
                help="Informe o mês e ano da medição no formato AAAA-MM."
            )
            etapa_id = st.text_input(
                "Etapa (ID ou 'Geral')",
                placeholder="Ex: 1, 2, Geral",
                help="Identifique a etapa da medição. Use 'Geral' se não houver etapas."
            )
            percentual_no_periodo = st.number_input(
                "% no período", 0.0, 100.0, 0.0,
                help="Percentual executado no período informado."
            )
            percentual_acumulado = st.number_input(
                "% acumulado", 0.0, 100.0, 0.0,
                help="Percentual acumulado até a data da medição."
            )
            valor_medido = st.number_input(
                "Valor medido (R$)", 0.0,
                help="Valor financeiro correspondente à medição."
            )
            data_medicao = st.date_input(
                "Data da medição",
                value=datetime.today(),
                help="Data de referência da medição."
            )
            ateste_status = st.selectbox(
                "Status do ateste",
                ["PENDENTE", "ATESTADO"],
                help="Indica se o ateste foi realizado."
            )
            responsavel_ateste = st.text_input(
                "Responsável pelo ateste (opcional)",
                placeholder="Ex: João da Silva",
                help="Nome do responsável pelo ateste, se aplicável."
            )
            observacoes = st.text_area(
                "Observações",
                placeholder="Inclua informações relevantes sobre a medição.",
                help="Descreva detalhes adicionais, se necessário."
            )
            evidencia_link = st.text_input(
                "Evidência (link ou caminho, opcional)",
                placeholder="Ex: https://drive.tjsp/...",
                help="Informe o link ou caminho do arquivo de evidência, se houver."
            )
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
            medicao_id = st.text_input(
                "ID da Medição (opcional)",
                placeholder="Ex: 2025-01-1",
                help="Identificador da medição relacionada, se aplicável."
            )
            data_pagamento = st.date_input(
                "Data do pagamento",
                value=datetime.today(),
                help="Data em que o pagamento foi realizado."
            )
            valor_pago = st.number_input(
                "Valor pago (R$)", 0.0,
                help="Valor financeiro efetivamente pago."
            )
            tipo = st.selectbox(
                "Tipo",
                ["MEDICAO", "ADIANTAMENTO", "REAJUSTE", "RETENCAO", "GLOSA", "OUTRO"],
                help="Classificação do pagamento."
            )
            referencia_nf = st.text_input(
                "Referência NF (opcional)",
                placeholder="Ex: NF 12345",
                help="Número da nota fiscal vinculada, se houver."
            )
            referencia_ne_empenho = st.text_input(
                "Referência NE/Empenho (opcional)",
                placeholder="Ex: NE 2025/0001",
                help="Número da NE ou empenho relacionado, se houver."
            )
            status = st.selectbox(
                "Status",
                ["PREVISTO", "REALIZADO"],
                help="Situação do pagamento."
            )
            observacoes = st.text_area(
                "Observações",
                placeholder="Inclua informações relevantes sobre o pagamento.",
                help="Descreva detalhes adicionais, se necessário."
            )
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
    """
    Renderiza alertas e pendências de execução físico-financeira.
    
    Integra com ff_alert_rules para calcular alertas reais baseados
    nos registros financeiros do contrato.
    """
    st.subheader("Alertas e Pendências")
    
    try:
        from services.ff_alert_rules import compute_ff_alerts_for_contract
        from services.contract_service import get_todos_contratos
        from services.history_service import log_event
        
        # Calcula alertas FF para o contrato
        alertas_ff = compute_ff_alerts_for_contract(contract_id)
        
        if not alertas_ff:
            st.success("✅ Nenhum alerta de execução físico-financeira identificado.")
            return
        
        # Agrupa alertas por tipo
        alertas_criticos = [a for a in alertas_ff if a.get('tipo') == 'critico']
        alertas_atencao = [a for a in alertas_ff if a.get('tipo') == 'atencao']
        alertas_info = [a for a in alertas_ff if a.get('tipo') == 'info']
        
        # Exibe resumo
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔴 Críticos", len(alertas_criticos))
        with col2:
            st.metric("🟡 Atenção", len(alertas_atencao))
        with col3:
            st.metric("🔵 Informativos", len(alertas_info))
        
        st.markdown("---")
        
        # Renderiza alertas críticos
        if alertas_criticos:
            st.markdown("### 🔴 Alertas Críticos")
            for alerta in alertas_criticos:
                with st.container():
                    st.error(f"**{alerta.get('titulo')}**")
                    st.write(alerta.get('descricao'))
                    
                    metadados = alerta.get('metadados_ff', {})
                    if metadados:
                        st.caption(f"📋 **Detalhes:** {', '.join([f'{k}: {v}' for k, v in metadados.items() if k != 'regra'])}")
                    
                    st.markdown("---")
        
        # Renderiza alertas de atenção
        if alertas_atencao:
            st.markdown("### 🟡 Alertas de Atenção")
            for alerta in alertas_atencao:
                with st.container():
                    st.warning(f"**{alerta.get('titulo')}**")
                    st.write(alerta.get('descricao'))
                    
                    metadados = alerta.get('metadados_ff', {})
                    if metadados:
                        st.caption(f"📋 **Detalhes:** {', '.join([f'{k}: {v}' for k, v in metadados.items() if k != 'regra'])}")
                    
                    st.markdown("---")
        
        # Renderiza alertas informativos
        if alertas_info:
            with st.expander(f"🔵 Alertas Informativos ({len(alertas_info)})"):
                for alerta in alertas_info:
                    st.info(f"**{alerta.get('titulo')}**")
                    st.write(alerta.get('descricao'))
                    st.markdown("---")
        
        # Registra evento de alertas FF calculados (apenas uma vez por sessão)
        session_key = f"ff_alertas_logged_{contract_id}"
        if session_key not in st.session_state:
            try:
                contratos = get_todos_contratos()
                contrato = next((c for c in contratos if c['id'] == contract_id), None)
                
                if contrato:
                    log_event(
                        contract=contrato,
                        event_type="FF_ALERTA_GERADO",
                        title=f"Alertas FF calculados: {len(alertas_ff)} alertas",
                        details=f"{len(alertas_criticos)} críticos, {len(alertas_atencao)} atenção, {len(alertas_info)} informativos",
                        source="Execução Físico-Financeira",
                        actor="Sistema",
                        metadata={
                            'total_alertas': len(alertas_ff),
                            'criticos': len(alertas_criticos),
                            'atencao': len(alertas_atencao),
                            'informativos': len(alertas_info)
                        }
                    )
                    st.session_state[session_key] = True
            except Exception as e:
                pass  # Não bloqueia UI se logging falhar
        
    except Exception as e:
        st.error(f"Erro ao calcular alertas: {e}")
        st.info("💡 **Observação:** Alertas de execução FF requerem registros financeiros cadastrados.")
