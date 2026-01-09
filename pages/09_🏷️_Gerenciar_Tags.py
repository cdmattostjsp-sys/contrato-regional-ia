"""
Página de Gerenciamento de Tags
================================
Interface para criar, editar e gerenciar tags de contratos.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state
from services.tag_service import get_tag_service
from services.contract_service import get_todos_contratos


def render_tag_badge(tag: dict, tamanho: str = "normal"):
    """Renderiza um badge de tag"""
    font_size = "0.75rem" if tamanho == "pequeno" else "0.85rem"
    padding = "0.2rem 0.5rem" if tamanho == "pequeno" else "0.3rem 0.7rem"
    
    return f"""
    <span style="background: {tag['cor']}; color: white; 
                 padding: {padding}; border-radius: 12px; 
                 font-size: {font_size}; font-weight: bold;
                 display: inline-block; margin: 0.2rem;">
        {tag['icone']} {tag['nome']}
    </span>
    """


def main():
    st.set_page_config(
        page_title="TJSP - Gerenciar Tags",
        page_icon="🏷️",
        layout="wide"
    )
    
    apply_tjsp_styles()
    initialize_session_state()
    
    tag_service = get_tag_service()
    
    # Cabeçalho padronizado institucional
    from components.layout_header import render_module_banner
    render_module_banner(
        title="Gerenciamento de Tags",
        subtitle="Organize e categorize contratos com tags personalizadas"
    )
    
    # Navegação
    col_nav1, col_nav2 = st.columns([6, 1])
    with col_nav1:
        if st.button("🏛️ Voltar à Home", use_container_width=False):
            st.switch_page("Home.py")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🏷️ Tags Disponíveis", "➕ Criar Tag", "📊 Estatísticas"])
    
    # ===== TAB 1: TAGS DISPONÍVEIS =====
    with tab1:
        st.markdown("## Tags do Sistema")
        
        todas_tags = tag_service.obter_todas_tags()
        
        # Separa tags do sistema e customizadas
        tags_sistema = [t for t in todas_tags if not t.get('customizada', False)]
        tags_customizadas = [t for t in todas_tags if t.get('customizada', False)]
        
        # Tags do sistema
        st.markdown("### Tags Pré-definidas")
        
        cols = st.columns(4)
        for idx, tag in enumerate(tags_sistema):
            with cols[idx % 4]:
                st.markdown(render_tag_badge(tag), unsafe_allow_html=True)
                st.caption(f"ID: `{tag['id']}`")
        
        st.markdown("---")
        
        # Tags customizadas
        st.markdown("### Tags Personalizadas")
        
        if tags_customizadas:
            for tag in tags_customizadas:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(render_tag_badge(tag), unsafe_allow_html=True)
                    st.caption(f"ID: `{tag['id']}` • Criada em: {tag.get('criada_em', 'N/A')[:10]}")
                
                with col2:
                    if st.button("✏️ Editar", key=f"edit_{tag['id']}", use_container_width=True):
                        st.session_state.editando_tag = tag['id']
                        st.rerun()
                
                with col3:
                    if st.button("🗑️ Excluir", key=f"del_{tag['id']}", use_container_width=True):
                        if tag_service.excluir_tag(tag['id']):
                            st.success(f"Tag '{tag['nome']}' excluída!")
                            st.rerun()
                        else:
                            st.error("Erro ao excluir tag")
                
                # Modal de edição
                if st.session_state.get('editando_tag') == tag['id']:
                    with st.form(key=f"form_edit_{tag['id']}"):
                        st.markdown(f"**Editando:** {tag['nome']}")
                        
                        novo_nome = st.text_input("Nome", value=tag['nome'])
                        nova_cor = st.color_picker("Cor", value=tag['cor'])
                        novo_icone = st.text_input("Ícone (emoji)", value=tag['icone'], max_chars=2)
                        
                        col_save, col_cancel = st.columns(2)
                        
                        with col_save:
                            if st.form_submit_button("💾 Salvar", use_container_width=True):
                                tag_service.atualizar_tag(
                                    tag['id'],
                                    nome=novo_nome,
                                    cor=nova_cor,
                                    icone=novo_icone
                                )
                                st.session_state.editando_tag = None
                                st.success("Tag atualizada!")
                                st.rerun()
                        
                        with col_cancel:
                            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                                st.session_state.editando_tag = None
                                st.rerun()
                
                st.markdown("---")
        else:
            st.info("💡 Nenhuma tag personalizada criada. Use a aba 'Criar Tag' para adicionar.")
    
    # ===== TAB 2: CRIAR TAG =====
    with tab2:
        st.markdown("## Criar Nova Tag")
        
        with st.form("criar_tag_form"):
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                nome_tag = st.text_input(
                    "Nome da Tag *",
                    placeholder="Ex: Em análise",
                    help="Nome descritivo para a tag"
                )
                
                icone_tag = st.text_input(
                    "Ícone (emoji) *",
                    value="🏷️",
                    max_chars=2,
                    help="Emoji que representa a tag"
                )
            
            with col_form2:
                cor_tag = st.color_picker(
                    "Cor da Tag *",
                    value="#6C757D",
                    help="Cor de fundo da tag"
                )
                
                st.markdown("### Pré-visualização")
                if nome_tag:
                    preview_tag = {
                        'nome': nome_tag,
                        'cor': cor_tag,
                        'icone': icone_tag
                    }
                    st.markdown(render_tag_badge(preview_tag), unsafe_allow_html=True)
            
            st.markdown("---")
            
            col_submit1, col_submit2, col_submit3 = st.columns([1, 1, 2])
            
            with col_submit1:
                submit = st.form_submit_button("✅ Criar Tag", type="primary", use_container_width=True)
            
            with col_submit2:
                if st.form_submit_button("🔄 Limpar", use_container_width=True):
                    st.rerun()
            
            if submit:
                if not nome_tag:
                    st.error("❌ Nome da tag é obrigatório")
                elif not icone_tag:
                    st.error("❌ Ícone é obrigatório")
                else:
                    nova_tag = tag_service.criar_tag(
                        nome=nome_tag,
                        cor=cor_tag,
                        icone=icone_tag
                    )
                    st.success(f"✅ Tag '{nova_tag['nome']}' criada com sucesso!")
                    st.markdown(f"**ID:** `{nova_tag['id']}`")
                    st.rerun()
        
        # Sugestões de cores
        st.markdown("---")
        st.markdown("### Paleta de Cores Sugeridas")
        
        cores_sugeridas = {
            "Vermelho": "#DC3545",
            "Laranja": "#FD7E14",
            "Amarelo": "#FFC107",
            "Verde": "#28A745",
            "Azul": "#007BFF",
            "Índigo": "#6610F2",
            "Roxo": "#6F42C1",
            "Rosa": "#E83E8C",
            "Ciano": "#17A2B8",
            "Cinza": "#6C757D",
            "Marrom": "#795548",
            "Verde-água": "#20C997"
        }
        
        cols_cores = st.columns(6)
        for idx, (nome_cor, hex_cor) in enumerate(cores_sugeridas.items()):
            with cols_cores[idx % 6]:
                st.markdown(
                    f"<div style='background: {hex_cor}; color: white; padding: 0.5rem; "
                    f"border-radius: 5px; text-align: center; font-size: 0.75rem;'>"
                    f"{nome_cor}<br><code style='color: white;'>{hex_cor}</code></div>",
                    unsafe_allow_html=True
                )
    
    # ===== TAB 3: ESTATÍSTICAS =====
    with tab3:
        st.markdown("## Estatísticas de Uso de Tags")
        
        estatisticas = tag_service.obter_estatisticas_tags()
        
        # Ordena por uso
        stats_ordenadas = sorted(
            estatisticas.items(),
            key=lambda x: x[1]['uso'],
            reverse=True
        )
        
        if stats_ordenadas:
            # Métricas gerais
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                total_tags = len(estatisticas)
                st.metric("Total de Tags", total_tags)
            
            with col_stat2:
                tags_usadas = sum(1 for _, stat in stats_ordenadas if stat['uso'] > 0)
                st.metric("Tags em Uso", tags_usadas)
            
            with col_stat3:
                total_uso = sum(stat['uso'] for _, stat in stats_ordenadas)
                st.metric("Total de Atribuições", total_uso)
            
            st.markdown("---")
            
            # Tabela de uso
            st.markdown("### Detalhamento por Tag")
            
            for tag_id, stat in stats_ordenadas:
                if stat['uso'] > 0:  # Mostra apenas tags em uso
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        tag_badge = {
                            'nome': stat['nome'],
                            'cor': stat['cor'],
                            'icone': stat['icone']
                        }
                        st.markdown(render_tag_badge(tag_badge), unsafe_allow_html=True)
                    
                    with col2:
                        st.metric("Contratos", stat['uso'])
                    
                    st.markdown("---")
            
            # Tags não utilizadas
            tags_nao_usadas = [
                (tag_id, stat) for tag_id, stat in stats_ordenadas 
                if stat['uso'] == 0
            ]
            
            if tags_nao_usadas:
                with st.expander(f"🔍 Tags Não Utilizadas ({len(tags_nao_usadas)})"):
                    for tag_id, stat in tags_nao_usadas:
                        tag_badge = {
                            'nome': stat['nome'],
                            'cor': stat['cor'],
                            'icone': stat['icone']
                        }
                        st.markdown(render_tag_badge(tag_badge), unsafe_allow_html=True)
        else:
            st.info("📭 Nenhuma tag cadastrada no sistema")


if __name__ == "__main__":
    main()
