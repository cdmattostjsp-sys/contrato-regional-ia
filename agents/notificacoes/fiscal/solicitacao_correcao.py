def get_template():
    return {
        "perfil": "fiscal",
        "tipo_notificacao": "solicitacao_correcao",
        "titulo": "Solicitação de Correção de Irregularidade",
        "corpo": (
            "No exercício da fiscalização contratual, foi constatada irregularidade na execução do objeto contratado. "
            "Solicita-se a imediata correção da(s) não conformidade(s) abaixo descrita(s), no prazo estabelecido, sob pena de adoção das providências previstas em contrato e legislação vigente.\n\n"
            "Descrição fática: {descricao_fatica}\n"
            "Prazo para correção: {prazo}"
        ),
        "campos_variaveis": [
            "descricao_fatica",
            "prazo",
            "contrato",
            "contratada"
        ],
        "fundamentacao_legal_padrao": [
            "Lei nº 14.133/2021, art. 117, §1º",
            "IN TJSP nº 012/2025, art. 29"
        ],
        "fundamentacao_contratual_placeholder": "Cláusula(s) contratual(is) relacionada(s) aos fatos descritos",
        "observacoes": "O não atendimento à solicitação poderá ensejar sanções administrativas."
    }
