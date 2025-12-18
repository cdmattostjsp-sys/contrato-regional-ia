"""
CONTRATO REGIONAL IA - Dashboard Principal
===========================================
Aplicativo piloto institucional para fiscalização e gestão de contratos regionais.

Instituição: Tribunal de Justiça do Estado de São Paulo (TJSP)
Projeto: Satélite ao ecossistema SAAB-Tech / Synapse.IA
Escopo inicial: RAJ 10.1

Autor: TJSP - Equipe SAAB-Tech
Data: 2025
"""

import streamlit as st
from datetime import datetime, timedelta
import sys
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import io

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state
from services.contract_service import get_todos_contratos
from services.alert_service import calcular_alertas
from services.tag_service import get_tag_service


def exportar_para_excel(contratos):
    """Exporta lista de contratos para Excel"""
    # Cria DataFrame
    dados = []
    for c in contratos:
        dados.append({
            'Número': c.get('numero', ''),
            'Fornecedor': c.get('fornecedor', ''),
            'Tipo': c.get('tipo', ''),
            'Status': c.get('status', ''),
            'Valor (R$)': c.get('valor', 0),
            'Data Início': c.get('data_inicio', ''),
            'Data Fim': c.get('data_fim', ''),
            'Fiscal': c.get('fiscal', ''),
            'Objeto': c.get('objeto', '')
        })
    
    df = pd.DataFrame(dados)
    
    # Cria arquivo Excel em memória
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Contratos', index=False)
        
        # Acessa o workbook e worksheet
        workbook = writer.book
        worksheet = writer.sheets['Contratos']
        
        # Formata header
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#003366',
            'font_color': 'white',
            'border': 1
        })
        
        # Aplica formato no header
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Ajusta largura das colunas
        worksheet.set_column('A:A', 20)  # Número
        worksheet.set_column('B:B', 35)  # Fornecedor
        worksheet.set_column('C:C', 15)  # Tipo
        worksheet.set_column('D:D', 12)  # Status
        worksheet.set_column('E:E', 15)  # Valor
        worksheet.set_column('F:G', 12)  # Datas
        worksheet.set_column('H:H', 25)  # Fiscal
        worksheet.set_column('I:I', 50)  # Objeto
    
    return output.getvalue()


def render_header():
    """Renderiza o cabeçalho institucional TJSP com botões de exportação"""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("""
            <div class="tjsp-header">
                <div class="tjsp-logo-container">
                    <h1>⚖️ TJSP - Gestão de Contratos Regionais</h1>
                    <p class="tjsp-subtitle">Sistema de Fiscalização e Acompanhamento - RAJ 10.1</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botão Meus Contratos
        if st.button("👤 Meus Contratos", use_container_width=True, type="primary"):
            st.switch_page("pages/10_Meus_Contratos.py")
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botão de exportação
        contratos = get_todos_contratos()
        
        if contratos:
            excel_data = exportar_para_excel(contratos)
            st.download_button(
                label="📥 Exportar Excel",
                data=excel_data,
                file_name=f"contratos_tjsp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="secondary"
            )


def render_metrics():
    """Renderiza métricas gerais do dashboard calculadas dinamicamente"""
    # Obtém todos os contratos
    contratos = get_todos_contratos()
    
    # Calcula alertas
    alertas = calcular_alertas(contratos)
    alertas_criticos = len([a for a in alertas if a.get('tipo') == 'critico'])
    
    # Calcula métricas reais
    total_contratos = len(contratos)
    contratos_ativos = len([c for c in contratos if c.get('status') == 'ativo'])
    contratos_atencao = len([c for c in contratos if c.get('status') == 'atencao'])
    contratos_criticos = len([c for c in contratos if c.get('status') == 'critico'])
    contratos_com_pendencias = len([c for c in contratos if c.get('pendencias')])
    
    # Valor total
    valor_total = sum(c.get('valor', 0) for c in contratos)
    
    # Taxa de conformidade (contratos sem pendências)
    taxa_conformidade = int((contratos_ativos / total_contratos * 100)) if total_contratos > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📋 Total de Contratos",
            value=f"{total_contratos}",
            delta=f"{contratos_ativos} ativos"
        )
    
    with col2:
        # Badge de alertas
        if alertas_criticos > 0:
            st.markdown(f"""
                <div style="text-align: center; cursor: pointer;" onclick="window.location.href='pages/07_🔔_Alertas.py'">
                    <span style="background: #DC3545; color: white; padding: 0.3rem 0.8rem;
                                border-radius: 20px; font-size: 0.85rem; font-weight: bold;">
                        🔔 {len(alertas)} Alertas
                    </span>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("🔔 Ver Alertas", use_container_width=True, type="primary" if alertas_criticos > 0 else "secondary"):
            st.switch_page("pages/07_🔔_Alertas.py")
        
        st.caption(f"{alertas_criticos} críticos • {len(alertas) - alertas_criticos} outros")
    
    with col3:
        st.metric(
            label="💰 Valor Total",
            value=f"R$ {valor_total/1_000_000:.1f}M",
            delta=f"{total_contratos} contratos"
        )
    
    with col4:
        st.metric(
            label="📊 Contratos Ativos",
            value=f"{taxa_conformidade}%",
            delta=f"{contratos_ativos}/{total_contratos}"
        )


def render_graficos_analytics():
    """Renderiza gráficos e visualizações analíticas do dashboard"""
    
    st.markdown("## 📊 Visão Executiva e Análises")
    
    # Obtém dados
    contratos = get_todos_contratos()
    
    if not contratos:
        st.info("Nenhum contrato disponível para análise.")
        return
    
    # Cria abas para organizar gráficos
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribuição", "📅 Timeline", "💰 Fornecedores", "📈 Status"])
    
    # ===== TAB 1: DISTRIBUIÇÃO =====
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de pizza: Contratos por Tipo
            tipos = {}
            for c in contratos:
                tipo = c.get('tipo', 'Outros')
                tipos[tipo] = tipos.get(tipo, 0) + 1
            
            fig_tipo = go.Figure(data=[go.Pie(
                labels=list(tipos.keys()),
                values=list(tipos.values()),
                hole=0.4,
                marker=dict(colors=['#003366', '#0066CC', '#66B2FF'])
            )])
            fig_tipo.update_layout(
                title="Contratos por Tipo",
                height=350,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            st.plotly_chart(fig_tipo, use_container_width=True)
        
        with col2:
            # Gráfico de pizza: Contratos por Status
            status_map = {
                'ativo': 'Ativos',
                'atencao': 'Atenção',
                'critico': 'Crítico'
            }
            status = {}
            for c in contratos:
                s = c.get('status', 'ativo')
                label = status_map.get(s, s)
                status[label] = status.get(label, 0) + 1
            
            fig_status = go.Figure(data=[go.Pie(
                labels=list(status.keys()),
                values=list(status.values()),
                hole=0.4,
                marker=dict(colors=['#28A745', '#FFC107', '#DC3545'])
            )])
            fig_status.update_layout(
                title="Contratos por Status",
                height=350,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            st.plotly_chart(fig_status, use_container_width=True)
    
    # ===== TAB 2: TIMELINE =====
    with tab2:
        st.markdown("### 📅 Vencimentos dos Próximos 6 Meses")
        
        # Filtra contratos com data_fim nos próximos 6 meses
        hoje = datetime.now()
        seis_meses = hoje + timedelta(days=180)
        
        vencimentos = []
        for c in contratos:
            data_fim = c.get('data_fim')
            if data_fim:
                if isinstance(data_fim, str):
                    try:
                        data_fim = datetime.fromisoformat(data_fim)
                    except:
                        continue
                
                if hoje <= data_fim <= seis_meses:
                    dias_restantes = (data_fim - hoje).days
                    vencimentos.append({
                        'Contrato': c.get('numero', 'N/A'),
                        'Data de Término': data_fim.strftime('%d/%m/%Y'),
                        'Dias Restantes': dias_restantes,
                        'Fornecedor': c.get('fornecedor', 'N/A'),
                        'Valor': c.get('valor', 0)
                    })
        
        if vencimentos:
            # Ordena por dias restantes
            vencimentos.sort(key=lambda x: x['Dias Restantes'])
            
            # Gráfico de barras horizontal
            df_venc = pd.DataFrame(vencimentos[:15])  # Top 15
            
            fig_timeline = px.bar(
                df_venc,
                x='Dias Restantes',
                y='Contrato',
                orientation='h',
                color='Dias Restantes',
                color_continuous_scale=['#DC3545', '#FFC107', '#28A745'],
                hover_data=['Fornecedor', 'Data de Término'],
                labels={'Dias Restantes': 'Dias para Vencimento'}
            )
            fig_timeline.update_layout(
                height=500,
                xaxis_title="Dias para Vencimento",
                yaxis_title="",
                showlegend=False
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            st.caption(f"📊 {len(vencimentos)} contratos vencem nos próximos 6 meses")
        else:
            st.info("Nenhum contrato vence nos próximos 6 meses.")
    
    # ===== TAB 3: FORNECEDORES =====
    with tab3:
        st.markdown("### 💰 Top 10 Fornecedores por Valor Total")
        
        # Agrupa por fornecedor
        fornecedores = {}
        for c in contratos:
            forn = c.get('fornecedor', 'N/A')
            valor = c.get('valor', 0)
            if forn in fornecedores:
                fornecedores[forn]['valor'] += valor
                fornecedores[forn]['contratos'] += 1
            else:
                fornecedores[forn] = {'valor': valor, 'contratos': 1}
        
        # Ordena e pega top 10
        top_fornecedores = sorted(fornecedores.items(), key=lambda x: x[1]['valor'], reverse=True)[:10]
        
        if top_fornecedores:
            df_forn = pd.DataFrame([
                {
                    'Fornecedor': f[0],
                    'Valor Total (R$)': f[1]['valor'],
                    'Contratos': f[1]['contratos']
                }
                for f in top_fornecedores
            ])
            
            fig_forn = px.bar(
                df_forn,
                x='Valor Total (R$)',
                y='Fornecedor',
                orientation='h',
                color='Contratos',
                color_continuous_scale='Blues',
                hover_data=['Contratos'],
                labels={'Valor Total (R$)': 'Valor Total Contratado (R$)'}
            )
            fig_forn.update_layout(
                height=450,
                xaxis_title="Valor Total Contratado (R$)",
                yaxis_title="",
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_forn, use_container_width=True)
            
            # Tabela resumo
            st.markdown("#### 📋 Detalhamento")
            df_forn['Valor Total (R$)'] = df_forn['Valor Total (R$)'].apply(lambda x: f"R$ {x:,.2f}")
            st.dataframe(df_forn, use_container_width=True, hide_index=True)
        else:
            st.info("Dados de fornecedores não disponíveis.")
    
    # ===== TAB 4: ANÁLISE DE STATUS =====
    with tab4:
        st.markdown("### 📈 Análise Detalhada por Status")
        
        # Métricas por status
        col1, col2, col3 = st.columns(3)
        
        ativos = [c for c in contratos if c.get('status') == 'ativo']
        atencao = [c for c in contratos if c.get('status') == 'atencao']
        criticos = [c for c in contratos if c.get('status') == 'critico']
        
        with col1:
            valor_ativos = sum(c.get('valor', 0) for c in ativos)
            st.metric(
                "✅ Contratos Ativos",
                f"{len(ativos)}",
                f"R$ {valor_ativos/1_000_000:.1f}M"
            )
        
        with col2:
            valor_atencao = sum(c.get('valor', 0) for c in atencao)
            st.metric(
                "⚠️ Requerem Atenção",
                f"{len(atencao)}",
                f"R$ {valor_atencao/1_000_000:.1f}M"
            )
        
        with col3:
            valor_criticos = sum(c.get('valor', 0) for c in criticos)
            st.metric(
                "🔴 Críticos",
                f"{len(criticos)}",
                f"R$ {valor_criticos/1_000_000:.1f}M"
            )
        
        # Gráfico de evolução (mockado - preparado para dados históricos)
        st.markdown("#### 📊 Distribuição de Valor por Status")
        
        df_status_valor = pd.DataFrame([
            {'Status': 'Ativos', 'Valor (Milhões)': valor_ativos/1_000_000, 'Quantidade': len(ativos)},
            {'Status': 'Atenção', 'Valor (Milhões)': valor_atencao/1_000_000, 'Quantidade': len(atencao)},
            {'Status': 'Críticos', 'Valor (Milhões)': valor_criticos/1_000_000, 'Quantidade': len(criticos)}
        ])
        
        fig_status_valor = px.bar(
            df_status_valor,
            x='Status',
            y='Valor (Milhões)',
            color='Status',
            color_discrete_map={'Ativos': '#28A745', 'Atenção': '#FFC107', 'Críticos': '#DC3545'},
            text='Quantidade',
            labels={'Valor (Milhões)': 'Valor Total (R$ Milhões)'}
        )
        fig_status_valor.update_traces(texttemplate='%{text} contratos', textposition='outside')
        fig_status_valor.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_status_valor, use_container_width=True)


def render_contract_card(contrato: dict):
    """Renderiza card de contrato individual"""
    status_colors = {
        "ativo": "🟢",
        "atencao": "🟡",
        "critico": "🔴"
    }
    
    status_icon = status_colors.get(contrato.get("status", "ativo"), "⚪")
    
    # Obtém tags do contrato
    tag_service = get_tag_service()
    tags_contrato = tag_service.obter_tags_do_contrato(contrato['id'])
    
    with st.container():
        st.markdown(f"""
            <div class="contract-card">
                <div class="contract-header">
                    <h3>{status_icon} {contrato['numero']}</h3>
                    <span class="contract-badge">{contrato['tipo']}</span>
                </div>
                <p><strong>Fornecedor:</strong> {contrato['fornecedor']}</p>
                <p><strong>Objeto:</strong> {contrato['objeto']}</p>
                <p><strong>Vigência:</strong> {contrato['vigencia']}</p>
                <p><strong>Valor:</strong> R$ {contrato['valor']:,.2f}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Renderiza tags
        if tags_contrato:
            tags_html = ""
            for tag in tags_contrato:
                tags_html += f"""
                <span style="background: {tag['cor']}; color: white; 
                             padding: 0.2rem 0.5rem; border-radius: 10px; 
                             font-size: 0.7rem; font-weight: bold;
                             display: inline-block; margin: 0.2rem;">
                    {tag['icone']} {tag['nome']}
                </span>
                """
            st.markdown(tags_html, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📄 Visualizar", key=f"view_{contrato['id']}", use_container_width=True):
                st.session_state.contrato_selecionado = contrato
                st.switch_page("pages/01_📄_Contrato.py")
        
        with col2:
            if st.button("💬 Copiloto", key=f"copilot_{contrato['id']}", use_container_width=True):
                st.session_state.contrato_selecionado = contrato
                st.switch_page("pages/02_💬_Copiloto.py")
        
        with col3:
            if st.button("📝 Notificar", key=f"notify_{contrato['id']}", use_container_width=True):
                st.session_state.contrato_selecionado = contrato
                st.switch_page("pages/03_📝_Notificações.py")
        
        with col4:
            if st.button("🏷️ Tags", key=f"tags_{contrato['id']}", use_container_width=True):
                st.session_state.contrato_para_tag = contrato['id']
                st.session_state.show_tag_modal = True
                st.rerun()


def render_tag_management_modal():
    """Modal para gerenciar tags de um contrato"""
    contrato_id = st.session_state.get('contrato_para_tag')
    if not contrato_id:
        return
    
    tag_service = get_tag_service()
    
    with st.container():
        st.markdown("---")
        st.markdown(f"### 🏷️ Gerenciar Tags - Contrato {contrato_id}")
        
        # Tags atuais
        tags_atuais = tag_service.obter_tags_do_contrato(contrato_id)
        
        col_modal1, col_modal2 = st.columns([3, 1])
        
        with col_modal1:
            # Seletor de tags
            todas_tags = tag_service.obter_todas_tags()
            tags_opcoes = {t['id']: f"{t['icone']} {t['nome']}" for t in todas_tags}
            
            tags_selecionadas = st.multiselect(
                "Selecione as tags",
                options=list(tags_opcoes.keys()),
                default=[t['id'] for t in tags_atuais],
                format_func=lambda x: tags_opcoes[x],
                key="multiselect_tags"
            )
        
        with col_modal2:
            st.write("")
            st.write("")
            if st.button("💾 Salvar", type="primary", use_container_width=True):
                tag_service.definir_tags_do_contrato(contrato_id, tags_selecionadas)
                st.success("Tags atualizadas!")
                st.session_state.show_tag_modal = False
                st.rerun()
            
            if st.button("❌ Cancelar", use_container_width=True):
                st.session_state.show_tag_modal = False
                st.rerun()
        
        st.markdown("---")


def render_contracts_dashboard():
    """Renderiza o dashboard de contratos"""
    st.markdown("## 📋 Contratos Regionais - RAJ 10.1")
    
    # Modal de gestão de tags (se ativo)
    if st.session_state.get('show_tag_modal', False):
        render_tag_management_modal()
    
    # Barra de busca geral
    busca = st.text_input(
        "🔍 Buscar contrato",
        placeholder="Digite número, objeto, fornecedor ou palavra-chave...",
        key="busca_contrato"
    )
    
    # Filtros avançados em expander
    with st.expander("🔎 Filtros Avançados", expanded=False):
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            filtro_num_contrato = st.text_input(
                "Número do Contrato",
                placeholder="Ex: 2024/00070406",
                key="filtro_num_contrato",
                help="Filtra por número exato ou parcial do contrato"
            )
            
            filtro_num_processo = st.text_input(
                "Número do Processo",
                placeholder="Ex: 2024/00070406",
                key="filtro_num_processo",
                help="Filtra por número exato ou parcial do processo"
            )
        
        with col_f2:
            # Lista de fornecedores únicos
            contratos_temp = get_todos_contratos()
            fornecedores = sorted(list(set([c.get('fornecedor', '') for c in contratos_temp if c.get('fornecedor')])))
            filtro_fornecedor = st.selectbox(
                "Fornecedor/Empresa",
                ["Todos"] + fornecedores,
                key="filtro_fornecedor",
                help="Filtra por empresa contratada"
            )
            
            # Lista de fiscais únicos
            fiscais = sorted(list(set([c.get('fiscal_titular', '') for c in contratos_temp if c.get('fiscal_titular')])))
            filtro_fiscal = st.selectbox(
                "Fiscal/Gestor",
                ["Todos"] + fiscais,
                key="filtro_fiscal",
                help="Filtra por fiscal titular do contrato"
            )
        
        with col_f3:
            # Filtro por tags
            tag_service = get_tag_service()
            todas_tags = tag_service.obter_todas_tags()
            tags_opcoes = {t['id']: f"{t['icone']} {t['nome']}" for t in todas_tags}
            
            filtro_tags = st.multiselect(
                "Tags",
                options=list(tags_opcoes.keys()),
                format_func=lambda x: tags_opcoes[x],
                key="filtro_tags",
                help="Filtra por tags aplicadas aos contratos"
            )
            
            st.caption("[🏷️ Gerenciar Tags](pages/09_🏷️_Gerenciar_Tags.py)")
    
    # Filtros básicos
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        filtro_status = st.selectbox(
            "Status",
            ["Todos", "Ativos", "Atenção", "Crítico"],
            key="filtro_status"
        )
    
    with col2:
        filtro_tipo = st.selectbox(
            "Tipo de Contrato",
            ["Todos", "Serviços", "Fornecimento", "Obras"],
            key="filtro_tipo"
        )
    
    with col3:
        # Contador de tags aplicadas
        if filtro_tags:
            st.metric("Tags Filtradas", len(filtro_tags))
        else:
            st.write("")
            st.write("")
            if st.button("🏷️ Gerenciar Tags", use_container_width=True):
                st.switch_page("pages/09_🏷️_Gerenciar_Tags.py")
    
    with col4:
        st.write("")
        st.write("")
        if st.button("🔄 Atualizar", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    # Lista de contratos (mock + cadastrados)
    contratos = get_todos_contratos()
    
    # APLICA FILTROS
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
    
    # Filtro por número do contrato (avançado)
    if filtro_num_contrato and filtro_num_contrato.strip():
        termo_contrato = filtro_num_contrato.lower().strip()
        contratos_filtrados = [
            c for c in contratos_filtrados
            if termo_contrato in c.get('numero', '').lower()
        ]
    
    # Filtro por número do processo (avançado)
    if filtro_num_processo and filtro_num_processo.strip():
        termo_processo = filtro_num_processo.lower().strip()
        contratos_filtrados = [
            c for c in contratos_filtrados
            if termo_processo in c.get('numero', '').lower()  # Número do processo geralmente está no campo 'numero'
        ]
    
    # Filtro por fornecedor (avançado)
    if filtro_fornecedor != "Todos":
        contratos_filtrados = [
            c for c in contratos_filtrados
            if c.get('fornecedor') == filtro_fornecedor
        ]
    
    # Filtro por fiscal (avançado)
    if filtro_fiscal != "Todos":
        contratos_filtrados = [
            c for c in contratos_filtrados
            if c.get('fiscal_titular') == filtro_fiscal
        ]
    
    # Filtro por tags
    if filtro_tags:
        tag_service = get_tag_service()
        contratos_filtrados = [
            c for c in contratos_filtrados
            if any(tag_id in [t['id'] for t in tag_service.obter_tags_do_contrato(c['id'])] 
                   for tag_id in filtro_tags)
        ]
    
    # Filtro por status
    if filtro_status != "Todos":
        status_map = {
            "Ativos": "ativo",
            "Atenção": "atencao",
            "Crítico": "critico"
        }
        status_busca = status_map.get(filtro_status)
        if status_busca:
            contratos_filtrados = [c for c in contratos_filtrados if c.get('status') == status_busca]
    
    # Filtro por tipo
    if filtro_tipo != "Todos":
        contratos_filtrados = [c for c in contratos_filtrados if c.get('tipo') == filtro_tipo]
    
    # Mostra contador de resultados
    total_original = len(contratos)
    total_filtrado = len(contratos_filtrados)
    
    if total_filtrado != total_original:
        filtros_ativos = []
        if busca and busca.strip():
            filtros_ativos.append(f"busca '{busca}'")
        if filtro_num_contrato and filtro_num_contrato.strip():
            filtros_ativos.append(f"contrato '{filtro_num_contrato}'")
        if filtro_num_processo and filtro_num_processo.strip():
            filtros_ativos.append(f"processo '{filtro_num_processo}'")
        if filtro_fornecedor != "Todos":
            filtros_ativos.append(f"fornecedor '{filtro_fornecedor}'")
        if filtro_fiscal != "Todos":
            filtros_ativos.append(f"fiscal '{filtro_fiscal}'")
        if filtro_status != "Todos":
            filtros_ativos.append(f"status '{filtro_status}'")
        if filtro_tipo != "Todos":
            filtros_ativos.append(f"tipo '{filtro_tipo}'")
        
        filtros_texto = " + ".join(filtros_ativos) if filtros_ativos else "filtros aplicados"
        st.info(f"🔍 Encontrados **{total_filtrado}** de {total_original} contratos ({filtros_texto})")
    
    # Renderiza contratos filtrados
    if not contratos_filtrados:
        st.warning("❌ Nenhum contrato encontrado com os filtros aplicados.")
        if busca and busca.strip() or filtro_num_contrato or filtro_num_processo:
            st.info(f"💡 **Dica:** Tente termos mais genéricos ou remova alguns filtros")
    else:
        for contrato in contratos_filtrados:
            render_contract_card(contrato)
            st.markdown("<br>", unsafe_allow_html=True)


def render_sidebar():
    """Renderiza a barra lateral com navegação e informações"""
    with st.sidebar:
        st.markdown("### 🏛️ TJSP")
        st.markdown("**Gestão de Contratos Regionais**")
        st.markdown("---")
        
        st.markdown("### 👤 Usuário")
        usuario = st.session_state.get("usuario", "Coordenador Regional")
        perfil = st.session_state.get("perfil", "Fiscal de Contrato")
        fiscal_nome = st.session_state.get("fiscal_nome", usuario)
        
        st.info(f"""
        **Nome:** {usuario}  
        **Perfil:** {perfil}  
        **RAJ:** 10.1
        """)
        
        # Seletor rápido de fiscal (para testes)
        with st.expander("🔄 Trocar Fiscal"):
            # Lista fiscais únicos dos contratos
            contratos_temp = get_todos_contratos()
            fiscais_unicos = set()
            for c in contratos_temp:
                if c.get('fiscal_titular'):
                    fiscais_unicos.add(c.get('fiscal_titular'))
                if c.get('fiscal_substituto'):
                    fiscais_unicos.add(c.get('fiscal_substituto'))
            
            fiscais_lista = sorted(list(fiscais_unicos))
            
            if fiscais_lista:
                fiscal_selecionado = st.selectbox(
                    "Selecione o fiscal:",
                    fiscais_lista,
                    index=fiscais_lista.index(fiscal_nome) if fiscal_nome in fiscais_lista else 0,
                    key="select_fiscal_sidebar"
                )
                
                if st.button("✅ Aplicar", use_container_width=True):
                    st.session_state.fiscal_nome = fiscal_selecionado
                    st.session_state.usuario = fiscal_selecionado
                    st.success(f"Fiscal alterado para: {fiscal_selecionado}")
                    st.rerun()
        
        st.markdown("---")
        
        st.markdown("### 📚 Navegação")
        st.page_link("app.py", label="🏠 Home", icon="🏠")
        st.page_link("pages/10_Meus_Contratos.py", label="👤 Meus Contratos", icon="👤")
        st.page_link("pages/04_📖_Como_Proceder.py", label="📖 Como Proceder", icon="📖")
        st.page_link("pages/05_📚_Biblioteca.py", label="📚 Biblioteca", icon="📚")
        st.page_link("pages/08_⚙️_Configurações.py", label="⚙️ Configurações", icon="⚙️")
        st.page_link("pages/09_🏷️_Gerenciar_Tags.py", label="🏷️ Gerenciar Tags", icon="🏷️")
        
        st.markdown("---")
        
        st.markdown("### ℹ️ Sobre")
        st.caption(f"""
        **Versão:** 1.0.1 (MVP)  
        **Última atualização:** {datetime.now().strftime('%d/%m/%Y')}  

        **Ambiente:** Piloto
        """)




def main():
    """Função principal do aplicativo"""
    # Configuração da página
    st.set_page_config(
        page_title="TJSP - Contratos Regionais IA",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Aplica estilos institucionais TJSP
    apply_tjsp_styles()
    
    with st.sidebar:
        st.markdown("### 🏛️ TJSP")
        st.markdown("**Gestão de Contratos Regionais**")
        st.markdown("---")

        st.markdown("### 👤 Usuário")
        usuario = st.session_state.get("usuario", "Coordenador Regional")
        perfil = st.session_state.get("perfil", "Fiscal de Contrato")
        fiscal_nome = st.session_state.get("fiscal_nome", usuario)

        st.info(f"""
        **Nome:** {usuario}  
        **Perfil:** {perfil}  
        **RAJ:** 10.1
        """)

        # Seletor rápido de fiscal (para testes)
        with st.expander("🔄 Trocar Fiscal"):
            contratos_temp = get_todos_contratos()
            fiscais_unicos = set()
            for c in contratos_temp:
                if c.get('fiscal_titular'):
                    fiscais_unicos.add(c.get('fiscal_titular'))
                if c.get('fiscal_substituto'):
                    fiscais_unicos.add(c.get('fiscal_substituto'))
            fiscais_lista = sorted(list(fiscais_unicos))
            if fiscais_lista:
                fiscal_selecionado = st.selectbox(
                    "Selecione o fiscal:",
                    fiscais_lista,
                    index=fiscais_lista.index(fiscal_nome) if fiscal_nome in fiscais_lista else 0,
                    key="select_fiscal_sidebar"
                )
                if st.button("✅ Aplicar", use_container_width=True):
                    st.session_state.fiscal_nome = fiscal_selecionado
                    st.session_state.usuario = fiscal_selecionado
                    st.success(f"Fiscal alterado para: {fiscal_selecionado}")
                    st.rerun()

        st.markdown("---")

        # Navegação centralizada e manual, sem duplicação
        st.markdown("### 📚 Navegação")
        st.page_link("app.py", label="🏠 Home", icon="🏠")
        st.page_link("pages/10_Meus_Contratos.py", label="👤 Meus Contratos", icon="👤")
        st.page_link("pages/04_📖_Como_Proceder.py", label="📖 Como Proceder", icon="📖")
        st.page_link("pages/05_📚_Biblioteca.py", label="📚 Biblioteca", icon="📚")
        st.page_link("pages/08_⚙️_Configurações.py", label="⚙️ Configurações", icon="⚙️")
        st.page_link("pages/09_🏷️_Gerenciar_Tags.py", label="🏷️ Gerenciar Tags", icon="🏷️")

        st.markdown("---")

        st.markdown("### ℹ️ Sobre")
        st.caption(f"""
        **Versão:** 1.0.1 (MVP)  
        **Última atualização:** {datetime.now().strftime('%d/%m/%Y')}  
        **Ambiente:** Piloto
        """)
