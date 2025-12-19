"""
Registry de templates de notificações contratuais TJSP
"""
import importlib
import os

BASE_DIR = os.path.dirname(__file__)

TIPOS = {
    "fiscal": [
        "advertencia",
        "solicitacao_correcao",
        "solicitacao_documentacao",
        "comunicado_irregularidade",
        "previa_penalidade"
    ],
    "gestor": [
        "inicio_vigencia",
        "designacao_fiscais",
        "reajuste",
        "alteracao_contratual",
        "rescisao"
    ]
}

def get_template(perfil: str, tipo_notificacao: str):
    if perfil not in TIPOS or tipo_notificacao not in TIPOS[perfil]:
        raise ValueError("Tipo de notificação não registrado.")
    modulo = f"agents.notificacoes.{perfil}.{tipo_notificacao}"
    template_mod = importlib.import_module(modulo)
    return template_mod.get_template()
