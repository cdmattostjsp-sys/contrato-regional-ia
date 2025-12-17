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


def salvar_contrato(dados_contrato: dict, arquivo_pdf):
    """
    Salva contrato no sistema (metadados + PDF)
    
    Args:
        dados_contrato: Dicionário com dados do contrato
        arquivo_pdf: Arquivo PDF uploaded
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
    
    # Salva PDF
    if arquivo_pdf:
        pdf_filename = f"{dados_contrato['id']}.pdf"
        pdf_path = contratos_dir / pdf_filename
        
        with open(pdf_path, 'wb') as f:
            f.write(arquivo_pdf.getbuffer())
        
        dados_contrato['pdf_path'] = str(pdf_path)
        dados_contrato['pdf_filename'] = pdf_filename
    
    # Adiciona timestamp
    dados_contrato['data_cadastro'] = datetime.now().isoformat()
    
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
            
            st.markdown("### 📎 Upload de Documento")
            
            arquivo_pdf = st.file_uploader(
                "Contrato em PDF *",
                type=['pdf'],
                help="Faça upload do contrato assinado em PDF"
            )
            
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
                        salvar_contrato(dados_contrato, arquivo_pdf)
                        st.success(f"✅ Contrato **{numero}** cadastrado com sucesso!")
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
                    
                    if 'pdf_filename' in contrato:
                        st.write(f"**PDF:** {contrato['pdf_filename']}")


if __name__ == "__main__":
    main()
