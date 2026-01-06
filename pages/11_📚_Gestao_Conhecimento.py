"""
Página de Gestão da Biblioteca de Conhecimento Institucional
==============================================================
FASE 2.1 - Biblioteca Institucional Curada

FUNCIONALIDADES:
- Upload de documentos PDF/DOCX (restrito por perfil)
- Formulário de metadados obrigatórios
- Visualização de documentos publicados
- Revogação de versões
- Estatísticas da biblioteca

GOVERNANÇA:
- Apenas perfis autorizados podem fazer upload
- Versionamento obrigatório
- Rastreabilidade completa

AUTOR: Fase 2.1 - Biblioteca de Conhecimento
DATA: Janeiro/2026
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, date

sys.path.append(str(Path(__file__).parent.parent))

from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state
from services.knowledge_governance_service import (
    verificar_perfil_autorizado,
    publicar_documento,
    listar_documentos,
    listar_documentos_ativos,
    revogar_documento,
    get_estatisticas_biblioteca,
    TIPOS_DOCUMENTO,
    STATUS_DOCUMENTO,
    PERFIS_AUTORIZADOS
)


def render_header():
    """Renderiza cabeçalho institucional."""
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;">
            <h1 style="color: white; margin: 0;">📚 Biblioteca de Conhecimento Institucional</h1>
            <p style="color: #e2e8f0; margin: 0.5rem 0 0 0;">
                Gestão de documentos orientativos do TJSP - Fase 2.1
            </p>
        </div>
    """, unsafe_allow_html=True)


def render_estatisticas():
    """Renderiza estatísticas da biblioteca."""
    stats = get_estatisticas_biblioteca()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📄 Total de Documentos", stats["total"])
    with col2:
        st.metric("✅ Documentos Ativos", stats["ativos"])
    with col3:
        st.metric("🚫 Revogados", stats["revogados"])
    with col4:
        st.metric("📝 Com Texto Extraído", stats["com_texto_extraido"])


def render_formulario_upload():
    """Renderiza formulário de upload com metadados."""
    
    st.markdown("### 📤 Publicar Novo Documento")
    
    # Verifica perfil
    autorizado, msg_perfil = verificar_perfil_autorizado()
    
    if not autorizado:
        st.warning(f"⚠️ {msg_perfil}")
        st.info(f"""
        **Perfis autorizados para publicação:**
        {', '.join(PERFIS_AUTORIZADOS)}
        
        Seu perfil atual: `{st.session_state.get('perfil', 'Não definido')}`
        
        *Para alterar seu perfil, acesse a página de Configurações.*
        """)
        return
    
    st.success(f"✅ {msg_perfil}")
    
    # Formulário de upload
    with st.form("form_upload_documento", clear_on_submit=True):
        
        # Upload de arquivo
        arquivo = st.file_uploader(
            "Selecione o documento (PDF ou DOCX)",
            type=["pdf", "docx"],
            help="Apenas arquivos PDF e DOCX são aceitos"
        )
        
        st.markdown("---")
        st.markdown("**Metadados Obrigatórios**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            titulo = st.text_input(
                "Título Institucional *",
                placeholder="Ex: Nota Técnica – ISS em Contratos Administrativos",
                help="Título oficial do documento"
            )
            
            tipo = st.selectbox(
                "Tipo de Documento *",
                options=[""] + TIPOS_DOCUMENTO,
                help="Categoria do documento"
            )
            
            versao = st.text_input(
                "Versão *",
                placeholder="Ex: 1.0, 2.1",
                help="Formato: X.Y (ex: 1.0, 1.1, 2.0)"
            )
        
        with col2:
            area = st.text_input(
                "Área Responsável *",
                placeholder="Ex: Assessoria Jurídica, Coordenadoria de Contratos",
                help="Área institucional responsável pelo documento"
            )
            
            status = st.selectbox(
                "Status",
                options=STATUS_DOCUMENTO,
                index=0,
                help="ATIVO: disponível para consulta. REVOGADO: não usado pela IA."
            )
            
            data_vigencia = st.date_input(
                "Data de Vigência",
                value=date.today(),
                help="Data a partir da qual o documento está vigente"
            )
        
        observacoes = st.text_area(
            "Observações",
            placeholder="Informações adicionais sobre o documento...",
            help="Notas, contexto ou instruções sobre uso do documento"
        )
        
        st.markdown("---")
        
        # Botão de submissão
        submitted = st.form_submit_button(
            "📤 Publicar Documento",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            if not arquivo:
                st.error("❌ Selecione um arquivo para upload.")
                return
            
            if not titulo or not tipo or not versao or not area:
                st.error("❌ Preencha todos os campos obrigatórios (*).")
                return
            
            # Monta metadados
            metadados = {
                "titulo": titulo.strip(),
                "tipo": tipo,
                "area": area.strip(),
                "versao": versao.strip(),
                "status": status,
                "data_vigencia": data_vigencia.isoformat() if data_vigencia else "",
                "observacoes": observacoes.strip()
            }
            
            # Tenta publicar
            with st.spinner("Publicando documento..."):
                sucesso, mensagem, documento = publicar_documento(
                    arquivo_bytes=arquivo.getvalue(),
                    nome_arquivo=arquivo.name,
                    metadados=metadados
                )
            
            if sucesso:
                st.success(mensagem)
                st.balloons()
            else:
                st.error(mensagem)


def render_lista_documentos():
    """Renderiza lista de documentos publicados."""
    
    st.markdown("### 📋 Documentos Publicados")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtro_tipo = st.selectbox(
            "Filtrar por Tipo",
            options=["Todos"] + TIPOS_DOCUMENTO,
            key="filtro_tipo"
        )
    
    with col2:
        filtro_status = st.selectbox(
            "Filtrar por Status",
            options=["Todos"] + STATUS_DOCUMENTO,
            key="filtro_status"
        )
    
    with col3:
        filtro_area = st.text_input(
            "Filtrar por Área",
            placeholder="Digite para filtrar...",
            key="filtro_area"
        )
    
    # Monta filtros
    filtros = {}
    if filtro_tipo != "Todos":
        filtros["tipo"] = filtro_tipo
    if filtro_status != "Todos":
        filtros["status"] = filtro_status
    
    # Busca documentos
    documentos = listar_documentos(filtros if filtros else None)
    
    # Aplica filtro de área (busca parcial)
    if filtro_area:
        documentos = [d for d in documentos if filtro_area.lower() in d.get("area", "").lower()]
    
    if not documentos:
        st.info("📭 Nenhum documento encontrado com os filtros aplicados.")
        return
    
    st.markdown(f"**{len(documentos)} documento(s) encontrado(s)**")
    
    # Exibe documentos em cards
    for doc in documentos:
        status_icon = "✅" if doc.get("status") == "ATIVO" else "🚫"
        texto_icon = "📝" if doc.get("texto_extraido") else "⚠️"
        
        with st.expander(f"{status_icon} {doc.get('titulo', 'Sem título')} (v{doc.get('versao', '?')})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                **Tipo:** {doc.get('tipo', '-')}  
                **Área:** {doc.get('area', '-')}  
                **Versão:** {doc.get('versao', '-')}  
                **Status:** {doc.get('status', '-')}  
                **Data de Publicação:** {doc.get('data_publicacao', '-')[:10] if doc.get('data_publicacao') else '-'}  
                **Publicado por:** {doc.get('usuario_responsavel', '-')}
                """)
                
                if doc.get("observacoes"):
                    st.markdown(f"**Observações:** {doc['observacoes']}")
                
                st.markdown(f"{texto_icon} Texto extraído: {'Sim' if doc.get('texto_extraido') else 'Não'}")
            
            with col2:
                st.markdown(f"**ID:** `{doc.get('doc_id', '-')}`")
                
                # Botão de revogação (apenas para documentos ATIVOS)
                if doc.get("status") == "ATIVO":
                    autorizado, _ = verificar_perfil_autorizado()
                    if autorizado:
                        if st.button(f"🚫 Revogar", key=f"revogar_{doc.get('doc_id')}"):
                            st.session_state[f"confirmar_revogacao_{doc.get('doc_id')}"] = True
                        
                        if st.session_state.get(f"confirmar_revogacao_{doc.get('doc_id')}"):
                            motivo = st.text_input(
                                "Motivo da revogação:",
                                key=f"motivo_{doc.get('doc_id')}"
                            )
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("✅ Confirmar", key=f"confirmar_{doc.get('doc_id')}"):
                                    sucesso, msg = revogar_documento(doc.get('doc_id'), motivo)
                                    if sucesso:
                                        st.success(msg)
                                        st.rerun()
                                    else:
                                        st.error(msg)
                            with col_b:
                                if st.button("❌ Cancelar", key=f"cancelar_{doc.get('doc_id')}"):
                                    st.session_state[f"confirmar_revogacao_{doc.get('doc_id')}"] = False
                                    st.rerun()


def render_ajuda():
    """Renderiza seção de ajuda."""
    
    with st.expander("ℹ️ Como usar a Biblioteca de Conhecimento"):
        st.markdown("""
        ### Sobre a Biblioteca Institucional
        
        A Biblioteca de Conhecimento Institucional é um repositório curado de documentos 
        orientativos do TJSP. Documentos publicados aqui podem ser consultados pelo 
        **COPILOTO** para fornecer respostas baseadas em normas e orientações oficiais.
        
        ### Quem pode publicar?
        
        Apenas usuários com perfis autorizados:
        - **ADMIN**: Administradores do sistema
        - **CURADOR**: Curadores de conteúdo
        - **JURIDICO**: Área jurídica
        
        ### Tipos de documentos aceitos
        
        - **Manual**: Manuais operacionais e de procedimentos
        - **Nota Técnica**: Notas técnicas e pareceres
        - **Orientação Jurídica**: Orientações da área jurídica
        - **Caderno Técnico**: Cadernos técnicos de funções
        - **Instrução Normativa**: Instruções normativas internas
        - **Guia de Boas Práticas**: Guias de boas práticas
        
        ### Versionamento
        
        - Cada documento deve ter uma versão única (formato X.Y)
        - Não é permitido sobrescrever versões existentes
        - Versões anteriores podem ser revogadas
        
        ### Status dos documentos
        
        - **ATIVO**: Documento disponível para consulta pela IA
        - **REVOGADO**: Documento não é mais usado pela IA (mantido para histórico)
        
        ### Governança
        
        - Todas as publicações são registradas no histórico
        - Revogações são rastreadas com motivo e responsável
        - Apenas documentos ATIVOS são consultados pelo COPILOTO
        """)


def main():
    st.set_page_config(
        page_title="TJSP - Biblioteca de Conhecimento",
        page_icon="📚",
        layout="wide"
    )
    
    apply_tjsp_styles()
    initialize_session_state()
    
    render_header()
    
    # Abas principais
    tab1, tab2, tab3 = st.tabs([
        "📤 Publicar Documento",
        "📋 Documentos Publicados",
        "📊 Estatísticas"
    ])
    
    with tab1:
        render_formulario_upload()
        render_ajuda()
    
    with tab2:
        render_lista_documentos()
    
    with tab3:
        render_estatisticas()
        
        st.markdown("---")
        
        # Detalhamento por tipo e área
        stats = get_estatisticas_biblioteca()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📁 Por Tipo de Documento")
            if stats["por_tipo"]:
                for tipo, qtd in stats["por_tipo"].items():
                    st.markdown(f"- **{tipo}**: {qtd}")
            else:
                st.info("Nenhum documento publicado ainda.")
        
        with col2:
            st.markdown("### 🏢 Por Área Responsável")
            if stats["por_area"]:
                for area, qtd in stats["por_area"].items():
                    st.markdown(f"- **{area}**: {qtd}")
            else:
                st.info("Nenhum documento publicado ainda.")


if __name__ == "__main__":
    main()
