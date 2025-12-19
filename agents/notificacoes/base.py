"""
Estruturas comuns para templates de notificações contratuais TJSP
"""

from typing import List, Dict, Any

# Constantes institucionais
LEI_14133 = "Lei nº 14.133/2021"
IN_TJSP_012_2025 = "IN TJSP nº 012/2025"

# Tipo padrão de template
TemplateType = Dict[str, Any]

def validar_template(template: TemplateType) -> bool:
    """Validação simples de campos obrigatórios do template."""
    obrigatorios = [
        "perfil", "tipo_notificacao", "titulo", "corpo",
        "campos_variaveis", "fundamentacao_legal_padrao",
        "fundamentacao_contratual_placeholder"
    ]
    return all(campo in template for campo in obrigatorios)
