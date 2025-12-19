def get_template():
    return {
        "perfil": "gestor",
        "tipo_notificacao": "alteracao_contratual",
        "titulo": "Comunicação de Alteração Contratual",
        "corpo": (
            "Comunicamos a formalização de alteração contratual, conforme especificações abaixo, para ciência e providências.\n\n"
            "Contrato: {contrato}\n"
            "Contratada: {contratada}\n"
            "Objeto da alteração: {objeto_alteracao}\n"
            "Data de vigência da alteração: {data_vigencia}"
        ),
        "campos_variaveis": [
            "contrato",
            "contratada",
            "objeto_alteracao",
            "data_vigencia"
        ],
        "fundamentacao_legal_padrao": [
            "Lei nº 14.133/2021, art. 124",
            "IN TJSP nº 012/2025, art. 21"
        ],
        "fundamentacao_contratual_placeholder": "Cláusula(s) contratual(is) sobre alterações",
        "observacoes": "A alteração foi formalizada por termo aditivo, conforme legislação vigente."
    }
