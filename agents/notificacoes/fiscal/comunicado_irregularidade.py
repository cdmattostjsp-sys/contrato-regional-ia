def get_template():
    return {
        "perfil": "fiscal",
        "tipo_notificacao": "comunicado_irregularidade",
        "titulo": "Comunicado de Irregularidade",
        "corpo": (
            "Comunicamos a identificação de irregularidade na execução contratual, conforme descrição abaixo. "
            "Solicita-se manifestação formal da contratada, no prazo estabelecido, para esclarecimentos e eventuais providências.\n\n"
            "Descrição fática: {descricao_fatica}\n"
            "Prazo para manifestação: {prazo}"
        ),
        "campos_variaveis": [
            "descricao_fatica",
            "prazo",
            "contrato",
            "contratada"
        ],
        "fundamentacao_legal_padrao": [
            "Lei nº 14.133/2021, art. 117, §3º",
            "IN TJSP nº 012/2025, art. 32"
        ],
        "fundamentacao_contratual_placeholder": "Cláusula(s) contratual(is) relacionada(s) à irregularidade comunicada",
        "observacoes": "A ausência de manifestação poderá ser interpretada como concordância tácita."
    }
