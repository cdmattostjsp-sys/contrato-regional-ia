"""
Testes Unitários para Alert Lifecycle Service V2
==================================================
Valida o funcionamento do novo módulo de ciclo de vida de alertas.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from services.alert_lifecycle_service import (
    criar_alerta_v2,
    get_alerta_v2_por_id,
    listar_alertas_v2,
    transicionar_estado,
    registrar_acao,
    get_acoes_por_alerta,
    criar_alerta_derivado,
    get_cadeia_alertas,
    calcular_score_risco,
    calcular_janela_seguranca,
    get_estatisticas_alertas_v2,
    importar_alerta_v1_para_v2,
    ESTADO_NOVO,
    ESTADO_EM_ANALISE,
    ESTADO_RESOLVIDO,
    TIPO_PREVENTIVO,
    TIPO_OPERACIONAL,
    CATEGORIA_VIGENCIA,
    CRITICIDADE_ALTA,
    ACAO_DECISAO_RENOVAR,
    ACAO_PROVIDENCIA_INICIAR_PROCESSO
)


def test_criar_alerta_v2():
    """Teste de criação de alerta V2"""
    print("\n=== Teste 1: Criação de Alerta V2 ===")
    
    alerta = criar_alerta_v2(
        tipo=TIPO_PREVENTIVO,
        categoria=CATEGORIA_VIGENCIA,
        titulo="Contrato próximo ao vencimento",
        descricao="Contrato 123/2025 vence em 90 dias",
        contrato_id="cont_001",
        contrato_numero="123/2025",
        responsavel="gestor.teste",
        prazo_resposta_dias=30,
        criticidade=CRITICIDADE_ALTA
    )
    
    print(f"✓ Alerta criado com ID: {alerta['id']}")
    print(f"  - Tipo: {alerta['tipo']}")
    print(f"  - Estado: {alerta['estado']}")
    print(f"  - Geração: {alerta['geracao']}")
    print(f"  - Versão: {alerta['versao']}")
    
    assert alerta['estado'] == ESTADO_NOVO
    assert alerta['versao'] == 2
    assert alerta['geracao'] == 1
    assert len(alerta['historico_estados']) == 1
    
    return alerta['id']


def test_transicionar_estado(alerta_id: str):
    """Teste de transição de estado"""
    print("\n=== Teste 2: Transição de Estado ===")
    
    sucesso = transicionar_estado(
        alerta_id=alerta_id,
        novo_estado=ESTADO_EM_ANALISE,
        usuario="gestor.teste",
        observacao="Iniciando análise do alerta"
    )
    
    alerta = get_alerta_v2_por_id(alerta_id)
    
    print(f"✓ Transição realizada: {sucesso}")
    print(f"  - Estado atual: {alerta['estado']}")
    print(f"  - Estado anterior: {alerta['estado_anterior']}")
    print(f"  - Histórico: {len(alerta['historico_estados'])} entradas")
    
    assert sucesso == True
    assert alerta['estado'] == ESTADO_EM_ANALISE
    assert alerta['estado_anterior'] == ESTADO_NOVO
    assert len(alerta['historico_estados']) == 2


def test_registrar_acao(alerta_id: str):
    """Teste de registro de ação"""
    print("\n=== Teste 3: Registro de Ação ===")
    
    acao = registrar_acao(
        alerta_id=alerta_id,
        tipo_acao=ACAO_DECISAO_RENOVAR,
        usuario="gestor.teste",
        justificativa="Necessidade de continuidade do serviço conforme Art. 57 da Lei 8.666/93",
        decisao="RENOVAR",
        prazo_novo_dias=60,
        metadados_acao={
            'parecer_juridico': 'PAJ-2025-001',
            'fundamentacao': 'Art. 57, II, Lei 8.666/93'
        }
    )
    
    print(f"✓ Ação registrada com ID: {acao['id']}")
    print(f"  - Tipo: {acao['tipo_acao']}")
    print(f"  - Decisão: {acao['decisao']}")
    print(f"  - Novo prazo: {acao['prazo_novo_dias']} dias")
    
    # Verifica vinculação
    acoes = get_acoes_por_alerta(alerta_id)
    print(f"  - Total de ações no alerta: {len(acoes)}")
    
    assert acao['decisao'] == "RENOVAR"
    assert len(acoes) == 1


def test_alerta_derivado(alerta_id: str):
    """Teste de criação de alerta derivado (encadeamento)"""
    print("\n=== Teste 4: Alerta Derivado (Encadeamento) ===")
    
    alerta_derivado = criar_alerta_derivado(
        alerta_origem_id=alerta_id,
        tipo=TIPO_OPERACIONAL,
        titulo="Iniciar processo de renovação",
        descricao="Após decisão de renovar, iniciar procedimento administrativo",
        prazo_resposta_dias=45,
        criticidade=CRITICIDADE_ALTA
    )
    
    print(f"✓ Alerta derivado criado: {alerta_derivado['id']}")
    print(f"  - Geração: {alerta_derivado['geracao']}")
    print(f"  - Alerta origem: {alerta_derivado['alerta_origem_id']}")
    
    # Verifica cadeia
    raiz, cadeia = get_cadeia_alertas(alerta_derivado['id'])
    print(f"  - Cadeia completa: {len(cadeia)} alertas")
    
    assert alerta_derivado['geracao'] == 2
    assert alerta_derivado['alerta_origem_id'] == alerta_id
    assert len(cadeia) == 2


def test_calcular_risco(alerta_id: str):
    """Teste de cálculo de score de risco"""
    print("\n=== Teste 5: Cálculo de Risco ===")
    
    score = calcular_score_risco(alerta_id)
    
    alerta = get_alerta_v2_por_id(alerta_id)
    
    print(f"✓ Score de risco calculado: {score}")
    print(f"  - Fatores:")
    for fator, valor in alerta['fatores_risco'].items():
        print(f"    • {fator}: {valor:.3f}")
    
    assert 0.0 <= score <= 1.0
    assert 'urgencia_temporal' in alerta['fatores_risco']


def test_janela_seguranca(alerta_id: str):
    """Teste de cálculo de janela de segurança"""
    print("\n=== Teste 6: Janela de Segurança ===")
    
    tempo_medio_renovacao = 20  # dias
    janela = calcular_janela_seguranca(alerta_id, tempo_medio_renovacao)
    
    alerta = get_alerta_v2_por_id(alerta_id)
    
    print(f"✓ Janela de segurança: {janela} dias")
    print(f"  - Dias restantes: {alerta['dias_restantes']}")
    print(f"  - Tempo médio execução: {tempo_medio_renovacao} dias")
    print(f"  - Janela real: {janela} dias")
    
    if janela < 0:
        print(f"  ⚠️  ATENÇÃO: Janela negativa indica risco de ruptura!")
    
    assert alerta['janela_seguranca_dias'] == janela


def test_estatisticas():
    """Teste de estatísticas gerais"""
    print("\n=== Teste 7: Estatísticas ===")
    
    stats = get_estatisticas_alertas_v2()
    
    print(f"✓ Estatísticas calculadas:")
    print(f"  - Total de alertas: {stats['total_alertas']}")
    print(f"  - Total de ações: {stats['total_acoes']}")
    print(f"  - Risco médio: {stats['risco_medio']:.3f}")
    print(f"  - Alertas risco alto: {stats['alertas_risco_alto']}")
    print(f"  - Por estado: {stats['por_estado']}")
    print(f"  - Por tipo: {stats['por_tipo']}")
    
    assert stats['total_alertas'] >= 2  # Pelo menos 2 alertas criados


def test_importar_v1():
    """Teste de importação de alerta V1"""
    print("\n=== Teste 8: Importação de Alerta V1 ===")
    
    alerta_v1 = {
        'id': 'VIG_CRIT_old_001',
        'tipo': 'critico',
        'categoria': 'Vigência',
        'titulo': 'Alerta V1 de teste',
        'descricao': 'Este é um alerta do sistema antigo',
        'contrato_id': 'cont_old_001',
        'contrato_numero': '999/2024',
        'dias_restantes': 45
    }
    
    alerta_v2 = importar_alerta_v1_para_v2(alerta_v1)
    
    print(f"✓ Alerta V1 importado com sucesso")
    print(f"  - ID V2: {alerta_v2['id']}")
    print(f"  - Versão: {alerta_v2['versao']}")
    print(f"  - Metadados importação: {alerta_v2['metadados']['importado_de_v1']}")
    print(f"  - ID original: {alerta_v2['metadados']['id_v1']}")
    
    assert alerta_v2['versao'] == 2
    assert alerta_v2['metadados']['importado_de_v1'] == True
    assert alerta_v2['metadados']['id_v1'] == alerta_v1['id']


def test_listagem_filtrada():
    """Teste de listagem com filtros"""
    print("\n=== Teste 9: Listagem Filtrada ===")
    
    # Lista todos
    todos = listar_alertas_v2()
    print(f"✓ Total de alertas: {len(todos)}")
    
    # Filtra por contrato
    por_contrato = listar_alertas_v2(contrato_id="cont_001")
    print(f"  - Por contrato 'cont_001': {len(por_contrato)}")
    
    # Filtra por estado
    novos = listar_alertas_v2(estado=ESTADO_NOVO)
    print(f"  - Estado 'novo': {len(novos)}")
    
    # Filtra por tipo
    preventivos = listar_alertas_v2(tipo=TIPO_PREVENTIVO)
    print(f"  - Tipo 'preventivo': {len(preventivos)}")
    
    assert len(todos) >= 3
    assert len(por_contrato) >= 2


def executar_suite_testes():
    """Executa suite completa de testes"""
    print("=" * 70)
    print("SUITE DE TESTES - ALERT LIFECYCLE SERVICE V2")
    print("=" * 70)
    
    try:
        # Teste 1: Criação
        alerta_id = test_criar_alerta_v2()
        
        # Teste 2: Transição de estado
        test_transicionar_estado(alerta_id)
        
        # Teste 3: Registro de ação
        test_registrar_acao(alerta_id)
        
        # Teste 4: Alerta derivado
        test_alerta_derivado(alerta_id)
        
        # Teste 5: Cálculo de risco
        test_calcular_risco(alerta_id)
        
        # Teste 6: Janela de segurança
        test_janela_seguranca(alerta_id)
        
        # Teste 7: Estatísticas
        test_estatisticas()
        
        # Teste 8: Importação V1
        test_importar_v1()
        
        # Teste 9: Listagem filtrada
        test_listagem_filtrada()
        
        print("\n" + "=" * 70)
        print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("=" * 70)
        
    except AssertionError as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        raise
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        raise


if __name__ == "__main__":
    executar_suite_testes()
