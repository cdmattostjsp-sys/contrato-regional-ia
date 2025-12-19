def get_template():
    return {
        "perfil": "gestor",
        "tipo_notificacao": "rescisao",
        "titulo": "Comunicação de Rescisão Contratual",
        "corpo": (
            "Comunicamos a rescisão do contrato, nos termos e fundamentos legais e contratuais, conforme dados abaixo.\n\n"
            "Contrato: {contrato}\n"
            "Contratada: {contratada}\n"
            "Motivo da rescisão: {motivo_rescisao}\n"
            "Data de efetivação: {data_efetivacao}"
        ),
        "campos_variaveis": [
            "contrato",
            "contratada",
            "motivo_rescisao",
            "data_efetivacao"
        ],
        "fundamentacao_legal_padrao": [
            "Lei nº 14.133/2021, art. 137",
            "IN TJSP nº 012/2025, art. 27"
        ],
        "fundamentacao_contratual_placeholder": "Cláusula(s) contratual(is) sobre rescisão",
        "observacoes": "A rescisão foi precedida dos trâmites legais e do contraditório."
    }
