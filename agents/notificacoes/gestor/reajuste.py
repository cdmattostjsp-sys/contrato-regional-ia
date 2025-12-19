def get_template():
    return {
        "perfil": "gestor",
        "tipo_notificacao": "reajuste",
        "titulo": "Comunicação de Reajuste Contratual",
        "corpo": (
            "Comunicamos a aplicação de reajuste contratual, nos termos previstos em contrato e legislação vigente.\n\n"
            "Contrato: {contrato}\n"
            "Contratada: {contratada}\n"
            "Índice/critério: {indice}\n"
            "Data de vigência do reajuste: {data_vigencia}"
        ),
        "campos_variaveis": [
            "contrato",
            "contratada",
            "indice",
            "data_vigencia"
        ],
        "fundamentacao_legal_padrao": [
            "Lei nº 14.133/2021, art. 134",
            "IN TJSP nº 012/2025, art. 24"
        ],
        "fundamentacao_contratual_placeholder": "Cláusula(s) contratual(is) sobre reajuste",
        "observacoes": "O reajuste observará os limites e condições contratuais e legais."
    }
