from collections import defaultdict
from datetime import datetime


# 1. Constantes de IDs de template
GESTOR_INICIO_VIGENCIA = "GESTOR_INICIO_VIGENCIA"
GESTOR_DESIGNACAO_FISCAIS = "GESTOR_DESIGNACAO_FISCAIS"
GESTOR_REAJUSTE = "GESTOR_REAJUSTE"
GESTOR_ADITAMENTO = "GESTOR_ADITAMENTO"
GESTOR_RESCISAO = "GESTOR_RESCISAO"
DEFAULT_GESTOR = "DEFAULT_GESTOR"

# Fiscal do Contrato
FISCAL_ADVERTENCIA = "FISCAL_ADVERTENCIA"
FISCAL_SOLIC_CORRECAO = "FISCAL_SOLIC_CORRECAO"
FISCAL_SOLIC_DOCUMENTACAO = "FISCAL_SOLIC_DOCUMENTACAO"
FISCAL_COMUNICADO_IRREGULARIDADE = "FISCAL_COMUNICADO_IRREGULARIDADE"
FISCAL_NOTIF_PREVIA_PENALIDADE = "FISCAL_NOTIF_PREVIA_PENALIDADE"
DEFAULT_FISCAL = "DEFAULT_FISCAL"

# 2. Mapa de seleção de template
TEMPLATE_MAP = {
    "Gestor do Contrato": {
        "Notificação de Início de Vigência": GESTOR_INICIO_VIGENCIA,
        "Notificação de Designação de Fiscais": GESTOR_DESIGNACAO_FISCAIS,
        "Notificação de Reajuste Contratual": GESTOR_REAJUSTE,
        "Notificação de Alteração Contratual (Aditamento)": GESTOR_ADITAMENTO,
        "Notificação de Rescisão Contratual": GESTOR_RESCISAO,
    },
    "Fiscal do Contrato": {
        "Advertência": FISCAL_ADVERTENCIA,
        "Solicitação de Correção": FISCAL_SOLIC_CORRECAO,
        "Solicitação de Documentação": FISCAL_SOLIC_DOCUMENTACAO,
        "Comunicado de Irregularidade": FISCAL_COMUNICADO_IRREGULARIDADE,
        "Notificação Prévia de Penalidade": FISCAL_NOTIF_PREVIA_PENALIDADE,
    }
}

# 3. Catálogo de templates
TEMPLATES = {
        # FISCAL: ADVERTÊNCIA
        FISCAL_ADVERTENCIA: '''À {contratada_nome} – CNPJ {contratada_cnpj}
    Endereço: {contratada_endereco}
    Assunto: Advertência / Orientação de ajuste – Contrato nº {contrato_numero}
    {local_data}

    Prezado(a) Senhor(a),

    CONSIDERANDO o Contrato nº {contrato_numero}, cujo objeto é “{contrato_objeto}”;
    CONSIDERANDO a necessidade de assegurar a conformidade da execução contratual e a manutenção do padrão esperado;
    CONSIDERANDO o registro da seguinte ocorrência: {motivo};

    FICA A CONTRATADA ADVERTIDA para que adote as medidas necessárias à imediata correção/adequação da execução, prevenindo reincidências e assegurando o fiel cumprimento das obrigações pactuadas.

    Caso entenda necessário, a CONTRATADA poderá apresentar esclarecimentos no prazo de {prazo_dias_uteis} dias úteis, contados do recebimento.

    {fundamentacao}

    Atenciosamente,
    {assinatura}
    ''',
        # FISCAL: SOLICITAÇÃO DE CORREÇÃO
        FISCAL_SOLIC_CORRECAO: '''À {contratada_nome} – CNPJ {contratada_cnpj}
    Endereço: {contratada_endereco}
    Assunto: Solicitação de correção/adequação – Contrato nº {contrato_numero}
    {local_data}

    Prezado(a) Senhor(a),

    CONSIDERANDO o Contrato nº {contrato_numero}, relativo a “{contrato_objeto}”;
    CONSIDERANDO a obrigação da CONTRATADA de manter a execução regular e conforme especificações/rotinas pactuadas;
    CONSIDERANDO a ocorrência registrada: {motivo};

    DETERMINA-SE que a CONTRATADA promova a correção/adequação do item apontado, com apresentação de evidências de regularização (relatório, fotos, checklist, documentos ou outros meios idôneos), no prazo de {prazo_dias_uteis} dias úteis.

    Se houver impedimento ou necessidade de alinhamento operacional, a CONTRATADA deve informar formalmente, justificando e propondo plano de correção no mesmo prazo.

    {fundamentacao}

    Atenciosamente,
    {assinatura}
    ''',
        # FISCAL: SOLICITAÇÃO DE DOCUMENTAÇÃO
        FISCAL_SOLIC_DOCUMENTACAO: '''À {contratada_nome} – CNPJ {contratada_cnpj}
    Endereço: {contratada_endereco}
    Assunto: Solicitação de documentação – Contrato nº {contrato_numero}
    {local_data}

    Prezado(a) Senhor(a),

    CONSIDERANDO o Contrato nº {contrato_numero} e a necessidade de instrução e controle da fiscalização;
    CONSIDERANDO a exigência de comprovação documental pertinente ao acompanhamento da execução;

    SOLICITA-SE o encaminhamento da seguinte documentação/informação, relacionada ao contrato em referência:
    {motivo}

    O envio deverá ocorrer no prazo de {prazo_dias_uteis} dias úteis, contados do recebimento, preferencialmente por meio do canal formal de comunicação definido pela unidade.

    A ausência de apresentação no prazo poderá ensejar registro de não conformidade e adoção de providências administrativas cabíveis, conforme contrato e normativos aplicáveis.

    {fundamentacao}

    Atenciosamente,
    {assinatura}
    ''',
        # FISCAL: COMUNICADO DE IRREGULARIDADE
        FISCAL_COMUNICADO_IRREGULARIDADE: '''À {contratada_nome} – CNPJ {contratada_cnpj}
    Endereço: {contratada_endereco}
    Assunto: Comunicado de irregularidade / Não conformidade – Contrato nº {contrato_numero}
    {local_data}

    Prezado(a) Senhor(a),

    CONSIDERANDO o Contrato nº {contrato_numero}, cujo objeto é “{contrato_objeto}”;
    CONSIDERANDO o dever de fiscalização e registro de ocorrências durante a execução;
    CONSIDERANDO a constatação da seguinte irregularidade/não conformidade: {motivo};

    COMUNICA-SE à CONTRATADA o registro formal da ocorrência, para ciência e adoção imediata das medidas de regularização.

    A CONTRATADA deverá:

    Regularizar a situação no prazo de {prazo_dias_uteis} dias úteis; e

    Apresentar resposta formal com evidências/justificativas e medidas preventivas para evitar reincidência.

    O não atendimento poderá ensejar escalonamento ao Gestor do Contrato para deliberação sobre medidas administrativas, sem prejuízo de outras providências previstas no contrato.

    {fundamentacao}

    Atenciosamente,
    {assinatura}
    ''',
        # FISCAL: NOTIFICAÇÃO PRÉVIA DE PENALIDADE
        FISCAL_NOTIF_PREVIA_PENALIDADE: '''À {contratada_nome} – CNPJ {contratada_cnpj}
    Endereço: {contratada_endereco}
    Assunto: Notificação prévia de penalidade – Contrato nº {contrato_numero}
    {local_data}

    Prezado(a) Senhor(a),

    CONSIDERANDO o Contrato nº {contrato_numero}, relativo a “{contrato_objeto}”;
    CONSIDERANDO o histórico/registro de ocorrências e/ou descumprimentos: {motivo};
    CONSIDERANDO a necessidade de assegurar contraditório e manifestação prévia antes de eventual encaminhamento para aplicação de sanção;

    NOTIFICA-SE PREVIAMENTE a CONTRATADA para que, no prazo de {prazo_dias_uteis} dias úteis, apresente manifestação formal, com justificativas, documentos e evidências pertinentes, sobre os fatos apontados.

    Findo o prazo, e à vista dos elementos disponíveis, o caso poderá ser encaminhado ao Gestor do Contrato/autoridade competente para avaliação de medidas administrativas e eventuais sanções previstas contratualmente e na legislação aplicável.

    {fundamentacao}

    Atenciosamente,
    {assinatura}
    ''',
        DEFAULT_FISCAL: '''Assunto: Notificação – Contrato nº {contrato_numero}\n{local_data}\n\nPrezado(a),\n\nEsta é uma notificação referente ao contrato informado.\n\nAtenciosamente,\n{assinatura}\n''',
    GESTOR_INICIO_VIGENCIA: '''À {contratada_nome} – CNPJ {contratada_cnpj}
Endereço: {contratada_endereco}
Assunto: Comunicação de início de vigência – Contrato nº {contrato_numero}
{local_data}

CONSIDERANDO o Contrato nº {contrato_numero}, cujo objeto é “{contrato_objeto}”;
CONSIDERANDO a obrigação da CONTRATADA de cumprir integralmente as cláusulas contratuais e assegurar a execução regular dos serviços;
CONSIDERANDO a necessidade de alinhamento operacional e documental para acompanhamento e fiscalização do ajuste;

RESOLVE: NOTIFICAR V.Sa. para que, no prazo de {prazo_dias_uteis} dias úteis, a contar do recebimento, adote as providências iniciais:

Confirmar a data efetiva de início da execução e indicar preposto/responsável técnico, com contatos atualizados;

Encaminhar a documentação inicial e evidências previstas no contrato e rotinas administrativas aplicáveis (quando cabível);

Indicar canal formal para comunicações e recebimento de determinações da fiscalização;

Assegurar o cumprimento dos requisitos de acesso, segurança e mobilização necessários ao início das atividades.

Eventual não atendimento poderá ensejar a adoção das medidas administrativas cabíveis, nos termos do contrato e da legislação aplicável.

Atenciosamente,
{assinatura}
''',
    GESTOR_DESIGNACAO_FISCAIS: '''À {contratada_nome} – CNPJ {contratada_cnpj}
Endereço: {contratada_endereco}
Assunto: Designação de fiscais e canal de interlocução – Contrato nº {contrato_numero}
{local_data}

CONSIDERANDO o Contrato nº {contrato_numero}, relativo a “{contrato_objeto}”;
CONSIDERANDO a necessidade de formalizar interlocução e rotinas de fiscalização e aceite;

RESOLVE: NOTIFICAR que ficam designados para acompanhamento e fiscalização do ajuste:

Gestor do Contrato: {gestor_nome}

Fiscal(is) do Contrato: {fiscais_nomes}

Canal formal para comunicações: {canal_formal}

A CONTRATADA deverá direcionar comunicações formais, justificativas, solicitações e envio de evidências exclusivamente pelos canais acima, observando o rito de aceite/medições previsto no contrato.

Atenciosamente,
{assinatura}
''',
    GESTOR_REAJUSTE: '''À {contratada_nome} – CNPJ {contratada_cnpj}
Endereço: {contratada_endereco}
Assunto: Reajuste contratual – Solicitação de documentos – Contrato nº {contrato_numero}
{local_data}

CONSIDERANDO o Contrato nº {contrato_numero} e as condições pactuadas quanto a reajuste;
CONSIDERANDO a necessidade de instrução completa para análise e decisão administrativa;

RESOLVE: NOTIFICAR a CONTRATADA para que apresente, no prazo de {prazo_dias_uteis} dias úteis, os documentos necessários à análise do pedido de reajuste, incluindo, quando aplicável:

Requerimento formal indicando base contratual, marco temporal e índice/fórmula;

Memória de cálculo e planilhas comparativas (antes/depois);

Documentos comprobatórios do fato gerador, quando exigível;

Declarações e demais elementos previstos no contrato.

{fundamentacao}

O pedido somente será apreciado após a instrução adequada, observados os limites contratuais e normativos.

Atenciosamente,
{assinatura}
''',
    GESTOR_ADITAMENTO: '''À {contratada_nome} – CNPJ {contratada_cnpj}
Endereço: {contratada_endereco}
Assunto: Alteração contratual (aditamento) – Providências – Contrato nº {contrato_numero}
{local_data}

CONSIDERANDO o Contrato nº {contrato_numero}, cujo objeto é “{contrato_objeto}”;
CONSIDERANDO a necessidade de formalização de alteração contratual para: {motivo};

RESOLVE: NOTIFICAR a CONTRATADA para que, no prazo de {prazo_dias_uteis} dias úteis, manifeste-se formalmente e encaminhe os documentos necessários à formalização do aditamento, incluindo, quando aplicável:

Aceite/manifestação expressa;

Proposta atualizada e justificativas técnicas (se houver impacto em valores/quantitativos/prazo);

Cronograma/plano de execução revisado (quando aplicável).

Até a formalização, permanecem vigentes as condições originais, salvo determinação expressa em sentido diverso.

Atenciosamente,
{assinatura}
''',
    GESTOR_RESCISAO: '''À {contratada_nome} – CNPJ {contratada_cnpj}
Endereço: {contratada_endereco}
Assunto: Rescisão contratual – Comunicação de instauração / prazo para manifestação – Contrato nº {contrato_numero}
{local_data}

CONSIDERANDO o Contrato nº {contrato_numero}, relativo a “{contrato_objeto}”;
CONSIDERANDO as ocorrências registradas e/ou descumprimentos relatados: {motivo};
CONSIDERANDO a necessidade de apuração e adoção das medidas administrativas cabíveis, assegurado o contraditório;

RESOLVE: NOTIFICAR a CONTRATADA acerca da instauração de procedimento para apuração de fatos que podem ensejar rescisão, para que apresente manifestação e documentos pertinentes no prazo de {prazo_dias_uteis} dias úteis, contados do recebimento.

O não atendimento poderá implicar deliberação com base nos elementos disponíveis, sem prejuízo de outras medidas previstas contratualmente e na legislação.

Atenciosamente,
{assinatura}
''',
    DEFAULT_GESTOR: '''Assunto: Notificação – Contrato nº {contrato_numero}\n{local_data}\n\nPrezado(a),\n\nEsta é uma notificação referente ao contrato informado.\n\nAtenciosamente,\n{assinatura}\n''',
}

class SafeDict(dict):
    def __missing__(self, key):
        return "(a preencher)"

def pick_template_id(categoria: str, tipo: str) -> str:
    """Seleciona o template_id correto para Gestor ou Fiscal do Contrato."""
    if not categoria or not tipo:
        return None
    cat_map = TEMPLATE_MAP.get(categoria, {})
    if categoria == "Gestor do Contrato":
        return cat_map.get(tipo, DEFAULT_GESTOR)
    elif categoria == "Fiscal do Contrato":
        return cat_map.get(tipo, DEFAULT_FISCAL)
    return None

def build_context(contrato: dict, form_data: dict) -> dict:
    """Extrai dados do contrato e do formulário para preencher o template."""
    ctx = {}
    # Contratada
    ctx["contratada_nome"] = contrato.get("fornecedor", "(a preencher)")
    ctx["contratada_cnpj"] = contrato.get("cnpj", "(a preencher)")
    ctx["contratada_endereco"] = contrato.get("endereco", "(a preencher)")
    # Contrato
    ctx["contrato_numero"] = contrato.get("numero", "(a preencher)")
    ctx["contrato_objeto"] = contrato.get("objeto", "(a preencher)")
    # Gestor/fiscais/canal
    ctx["gestor_nome"] = contrato.get("fiscal_titular", "(a preencher)")
    ctx["fiscais_nomes"] = contrato.get("fiscais", contrato.get("fiscal_substituto", "(a preencher)"))
    ctx["canal_formal"] = contrato.get("canal_formal", "(a preencher)")
    # Formulário
    ctx["prazo_dias_uteis"] = form_data.get("prazo", "(a preencher)")
    ctx["motivo"] = form_data.get("motivo", "(a preencher)")
    ctx["fundamentacao"] = form_data.get("fundamentacao", "")
    # Data e assinatura
    try:
        data = datetime.now()
        ctx["local_data"] = f"São Paulo, {data.day} de {data.strftime('%B')} de {data.year}"
    except Exception:
        ctx["local_data"] = "(a preencher)"
    ctx["assinatura"] = "(Assinatura e identificação do responsável)"
    return ctx

def render_notification_text(template_id: str, ctx: dict) -> str:
    """Renderiza o texto final do template com o contexto fornecido."""
    template = TEMPLATES.get(template_id, TEMPLATES[DEFAULT_GESTOR])
    return template.format_map(SafeDict(ctx))
