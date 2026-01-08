"""
Testes automatizados para Dual Write Service
Fase 3 - contrato-regional-ia
"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "services"))
import dual_write_service

def test_mapear_v1_para_v2_basico():
    alerta_v1 = {
        'contrato_id': 'C-001',
        'titulo': 'Teste de alerta',
        'descricao': 'Descrição teste',
        'prazo': 10,
        'responsavel': 'gestor.teste',
    }
    v2 = dual_write_service.mapear_v1_para_v2(alerta_v1)
    assert v2['contrato_id'] == 'C-001'
    assert v2['titulo'] == 'Teste de alerta'
    assert v2['descricao'] == 'Descrição teste'
    assert v2['prazo'] == 10
    assert v2['responsavel'] == 'gestor.teste'

def test_criar_alerta_dual_sem_erro():
    alerta_v1 = {
        'contrato_id': 'C-002',
        'titulo': 'Alerta dual',
        'descricao': 'Dual write teste',
        'prazo': 20,
        'responsavel': 'gestor.dual',
    }
    # Não deve lançar exceção
    try:
        dual_write_service.criar_alerta_dual(alerta_v1)
    except Exception as e:
        pytest.fail(f"criar_alerta_dual lançou exceção: {e}")

def test_sincronizar_acao_dual_sem_erro():
    acao_v1 = {
        'id': 'A-001',
        'alerta_id': 'VIG_CRIT_C-001',
        'tipo_acao': 'resolucao',
        'justificativa': 'Teste justificativa',
        'usuario': 'gestor.teste',
    }
    try:
        dual_write_service.sincronizar_acao_dual(acao_v1)
    except Exception as e:
        pytest.fail(f"sincronizar_acao_dual lançou exceção: {e}")
