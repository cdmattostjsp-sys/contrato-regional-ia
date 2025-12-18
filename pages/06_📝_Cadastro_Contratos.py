"""
Página de Cadastro de Contratos
================================
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


def salvar_contrato(dados_contrato: dict, arquivo_pdf, arquivos_aditivos=None, dados_aditivos=None):
    """
    Salva contrato no sistema (metadados + PDF + aditivos)
    
    Args:
        dados_contrato: Dicionário com dados do contrato
        arquivo_pdf: Arquivo PDF principal do contrato
        arquivos_aditivos: Lista de arquivos de aditivos (opcional)
        dados_aditivos: Lista de dicionários com dados de cada aditivo (tipo, impactos, etc)
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
            
            # Obtém dados do aditivo (se fornecidos)
            dados_aditivo_item = {}
            if dados_aditivos and i <= len(dados_aditivos):
                dados_aditivo_item = dados_aditivos[i-1]
            
            dados_contrato['aditivos'].append({
                'numero': i,
                'filename': aditivo_filename,
                'path': str(aditivo_path),
                'data_upload': datetime.now().isoformat(),
                'nome_original': aditivo_file.name,
                # Metadados de impacto do aditivo
                'tipo_modificacao': dados_aditivo_item.get('tipo_modificacao', []),
                'data_aditivo': dados_aditivo_item.get('data_aditivo', ''),
                'justificativa': dados_aditivo_item.get('justificativa', ''),
                'prorrogacao_dias': dados_aditivo_item.get('prorrogacao_dias', 0),
                'nova_data_fim': dados_aditivo_item.get('nova_data_fim', ''),
                'percentual_acrescimo': dados_aditivo_item.get('percentual_acrescimo', 0.0),
                'percentual_supressao': dados_aditivo_item.get('percentual_supressao', 0.0),
                'valor_acrescimo': dados_aditivo_item.get('valor_acrescimo', 0.0),
                'valor_supressao': dados_aditivo_item.get('valor_supressao', 0.0),
                'alteracoes_qualitativas': dados_aditivo_item.get('alteracoes_qualitativas', '')
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
        page_title="TJSP - Cadastro de Contratos",
        page_icon="📝",
        layout="wide"
    )
    
    apply_tjsp_styles()
    initialize_session_state()
    
    # Cabeçalho
    st.markdown("""
        <div class="tjsp-header">
            <h1>📝 Cadastro de Contratos</h1>
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
            
            # Container para dados dos aditivos
            dados_aditivos_list = []
            
            if arquivos_aditivos:
                st.info(f"📋 **{len(arquivos_aditivos)} aditivo(s) selecionado(s)** - Informe os dados de cada um:")
                
                for i, aditivo in enumerate(arquivos_aditivos, 1):
                    st.markdown(f"##### Aditivo {i:02d} - {aditivo.name}")
                    
                    with st.container():
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            data_aditivo = st.date_input(
                                f"Data do Aditivo {i}",
                                key=f"data_aditivo_{i}",
                                help="Data de assinatura do aditivo"
                            )
                            
                            tipos_modificacao = st.multiselect(
                                f"Tipo(s) de Modificação {i}",
                                [
                                    "Prorrogação de Prazo",
                                    "Acréscimo de Valor",
                                    "Supressão de Valor",
                                    "Alteração Qualitativa",
                                    "Alteração de Dotação Orçamentária",
                                    "Outros"
                                ],
                                key=f"tipos_mod_{i}",
                                help="Selecione um ou mais tipos de modificação"
                            )
                        
                        with col_b:
                            justificativa = st.text_area(
                                f"Justificativa {i}",
                                key=f"justificativa_{i}",
                                height=100,
                                help="Justificativa legal/técnica para o aditivo"
                            )
                        
                        # Campos condicionais baseados no tipo
                        dados_aditivo = {
                            'data_aditivo': data_aditivo.isoformat() if data_aditivo else '',
                            'tipo_modificacao': tipos_modificacao,
                            'justificativa': justificativa,
                            'prorrogacao_dias': 0,
                            'nova_data_fim': '',
                            'percentual_acrescimo': 0.0,
                            'percentual_supressao': 0.0,
                            'valor_acrescimo': 0.0,
                            'valor_supressao': 0.0,
                            'alteracoes_qualitativas': ''
                        }
                        
                        if "Prorrogação de Prazo" in tipos_modificacao:
                            col_p1, col_p2 = st.columns(2)
                            with col_p1:
                                prorrogacao_dias = st.number_input(
                                    f"Dias de Prorrogação {i}",
                                    min_value=0,
                                    step=1,
                                    key=f"prorrog_{i}"
                                )
                                dados_aditivo['prorrogacao_dias'] = prorrogacao_dias
                            
                            with col_p2:
                                nova_data_fim = st.date_input(
                                    f"Nova Data de Término {i}",
                                    key=f"nova_data_{i}"
                                )
                                dados_aditivo['nova_data_fim'] = nova_data_fim.isoformat() if nova_data_fim else ''
                        
                        if "Acréscimo de Valor" in tipos_modificacao:
                            col_a1, col_a2 = st.columns(2)
                            with col_a1:
                                percentual_acrescimo = st.number_input(
                                    f"Percentual de Acréscimo (%) {i}",
                                    min_value=0.0,
                                    max_value=100.0,
                                    step=0.1,
                                    key=f"perc_acr_{i}"
                                )
                                dados_aditivo['percentual_acrescimo'] = percentual_acrescimo
                            
                            with col_a2:
                                valor_acrescimo = st.number_input(
                                    f"Valor do Acréscimo (R$) {i}",
                                    min_value=0.0,
                                    step=1000.0,
                                    format="%.2f",
                                    key=f"val_acr_{i}"
                                )
                                dados_aditivo['valor_acrescimo'] = float(valor_acrescimo)
                        
                        if "Supressão de Valor" in tipos_modificacao:
                            col_s1, col_s2 = st.columns(2)
                            with col_s1:
                                percentual_supressao = st.number_input(
                                    f"Percentual de Supressão (%) {i}",
                                    min_value=0.0,
                                    max_value=100.0,
                                    step=0.1,
                                    key=f"perc_sup_{i}"
                                )
                                dados_aditivo['percentual_supressao'] = percentual_supressao
                            
                            with col_s2:
                                valor_supressao = st.number_input(
                                    f"Valor da Supressão (R$) {i}",
                                    min_value=0.0,
                                    step=1000.0,
                                    format="%.2f",
                                    key=f"val_sup_{i}"
                                )
                                dados_aditivo['valor_supressao'] = float(valor_supressao)
                        
                        if "Alteração Qualitativa" in tipos_modificacao:
                            alteracoes_qualitativas = st.text_area(
                                f"Descrição das Alterações Qualitativas {i}",
                                key=f"alt_qual_{i}",
                                help="Descreva as alterações nas especificações, escopo, etc."
                            )
                            dados_aditivo['alteracoes_qualitativas'] = alteracoes_qualitativas
                        
                        dados_aditivos_list.append(dados_aditivo)
                        st.markdown("---")
            
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
                        salvar_contrato(dados_contrato, arquivo_pdf, arquivos_aditivos, dados_aditivos_list)
                        
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
                    
                    # Exibe aditivos com detalhes de impacto
                    if 'aditivos' in contrato and len(contrato['aditivos']) > 0:
                        st.write(f"**📑 Aditivos ({len(contrato['aditivos'])}):**")
                        for aditivo in contrato['aditivos']:
                            st.write(f"  • **Aditivo {aditivo['numero']:02d}:** {aditivo.get('nome_original', aditivo['filename'])}")
                            
                            if aditivo.get('tipo_modificacao'):
                                st.write(f"    → Tipo: {', '.join(aditivo['tipo_modificacao'])}")
                            
                            if aditivo.get('data_aditivo'):
                                st.write(f"    → Data: {aditivo['data_aditivo']}")
                            
                            if aditivo.get('prorrogacao_dias', 0) > 0:
                                st.write(f"    → Prorrogação: {aditivo['prorrogacao_dias']} dias (Nova data: {aditivo.get('nova_data_fim', 'N/A')})")
                            
                            if aditivo.get('valor_acrescimo', 0) > 0:
                                st.write(f"    → Acréscimo: R$ {aditivo['valor_acrescimo']:,.2f} ({aditivo.get('percentual_acrescimo', 0):.1f}%)")
                            
                            if aditivo.get('valor_supressao', 0) > 0:
                                st.write(f"    → Supressão: R$ {aditivo['valor_supressao']:,.2f} ({aditivo.get('percentual_supressao', 0):.1f}%)")
                            
                            if aditivo.get('justificativa'):
                                st.write(f"    → Justificativa: {aditivo['justificativa'][:100]}...")
                    else:
                        st.write("**📑 Aditivos:** Nenhum aditivo cadastrado")


if __name__ == "__main__":
    main()
