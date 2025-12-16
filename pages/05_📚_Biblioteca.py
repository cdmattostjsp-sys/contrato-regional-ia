"""
Página de Consulta aos Manuais Institucionais
==============================================
Permite visualização e futura busca nos manuais em PDF.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state
from services.document_service import (
    listar_documentos_disponiveis,
    obter_referencias_legais,
    gerar_resumo_documentos
)


def render_documento_card(doc: dict):
    """Renderiza card de documento"""
    icons = {
        "Manual Institucional TJSP": "📘",
        "Instrução Normativa": "📜",
        "Manual de Boas Práticas": "📗",
        "Documento Institucional": "📄"
    }
    
    icon = icons.get(doc['tipo'], "📄")
    
    st.markdown(f"""
        <div class="contract-card">
            <div class="contract-header">
                <h3>{icon} {doc['tipo']}</h3>
                <span class="contract-badge">{doc['tamanho_mb']} MB</span>
            </div>
            <p><strong>Arquivo:</strong> {doc['nome']}</p>
            <p><strong>Localização:</strong> knowledge/raj_10_1/</p>
            <p style="color: #28A745;"><strong>Status:</strong> ✅ Disponível</p>
        </div>
    """, unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="TJSP - Biblioteca de Manuais",
        page_icon="📚",
        layout="wide"
    )
    
    apply_tjsp_styles()
    initialize_session_state()
    
    # Cabeçalho
    st.markdown("""
        <div style="background: linear-gradient(135deg, #003366 0%, #0066CC 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem; color: white;">
            <h1>📚 Biblioteca de Manuais Institucionais</h1>
            <p style="font-size: 1.1rem; opacity: 0.9;">
            Base de conhecimento para fiscalização e gestão de contratos - RAJ 10.1
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Botão de navegação
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🏠 Dashboard", use_container_width=True):
            st.switch_page("app.py")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📄 Documentos", "⚖️ Referências Legais", "🔍 Busca (Em Breve)"])
    
    with tab1:
        st.markdown("## 📄 Documentos Disponíveis")
        
        documentos = listar_documentos_disponiveis()
        
        if documentos:
            st.success(f"✅ {len(documentos)} documento(s) disponível(is) na base de conhecimento")
            
            for doc in documentos:
                render_documento_card(doc)
                st.markdown("<br>", unsafe_allow_html=True)
            
            # Informações sobre implementação futura
            with st.expander("ℹ️ Sobre a Integração dos Documentos"):
                st.info("""
                ### 📖 Status Atual
                
                Os documentos estão **disponíveis e armazenados** na base de conhecimento,
                mas a **extração automática de conteúdo** será implementada na próxima fase.
                
                ### 🚀 Próximas Funcionalidades
                
                Quando implementarmos a extração de PDF, você poderá:
                
                - 🔍 **Buscar** termos específicos em todos os manuais
                - 💬 **Copilot aprimorado** com respostas baseadas nos documentos reais
                - 📝 **Notificações automáticas** usando fundamentação dos manuais
                - 📊 **Referências cruzadas** entre contratos e normas
                - 🎯 **Citações automáticas** de artigos e cláusulas
                
                ### 🔧 Implementação Técnica
                
                Para desenvolvedores:
                ```python
                # Adicionar ao requirements.txt:
                PyPDF2==3.0.1
                # ou
                pdfplumber==0.10.3
                
                # Implementar em services/document_service.py
                ```
                """)
        else:
            st.warning("⚠️ Nenhum documento encontrado na base de conhecimento.")
    
    with tab2:
        st.markdown("## ⚖️ Referências Legais")
        
        referencias = obter_referencias_legais()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📜 Legislação Federal")
            
            st.markdown("""
            #### Lei 8.666/1993
            **Lei de Licitações e Contratos Administrativos**
            
            Artigos importantes para fiscalização:
            - **Art. 67** - Fiscalização e acompanhamento
            - **Art. 77** - Inexecução total ou parcial
            - **Art. 78** - Motivos de rescisão
            - **Art. 87** - Penalidades aplicáveis
            - **Art. 88** - Sanções previstas
            """)
            
            st.markdown("---")
            
            st.markdown("""
            #### Lei 14.133/2021
            **Nova Lei de Licitações**
            
            Artigos importantes:
            - **Art. 117** - Fiscalização técnica e administrativa
            - **Art. 137** - Inexecução contratual
            - **Art. 155** - Penalidades e sanções
            - **Art. 156** - Sanções administrativas
            """)
        
        with col2:
            st.markdown("### 📘 Normas TJSP")
            
            for key, ref in referencias.items():
                if "arquivo" in ref:
                    st.markdown(f"""
                    #### {ref['nome']}
                    **{ref['descricao']}**
                    
                    📄 Arquivo: `{ref['arquivo']}`  
                    ✅ Status: Disponível na base de conhecimento
                    """)
                    st.markdown("---")
    
    with tab3:
        st.markdown("## 🔍 Busca nos Manuais")
        
        st.info("""
        ### 🚧 Funcionalidade em Desenvolvimento
        
        A busca automática nos manuais será implementada em breve!
        """)
        
        # Interface de busca (mockup)
        st.text_input(
            "Digite o termo que deseja buscar nos manuais:",
            placeholder="Ex: fiscalização, penalidades, atestação...",
            disabled=True,
            key="busca_manual"
        )
        
        col1, col2, col3 = st.columns([1, 1, 3])
        
        with col1:
            st.button("🔍 Buscar", disabled=True, use_container_width=True)
        
        with col2:
            st.button("🗑️ Limpar", disabled=True, use_container_width=True)
        
        st.markdown("---")
        
        with st.expander("📋 Recursos Planejados"):
            st.markdown("""
            ### Recursos da Busca (Futuros)
            
            ✨ **Busca por palavra-chave**
            - Pesquisa em todos os documentos simultaneamente
            - Destacar trechos relevantes
            - Indicar página e documento de origem
            
            🎯 **Busca contextual**
            - Busca por tipo de contrato
            - Filtro por documento (Manual TJSP, Instrução Normativa, etc.)
            - Busca em seções específicas
            
            🤖 **Busca inteligente com IA**
            - Busca semântica (significado, não apenas palavras)
            - Respostas geradas automaticamente
            - Citações e referências automáticas
            
            📊 **Resultados enriquecidos**
            - Resumo do trecho encontrado
            - Links para documentos completos
            - Histórico de buscas
            - Buscas frequentes
            """)
    
    # Rodapé
    st.markdown("---")
    st.markdown("""
        <div class="tjsp-footer">
            <p>📚 Base de Conhecimento - TJSP RAJ 10.1</p>
            <p>Documentos institucionais para apoio à fiscalização de contratos</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
