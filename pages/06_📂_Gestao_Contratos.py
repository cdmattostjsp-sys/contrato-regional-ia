"""
Página de Gestão de Contratos
==============================
Permite cadastro e upload de novos contratos em PDF.

Funcionalidades:
- Cadastrar novos contratos com metadados
- Upload de PDFs (contrato + aditivos)
- Listagem de contratos cadastrados
- Edição e exclusão
"""

import streamlit as st
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state


def salvar_contrato(dados_contrato: dict, arquivo_pdf, arquivos_aditivos=None):
    """
    Salva contrato no sistema (metadados + PDF + aditivos)
    
    Args:
        dados_contrato: Dicionário com dados do contrato
        arquivo_pdf: Arquivo PDF principal do contrato
        arquivos_aditivos: Lista de arquivos de aditivos (opcional)
    """
    # Define caminhos
    data_dir = Path("data")
    contratos_dir = Path("knowledge/contratos")
    json_path = data_dir / "contratos_cadastrados.json"
    
    # Carrega contratos existentes
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            contratos = json.load(f)
    else:
        contratos = []
    
    # Cria subdiretório para o contrato (comporta múltiplos PDFs)
    contrato_dir = contratos_dir / dados_contrato['id']
    contrato_dir.mkdir(exist_ok=True)
    
    # Salva PDF principal
    if arquivo_pdf:
        pdf_filename = f"{dados_contrato['id']}_PRINCIPAL.pdf"
        pdf_path = contrato_dir / pdf_filename
        
        with open(pdf_path, 'wb') as f:
            f.write(arquivo_pdf.getbuffer())
        
        dados_contrato['pdf_path'] = str(pdf_path)
        dados_contrato['pdf_filename'] = pdf_filename
    
    # Salva aditivos (se houver)
    dados_contrato['aditivos'] = []
    if arquivos_aditivos and len(arquivos_aditivos) > 0:
        for i, aditivo_file in enumerate(arquivos_aditivos, 1):
            aditivo_filename = f"{dados_contrato['id']}_ADITIVO_{i:02d}.pdf"
            aditivo_path = contrato_dir / aditivo_filename
            
            with open(aditivo_path, 'wb') as f:
                f.write(aditivo_file.getbuffer())
            
            dados_contrato['aditivos'].append({
                'numero': i,
                'filename': aditivo_filename,
                'path': str(aditivo_path),
                'data_upload': datetime.now().isoformat(),
                'nome_original': aditivo_file.name
            })
    
    # Adiciona timestamp
    dados_contrato['data_cadastro'] = datetime.now().isoformat()
    dados_contrato['total_aditivos'] = len(dados_contrato['aditivos'])
    
    # Adiciona à lista
    contratos.append(dados_contrato)
    
    # Salva JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(contratos, f, ensure_ascii=False, indent=2)
    
    return True


def listar_contratos_cadastrados():
    """Lista todos os contratos cadastrados via upload"""
    json_path = Path("data/contratos_cadastrados.json")
    
    if not json_path.exists():
        return []
    
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    st.set_page_config(
        page_title="TJSP - Gestão de Contratos",
        page_icon="📂",
        layout="wide"
    )
    
    apply_tjsp_styles()
    initialize_session_state()
    
    # Cabeçalho
    st.markdown("""
        <div class="tjsp-header">
            <h1>📂 Gestão de Contratos</h1>
            <p class="tjsp-subtitle">Cadastro e Upload de Contratos em PDF</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Botão de retorno
    if st.button("🏠 Voltar ao Dashboard", use_container_width=False):
        st.switch_page("Home.py")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2 = st.tabs(["➕ Cadastrar Novo Contrato", "📋 Contratos Cadastrados"])
    
    with tab1:
        st.markdown("### 📝 Cadastro de Novo Contrato")
        
        with st.form("form_novo_contrato"):
            col1, col2 = st.columns(2)
            
            with col1:
                numero = st.text_input(
                    "Número do Contrato *",
                    placeholder="Ex: 001/2025 - RAJ 10.1",
                    help="Número completo do contrato"
                )
                
                tipo = st.selectbox(
                    "Tipo *",
                    ["Serviços", "Fornecimento", "Obras"],
                    help="Tipo de contratação"
                )
                
                fornecedor = st.text_input(
                    "Fornecedor/Contratada *",
                    placeholder="Ex: Empresa XYZ Ltda",
                    help="Nome da empresa contratada"
                )
                
                objeto = st.text_area(
                    "Objeto do Contrato *",
                    placeholder="Ex: Prestação de serviços de limpeza e conservação",
                    help="Descrição do objeto contratual"
                )
                
                valor = st.number_input(
                    "Valor Total (R$) *",
                    min_value=0.0,
                    step=1000.0,
                    format="%.2f",
                    help="Valor total do contrato"
                )
            
            with col2:
                data_inicio = st.date_input(
                    "Data de Início *",
                    help="Data de início da vigência"
                )
                
                data_fim = st.date_input(
                    "Data de Término *",
                    help="Data de término da vigência"
                )
                
                fiscal_titular = st.text_input(
                    "Fiscal Titular *",
                    placeholder="Ex: João Silva Santos",
                    help="Nome do fiscal titular"
                )
                
                fiscal_substituto = st.text_input(
                    "Fiscal Substituto *",
                    placeholder="Ex: Maria Oliveira Costa",
                    help="Nome do fiscal substituto"
                )
                
                status = st.selectbox(
                    "Status *",
                    ["ativo", "atencao", "critico"],
                    help="Status atual do contrato"
                )
            
            st.markdown("### 📎 Upload de Documentos")
            
            arquivo_pdf = st.file_uploader(
                "Contrato Principal em PDF *",
                type=['pdf'],
                help="Faça upload do contrato assinado em PDF",
                key="pdf_principal"
            )
            
            st.markdown("#### 📑 Termos Aditivos (Opcional)")
            st.caption("Contratos podem ter múltiplos aditivos. Faça upload de todos de uma vez ou adicione depois.")
            
            arquivos_aditivos = st.file_uploader(
                "Aditivos em PDF (pode selecionar múltiplos)",
                type=['pdf'],
                accept_multiple_files=True,
                help="Selecione um ou mais arquivos de aditivos contratuais",
                key="pdfs_aditivos"
            )
            
            if arquivos_aditivos:
                st.info(f"📋 **{len(arquivos_aditivos)} aditivo(s) selecionado(s):**")
                for i, aditivo in enumerate(arquivos_aditivos, 1):
                    st.write(f"  {i}. {aditivo.name}")
            
            # Botão de submissão
            submitted = st.form_submit_button(
                "✅ Cadastrar Contrato",
                type="primary",
                use_container_width=True
            )
            
            if submitted:
                # Validações
                if not all([numero, fornecedor, objeto, valor, fiscal_titular, fiscal_substituto, arquivo_pdf]):
                    st.error("⚠️ Preencha todos os campos obrigatórios (*) e faça upload do PDF!")
                elif data_fim <= data_inicio:
                    st.error("⚠️ A data de término deve ser posterior à data de início!")
                else:
                    # Gera ID único
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    contrato_id = f"CTR{timestamp}"
                    
                    # Monta dados do contrato
                    dados_contrato = {
                        "id": contrato_id,
                        "numero": numero,
                        "tipo": tipo,
                        "fornecedor": fornecedor,
                        "objeto": objeto,
                        "vigencia": f"{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}",
                        "valor": float(valor),
                        "status": status,
                        "data_inicio": data_inicio.isoformat(),
                        "data_fim": data_fim.isoformat(),
                        "fiscal_titular": fiscal_titular,
                        "fiscal_substituto": fiscal_substituto,
                        "ultima_atualizacao": datetime.now().isoformat()
                    }
                    
                    # Salva contrato
                    try:
                        salvar_contrato(dados_contrato, arquivo_pdf, arquivos_aditivos)
                        
                        st.success(f"✅ Contrato **{numero}** cadastrado com sucesso!")
                        
                        if arquivos_aditivos and len(arquivos_aditivos) > 0:
                            st.success(f"📑 **{len(arquivos_aditivos)} aditivo(s)** anexado(s) com sucesso!")
                        
                        st.balloons()
                        st.info(f"**ID gerado:** {contrato_id}")
                    except Exception as e:
                        st.error(f"❌ Erro ao salvar contrato: {str(e)}")
    
    with tab2:
        st.markdown("### 📋 Contratos Cadastrados via Upload")
        
        contratos = listar_contratos_cadastrados()
        
        if not contratos:
            st.info("ℹ️ Nenhum contrato cadastrado ainda. Use a aba 'Cadastrar Novo Contrato' para adicionar.")
        else:
            st.success(f"**Total de contratos cadastrados:** {len(contratos)}")
            
            for i, contrato in enumerate(contratos):
                with st.expander(f"📄 {contrato['numero']} - {contrato['fornecedor']}", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**ID:** {contrato['id']}")
                        st.write(f"**Tipo:** {contrato['tipo']}")
                        st.write(f"**Valor:** R$ {contrato['valor']:,.2f}")
                    
                    with col2:
                        st.write(f"**Vigência:** {contrato['vigencia']}")
                        st.write(f"**Status:** {contrato['status']}")
                    
                    with col3:
                        st.write(f"**Fiscal Titular:** {contrato['fiscal_titular']}")
                        st.write(f"**Fiscal Substituto:** {contrato['fiscal_substituto']}")
                    
                    st.write(f"**Objeto:** {contrato['objeto']}")
                    
                    # Exibe PDFs
                    if 'pdf_filename' in contrato:
                        st.write(f"**📄 Contrato Principal:** {contrato['pdf_filename']}")
                    
                    # Exibe aditivos
                    if 'aditivos' in contrato and len(contrato['aditivos']) > 0:
                        st.write(f"**📑 Aditivos ({len(contrato['aditivos'])}):**")
                        for aditivo in contrato['aditivos']:
                            st.write(f"  • Aditivo {aditivo['numero']:02d}: {aditivo.get('nome_original', aditivo['filename'])}")
                    else:
                        st.write("**📑 Aditivos:** Nenhum aditivo cadastrado")


if __name__ == "__main__":
    main()
