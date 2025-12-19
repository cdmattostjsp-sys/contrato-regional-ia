def get_template():
    return {
        "perfil": "gestor",
        "tipo_notificacao": "inicio_vigencia",
        "titulo": "Comunicação de Início de Vigência Contratual",
        "corpo": (
            "Comunicamos o início da vigência do contrato, conforme dados abaixo, para ciência e adoção das providências cabíveis.\n\n"
            "Contrato: {contrato}\n"
            "Contratada: {contratada}\n"
            "Data de início: {data_inicio}"
        ),
        "campos_variaveis": [
            "contrato",
            "contratada",
            "data_inicio"
        ],
        "fundamentacao_legal_padrao": [
            "Lei nº 14.133/2021, art. 137",
            "IN TJSP nº 012/2025, art. 12"
        ],
        "fundamentacao_contratual_placeholder": "Cláusula(s) contratual(is) sobre vigência",
        "observacoes": "Providenciar publicação e registro conforme normativos."
    }
