def get_template():
    return {
        "perfil": "gestor",
        "tipo_notificacao": "designacao_fiscais",
        "titulo": "Designação de Fiscais Contratuais",
        "corpo": (
            "Comunicamos a designação dos fiscais responsáveis pelo acompanhamento e fiscalização do contrato, conforme relação abaixo.\n\n"
            "Contrato: {contrato}\n"
            "Fiscais designados: {fiscais}\n"
            "Período de atuação: {periodo}"
        ),
        "campos_variaveis": [
            "contrato",
            "fiscais",
            "periodo"
        ],
        "fundamentacao_legal_padrao": [
            "Lei nº 14.133/2021, art. 117",
            "IN TJSP nº 012/2025, art. 7º"
        ],
        "fundamentacao_contratual_placeholder": "Cláusula(s) contratual(is) sobre fiscalização",
        "observacoes": "Os fiscais deverão atuar conforme atribuições normativas e contratuais."
    }
