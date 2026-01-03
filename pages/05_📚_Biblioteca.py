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
    
    # Cabeçalho padronizado institucional
    from components.layout_header import render_module_banner
    render_module_banner(
        title="Biblioteca de Manuais Institucionais",
        subtitle="Base de conhecimento para fiscalização e gestão de contratos - RAJ 10.1"
    )
    
    # Botão de navegação
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("Home.py")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📄 Documentos", "⚖️ Referências Legais", "🔍 Busca"])
    
    with tab1:
        st.markdown("## 📄 Documentos Disponíveis")
        
        documentos = listar_documentos_disponiveis()
        
        if documentos:
            # Agrupa por categoria
            categorias = {}
            for doc in documentos:
                cat = doc.get('categoria', 'Outros')
                if cat not in categorias:
                    categorias[cat] = []
                categorias[cat].append(doc)
            
            total_docs = len(documentos)
            total_mb = sum(d['tamanho_mb'] for d in documentos)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📚 Documentos", total_docs)
            with col2:
                st.metric("💾 Tamanho Total", f"{total_mb:.1f} MB")
            with col3:
                st.metric("🗂️ Categorias", len(categorias))
            
            st.markdown("---")
            
            # Exibe por categoria
            for categoria, docs in categorias.items():
                st.markdown(f"### {categoria}")
                
                if categoria == "Cadernos Técnicos":
                    # Agrupa por serviço
                    por_servico = {}
                    for doc in docs:
                        servico = doc.get('servico', 'Outros')
                        if servico not in por_servico:
                            por_servico[servico] = []
                        por_servico[servico].append(doc)
                    
                    for servico, docs_servico in por_servico.items():
                        with st.expander(f"📋 {servico}"):
                            for doc in docs_servico:
                                col1, col2 = st.columns([4, 1])
                                with col1:
                                    st.write(f"📄 {doc['nome']}")
                                with col2:
                                    st.write(f"{doc['tamanho_mb']} MB")
                else:
                    for doc in docs:
                        render_documento_card(doc)
                        st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown("---")
            
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
        from services.library_index_service import build_or_update_index, get_index_status
        from services.library_search_service import search_library
        st.markdown("## 🔍 Busca nos Manuais")
        status = get_index_status()
        st.info(f"**Status do índice:** {status['n_docs']} documentos, {status['n_pages']} páginas, última indexação: {status['last_indexed']}")
        if st.button("🔄 Atualizar índice", use_container_width=True):
            with st.spinner("Indexando documentos..."):
                build_or_update_index()
            st.success("Índice atualizado!")
            st.experimental_rerun()
        st.markdown("---")
        with st.form("form_busca_biblioteca"):
            query = st.text_input("Digite o termo que deseja buscar nos manuais:", placeholder="Ex: fiscalização, penalidades, atestação...", key="busca_manual")
            col1, col2 = st.columns([1, 1])
            with col1:
                categoria = st.selectbox("Categoria", ["Todas", "Manuais Institucionais", "Cadernos Técnicos", "Outros"])
            with col2:
                tipo = st.selectbox("Tipo", ["Todos", "Manual Institucional TJSP", "Instrução Normativa", "Manual de Boas Práticas", "Documento Institucional"])
            submitted = st.form_submit_button("🔍 Buscar")
        results = []
        if submitted and query:
            cat = None if categoria == "Todas" else categoria
            t = None if tipo == "Todos" else tipo
            with st.spinner("Buscando nos documentos..."):
                results = search_library(query, category=cat, doc_type=t, limit=20)
        if results:
            st.markdown(f"### Resultados ({len(results)})")
            for r in results:
                badge = "<span style='color:#fff;background:#888;padding:2px 8px;border-radius:8px;font-size:0.8em;'>Digitalizado</span>" if r["is_scanned"] else ""
                st.markdown(f"""
                <div style='border:1px solid #eee;border-radius:8px;padding:1em;margin-bottom:1em;'>
                <b>{r['title']}</b> <span style='color:#888;font-size:0.9em;'>({r['category']} / {r['doc_type']})</span> {badge}<br>
                <b>Página:</b> {r['page_no']}<br>
                <b>Trecho:</b> <span style='background:#f8f8f8;'>{r['snippet']}</span>
                </div>
                """, unsafe_allow_html=True)
        elif submitted:
            st.warning("Nenhum resultado encontrado.")
        st.markdown("---")
        with st.expander("📋 Recursos Planejados"):
            st.markdown("""
            ### Recursos futuros: busca semântica, integração IA, citações automáticas, OCR sob demanda.
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
