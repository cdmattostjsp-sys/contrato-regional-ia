"""
Pacote de Prompts
=================
Biblioteca centralizada de prompts para agentes de IA.
"""

from .system_prompts import (
    COPILOT_SYSTEM_PROMPT,
    NOTIFICACAO_SYSTEM_PROMPT,
    CONTRATO_CONTEXT_TEMPLATE,
    build_copilot_prompt,
    build_notificacao_prompt
)

__all__ = [
    'COPILOT_SYSTEM_PROMPT',
    'NOTIFICACAO_SYSTEM_PROMPT',
    'CONTRATO_CONTEXT_TEMPLATE',
    'build_copilot_prompt',
    'build_notificacao_prompt'
]
