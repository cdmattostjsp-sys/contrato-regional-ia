"""
Pacote de Serviços
==================
Contém serviços de negócio da aplicação.
"""

from .session_manager import (
    initialize_session_state,
    reset_chat_history,
    reset_notificacao,
    add_log,
    get_current_user_info
)
from .contract_service import (
    get_contratos_mock,
    get_contrato_by_id,
    get_contrato_detalhes
)

__all__ = [
    'initialize_session_state',
    'reset_chat_history',
    'reset_notificacao',
    'add_log',
    'get_current_user_info',
    'get_contratos_mock',
    'get_contrato_by_id',
    'get_contrato_detalhes'
]
