"""
Página de Visualização de Contrato
===================================
Exibe detalhes completos de um contrato selecionado.
"""

import streamlit as st
import sys
from pathlib import Path
import textwrap

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


def render_bloco_pagamentos(contrato: dict):
    """
    BLOCO DE ATESTES E PAGAMENTOS
    ==============================
    Feedback RAJ 10: Indicador simples de atestes e pagamentos.
    Objetivo: Permitir visualização rápida do status de pagamentos
    sem detalhamento financeiro complexo.
    """
    pagamentos = contrato.get("pagamentos_resumo", {
        "total_previstos": 12,
        "total_realizados": 9,
        "status": "em_dia",
        "forma_pagamento": "medicao"
    })
    total_previstos = pagamentos.get("total_previstos", 12)
    total_realizados = pagamentos.get("total_realizados", 9)
    status = pagamentos.get("status", "em_dia")
    forma_pagamento = pagamentos.get("forma_pagamento", "medicao")

    # Obtém informação de ISS (mesma fonte da seção Tributação)
    tributacao = contrato.get("tributacao", {})
    retem_iss = tributacao.get("retem_iss", False)
    aliquota_iss = tributacao.get("aliquota_iss", 5.0)

    badge_iss_aliquota = f'''
    <div style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 2.5rem; margin-bottom: 0.5rem;">
        <div style="display: flex; flex-direction: column; align-items: center;">
            <span style="font-size: 1rem; color: #003366; font-weight: 600; margin-bottom: 0.2rem;">Retenção de ISS</span>
            <span style="background: {'#28A745' if retem_iss else '#6C757D'}; color: white; padding: 0.4rem 1.2rem; border-radius: 16px; font-size: 1.1rem; font-weight: 700; box-shadow: 0 2px 8px {'#28a74522' if retem_iss else '#6c757d22'}; letter-spacing: 1px;">{'🟢 SIM' if retem_iss else '⚪ NÃO'}</span>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center;">
            <span style="font-size: 1rem; color: #003366; font-weight: 600; margin-bottom: 0.2rem;">Alíquota de ISS</span>
            <span style="background: #007bff; color: white; padding: 0.4rem 1.2rem; border-radius: 16px; font-size: 1.1rem; font-weight: 700; box-shadow: 0 2px 8px #007bff22; letter-spacing: 1px;">{aliquota_iss:.2f}%</span>
        </div>
    </div>
    '''
    st.markdown(badge_iss_aliquota, unsafe_allow_html=True)

    # Renderização do bloco de status de pagamentos
    html_status = textwrap.dedent(f"""
    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; align-items: center;">
      <div>
        <p style="margin: 0 0 0.5rem 0; font-size: 1rem; color: #495057;">
          <strong>Status:</strong>
          <span style="color: #28A745; font-weight: 600;">✅ Pagamentos em Dia</span>
        </p>
        <p style="margin: 0; font-size: 0.95rem; color: #6C757D;">
          {total_realizados} pagamentos realizados de {total_previstos} previstos
        </p>
      </div>
      <div style="text-align: center;">
        <div style="background: white; padding: 1rem; border-radius: 8px; border: 2px solid #28A745;">
          <p style="margin: 0; font-size: 2rem; font-weight: bold; color: #28A745;">{total_realizados}/{total_previstos}</p>
          <p style="margin: 0.3rem 0 0 0; font-size: 0.85rem; color: #6C757D;">Pagamentos</p>
        </div>
      </div>
    </div>
    """).strip()
    st.markdown(html_status, unsafe_allow_html=True)

    # Submenu expansível - Forma de Pagamento
    with st.expander("📋 **Detalhes da Forma de Pagamento**"):
        st.markdown("### Forma de Pagamento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if forma_pagamento == "integral":
                st.markdown("""
                    <div style="background: #E3F2FD; padding: 1rem; border-radius: 8px; border-left: 4px solid #2196F3;">
                        <p style="margin: 0; font-weight: 600; color: #1976D2;">
                            ✓ Pagamento Integral
                        </p>
                        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #555;">
                            Pagamento realizado em parcelas fixas, independente de medição.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="background: #F5F5F5; padding: 1rem; border-radius: 8px; opacity: 0.7;">
                        <p style="margin: 0; color: #666;">
                            ○ Pagamento Integral
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if forma_pagamento == "medicao":
                st.markdown("""
                    <div style="background: #E8F5E9; padding: 1rem; border-radius: 8px; border-left: 4px solid #4CAF50;">
                        <p style="margin: 0; font-weight: 600; color: #2E7D32;">
                            ✓ Pagamento Atrelado à Medição
                        </p>
                        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #555;">
                            Pagamento vinculado à medição e atestação dos serviços executados.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="background: #F5F5F5; padding: 1rem; border-radius: 8px; opacity: 0.7;">
                        <p style="margin: 0; color: #666;">
                            ○ Pagamento Atrelado à Medição
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        
        st.info("💡 **Observação:** Dados de atestes e pagamentos são indicativos. Para informações financeiras detalhadas, consulte o SGF.")
    
    # Lista detalhada de pagamentos
    with st.expander("📄 **Histórico Detalhado de Atestes**"):
        st.markdown("### Registros de Ateste e Pagamento")
        
        # Dados mockados de pagamentos individuais (preparado para integração)
        itens_pagamento = contrato.get("itens_pagamento", [
            {"competencia": "Nov/2024", "nota_fiscal": "NF-12345", "valor": 15000.00, "status": "atestado", "data_ateste": "05/12/2024"},
            {"competencia": "Out/2024", "nota_fiscal": "NF-12344", "valor": 15000.00, "status": "atestado", "data_ateste": "05/11/2024"},
            {"competencia": "Set/2024", "nota_fiscal": "NF-12343", "valor": 15000.00, "status": "atestado", "data_ateste": "05/10/2024"},
            {"competencia": "Ago/2024", "nota_fiscal": "NF-12342", "valor": 15000.00, "status": "atestado", "data_ateste": "05/09/2024"},
            {"competencia": "Jul/2024", "nota_fiscal": "NF-12341", "valor": 15000.00, "status": "atestado", "data_ateste": "05/08/2024"},
            {"competencia": "Jun/2024", "nota_fiscal": "NF-12340", "valor": 15000.00, "status": "atestado", "data_ateste": "05/07/2024"},
            {"competencia": "Mai/2024", "nota_fiscal": "NF-12339", "valor": 15000.00, "status": "atestado", "data_ateste": "05/06/2024"},
            {"competencia": "Abr/2024", "nota_fiscal": "NF-12338", "valor": 15000.00, "status": "atestado", "data_ateste": "05/05/2024"},
            {"competencia": "Mar/2024", "nota_fiscal": "NF-12337", "valor": 15000.00, "status": "atestado", "data_ateste": "05/04/2024"},
            {"competencia": "Fev/2024", "nota_fiscal": "Pendente", "valor": 15000.00, "status": "pendente", "data_ateste": None},
            {"competencia": "Jan/2024", "nota_fiscal": "Pendente", "valor": 15000.00, "status": "pendente", "data_ateste": None},
            {"competencia": "Dez/2023", "nota_fiscal": "Pendente", "valor": 15000.00, "status": "pendente", "data_ateste": None},
        ])
        
        # Renderiza cada item de pagamento
        for idx, item in enumerate(itens_pagamento, 1):
            competencia = item.get("competencia", "N/A")
            nota_fiscal = item.get("nota_fiscal", "N/A")
            valor = item.get("valor", 0.0)
            status_item = item.get("status", "pendente")
            data_ateste = item.get("data_ateste")
            
            # Define cor e ícone por status
            if status_item == "atestado":
                cor_status = "#28A745"
                icone_status = "✅"
                texto_status = "Atestado"
            else:
                cor_status = "#FFC107"
                icone_status = "⏳"
                texto_status = "Pendente"
            
            # Card do item com data do ateste (se houver)
            data_ateste_html = f"<div style='color: #00796B; font-size: 0.85rem; margin-top: 0.2rem;'><strong>Data do Ateste:</strong> {data_ateste}</div>" if data_ateste else ""
            st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 8px; 
                            margin-bottom: 0.8rem; border-left: 3px solid {cor_status};">
                    <div style="display: grid; grid-template-columns: auto 1fr auto auto; gap: 1rem; align-items: center;">
                        <div style="font-weight: bold; color: #003366;">
                            {competencia}
                        </div>
                        <div style="color: #495057;">
                            <strong>NF:</strong> {nota_fiscal}
                        </div>
                        <div style="color: #495057;">
                            <strong>R$ {valor:,.2f}</strong>
                        </div>
                        <div>
                            <span style="background: {cor_status}; color: white; padding: 0.3rem 0.8rem;
                                        border-radius: 15px; font-size: 0.8rem; font-weight: bold;">
                                {icone_status} {texto_status}
                            </span>
                        </div>
                    </div>
                    {data_ateste_html}
                </div>
            """, unsafe_allow_html=True)
            
            # Informação secundária - Data do Ateste
            if status_item == "atestado" and data_ateste:
                st.caption(f"📅 Data do ateste: **{data_ateste}** • Previsão de pagamento: até 30 dias após o ateste")
            else:
                st.caption(f"📅 Data do ateste: **aguardando realização**")
            
            # Espaçamento entre itens
            if idx < len(itens_pagamento):
                st.markdown("<br>", unsafe_allow_html=True)
        
        st.info("💡 **Informação para fornecedores:** O prazo de pagamento é de até 30 dias após o ateste da Nota Fiscal pelo fiscal titular.")


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


def render_bloco_aditivos(contrato: dict):
    """
    BLOCO DE ADITIVOS CONTRATUAIS
    ==============================
    Exibe timeline de aditivos com impactos consolidados.
    Mostra evolução do contrato com prorrogações, acréscimos/supressões e alterações qualitativas.
    """
    st.markdown("""
        <h3 style="color: #003366; margin: 0 0 1rem 0;">
            📑 HISTÓRICO DE ADITIVOS CONTRATUAIS
        </h3>
    """, unsafe_allow_html=True)
    
    # Verifica se contrato foi consolidado
    if not contrato.get('consolidado_com_aditivos', False):
        st.info("Este contrato não possui aditivos cadastrados.")
        return
    
    # Mostra resumo de impacto
    total_aditivos = contrato.get('total_aditivos_aplicados', 0)
    valor_original = contrato.get('valor_original', 0.0)
    valor_atual = contrato.get('valor', 0.0)
    data_fim_original = contrato.get('data_fim_original')
    data_fim_atual = contrato.get('data_fim')
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;">
            <h4 style="margin: 0 0 1rem 0; color: #003366;">📊 RESUMO DE IMPACTOS</h4>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;">
                <div>
                    <p style="margin: 0; font-size: 0.9rem; color: #666;">Total de Aditivos</p>
                    <p style="margin: 0.3rem 0 0 0; font-size: 1.5rem; font-weight: bold; color: #003366;">
                        {total_aditivos}
                    </p>
                </div>
                <div>
                    <p style="margin: 0; font-size: 0.9rem; color: #666;">Valor do Contrato</p>
                    <p style="margin: 0.3rem 0 0 0; font-size: 1.1rem; font-weight: bold, color: #003366;">
                        R$ {valor_original:,.2f} → R$ {valor_atual:,.2f}
                    </p>
                    <p style="margin: 0.2rem 0 0 0; font-size: 0.85rem; color: {'#28A745' if valor_atual >= valor_original else '#DC3545'};">
                        {'▲' if valor_atual > valor_original else ('▼' if valor_atual < valor_original else '=')} 
                        {abs(((valor_atual - valor_original) / valor_original * 100) if valor_original > 0 else 0):.1f}%
                    </p>
                </div>
                <div>
                    <p style="margin: 0; font-size: 0.9rem; color: #666;">Vigência</p>
                    <p style="margin: 0.3rem 0 0 0; font-size: 0.95rem; font-weight: bold; color: #003366;">
                        {data_fim_original.strftime('%d/%m/%Y') if data_fim_original else 'N/A'}
                    </p>
                    <p style="margin: 0.2rem 0 0 0; font-size: 0.95rem; font-weight: bold; color: #FFC107;">
                        ↓ {data_fim_atual.strftime('%d/%m/%Y') if data_fim_atual else 'N/A'}
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Timeline de aditivos
    st.markdown("### 📅 Timeline de Modificações")
    
    historico = contrato.get('historico_aditivos', [])
    
    if not historico:
        st.info("Nenhuma modificação registrada ainda.")
        return
    
    for item in historico:
        # Define cor baseada nos tipos
        tipos = item.get('tipos', [])
        if 'Prorrogação de Prazo' in tipos:
            cor_border = "#FFC107"
            icone = "⏰"
        elif 'Acréscimo de Valor' in tipos:
            cor_border = "#28A745"
            icone = "💰"
        elif 'Supressão de Valor' in tipos:
            cor_border = "#DC3545"
            icone = "💸"
        else:
            cor_border = "#6C757D"
            icone = "📝"
        
        st.markdown(f"""
            <div style="background: white; border-left: 5px solid {cor_border}; 
                        padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; 
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h4 style="margin: 0; color: #003366;">
                        {icone} ADITIVO Nº {item.get('numero', 'N/A'):02d}
                    </h4>
                    <span style="background: {cor_border}; color: white; padding: 0.3rem 0.8rem; 
                                border-radius: 15px; font-size: 0.85rem; font-weight: bold;">
                        {item.get('data', 'Sem data')}
                    </span>
                </div>
                <div style="margin-bottom: 1rem;">
                    <p style="margin: 0; font-size: 0.9rem; color: #666;">Tipo(s) de Modificação:</p>
                    <p style="margin: 0.3rem 0 0 0; font-weight: 600; color: #003366;">
                        {', '.join(tipos) if tipos else 'Não especificado'}
                    </p>
                </div>
        """, unsafe_allow_html=True)
        
        # Lista alterações
        alteracoes = item.get('alteracoes', [])
        if alteracoes:
            st.markdown('<div style="margin-top: 1rem;"><strong>Alterações Aplicadas:</strong></div>', unsafe_allow_html=True)
            for alt in alteracoes:
                tipo_alt = alt.get('tipo', '')
                descricao = alt.get('descricao', '')
                
                if tipo_alt == 'Prorrogação de Prazo':
                    nova_data = alt.get('nova_data_fim', '')
                    st.markdown(f"""
                        <div style="background: #FFF3CD; padding: 0.8rem; border-radius: 5px; margin: 0.5rem 0;">
                            <p style="margin: 0; color: #856404;">
                                ⏰ <strong>{descricao}</strong><br>
                                Nova data de término: <strong>{nova_data}</strong>
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                
                elif tipo_alt == 'Acréscimo de Valor':
                    valor = alt.get('valor', 0.0)
                    novo_total = alt.get('novo_valor_total', 0.0)
                    st.markdown(f"""
                        <div style="background: #D4EDDA; padding: 0.8rem; border-radius: 5px; margin: 0.5rem 0;">
                            <p style="margin: 0; color: #155724;">
                                💰 <strong>{descricao}</strong><br>
                                Valor acrescido: <strong>R$ {valor:,.2f}</strong><br>
                                Novo valor total: <strong>R$ {novo_total:,.2f}</strong>
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                
                elif tipo_alt == 'Supressão de Valor':
                    valor = alt.get('valor', 0.0)
                    novo_total = alt.get('novo_valor_total', 0.0)
                    st.markdown(f"""
                        <div style="background: #F8D7DA; padding: 0.8rem; border-radius: 5px; margin: 0.5rem 0;">
                            <p style="margin: 0; color: #721C24;">
                                💸 <strong>{descricao}</strong><br>
                                Valor suprimido: <strong>R$ {abs(valor):,.2f}</strong><br>
                                Novo valor total: <strong>R$ {novo_total:,.2f}</strong>
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                
                elif tipo_alt == 'Alteração Qualitativa':
                    st.markdown(f"""
                        <div style="background: #E7F3FF; padding: 0.8rem; border-radius: 5px; margin: 0.5rem 0;">
                            <p style="margin: 0; color: #004085;">
                                📝 <strong>Alteração Qualitativa</strong><br>
                                {descricao}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
        
        # Justificativa
        justificativa = item.get('justificativa', '')
        if justificativa:
            st.markdown(f"""
                <div style="margin-top: 1rem; padding: 0.8rem; background: #F8F9FA; 
                            border-radius: 5px; border-left: 3px solid #6C757D;">
                    <p style="margin: 0; font-size: 0.85rem; color: #666;">Justificativa:</p>
                    <p style="margin: 0.3rem 0 0 0; color: #212529;">{justificativa}</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Link para PDFs dos aditivos
    aditivos_pdfs = contrato.get('aditivos', [])
    if aditivos_pdfs:
        st.markdown("---")
        st.markdown("### 📎 Documentos dos Aditivos")
        
        for aditivo in aditivos_pdfs:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📄 **Aditivo {aditivo.get('numero', 0):02d}:** {aditivo.get('nome_original', aditivo.get('filename', 'N/A'))}")
            with col2:
                if st.button(f"📥 Baixar", key=f"download_aditivo_{aditivo.get('numero', 0)}"):
                    st.info("Funcionalidade de download em desenvolvimento")
    
    # Botão para adicionar novo aditivo
    st.markdown("---")
    
    # Verifica se é um contrato cadastrado (não mock)
    contrato_id = contrato.get('id', '')
    eh_contrato_cadastrado = contrato_id.startswith('PNCP_') or 'pdf_path' in contrato
    
    if eh_contrato_cadastrado:
        with st.expander("➕ **Adicionar Novo Aditivo**", expanded=False):
            render_formulario_aditivo(contrato)
    else:
        st.info("💡 Para adicionar aditivos, utilize a página **📂 Gestão de Contratos** para cadastrar contratos completos.")


def render_formulario_aditivo(contrato: dict):
    """
    Renderiza formulário para adicionar novo aditivo a contrato existente
    """
    from services.contract_service import adicionar_aditivo_contrato
    from datetime import date
    
    st.markdown("""
        <p style="color: #666; margin-bottom: 1rem;">
        Preencha os dados do novo aditivo contratual e faça upload do PDF.
        O contrato será automaticamente atualizado com as modificações.
        </p>
    """, unsafe_allow_html=True)
    
    with st.form("form_novo_aditivo", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            arquivo_aditivo = st.file_uploader(
                "Documento PDF do Aditivo *",
                type=['pdf'],
                help="Faça upload do termo aditivo assinado",
                key="upload_aditivo"
            )
            
            data_aditivo = st.date_input(
                "Data do Aditivo *",
                help="Data de assinatura do aditivo",
                key="data_novo_aditivo"
            )
            
            tipos_modificacao = st.multiselect(
                "Tipo(s) de Modificação *",
                [
                    "Prorrogação de Prazo",
                    "Acréscimo de Valor",
                    "Supressão de Valor",
                    "Alteração Qualitativa",
                    "Alteração de Dotação Orçamentária",
                    "Outros"
                ],
                help="Selecione um ou mais tipos de modificação",
                key="tipos_mod_novo"
            )
        
        with col2:
            justificativa = st.text_area(
                "Justificativa *",
                height=150,
                help="Justificativa legal/técnica para o aditivo",
                key="justificativa_novo"
            )
        
        # Campos condicionais baseados no tipo
        dados_aditivo = {
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
            st.markdown("#### ⏰ Dados da Prorrogação")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                prorrogacao_dias = st.number_input(
                    "Dias de Prorrogação",
                    min_value=0,
                    step=1,
                    key="prorrog_novo"
                )
                dados_aditivo['prorrogacao_dias'] = prorrogacao_dias
            
            with col_p2:
                nova_data_fim = st.date_input(
                    "Nova Data de Término",
                    key="nova_data_novo"
                )
                dados_aditivo['nova_data_fim'] = nova_data_fim.isoformat() if nova_data_fim else ''
        
        if "Acréscimo de Valor" in tipos_modificacao:
            st.markdown("#### 💰 Dados do Acréscimo")
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                percentual_acrescimo = st.number_input(
                    "Percentual de Acréscimo (%)",
                    min_value=0.0,
                    max_value=100.0,
                    step=0.1,
                    key="perc_acr_novo"
                )
                dados_aditivo['percentual_acrescimo'] = percentual_acrescimo
            
            with col_a2:
                valor_acrescimo = st.number_input(
                    "Valor do Acréscimo (R$)",
                    min_value=0.0,
                    step=1000.0,
                    format="%.2f",
                    key="val_acr_novo"
                )
                dados_aditivo['valor_acrescimo'] = float(valor_acrescimo)
        
        if "Supressão de Valor" in tipos_modificacao:
            st.markdown("#### 💸 Dados da Supressão")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                percentual_supressao = st.number_input(
                    "Percentual de Supressão (%)",
                    min_value=0.0,
                    max_value=100.0,
                    step=0.1,
                    key="perc_sup_novo"
                )
                dados_aditivo['percentual_supressao'] = percentual_supressao
            
            with col_s2:
                valor_supressao = st.number_input(
                    "Valor da Supressão (R$)",
                    min_value=0.0,
                    step=1000.0,
                    format="%.2f",
                    key="val_sup_novo"
                )
                dados_aditivo['valor_supressao'] = float(valor_supressao)
        
        if "Alteração Qualitativa" in tipos_modificacao:
            st.markdown("#### 📝 Alterações Qualitivas")
            alteracoes_qualitativas = st.text_area(
                "Descreva as alterações qualitativas",
                height=100,
                key="alt_qual_novo"
            )
            dados_aditivo['alteracoes_qualitativas'] = alteracoes_qualitativas
        
        # Adiciona data do aditivo
        if data_aditivo:
            dados_aditivo['data_aditivo'] = data_aditivo.isoformat()
        
        # Botões
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            submitted = st.form_submit_button("✅ Salvar Aditivo", use_container_width=True, type="primary")
        
        with col_btn2:
            cancelado = st.form_submit_button("❌ Cancelar", use_container_width=True)
        
        if submitted:
            # Validações
            if not arquivo_aditivo:
                st.error("❌ É necessário fazer upload do PDF do aditivo!")
                return
            
            if not tipos_modificacao:
                st.error("❌ Selecione pelo menos um tipo de modificação!")
                return
            
            if not justificativa or not justificativa.strip():
                st.error("❌ A justificativa é obrigatória!")
                return
            
            # Salva aditivo
            with st.spinner("Salvando aditivo..."):
                sucesso = adicionar_aditivo_contrato(
                    contrato['id'],
                    arquivo_aditivo,
                    dados_aditivo
                )
            
            if sucesso:
                st.success("✅ Aditivo adicionado com sucesso!")
                st.info("🔄 Recarregando contrato para exibir atualização...")
                st.rerun()
            else:
                st.error("❌ Erro ao salvar aditivo. Tente novamente.")
        
        if cancelado:
            st.info("Operação cancelada.")


def render_acoes_documentos(contrato: dict):
    """
    AÇÕES RÁPIDAS DE DOCUMENTOS
    ============================
    Feedback RAJ 10: Botão fixo "Gerar Documento" com opções padronizadas.
    O conteúdo é gerado pelo copilot baseado no contrato.
    """
    icon = "📄"
    st.markdown("""
        <h3 style="color: #003366; margin: 1.5rem 0 1rem 0;">
            📄 AÇÕES RÁPIDAS - DOCUMENTOS
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #003366 0%, #0066CC 100%); 
                        padding: 2rem; border-radius: 10px; margin-bottom: 1rem; color: white;">
                <h1>{icon} {contrato['numero']}</h1>
                <p style="font-size: 1.2rem; margin: 0.5rem 0;">{contrato['objeto']}</p>
                <p style="opacity: 0.9;"><strong>Fornecedor:</strong> {contrato['fornecedor']}</p>
            </div>
        """, unsafe_allow_html=True)


    with col2:
        if st.button("Abrir Relatório do Fiscal", use_container_width=True, key="relatorio_fiscal_btn_funcional_aba_contrato"):
            st.info("🤖 Recurso em desenvolvimento. O copiloto gerará o relatório baseado nos dados do contrato.")

    with col3:
        if st.button("Abrir Relatório Final ao Gestor", use_container_width=True, key="relatorio_final_btn_funcional_aba_contrato"):
            st.info("🤖 Recurso em desenvolvimento. O copiloto gerará o relatório final consolidado.")


def render_contrato_detalhes(contrato: dict):
    """
    Renderiza detalhes do contrato em tabs
    =======================================
    EVOLUÇÃO RAJ 10: Reorganizado com nova aba "Apoio ao Gestor" e dados consolidados.
    """
    
    from services.execution_financial_service import (
        listar_por_contrato, criar_registro, filtrar, atualizar_status
    )
    import pandas as pd


def render_bloco_dados_gerais(contrato: dict):
    st.markdown("### 🔘 Ações rápidas")

    c1, c2, c3, c4 = st.columns(4)
    kid = str(contrato.get("id", contrato.get("numero", "sem_id")))

    with c1:
        if st.button("🏠 Dashboard", width="stretch", key=f"btn_dash_{kid}"):
            st.switch_page("Home.py")

    with c2:
        if st.button("💬 Copiloto", width="stretch", key=f"btn_cop_{kid}"):
            st.switch_page("pages/02_💬_Copiloto.py")

    with c3:
        if st.button("📝 Notificar", width="stretch", key=f"btn_notif_{kid}"):
            st.session_state["contrato_selecionado"] = {"id": contrato.get("id"), "numero": contrato.get("numero")}
            st.switch_page("pages/03_📝_Notificações.py")

    with c4:
        if st.button("📖 Como Proceder", width="stretch", key=f"btn_como_{kid}"):
            st.switch_page("pages/04_📖_Como_Proceder.py")

    st.markdown("---")
    st.markdown("### 📌 Resumo do Contrato")
    st.write(f"**Número:** {contrato.get('numero','')}")
    st.write(f"**Objeto:** {contrato.get('objeto','')}")
    st.write(f"**Fornecedor:** {contrato.get('fornecedor','')}")
    st.write(f"**Unidade/RAJ:** {contrato.get('unidade','')}")
    st.write(f"**Status:** {contrato.get('status','')}")
    st.write(f"**Vigência:** {contrato.get('vigencia','')}")
    st.markdown("### ⚠️ Pendências")
    st.info("Nenhuma pendência registrada.")

def render_bloco_apoio_gestor(contrato: dict):
    st.markdown("""
        <div style=\"background: #FFF3CD; border-left: 4px solid #FFC107; padding: 1rem;\"
            border-radius: 5px; margin-bottom: 1.5rem;\">
            <h3 style=\"color: #856404; margin: 0 0 0.5rem 0;\">
                👔 APOIO AO GESTOR - SUPORTE NORMATIVO
            </h3>
            <p style=\"color: #856404; margin: 0; font-size: 0.9rem;\">
                ⚠️ Informações orientativas baseadas em legislação e cláusulas contratuais.<br>
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
    if st.button("💬 Abrir Copiloto para Consulta Normativa", width="stretch", type="primary"):
        st.session_state.copilot_contexto = "normativo"
        st.switch_page("pages/02_💬_Copiloto.py")

def render_bloco_documentos(contrato: dict):
    st.info("Conteúdo de Documentos em desenvolvimento.")

def render_bloco_historico(contrato: dict):
    st.info("Conteúdo de Histórico em desenvolvimento.")

def render_bloco_execucao_fisico_financeira(contrato: dict):
    st.info("Conteúdo de Execução Físico-Financeira em desenvolvimento.")


def main():
    st.set_page_config(
        page_title="TJSP - Detalhes do Contrato",
        page_icon="📄",
        layout="wide"
    )
    apply_tjsp_styles()
    initialize_session_state()

    # Verifica se há contrato selecionado
    if not st.session_state.get("contrato_selecionado"):
        st.warning("⚠️ Nenhum contrato selecionado. Retorne ao dashboard.")
        if st.button("🏠 Voltar ao Dashboard"):
            st.switch_page("Home.py")
        return

    contrato = get_contrato_detalhes(st.session_state.contrato_selecionado["id"])
    if not contrato:
        st.error("❌ Erro ao carregar detalhes do contrato.")
        return

    render_contrato_header(contrato)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📋 Dados Gerais", 
        "💰 Pagamentos & ISS",
        "📑 Aditivos",
        "👔 Apoio ao Gestor",
        "📁 Documentos", 
        "📊 Histórico",
        "🧾 Execução Físico-Financeira"
    ])

    with tab1:
        render_bloco_dados_gerais(contrato)
    with tab2:
        render_bloco_pagamentos(contrato)
        render_bloco_iss(contrato)
    with tab3:
        render_bloco_aditivos(contrato)
    with tab4:
        render_bloco_apoio_gestor(contrato)
    with tab5:
        render_bloco_documentos(contrato)
    with tab6:
        render_bloco_historico(contrato)
    with tab7:
        render_bloco_execucao_fisico_financeira(contrato)


if __name__ == "__main__":
    main()
