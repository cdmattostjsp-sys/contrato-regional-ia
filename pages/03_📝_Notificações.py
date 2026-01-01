"""
Página de Geração de Notificações
==================================
Geração assistida de notificações contratuais por IA.
"""

import streamlit as st
import sys
from services.notificacao_templates import pick_template_id, build_context, render_notification_text
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from ui.styles import apply_tjsp_styles

from services.session_manager import initialize_session_state, reset_notificacao, add_log
# Importa o serviço de histórico
from services.history_service import log_event


from agents.notificacoes.registry import get_template
from components.layout_header import ensure_contrato_context, render_context_bar, render_module_banner


def main():
    st.set_page_config(
        page_title="TJSP - Notificações Contratuais",
        page_icon="📝",
        layout="wide"
    )
    
    apply_tjsp_styles()
    initialize_session_state()
    
    # Seleção interna de contrato
    from components.contrato_selector import render_contrato_selector
    from services.contract_service import get_todos_contratos
    if (
        not st.session_state.get("contrato_selecionado") 
        or st.session_state.get("modo_selecao_contrato")
    ):
        contratos = get_todos_contratos()
        selecionado = render_contrato_selector(
            contratos,
            titulo="Central de Consulta de Contratos",
            help_text="Selecione um contrato para gerar notificações.",
            key_prefix="notificacoes"
        )
        if selecionado:
            st.session_state["contrato_selecionado"] = {"id": selecionado["id"], "numero": selecionado["numero"], "fornecedor": selecionado.get("fornecedor", "")}
            st.session_state["modo_selecao_contrato"] = False
            st.rerun()
        return
    contrato = st.session_state["contrato_selecionado"]
    # Faixa de contrato selecionado + botão trocar
    render_context_bar(contrato, key_prefix="notificacoes")
    

    # Cabeçalho padronizado institucional
    render_module_banner(
        title="Geração de Notificações Contratuais",
        subtitle=f"Contrato: {contrato.get('numero', '(a preencher)')} — {contrato.get('objeto', '(a preencher)')}"
    )

    # Botões de navegação
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🏠 Dashboard", use_container_width=True):
            st.switch_page("Home.py")
    with col2:
        if st.button("📄 Ver Contrato", use_container_width=True):
            st.switch_page("pages/01_📄_Contrato.py")
    with col3:
        if st.button("💬 Copiloto", use_container_width=True):
            st.switch_page("pages/02_💬_Copiloto.py")
    with col4:
        if st.button("📖 Como Proceder", use_container_width=True):
            st.switch_page("pages/04_📖_Como_Proceder.py")

    # --- SELEÇÃO DE PERFIL E TIPO DE NOTIFICAÇÃO ---
    from services.notificacao_templates import TEMPLATE_MAP
    perfil_opcoes = list(TEMPLATE_MAP.keys())
    categoria_notificacao = st.radio(
        "Perfil do Responsável pela Notificação",
        perfil_opcoes,
        horizontal=True,
        key="perfil_notificacao"
    )
    tipo_opcoes = list(TEMPLATE_MAP[categoria_notificacao].keys())
    tipo_notificacao_legivel = st.selectbox(
        "Tipo de Notificação",
        tipo_opcoes,
        key="tipo_notificacao"
    )

    from ui.forms_help import help_motivo, help_prazo, help_fundamentacao
    motivo = st.text_area(
        "Motivo da Notificação",
        placeholder="Ex: Atraso na entrega do serviço entre jan/2025 e mar/2025, com impacto na rotina do setor.",
        help=help_motivo(),
        height=80,
        key="notif_motivo"
    )
    st.caption("Descreva fatos, período e impacto. Evite juízo de valor.")
    prazo = st.number_input(
        "Prazo para Resposta (dias úteis)",
        min_value=1,
        max_value=30,
        value=5,
        help=help_prazo(),
        key="notif_prazo"
    )
    st.caption("O prazo deve ser contado em dias úteis, a partir do recebimento da notificação.")
    fundamentacao = st.text_area(
        "Fundamentação Legal (opcional)",
        placeholder="Ex: Cláusula 7ª do contrato; Lei 14.133/2021, art. 115; IN TJSP nº 12/2025.",
        help=help_fundamentacao(),
        height=80,
        key="notif_fundamentacao"
    )
    st.caption("Exemplos: Cláusula X do contrato; Lei 14.133/2021, art. ...; IN TJSP nº 12/2025.")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🤖 Gerar com IA", type="primary", use_container_width=True):
            if not motivo:
                st.error("⚠️ Por favor, descreva o motivo da notificação.")
            else:
                with st.spinner("Gerando notificação..."):
                    st.session_state.notificacao_campos_ai = {
                        "tipo": tipo_notificacao_legivel,
                        "motivo": motivo,
                        "prazo": prazo,
                        "fundamentacao": fundamentacao,
                        "destinatario": contrato.get("fornecedor", "")
                    }
                    notificacao_gerada = "(Funcionalidade IA em desenvolvimento)"
                    st.session_state.notificacao_buffer = notificacao_gerada
                    # Log de evento de geração de notificação
                    log_event(
                        contrato,
                        event_type="NOTIFICACAO_GERADA",
                        title="Notificação gerada",
                        details=f"{categoria_notificacao} - {tipo_notificacao_legivel} | prazo {prazo} dias úteis",
                        source="Notificações",
                        metadata={
                            "categoria": categoria_notificacao,
                            "tipo": tipo_notificacao_legivel,
                            "prazo": prazo,
                            "fundamentacao": fundamentacao,
                            "tamanho_texto": len(notificacao_gerada) if notificacao_gerada else 0
                        }
                    )
                    add_log("INFO", f"Notificação gerada para contrato {contrato['id']}")
                    st.rerun()
    with col_btn2:
        if st.button("🗑️ Limpar", use_container_width=True):
            reset_notificacao()
            st.rerun()
    

    # Pré-visualização da notificação
    with st.container():
        st.markdown("### Pré-visualização")  # institucional, sem emoji

        # Monta dicionário de campos do formulário
        form_data = {
            "categoria": categoria_notificacao,
            "tipo": tipo_notificacao_legivel,
            "motivo": motivo,
            "prazo": prazo,
            "fundamentacao": fundamentacao,
        }

        template_id = pick_template_id(categoria_notificacao, tipo_notificacao_legivel)
        ctx = build_context(contrato, form_data)
        texto_final = render_notification_text(template_id, ctx)

        preview_height = 720  # ajustar conforme necessário
        with st.container(height=preview_height):
            st.markdown(
                f"""
                <div style="
                    background: #ffffff;
                    padding: 1.2rem 1.2rem;
                    border-radius: 12px;
                    border: 1px solid rgba(0,0,0,.08);
                    box-shadow: 0 2px 10px rgba(0,0,0,.04);
                    white-space: pre-wrap;
                    line-height: 1.45;
                    font-size: 0.98rem;
                ">
                {texto_final}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Botões de ação (mantidos)
        col_act1, col_act2, col_act3 = st.columns(3)
        DOCX_OK = True
        try:
            from services.docx_service import build_notificacao_docx_bytes
        except ModuleNotFoundError:
            DOCX_OK = False
        from datetime import datetime
        with col_act1:
            if DOCX_OK:
                dt = datetime.now()
                file_name = (
                    f"notificacao_{categoria_notificacao}_{tipo_notificacao_legivel}_"
                    f"{contrato.get('numero','sem_numero')}_{dt.strftime('%Y%m%d_%H%M')}.docx"
                ).replace(" ", "_")

                docx_bytes = build_notificacao_docx_bytes(
                    texto=texto_final,
                    titulo=f"Notificação – {tipo_notificacao_legivel}",
                    contrato_numero=str(contrato.get("numero", "")),
                    fornecedor=str(contrato.get("fornecedor", "")),
                    categoria=categoria_notificacao,
                    tipo=tipo_notificacao_legivel,
                    cidade="São Paulo",
                    dt=dt,
                )

                # Log de evento de exportação DOCX
                log_event(
                    contrato,
                    event_type="NOTIFICACAO_EXPORTADA_DOCX",
                    title="DOCX exportado",
                    details="Usuário exportou a notificação em DOCX.",
                    source="Notificações",
                    metadata={
                        "categoria": categoria_notificacao,
                        "tipo": tipo_notificacao_legivel,
                        "prazo": prazo,
                        "tamanho_texto": len(texto_final) if texto_final else 0
                    }
                )

                st.download_button(
                    label="📥 Baixar DOCX",
                    data=docx_bytes,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                    key="btn_baixar_docx_notificacao"
                )
            else:
                st.warning("A funcionalidade de download em DOCX está indisponível. Instale a dependência 'python-docx' para habilitar.")
        with col_act2:
            if st.button("📧 Enviar", use_container_width=True):
                st.info("Funcionalidade em desenvolvimento")
        with col_act3:
            if st.button("✏️ Editar", use_container_width=True):
                st.info("Funcionalidade em desenvolvimento")
def montar_texto_notificacao(modelo: str, contrato: dict, form: dict) -> str:
    """
    Gera o corpo textual da notificação conforme modelo institucional.
    modelo: 'Ofício/Comunicado' ou 'Notificação Extrajudicial'
    contrato: dict com dados do contrato selecionado
    form: dict com campos do formulário preenchidos pelo usuário
    """
    from datetime import datetime
    def get(v, default="(a preencher)"):
        return v if v else default
    def format_data_extenso(dt=None):
        meses = [
            "janeiro", "fevereiro", "março", "abril", "maio", "junho",
            "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
        ]
        dt = dt or datetime.now()
        return f"{dt.day} de {meses[dt.month-1]} de {dt.year}"
    numero = get(contrato.get("numero"))
    objeto = get(contrato.get("objeto"))
    fornecedor = contrato.get("fornecedor")
    cnpj = contrato.get("cnpj", None)
    endereco = contrato.get("endereco", None)
    unidade = contrato.get("unidade", None)
    data_inicio = contrato.get("data_inicio", None)
    if isinstance(data_inicio, datetime):
        data_inicio_fmt = data_inicio.strftime("%d/%m/%Y")
    elif data_inicio:
        data_inicio_fmt = str(data_inicio)
    else:
        data_inicio_fmt = None
    categoria = get(form.get("categoria"))
    tipo = get(form.get("tipo"))
    motivo = get(form.get("motivo"))
    prazo = get(form.get("prazo"))
    fundamentacao = form.get("fundamentacao", None)
    email = form.get("email", None)
    local_data = f"São Paulo, {format_data_extenso()}"
    if modelo == "Ofício/Comunicado":
        cabecalho = f"OFÍCIO/COMUNICADO Nº (a preencher) – {unidade or '(a preencher)'}\n{local_data}\n"
        destinatario = ""
        if fornecedor:
            destinatario = f"À {fornecedor}"
            if cnpj:
                destinatario += f" | CNPJ: {cnpj}"
            if endereco:
                destinatario += f" | Endereço: {endereco}"
            destinatario += "\n"
        assunto = f"Assunto: Notificação referente ao Contrato nº {numero} – {objeto}\n"
        corpo = (
            f"1. Do Objeto da Notificação\n"
            f"{tipo}: {motivo}\n\n"
            f"2. Das Exigências/Providências Necessárias\n"
            f"Solicitamos as providências necessárias no prazo de {prazo} dias úteis, conforme previsto contratualmente."
        )
        if fundamentacao:
            corpo += f"\n\nFundamentação legal: {fundamentacao}"
        corpo += (
            f"\n\n3. Das Consequências\n"
            f"O não atendimento poderá ensejar a aplicação das sanções previstas no contrato e na legislação vigente.\n"
            f"\n4. Do Prazo\n"
            f"O prazo para resposta é de {prazo} dias úteis, contados a partir do recebimento desta comunicação.\n"
        )
        fecho = "Solicitamos posicionamento formal dentro do prazo estabelecido."
        if email:
            fecho += f" Dúvidas podem ser encaminhadas para {email}."
        assinatura = "\n\nAtenciosamente,\n(Assinatura e identificação do responsável)\n"
        return "\n".join([cabecalho, destinatario, assunto, corpo, fecho, assinatura])
    elif modelo == "Notificação Extrajudicial":
        destinatario = f"À {fornecedor or '(a preencher)'}"
        if cnpj:
            destinatario += f" | CNPJ: {cnpj}"
        if endereco:
            destinatario += f" | Endereço: {endereco}"
        destinatario += "\n"
        considerandos = [
            f"CONSIDERANDO o Contrato nº {numero} firmado para {objeto};",
            f"CONSIDERANDO a obrigação da contratada de cumprir integralmente as cláusulas contratuais;",
        ]
        if motivo:
            considerandos.append(f"CONSIDERANDO o seguinte fato: {motivo};")
        if fundamentacao:
            considerandos.append(f"CONSIDERANDO a fundamentação legal: {fundamentacao};")
        considerandos.append("CONSIDERANDO a necessidade de garantir a regularidade da execução contratual;")
        resolve = (
            f"RESOLVE: NOTIFICAR a empresa acima para que, no prazo de {prazo} dias úteis, adote as providências necessárias, sob pena de aplicação das medidas administrativas cabíveis."
        )
        fecho = "O não atendimento poderá ensejar sanções previstas em contrato e legislação."
        assinatura = "\n\nAtenciosamente,\n(Assinatura e identificação do responsável)\n"
        return "\n".join([
            destinatario,
            *considerandos,
            "",
            resolve,
            "",
            fecho,
            assinatura
        ])
    else:
        return "Modelo de notificação não reconhecido."


if __name__ == "__main__":
    main()
