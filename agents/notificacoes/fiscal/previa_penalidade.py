def get_template():
    return {
        "perfil": "fiscal",
        "tipo_notificacao": "previa_penalidade",
        "titulo": "Comunicação de Instauração de Fase Prévia à Aplicação de Penalidade",
        "corpo": (
            "Considerando o descumprimento das obrigações contratuais, comunica-se a instauração de fase prévia à aplicação de penalidade, garantindo o direito ao contraditório e à ampla defesa. "
            "A contratada poderá apresentar manifestação e documentos pertinentes no prazo estabelecido.\n\n"
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
            "Lei nº 14.133/2021, art. 156, §4º",
            "IN TJSP nº 012/2025, art. 33"
        ],
        "fundamentacao_contratual_placeholder": "Cláusula(s) contratual(is) relacionada(s) à infração apurada",
        "observacoes": "Esta comunicação não implica juízo prévio de culpabilidade."
    }
