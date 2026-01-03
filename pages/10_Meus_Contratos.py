"""
Página Meus Contratos - Dashboard Personalizado por Fiscal
===========================================================
Vista personalizada com contratos, alertas e performance individual.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

sys.path.append(str(Path(__file__).parent.parent))

from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state
from services.contract_service import get_todos_contratos
from services.alert_service import calcular_alertas
from services.tag_service import get_tag_service


def render_metrics_fiscal(contratos_fiscal: list, alertas_fiscal: list):
    """Renderiza métricas individuais do fiscal"""
    
    total_contratos = len(contratos_fiscal)
    valor_total = sum(c.get('valor', 0) for c in contratos_fiscal)
    
    # Contadores por status
    ativos = len([c for c in contratos_fiscal if c.get('status') == 'ativo'])
    atencao = len([c for c in contratos_fiscal if c.get('status') == 'atencao'])
    criticos = len([c for c in contratos_fiscal if c.get('status') == 'critico'])
    
    # Alertas críticos
    alertas_criticos = len([a for a in alertas_fiscal if a.get('tipo') == 'critico'])
    
    # Taxa de conformidade
    taxa_conformidade = int((ativos / total_contratos * 100)) if total_contratos > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📋 Meus Contratos",
            value=f"{total_contratos}",
            delta=f"{ativos} ativos"
        )
    
    with col2:
        st.metric(
            label="💲 Valor Total",
            value=f"R$ {valor_total/1_000_000:.1f}M",
            delta=f"{total_contratos} contratos"
        )
    
    with col3:
        delta_text = "Excelente" if taxa_conformidade >= 80 else "Atenção"
        delta_color = "normal" if taxa_conformidade >= 80 else "inverse"
        st.metric(
            label="✅ Taxa de Conformidade",
            value=f"{taxa_conformidade}%",
            delta=delta_text,
            delta_color=delta_color
        )
    
    with col4:
        if alertas_criticos > 0:
            st.metric(
                label="🔴 Alertas Críticos",
                value=f"{alertas_criticos}",
                delta="Ação necessária",
                delta_color="inverse"
            )
        else:
            st.metric(
                label="🔴 Alertas Críticos",
                value="0",
                delta="Tudo OK",
                delta_color="normal"
            )


def render_performance_charts(contratos_fiscal: list):
    """Renderiza gráficos de performance individual"""
    
    st.markdown("### 📊 Minha Performance")
    
    tab1, tab2, tab3 = st.tabs(["📈 Status", "📅 Vencimentos", "💲 Por Tipo"])
    
    # TAB 1: DISTRIBUIÇÃO POR STATUS
    with tab1:
        status_map = {
            'ativo': 'Ativos',
            'atencao': 'Atenção',
            'critico': 'Crítico'
        }
        
        status_count = {}
        for c in contratos_fiscal:
            s = c.get('status', 'ativo')
            label = status_map.get(s, s)
            status_count[label] = status_count.get(label, 0) + 1
        
        if status_count:
            fig_status = go.Figure(data=[go.Pie(
                labels=list(status_count.keys()),
                values=list(status_count.values()),
                hole=0.4,
                marker=dict(colors=['#28A745', '#FFC107', '#DC3545'])
            )])
            fig_status.update_layout(
                title="Distribuição por Status",
                height=350,
                showlegend=True
            )
            st.plotly_chart(fig_status, use_container_width=True)
            
            # Métricas detalhadas
            col_s1, col_s2, col_s3 = st.columns(3)
            
            with col_s1:
                st.metric("✅ Ativos", status_count.get('Ativos', 0))
            with col_s2:
                st.metric("⚠️ Atenção", status_count.get('Atenção', 0))
            with col_s3:
                st.metric("🔴 Críticos", status_count.get('Crítico', 0))
    
    # TAB 2: VENCIMENTOS PRÓXIMOS
    with tab2:
        hoje = datetime.now()
        seis_meses = hoje + timedelta(days=180)
        
        vencimentos = []
        for c in contratos_fiscal:
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
                        'Contrato': c.get('numero', 'N/A')[:20],
                        'Data': data_fim.strftime('%d/%m/%Y'),
                        'Dias': dias_restantes,
                        'Valor': c.get('valor', 0)
                    })
        
        if vencimentos:
            vencimentos.sort(key=lambda x: x['Dias'])
            
            # Gráfico
            import pandas as pd
            df_venc = pd.DataFrame(vencimentos[:10])
            
            fig_venc = px.bar(
                df_venc,
                x='Dias',
                y='Contrato',
                orientation='h',
                color='Dias',
                color_continuous_scale=['#DC3545', '#FFC107', '#28A745'],
                labels={'Dias': 'Dias para Vencimento'}
            )
            fig_venc.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_venc, use_container_width=True)
            
            st.caption(f"📊 {len(vencimentos)} contratos vencem nos próximos 6 meses")
        else:
            st.info("✅ Nenhum contrato vence nos próximos 6 meses")
    
    # TAB 3: VALOR POR TIPO
    with tab3:
        tipo_valor = {}
        for c in contratos_fiscal:
            tipo = c.get('tipo', 'Outros')
            valor = c.get('valor', 0)
            tipo_valor[tipo] = tipo_valor.get(tipo, 0) + valor
        
        if tipo_valor:
            fig_tipo = px.bar(
                x=list(tipo_valor.keys()),
                y=list(tipo_valor.values()),
                labels={'x': 'Tipo de Contrato', 'y': 'Valor Total (R$)'},
                color=list(tipo_valor.keys()),
                color_discrete_sequence=['#003366', '#0066CC', '#66B2FF']
            )
            fig_tipo.update_layout(
                title="Valor Total por Tipo de Contrato",
                height=350,
                showlegend=False
            )
            st.plotly_chart(fig_tipo, use_container_width=True)
            
            # Tabela resumo
            st.markdown("#### 💲 Detalhamento")
            for tipo, valor in sorted(tipo_valor.items(), key=lambda x: x[1], reverse=True):
                count = len([c for c in contratos_fiscal if c.get('tipo') == tipo])
                col_t1, col_t2, col_t3 = st.columns([2, 1, 1])
                with col_t1:
                    st.write(f"**{tipo}**")
                with col_t2:
                    st.write(f"{count} contrato(s)")
                with col_t3:
                    st.write(f"R$ {valor/1_000_000:.2f}M")


def render_alertas_fiscal(alertas_fiscal: list):
    """Renderiza alertas específicos do fiscal"""
    
    st.markdown("### 🔔 Meus Alertas")
    
    if not alertas_fiscal:
        st.success("✅ Nenhum alerta no momento. Todos os contratos estão em ordem!")
        return
    
    # Separar por tipo
    criticos = [a for a in alertas_fiscal if a.get('tipo') == 'critico']
    atencao = [a for a in alertas_fiscal if a.get('tipo') == 'atencao']
    info = [a for a in alertas_fiscal if a.get('tipo') == 'info']
    
    # Tabs por tipo
    if criticos:
        st.markdown("#### 🔴 Críticos - Ação Imediata")
        for alerta in criticos[:3]:  # Primeiros 3
            with st.container():
                col_a1, col_a2 = st.columns([3, 1])
                
                with col_a1:
                    st.markdown(f"**{alerta.get('titulo', 'Sem título')}**")
                    st.caption(alerta.get('descricao', 'Sem descrição'))
                
                with col_a2:
                    if st.button("Ver Detalhes", key=f"alert_{alerta['id']}", use_container_width=True):
                        st.switch_page("pages/07_🔔_Alertas.py")
                
                st.markdown("---")
        
        if len(criticos) > 3:
            st.caption(f"+ {len(criticos) - 3} alertas críticos. Ver todos em Alertas.")
    
    # Resumo de outros alertas
    if atencao or info:
        with st.expander(f"⚠️ Outros Alertas ({len(atencao) + len(info)})"):
            for alerta in (atencao + info)[:5]:
                st.markdown(f"• **{alerta.get('titulo')}** - {alerta.get('categoria', 'Geral')}")


def render_contratos_lista(contratos_fiscal: list):
    """Renderiza lista de contratos do fiscal"""
    
    st.markdown("### 📋 Lista de Contratos")
    
    # Filtros rápidos
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        filtro_status_fiscal = st.selectbox(
            "Status",
            ["Todos", "Ativos", "Atenção", "Crítico"],
            key="filtro_status_fiscal"
        )
    
    with col_f2:
        filtro_tipo_fiscal = st.selectbox(
            "Tipo",
            ["Todos", "Serviços", "Fornecimento", "Obras"],
            key="filtro_tipo_fiscal"
        )
    
    with col_f3:
        # Filtro por tags
        tag_service = get_tag_service()
        todas_tags = tag_service.obter_todas_tags()
        tags_opcoes = {t['id']: f"{t['icone']} {t['nome']}" for t in todas_tags}
        
        filtro_tags_fiscal = st.multiselect(
            "Tags",
            options=list(tags_opcoes.keys()),
            format_func=lambda x: tags_opcoes[x],
            key="filtro_tags_fiscal"
        )
    
    # Aplica filtros
    contratos_filtrados = contratos_fiscal
    
    if filtro_status_fiscal != "Todos":
        status_map = {"Ativos": "ativo", "Atenção": "atencao", "Crítico": "critico"}
        contratos_filtrados = [
            c for c in contratos_filtrados 
            if c.get('status') == status_map.get(filtro_status_fiscal)
        ]
    
    if filtro_tipo_fiscal != "Todos":
        contratos_filtrados = [
            c for c in contratos_filtrados 
            if c.get('tipo') == filtro_tipo_fiscal
        ]
    
    if filtro_tags_fiscal:
        contratos_filtrados = [
            c for c in contratos_filtrados
            if any(tag_id in [t['id'] for t in tag_service.obter_tags_do_contrato(c['id'])] 
                   for tag_id in filtro_tags_fiscal)
        ]
    
    st.caption(f"Mostrando {len(contratos_filtrados)} de {len(contratos_fiscal)} contratos")
    st.markdown("---")
    
    # Renderiza contratos
    if contratos_filtrados:
        for contrato in contratos_filtrados:
            render_contrato_card_compacto(contrato)
    else:
        st.info("Nenhum contrato encontrado com os filtros aplicados")


def render_contrato_card_compacto(contrato: dict):
    """Renderiza card compacto de contrato"""
    
    status_colors = {
        "ativo": "🟢",
        "atencao": "🟡",
        "critico": "🔴"
    }
    
    status_icon = status_colors.get(contrato.get("status", "ativo"), "⚪")
    
    # Tags do contrato
    tag_service = get_tag_service()
    tags_contrato = tag_service.obter_tags_do_contrato(contrato['id'])
    
    with st.container():
        col_c1, col_c2, col_c3 = st.columns([3, 2, 1])
        
        with col_c1:
            st.markdown(f"**{status_icon} {contrato.get('numero', 'N/A')}**")
            st.caption(f"{contrato.get('fornecedor', 'N/A')}")
        
        with col_c2:
            st.write(f"**Valor:** R$ {contrato.get('valor', 0):,.2f}")
            st.caption(f"Vigência: {contrato.get('vigencia', 'N/A')}")
        
        with col_c3:
            if st.button("📄 Ver", key=f"ver_{contrato['id']}", use_container_width=True):
                st.session_state.contrato_selecionado = contrato
                st.switch_page("pages/01_📄_Contrato.py")
        
        # Tags
        if tags_contrato:
            tags_html = ""
            for tag in tags_contrato:
                tags_html += f"""
                <span style="background: {tag['cor']}; color: white; 
                             padding: 0.15rem 0.4rem; border-radius: 8px; 
                             font-size: 0.65rem; font-weight: bold;
                             display: inline-block; margin: 0.1rem;">
                    {tag['icone']} {tag['nome']}
                </span>
                """
            st.markdown(tags_html, unsafe_allow_html=True)
        
        st.markdown("---")


def main():
    st.set_page_config(
        page_title="TJSP - Meus Contratos",
        page_icon="👤",
        layout="wide"
    )
    
    apply_tjsp_styles()
    initialize_session_state()
    
    # Obtém usuário logado
    usuario = st.session_state.get("usuario", "Coordenador Regional")
    perfil = st.session_state.get("perfil", "Fiscal de Contrato")
    fiscal_nome = st.session_state.get("fiscal_nome", usuario)
    
    # Cabeçalho padronizado institucional
    from components.layout_header import render_module_banner
    render_module_banner(
        title="Meus Contratos",
        subtitle=f"{usuario} • {perfil} — Dashboard Personalizado - RAJ 10.1"
    )
    
    # Navegação
    col_nav1, col_nav2, col_nav3 = st.columns([4, 1, 1])
    
    with col_nav1:
        if st.button("🏠 Home Geral", use_container_width=False):
            st.switch_page("Home.py")
    
    with col_nav2:
        if st.button("🔔 Alertas", use_container_width=True):
            st.switch_page("pages/07_🔔_Alertas.py")
    
    with col_nav3:
        if st.button("⚙️ Config", use_container_width=True):
            st.switch_page("pages/08_⚙️_Configurações.py")
    
    st.markdown("---")
    
    # Carrega dados
    todos_contratos = get_todos_contratos()
    
    # Filtra contratos do fiscal
    # Verifica se é fiscal titular ou substituto
    contratos_fiscal = [
        c for c in todos_contratos
        if c.get('fiscal_titular') == fiscal_nome 
        or c.get('fiscal_substituto') == fiscal_nome
    ]
    
    # Se não houver contratos, mostra mensagem
    if not contratos_fiscal:
        st.warning(f"""
            ⚠️ Nenhum contrato encontrado para **{fiscal_nome}**.
            
            Você pode estar listado como fiscal titular ou substituto em contratos.
            Verifique o nome configurado no perfil ou consulte o coordenador.
        """)
        
        with st.expander("🔧 Configurar Nome do Fiscal"):
            novo_nome = st.text_input(
                "Nome completo do fiscal",
                value=fiscal_nome,
                help="Digite seu nome exatamente como aparece nos contratos"
            )
            
            if st.button("💾 Salvar Nome"):
                st.session_state.fiscal_nome = novo_nome
                st.session_state.usuario = novo_nome
                st.success(f"Nome atualizado para: {novo_nome}")
                st.rerun()
        
        return
    
    # Calcula alertas do fiscal
    alertas_fiscal = []
    todos_alertas = calcular_alertas(contratos_fiscal)
    for alerta in todos_alertas:
        # Verifica se o alerta é de um contrato do fiscal
        contrato_alerta = next(
            (c for c in contratos_fiscal if c['id'] == alerta.get('contrato_id')),
            None
        )
        if contrato_alerta:
            alertas_fiscal.append(alerta)
    
    # Renderiza métricas
    render_metrics_fiscal(contratos_fiscal, alertas_fiscal)
    
    st.markdown("---")
    
    # Renderiza performance
    render_performance_charts(contratos_fiscal)
    
    st.markdown("---")
    
    # Renderiza alertas
    render_alertas_fiscal(alertas_fiscal)
    
    st.markdown("---")
    
    # Renderiza lista de contratos
    render_contratos_lista(contratos_fiscal)
    
    # Rodapé
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #6c757d; padding: 1rem;">
            <p>Dashboard Personalizado - TJSP Sistema de Gestão de Contratos</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
