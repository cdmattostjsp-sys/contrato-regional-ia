"""
Página de Visualização de Contrato
===================================
Exibe detalhes completos de um contrato selecionado.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state
from services.contract_service import get_contrato_detalhes


def render_contrato_header(contrato: dict):
    """
    Renderiza cabeçalho do contrato
    ================================
    EVOLUÇÃO RAJ 10: Cabeçalho simplificado, foco no contrato como objeto central.
    """
    status_colors = {
        "ativo": ("🟢", "#28A745"),
        "atencao": ("🟡", "#FFC107"),
        "critico": ("🔴", "#DC3545")
    }
    
    icon, color = status_colors.get(contrato.get("status", "ativo"), ("⚪", "#666"))
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #003366 0%, #0066CC 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 1rem; color: white;">
            <h1>{icon} {contrato['numero']}</h1>
            <p style="font-size: 1.2rem; margin: 0.5rem 0;">{contrato['objeto']}</p>
            <p style="opacity: 0.9;"><strong>Fornecedor:</strong> {contrato['fornecedor']}</p>
        </div>
    """, unsafe_allow_html=True)


def render_bloco_vigencia(contrato: dict):
    """
    BLOCO DE VIGÊNCIA - PRIORIDADE ALTA
    ====================================
    Feedback RAJ 10: Exibir vigência no TOPO com semáforo visual.
    
    Lógica de semáforo:
    🟢 Verde: > 120 dias restantes
    🟡 Amarelo: 60-120 dias restantes  
    🔴 Vermelho: < 60 dias restantes
    """
    vigencia = contrato.get("vigencia_detalhada", {})
    
    dias_restantes = vigencia.get("dias_restantes", 0)
    data_inicio = vigencia.get("data_inicio")
    data_fim = vigencia.get("data_fim")
    status_semaforo = vigencia.get("status_semaforo", "verde")
    
    # Define cores do semáforo
    cores_semaforo = {
        "verde": {"cor": "#28A745", "icone": "🟢", "texto": "Vigência Regular"},
        "amarelo": {"cor": "#FFC107", "icone": "🟡", "texto": "Atenção: Vigência Próxima do Fim"},
        "vermelho": {"cor": "#DC3545", "icone": "🔴", "texto": "Crítico: Vigência Terminando"}
    }
    
    config = cores_semaforo.get(status_semaforo, cores_semaforo["verde"])
    
    st.markdown(f"""
        <div style="background: {config['cor']}; padding: 1.5rem; border-radius: 10px; 
                    margin-bottom: 1.5rem; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h2 style="margin: 0 0 1rem 0; font-size: 1.5rem;">
                {config['icone']} VIGÊNCIA DO CONTRATO
            </h2>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;">
                <div>
                    <p style="opacity: 0.9; margin: 0; font-size: 0.9rem;">Data Inicial</p>
                    <p style="margin: 0.3rem 0 0 0; font-size: 1.3rem; font-weight: bold;">
                        {data_inicio.strftime('%d/%m/%Y') if data_inicio else '-'}
                    </p>
                </div>
                <div>
                    <p style="opacity: 0.9; margin: 0; font-size: 0.9rem;">Data Final</p>
                    <p style="margin: 0.3rem 0 0 0; font-size: 1.3rem; font-weight: bold;">
                        {data_fim.strftime('%d/%m/%Y') if data_fim else '-'}
                    </p>
                </div>
                <div>
                    <p style="opacity: 0.9; margin: 0; font-size: 0.9rem;">Dias Restantes</p>
                    <p style="margin: 0.3rem 0 0 0; font-size: 1.3rem; font-weight: bold;">
                        {dias_restantes} dias
                    </p>
                </div>
            </div>
            <p style="margin: 1rem 0 0 0; font-size: 1rem; font-weight: 500; opacity: 0.95;">
                {config['texto']}
            </p>
        </div>
    """, unsafe_allow_html=True)


def render_bloco_iss(contrato: dict):
    """
    BLOCO DE TRIBUTAÇÃO (ISS)
    ==========================
    Feedback RAJ 10: Indicador simples de retenção de ISS com base legal.
    
    Nota: Caráter orientativo. Não calcula tributos.
    """
    tributacao = contrato.get("tributacao", {})
    
    retem_iss = tributacao.get("retem_iss", False)
    base_legal = tributacao.get("base_legal_iss", "Não informada")
    observacao = tributacao.get("observacao_iss", "")
    
    cor_badge = "#28A745" if retem_iss else "#6C757D"
    texto_badge = "SIM" if retem_iss else "NÃO"
    
    st.markdown(f"""
        <div style="background: #F8F9FA; padding: 1.5rem; border-radius: 10px; 
                    border-left: 4px solid {cor_badge}; margin-bottom: 1.5rem;">
            <h3 style="margin: 0 0 1rem 0; color: #003366;">
                💰 TRIBUTAÇÃO - ISS (Imposto Sobre Serviços)
            </h3>
            <div style="margin-bottom: 1rem;">
                <span style="background: {cor_badge}; color: white; padding: 0.4rem 1rem; 
                            border-radius: 20px; font-weight: bold; font-size: 0.9rem;">
                    Retém ISS: {texto_badge}
                </span>
            </div>
    """, unsafe_allow_html=True)
    
    if retem_iss:
        st.markdown(f"""
            <div style="margin-top: 1rem;">
                <p style="margin: 0.5rem 0; color: #495057;">
                    <strong>Base Legal:</strong> {base_legal}
                </p>
                <p style="margin: 0.5rem 0; color: #495057;">
                    <strong>Observação:</strong> {observacao}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <p style="margin: 1rem 0 0 0; font-size: 0.85rem; color: #6C757D; font-style: italic;">
            ⚠️ Informação orientativa. Não substitui análise da área tributária.
        </p>
        </div>
    """, unsafe_allow_html=True)


def render_bloco_pagamentos(contrato: dict):
    """
    BLOCO DE ATESTES E PAGAMENTOS
    ==============================
    Feedback RAJ 10: Visão complementar aos dados financeiros do SGF.
    Exibe histórico de pagamentos com status de ateste.
    """
    pagamentos = contrato.get("pagamentos", [])
    
    st.markdown("""
        <h3 style="color: #003366; margin: 0 0 1rem 0;">
            📋 ATESTES E PAGAMENTOS
        </h3>
    """, unsafe_allow_html=True)
    
    if not pagamentos:
        st.info("Nenhum pagamento registrado ainda.")
        return
    
    # Tabela de pagamentos
    for i, pag in enumerate(pagamentos):
        status_cor = "#28A745" if pag["status"] == "Atestado" else "#FFC107"
        status_icone = "✅" if pag["status"] == "Atestado" else "⏳"
        
        st.markdown(f"""
            <div style="background: white; border: 1px solid #DEE2E6; border-radius: 8px; 
                        padding: 1rem; margin-bottom: 0.8rem; border-left: 4px solid {status_cor};">
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 0.8rem;">
                    <div>
                        <p style="margin: 0; font-size: 0.8rem; color: #6C757D;">Competência</p>
                        <p style="margin: 0.2rem 0 0 0; font-weight: bold; color: #212529;">{pag['competencia']}</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 0.8rem; color: #6C757D;">Nota Fiscal</p>
                        <p style="margin: 0.2rem 0 0 0; font-weight: bold; color: #212529;">{pag['nota_fiscal']}</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 0.8rem; color: #6C757D;">Valor</p>
                        <p style="margin: 0.2rem 0 0 0; font-weight: bold; color: #212529;">R$ {pag['valor']:,.2f}</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 0.8rem; color: #6C757D;">Status</p>
                        <p style="margin: 0.2rem 0 0 0; font-weight: bold; color: {status_cor};">
                            {status_icone} {pag['status']}
                        </p>
                    </div>
                </div>
        """, unsafe_allow_html=True)
        
        if pag["status"] == "Atestado":
            data_ateste_fmt = pag['data_ateste'].strftime('%d/%m/%Y') if pag['data_ateste'] else '-'
            st.markdown(f"""
                <div style="background: #F8F9FA; padding: 0.6rem; border-radius: 5px; font-size: 0.85rem;">
                    <p style="margin: 0.2rem 0; color: #495057;">
                        <strong>Unidade:</strong> {pag['unidade_ateste']}
                    </p>
                    <p style="margin: 0.2rem 0; color: #495057;">
                        <strong>Data do Ateste:</strong> {data_ateste_fmt} | 
                        <strong>Responsável:</strong> {pag['responsavel_ateste']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


def render_acoes_documentos():
    """
    AÇÕES RÁPIDAS DE DOCUMENTOS
    ============================
    Feedback RAJ 10: Botão fixo "Gerar Documento" com opções padronizadas.
    O conteúdo é gerado pelo copilot baseado no contrato.
    """
    st.markdown("""
        <h3 style="color: #003366; margin: 1.5rem 0 1rem 0;">
            📄 AÇÕES RÁPIDAS - DOCUMENTOS
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Notificação Contratual", use_container_width=True, type="primary"):
            st.session_state.documento_tipo = "notificacao"
            st.switch_page("pages/03_📝_Notificações.py")
    
    with col2:
        if st.button("📊 Relatório do Fiscal", use_container_width=True):
            st.info("🤖 Recurso em desenvolvimento. O copiloto gerará o relatório baseado nos dados do contrato.")
    
    with col3:
        if st.button("📋 Relatório Final ao Gestor", use_container_width=True):
            st.info("🤖 Recurso em desenvolvimento. O copiloto gerará o relatório final consolidado.")


def render_contrato_detalhes(contrato: dict):
    """
    Renderiza detalhes do contrato em tabs
    =======================================
    EVOLUÇÃO RAJ 10: Reorganizado com nova aba "Apoio ao Gestor" e dados consolidados.
    """
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Dados Gerais", 
        "💰 Pagamentos & ISS",
        "👔 Apoio ao Gestor",
        "📁 Documentos", 
        "📊 Histórico"
    ])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💰 Informações Financeiras")
            st.info(f"""
            **Valor Total:** R$ {contrato['valor']:,.2f}  
            **Tipo:** {contrato['tipo']}  
            **Status:** {contrato['status'].upper()}
            """)
            
            st.markdown("### 📅 Informações de Vigência")
            st.info(f"""
            **Período:** {contrato['vigencia']}  
            **Última Atualização:** {contrato['ultima_atualizacao'].strftime('%d/%m/%Y %H:%M')}
            """)
        
        with col2:
            st.markdown("### 👥 Fiscalização")
            st.success(f"""
            **Fiscal Titular:** {contrato['fiscal_titular']}  
            **Fiscal Substituto:** {contrato['fiscal_substituto']}
            """)
            
            if "pendencias" in contrato and contrato["pendencias"]:
                st.markdown("### ⚠️ Pendências")
                for pendencia in contrato["pendencias"]:
                    st.warning(f"• {pendencia}")
    
    with tab2:
        # Bloco de Pagamentos e Atestes
        render_bloco_pagamentos(contrato)
        
        st.markdown("---")
        
        # Bloco de ISS
        render_bloco_iss(contrato)
    
    with tab3:
        # MODO GESTOR - Suporte Normativo
        st.markdown("""
            <div style="background: #FFF3CD; border-left: 4px solid #FFC107; padding: 1rem; 
                        border-radius: 5px; margin-bottom: 1.5rem;">
                <h3 style="color: #856404; margin: 0 0 0.5rem 0;">
                    👔 APOIO AO GESTOR - SUPORTE NORMATIVO
                </h3>
                <p style="color: #856404; margin: 0; font-size: 0.9rem;">
                    ⚠️ Informações orientativas baseadas em legislação e cláusulas contratuais.
                    <strong>Não substitui análise jurídica.</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        info_trabalhista = contrato.get("info_trabalhista", {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📖 Informações Trabalhistas")
            
            possui_mao_obra = info_trabalhista.get("possui_mao_obra_residente", False)
            aplica_cc = info_trabalhista.get("aplica_convencao_coletiva", False)
            
            if possui_mao_obra:
                st.success("✅ Contrato com mão de obra residente")
            else:
                st.info("ℹ️ Contrato sem mão de obra residente")
            
            if aplica_cc:
                st.info(f"""
                **Categoria:** {info_trabalhista.get('categoria_profissional', 'Não informada')}  
                **Sindicato:** {info_trabalhista.get('sindicato', 'Não informado')}
                """)
                st.warning("⚠️ Aplicável: Acordo/Convenção Coletiva de Trabalho")
        
        with col2:
            st.markdown("### 📚 Base Normativa")
            
            with st.expander("📕 CLT - Consolidação das Leis do Trabalho"):
                st.write("""
                - **Art. 58**: Jornada de trabalho (8h diárias, 44h semanais)
                - **Art. 71**: Intervalos para repouso e alimentação
                - **Art. 457**: Composição do salário
                - **Art. 468**: Alteração das condições de trabalho
                """)
            
            with st.expander("📘 Normativas Correlatas"):
                st.write("""
                - **IN SEGES/ME nº 5/2017**: Contratação de serviços com dedicação exclusiva
                - **Lei nº 8.666/93**: Licitações e Contratos Administrativos
                - **IN TJSP nº 12/2025**: Manual de Contratos TJSP
                """)
        
        st.markdown("---")
        
        st.markdown("### 💬 Tire Dúvidas com o Copiloto")
        st.write("O Copiloto pode responder questões sobre legislação trabalhista aplicável a este contrato.")
        
        if st.button("💬 Abrir Copiloto para Consulta Normativa", use_container_width=True, type="primary"):
            st.session_state.copilot_contexto = "normativo"
            st.switch_page("pages/02_💬_Copiloto.py")
    
    with tab4:
        st.markdown("### 📁 Documentos do Contrato")
        if "documentos" in contrato:
            for doc in contrato["documentos"]:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"📄 **{doc['tipo']}**")
                with col2:
                    st.write(doc['data'])
                with col3:
                    st.write(f"✓ {doc['status']}")
                st.markdown("---")
        else:
            st.info("Documentos serão carregados em breve.")
    
    with tab5:
        st.markdown("### 📊 Histórico de Eventos")
        if "historico_eventos" in contrato:
            for evento in contrato["historico_eventos"]:
                st.markdown(f"""
                    <div class="contract-card">
                        <p><strong>{evento['data'].strftime('%d/%m/%Y %H:%M')}</strong></p>
                        <p>{evento['evento']}</p>
                        <p style="color: #666; font-size: 0.9rem;">Por: {evento['responsavel']}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Histórico será carregado em breve.")


def main():
    st.set_page_config(
        page_title="TJSP - Detalhes do Contrato",
        page_icon="📄",
        layout="wide"
    )
    
    apply_tjsp_styles()
    initialize_session_state()
    
    # Verifica se há contrato selecionado
    if not st.session_state.contrato_selecionado:
        st.warning("⚠️ Nenhum contrato selecionado. Retorne ao dashboard.")
        if st.button("🏠 Voltar ao Dashboard"):
            st.switch_page("app.py")
        return
    
    # Obtém detalhes completos do contrato
    contrato = get_contrato_detalhes(st.session_state.contrato_selecionado["id"])
    
    if not contrato:
        st.error("❌ Erro ao carregar detalhes do contrato.")
        return
    
    # Renderiza cabeçalho
    render_contrato_header(contrato)
    
    # 🚨 BLOCO DE VIGÊNCIA - PRIORIDADE ALTA (Feedback RAJ 10)
    render_bloco_vigencia(contrato)
    
    # Ações Rápidas de Documentos
    render_acoes_documentos()
    
    st.markdown("---")
    
    # Botões de navegação
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Dashboard", use_container_width=True):
            st.switch_page("app.py")
    
    with col2:
        if st.button("💬 Copiloto", use_container_width=True):
            st.switch_page("pages/02_💬_Copiloto.py")
    
    with col3:
        if st.button("📝 Notificar", use_container_width=True):
            st.switch_page("pages/03_📝_Notificações.py")
    
    with col4:
        if st.button("📖 Como Proceder", use_container_width=True):
            st.switch_page("pages/04_📖_Como_Proceder.py")
    
    st.markdown("---")
    
    # Renderiza detalhes
    render_contrato_detalhes(contrato)


if __name__ == "__main__":
    main()
