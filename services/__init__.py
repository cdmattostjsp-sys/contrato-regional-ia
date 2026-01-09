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
from .dual_write_service import (
    criar_alerta_dual,
    sincronizar_resolucao,
    sincronizar_acao_dual,
    mapear_v1_para_v2,
    buscar_v2_por_v1,
    buscar_v1_por_v2,
    registrar_mapeamento,
    obter_estatisticas_mapeamento,
    obter_estatisticas_dual_write,
    validar_integridade
)
from .contract_service import (
    get_contratos_mock,
    get_contrato_by_id,
    get_contrato_detalhes
)
from .document_service import (
    listar_documentos_disponiveis,
    classificar_documento,
    extrair_texto_pdf,
    buscar_em_documento,
    obter_contexto_para_copilot,
    obter_referencias_legais,
    gerar_resumo_documentos
)

__all__ = [
        'criar_alerta_dual',
        'sincronizar_resolucao',
        'sincronizar_acao_dual',
        'mapear_v1_para_v2',
        'buscar_v2_por_v1',
        'buscar_v1_por_v2',
        'registrar_mapeamento',
        'obter_estatisticas_mapeamento',
        'obter_estatisticas_dual_write',
        'validar_integridade',
        'buscar_v2_por_v1',
    'initialize_session_state',
    'reset_chat_history',
    'reset_notificacao',
    'add_log',
    'get_current_user_info',
    'get_contratos_mock',
    'get_contrato_by_id',
    'get_contrato_detalhes',
    'listar_documentos_disponiveis',
    'classificar_documento',
    'extrair_texto_pdf',
    'buscar_em_documento',
    'obter_contexto_para_copilot',
    'obter_referencias_legais',
    'gerar_resumo_documentos'
]
