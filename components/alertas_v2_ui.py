"""
Componente de UI para Alertas V2 (Ciclo de Vida)
=================================================
Interface visual para o novo modelo de alertas com ciclo de vida completo.
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional, Callable


def render_alerta_v2_card(alerta: Dict, on_action: Optional[Callable] = None):
    """
    Renderiza card de alerta V2 com informações completas de ciclo de vida.
    
    Args:
        alerta: Dicionário com dados do alerta V2
        on_action: Callback para ações do usuário
    """
    
    # Configurações visuais por tipo
    config_tipos = {
        'preventivo': {
            'cor': '#17A2B8',
            'cor_bg': '#D1ECF1',
            'icone': '🔵',
            'label': 'PREVENTIVO'
        },
        'operacional': {
            'cor': '#6C757D',
            'cor_bg': '#E2E3E5',
            'icone': '⚙️',
            'label': 'OPERACIONAL'
        },
        'critico': {
            'cor': '#DC3545',
            'cor_bg': '#F8D7DA',
            'icone': '🔴',
            'label': 'CRÍTICO'
        },
        'escalonado': {
            'cor': '#CC0000',
            'cor_bg': '#FFCCCC',
            'icone': '🚨',
            'label': 'ESCALONADO'
        },
        'informativo': {
            'cor': '#28A745',
            'cor_bg': '#D4EDDA',
            'icone': 'ℹ️',
            'label': 'INFORMATIVO'
        }
    }
    
    config = config_tipos.get(alerta.get('tipo', 'informativo'), config_tipos['informativo'])
    
    # Configuração de criticidade
    config_criticidade = {
        'baixa': {'cor': '#28A745', 'icone': '▼'},
        'media': {'cor': '#FFC107', 'icone': '●'},
        'alta': {'cor': '#DC3545', 'icone': '▲'},
        'urgente': {'cor': '#CC0000', 'icone': '⚠️'}
    }
    
    crit = config_criticidade.get(alerta.get('criticidade', 'media'), config_criticidade['media'])
    
    # Configuração de estado
    config_estado = {
        'novo': {'cor': '#007BFF', 'label': 'Novo'},
        'em_analise': {'cor': '#17A2B8', 'label': 'Em Análise'},
        'providencia_em_curso': {'cor': '#FFC107', 'label': 'Em Execução'},
        'aguardando_prazo': {'cor': '#6C757D', 'label': 'Aguardando'},
        'resolvido': {'cor': '#28A745', 'label': 'Resolvido'},
        'encerrado': {'cor': '#343A40', 'label': 'Encerrado'},
        'escalonado': {'cor': '#DC3545', 'label': 'Escalonado'}
    }
    
    estado_config = config_estado.get(alerta.get('estado', 'novo'), config_estado['novo'])
    
    # Container do card
    with st.container():
        # Cabeçalho com badges
        col_badges, col_data = st.columns([3, 1])
        
        with col_badges:
            st.markdown(
                f"<span style='background: {config['cor']}; color: white; padding: 0.3rem 0.8rem; "
                f"border-radius: 15px; font-size: 0.75rem; font-weight: bold;'>"
                f"{config['icone']} {config['label']}</span>&nbsp;&nbsp;"
                f"<span style='background: {estado_config['cor']}; color: white; padding: 0.3rem 0.8rem; "
                f"border-radius: 15px; font-size: 0.75rem; font-weight: bold;'>"
                f"{alerta.get('estado', 'novo').upper()}</span>&nbsp;&nbsp;"
                f"<span style='background: {crit['cor']}; color: white; padding: 0.3rem 0.8rem; "
                f"border-radius: 15px; font-size: 0.75rem; font-weight: bold;'>"
                f"{crit['icone']} {alerta.get('criticidade', 'media').upper()}</span>",
                unsafe_allow_html=True
            )
        
        with col_data:
            data_criacao = alerta.get('data_criacao', '')
            if data_criacao:
                try:
                    dt = datetime.fromisoformat(data_criacao)
                    data_formatada = dt.strftime('%d/%m/%Y %H:%M')
                except:
                    data_formatada = str(data_criacao)
            else:
                data_formatada = 'N/A'
            st.caption(data_formatada)
        
        # Título e descrição
        titulo = alerta.get('titulo', 'Sem título')
        st.markdown(f"### {config['icone']} {titulo}")
        
        descricao = alerta.get('descricao', 'Sem descrição')
        st.write(descricao)
        
        # Informações principais
        col_info1, col_info2, col_info3 = st.columns(3)
        
        with col_info1:
            st.caption("**Contrato:**")
            st.write(alerta.get('contrato_numero', 'N/A'))
        
        with col_info2:
            st.caption("**Responsável:**")
            st.write(alerta.get('responsavel', 'Não definido'))
        
        with col_info3:
            st.caption("**Geração:**")
            geracao = alerta.get('geracao', 1)
            if geracao == 1:
                st.write(f"🌱 {geracao} (raiz)")
            else:
                st.write(f"🔗 {geracao} (derivado)")
        
        # Métricas de prazo e risco
        st.markdown("---")
        
        col_prazo, col_janela, col_risco = st.columns(3)
        
        with col_prazo:
            dias_restantes = alerta.get('dias_restantes', 0)
            if dias_restantes < 0:
                st.metric("⏱️ Prazo", f"{abs(dias_restantes)}d", "VENCIDO", delta_color="inverse")
            elif dias_restantes < 7:
                st.metric("⏱️ Prazo", f"{dias_restantes}d", "Urgente", delta_color="inverse")
            else:
                st.metric("⏱️ Prazo", f"{dias_restantes}d", "Restantes")
        
        with col_janela:
            janela = alerta.get('janela_seguranca_dias')
            if janela is not None:
                if janela < 0:
                    st.metric("🛡️ Janela", f"{abs(janela)}d", "Insuficiente", delta_color="inverse")
                elif janela < 5:
                    st.metric("🛡️ Janela", f"{janela}d", "Apertado", delta_color="off")
                else:
                    st.metric("🛡️ Janela", f"{janela}d", "Adequado", delta_color="normal")
            else:
                st.metric("🛡️ Janela", "N/A", "Não calculado")
        
        with col_risco:
            score_risco = alerta.get('score_risco')
            if score_risco is not None:
                percentual = int(score_risco * 100)
                if score_risco > 0.7:
                    st.metric("⚠️ Risco", f"{percentual}%", "Alto", delta_color="inverse")
                elif score_risco > 0.4:
                    st.metric("⚠️ Risco", f"{percentual}%", "Médio", delta_color="off")
                else:
                    st.metric("⚠️ Risco", f"{percentual}%", "Baixo", delta_color="normal")
            else:
                st.metric("⚠️ Risco", "N/A", "Não calculado")
        
        # Ações registradas
        num_acoes = len(alerta.get('acoes_ids', []))
        if num_acoes > 0:
            st.info(f"📋 {num_acoes} ação(ões) registrada(s)")
        
        # Encadeamento
        if alerta.get('alerta_origem_id'):
            st.info(f"🔗 Derivado de outro alerta (Geração {geracao})")
        
        num_derivados = len(alerta.get('alertas_derivados', []))
        if num_derivados > 0:
            st.info(f"🌿 {num_derivados} alerta(s) derivado(s) criado(s)")
        
        st.markdown("---")
        
        # Botões de ação
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📄 Contrato", key=f"v2_ver_{alerta['id']}", use_container_width=True):
                if on_action:
                    on_action('ver_contrato', alerta)
        
        with col2:
            if st.button("📝 Registrar Ação", key=f"v2_acao_{alerta['id']}", use_container_width=True):
                if on_action:
                    on_action('registrar_acao', alerta)
        
        with col3:
            if st.button("📊 Histórico", key=f"v2_hist_{alerta['id']}", use_container_width=True):
                if on_action:
                    on_action('ver_historico', alerta)
        
        with col4:
            if alerta.get('estado') not in ['resolvido', 'encerrado']:
                if st.button("✅ Resolver", key=f"v2_resolve_{alerta['id']}", use_container_width=True):
                    if on_action:
                        on_action('resolver', alerta)


def render_registro_acao_form(alerta: Dict, on_submit: Optional[Callable] = None):
    """
    Renderiza formulário para registro de ação em um alerta.
    
    Args:
        alerta: Alerta para o qual a ação será registrada
        on_submit: Callback quando o formulário for submetido
    """
    st.subheader("📝 Registrar Ação no Alerta")
    
    with st.form(key=f"form_acao_{alerta['id']}"):
        st.write(f"**Alerta:** {alerta.get('titulo', 'N/A')}")
        st.caption(f"Contrato: {alerta.get('contrato_numero', 'N/A')}")
        
        st.markdown("---")
        
        # Tipo de ação
        tipo_acao = st.selectbox(
            "Tipo de Ação",
            options=[
                'decisao_renovar',
                'decisao_nao_renovar',
                'decisao_licitar',
                'providencia_iniciar_processo',
                'providencia_solicitar_doc',
                'justificativa_adiamento',
                'verificacao_realizada'
            ],
            format_func=lambda x: {
                'decisao_renovar': '✅ Decisão: Renovar contrato',
                'decisao_nao_renovar': '❌ Decisão: Não renovar',
                'decisao_licitar': '📢 Decisão: Nova licitação',
                'providencia_iniciar_processo': '⚙️ Providência: Iniciar processo',
                'providencia_solicitar_doc': '📄 Providência: Solicitar documentação',
                'justificativa_adiamento': '⏱️ Justificativa: Adiamento',
                'verificacao_realizada': '🔍 Verificação realizada'
            }.get(x, x)
        )
        
        # Decisão (se aplicável)
        decisao = None
        if 'decisao' in tipo_acao:
            decisao = st.text_input("Decisão Tomada", placeholder="Ex: RENOVAR, NÃO RENOVAR, LICITAR")
        
        # Justificativa (obrigatória)
        justificativa = st.text_area(
            "Justificativa (obrigatória)",
            placeholder="Descreva a ação tomada, fundamentação legal, contexto, etc.",
            height=150
        )
        
        # Novo prazo (opcional)
        col_prazo, col_dias = st.columns(2)
        
        with col_prazo:
            definir_prazo = st.checkbox("Definir novo prazo")
        
        with col_dias:
            prazo_novo_dias = None
            if definir_prazo:
                prazo_novo_dias = st.number_input("Prazo (dias)", min_value=1, max_value=365, value=30)
        
        # Documentos (opcional)
        documentos_texto = st.text_input(
            "Documentos relacionados (opcional)",
            placeholder="Ex: Parecer PAJ-2025-001, Processo SEI 2025.1.0001"
        )
        
        documentos = []
        if documentos_texto:
            documentos = [doc.strip() for doc in documentos_texto.split(',')]
        
        # Botões
        col_submit, col_cancel = st.columns(2)
        
        with col_submit:
            submitted = st.form_submit_button("✅ Registrar Ação", use_container_width=True, type="primary")
        
        with col_cancel:
            cancel = st.form_submit_button("❌ Cancelar", use_container_width=True)
        
        if submitted:
            if not justificativa or len(justificativa.strip()) < 10:
                st.error("⚠️ Justificativa deve ter pelo menos 10 caracteres.")
            else:
                if on_submit:
                    on_submit({
                        'tipo_acao': tipo_acao,
                        'decisao': decisao,
                        'justificativa': justificativa,
                        'prazo_novo_dias': prazo_novo_dias,
                        'documentos': documentos
                    })
        
        if cancel:
            st.rerun()


def render_historico_alerta(alerta: Dict):
    """
    Renderiza histórico completo de um alerta V2.
    
    Args:
        alerta: Alerta para exibir histórico
    """
    st.subheader("📊 Histórico do Alerta")
    
    st.write(f"**Alerta:** {alerta.get('titulo', 'N/A')}")
    st.caption(f"ID: {alerta.get('id', 'N/A')}")
    
    st.markdown("---")
    
    # Timeline de estados
    st.markdown("### 📅 Linha do Tempo de Estados")
    
    historico = alerta.get('historico_estados', [])
    
    if not historico:
        st.info("Nenhuma transição de estado registrada.")
    else:
        for idx, entrada in enumerate(reversed(historico)):
            estado = entrada.get('estado', 'N/A')
            data = entrada.get('data', '')
            usuario = entrada.get('usuario', 'N/A')
            observacao = entrada.get('observacao', '')
            
            try:
                dt = datetime.fromisoformat(data)
                data_formatada = dt.strftime('%d/%m/%Y %H:%M')
            except:
                data_formatada = str(data)
            
            # Icone por estado
            icones = {
                'novo': '🆕',
                'em_analise': '🔍',
                'providencia_em_curso': '⚙️',
                'aguardando_prazo': '⏱️',
                'resolvido': '✅',
                'encerrado': '🔒',
                'escalonado': '🚨'
            }
            
            icone = icones.get(estado, '●')
            
            with st.expander(f"{icone} {estado.upper()} - {data_formatada}", expanded=(idx == 0)):
                st.write(f"**Usuário:** {usuario}")
                if observacao:
                    st.write(f"**Observação:** {observacao}")
                
                if entrada.get('estado_anterior'):
                    st.caption(f"Anterior: {entrada.get('estado_anterior')}")
    
    # Ações registradas
    st.markdown("---")
    st.markdown("### 📋 Ações Registradas")
    
    num_acoes = len(alerta.get('acoes_ids', []))
    
    if num_acoes == 0:
        st.info("Nenhuma ação registrada ainda.")
    else:
        st.write(f"Total de ações: **{num_acoes}**")
        st.caption("Para visualizar detalhes das ações, use o módulo de consulta de histórico completo.")
    
    # Métricas de risco
    if alerta.get('score_risco') is not None:
        st.markdown("---")
        st.markdown("### ⚠️ Análise de Risco")
        
        col_score, col_fatores = st.columns(2)
        
        with col_score:
            score = alerta['score_risco']
            percentual = int(score * 100)
            st.metric("Score de Risco", f"{percentual}%")
        
        with col_fatores:
            st.write("**Fatores:**")
            fatores = alerta.get('fatores_risco', {})
            for fator, valor in fatores.items():
                st.caption(f"• {fator}: {valor:.2f}")


def render_comparacao_v1_v2(alertas_v1: List[Dict], alertas_v2: List[Dict]):
    """
    Renderiza comparação lado a lado entre alertas V1 e V2.
    
    Args:
        alertas_v1: Lista de alertas do sistema V1
        alertas_v2: Lista de alertas do sistema V2
    """
    st.markdown("## 🔄 Comparação: Sistema Atual vs. Novo Modelo")
    
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.markdown("### 📌 Sistema Atual (V1)")
        st.info(f"**Total:** {len(alertas_v1)} alerta(s)")
        st.caption("Modelo tradicional: alerta = notificação")
        
        if alertas_v1:
            # Resumo V1
            criticos = sum(1 for a in alertas_v1 if a.get('tipo') == 'critico')
            atencao = sum(1 for a in alertas_v1 if a.get('tipo') == 'atencao')
            info = sum(1 for a in alertas_v1 if a.get('tipo') == 'info')
            
            st.metric("🔴 Críticos", criticos)
            st.metric("🟡 Atenção", atencao)
            st.metric("🔵 Informativos", info)
    
    with col_v2:
        st.markdown("### 🚀 Novo Modelo (V2)")
        st.success(f"**Total:** {len(alertas_v2)} alerta(s)")
        st.caption("Modelo evolutivo: alerta = processo com ciclo de vida")
        
        if alertas_v2:
            # Resumo V2
            por_tipo = {}
            por_estado = {}
            
            for alerta in alertas_v2:
                tipo = alerta.get('tipo', 'N/A')
                estado = alerta.get('estado', 'N/A')
                por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
                por_estado[estado] = por_estado.get(estado, 0) + 1
            
            st.write("**Por Tipo:**")
            for tipo, qtd in por_tipo.items():
                st.caption(f"• {tipo}: {qtd}")
            
            st.write("**Por Estado:**")
            for estado, qtd in por_estado.items():
                st.caption(f"• {estado}: {qtd}")
