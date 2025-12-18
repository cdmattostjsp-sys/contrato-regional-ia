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
from datetime import datetime
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state
from services.contract_service import get_todos_contratos
from services.alert_service import calcular_alertas


def render_header():
    """Renderiza o cabeçalho institucional TJSP"""
    st.markdown("""
        <div class="tjsp-header">
            <div class="tjsp-logo-container">
                <h1>⚖️ TJSP - Gestão de Contratos Regionais</h1>
                <p class="tjsp-subtitle">Sistema de Fiscalização e Acompanhamento - RAJ 10.1</p>
            </div>
        </div>
    """, unsafe_allow_html=True)


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


def render_contract_card(contrato: dict):
    """Renderiza card de contrato individual"""
    status_colors = {
        "ativo": "🟢",
        "atencao": "🟡",
        "critico": "🔴"
    }
    
    status_icon = status_colors.get(contrato.get("status", "ativo"), "⚪")
    
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
        
        col1, col2, col3 = st.columns(3)
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


def render_contracts_dashboard():
    """Renderiza o dashboard de contratos"""
    st.markdown("## 📋 Contratos Regionais - RAJ 10.1")
    
    # Barra de busca geral
    busca = st.text_input(
        "🔍 Buscar contrato",
        placeholder="Digite número, objeto, fornecedor ou palavra-chave...",
        key="busca_contrato"
    )
    
    # Filtros avançados em expander
    with st.expander("🔎 Filtros Avançados", expanded=False):
        col_f1, col_f2 = st.columns(2)
        
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
    
    # Filtros básicos
    col1, col2, col3 = st.columns([2, 2, 1])
    
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
        
        st.info(f"""
        **Nome:** {usuario}  
        **Perfil:** {perfil}  
        **RAJ:** 10.1
        """)
        
        st.markdown("---")
        
        st.markdown("### 📚 Navegação")
        st.page_link("app.py", label="🏠 Home", icon="🏠")
        st.page_link("pages/04_📖_Como_Proceder.py", label="📖 Como Proceder", icon="📖")
        st.page_link("pages/05_📚_Biblioteca.py", label="📚 Biblioteca", icon="📚")
        
        st.markdown("---")
        
        st.markdown("### ℹ️ Sobre")
        st.caption(f"""
        **Versão:** 1.0.0 (MVP)  
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
    
    # Inicializa session state
    initialize_session_state()
    
    # Renderiza sidebar
    render_sidebar()
    
    # Renderiza cabeçalho
    render_header()
    
    # Renderiza métricas
    render_metrics()
    
    st.markdown("---")
    
    # Renderiza dashboard de contratos
    render_contracts_dashboard()
    
    # Rodapé institucional
    st.markdown("---")
    st.markdown("""
        <div class="tjsp-footer">
            <p>© 2025 Tribunal de Justiça do Estado de São Paulo - TJSP</p>
            <p>Projeto SAAB-Tech / Synapse.IA - Aplicativo Piloto Institucional</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
