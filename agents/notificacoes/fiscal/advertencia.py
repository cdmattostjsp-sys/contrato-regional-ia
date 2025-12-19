def get_template():
    return {
        "perfil": "fiscal",
        "tipo_notificacao": "advertencia",
        "titulo": "Advertência Contratual",
        "corpo": (
            "Considerando o acompanhamento da execução contratual, comunicamos a ocorrência de situação que configura descumprimento das obrigações assumidas pela contratada. "
            "Diante do exposto, formaliza-se a presente ADVERTÊNCIA, com vistas à imediata regularização dos fatos descritos, sob pena de adoção das medidas cabíveis.\n\n"
            "Descrição fática: {descricao_fatica}\n"
            "Prazo para regularização: {prazo}"
        ),
        "campos_variaveis": [
            "descricao_fatica",
            "prazo",
            "contrato",
            "contratada"
        ],
        "fundamentacao_legal_padrao": [
            "Lei nº 14.133/2021, art. 122, §1º, I",
            "IN TJSP nº 012/2025, art. 31"
        ],
        "fundamentacao_contratual_placeholder": "Cláusula(s) contratual(is) relacionada(s) aos fatos descritos",
        "observacoes": "Esta advertência não exime a contratada do cumprimento integral das obrigações contratuais."
    }
