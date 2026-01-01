"""
Helper de microtextos institucionais para formulários do app.
Padroniza tooltips, exemplos e orientações para campos de entrada.
"""

def help_motivo():
    return (
        "Descreva fatos, período e impacto relacionados ao evento. Evite juízo de valor."
    )

def help_fundamentacao():
    return (
        "Exemplos: Cláusula X do contrato; Lei 14.133/2021, art. ...; IN TJSP nº 12/2025. "
        "Informe a base legal ou contratual, se aplicável."
    )

def help_prazo():
    return (
        "Informe o prazo em dias úteis. O prazo deve ser contado a partir do recebimento da notificação, excluindo finais de semana e feriados."
    )

def help_busca_contrato():
    return (
        "Digite número, objeto ou fornecedor para localizar o contrato desejado."
    )

def help_pergunta_ia():
    return (
        "Descreva sua dúvida de forma clara e objetiva. Inclua contexto relevante para obter resposta precisa."
    )

def help_filtro_home():
    return (
        "Utilize os filtros para refinar a busca por contratos, notificações ou documentos."
    )
