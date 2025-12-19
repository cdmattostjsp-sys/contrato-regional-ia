def get_template():
    return {
        "perfil": "fiscal",
        "tipo_notificacao": "solicitacao_documentacao",
        "titulo": "Solicitação de Documentação",
        "corpo": (
            "Solicita-se, para fins de acompanhamento e regularidade contratual, o envio da documentação relacionada abaixo, no prazo estabelecido.\n\n"
            "Descrição fática: {descricao_fatica}\n"
            "Prazo para apresentação: {prazo}"
        ),
        "campos_variaveis": [
            "descricao_fatica",
            "prazo",
            "contrato",
            "contratada"
        ],
        "fundamentacao_legal_padrao": [
            "Lei nº 14.133/2021, art. 117, §2º",
            "IN TJSP nº 012/2025, art. 30"
        ],
        "fundamentacao_contratual_placeholder": "Cláusula(s) contratual(is) relacionada(s) à documentação solicitada",
        "observacoes": "O não envio da documentação poderá ensejar restrições contratuais."
    }
