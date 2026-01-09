"""
Testes Automatizados - BI Alertas Service
==========================================
CICLO 5 - Validação dos indicadores prospectivos

Data: 09/01/2026
"""

import unittest
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.bi_alertas_service import (
    calcular_risco_ruptura,
    calcular_consumo_silencioso,
    calcular_eficiencia_gestores,
    prever_rupturas,
    obter_kpis_dashboard,
    analisar_tendencia_temporal
)


class TestBIAlertasService(unittest.TestCase):
    """Suite de testes do serviço de BI"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.hoje = datetime.now()
        
        # Contrato de exemplo
        self.contrato_exemplo = {
            'id': 'CNT_001',
            'numero': '100/2025',
            'objeto': 'Contrato de teste',
            'data_fim': (self.hoje + timedelta(days=90)).isoformat()
        }
        
        # Alerta de exemplo
        self.alerta_exemplo = {
            'id': 'ALT_001',
            'tipo': 'critico',
            'categoria': 'Vigência',
            'titulo': 'Teste',
            'descricao': 'Alerta de teste',
            'contrato_id': 'CNT_001',
            'contrato_numero': '100/2025',
            'responsavel': 'gestor.silva',
            'estado': 'em_analise',
            'data_criacao': (self.hoje - timedelta(days=10)).isoformat(),
            'data_ultima_atualizacao': (self.hoje - timedelta(days=1)).isoformat()
        }
    
    def test_01_calcular_risco_ruptura_baixo(self):
        """Teste 1: Risco baixo (tempo suficiente)"""
        print("\n🧪 Teste 1: Risco de ruptura baixo")
        
        # Contrato com 180 dias restantes
        contrato = {
            **self.contrato_exemplo,
            'data_fim': (self.hoje + timedelta(days=180)).isoformat()
        }
        
        risco = calcular_risco_ruptura(contrato, [])
        
        self.assertEqual(risco['nivel_risco'], 'baixo')
        self.assertIn('✅', risco['status'])
        self.assertEqual(risco['cor'], 'green')
        self.assertGreater(risco['tempo_real_restante'], 0)
        
        print(f"✓ Risco: {risco['nivel_risco']} - {risco['status']}")
    
    def test_02_calcular_risco_ruptura_alto(self):
        """Teste 2: Risco alto (tempo insuficiente)"""
        print("\n🧪 Teste 2: Risco de ruptura alto")
        
        # Contrato com 30 dias restantes
        contrato = {
            **self.contrato_exemplo,
            'data_fim': (self.hoje + timedelta(days=30)).isoformat()
        }
        
        # Com alerta crítico ativo
        alerta = {**self.alerta_exemplo, 'tipo': 'critico'}
        
        risco = calcular_risco_ruptura(contrato, [alerta])
        
        self.assertIn(risco['nivel_risco'], ['alto', 'urgente'])
        # Verifica se status contém um dos símbolos
        tem_simbolo = ('⚠️' in risco['status']) or ('⛔' in risco['status'])
        self.assertTrue(tem_simbolo, f"Status deve conter ⚠️ ou ⛔: {risco['status']}")
        self.assertIn(risco['cor'], ['orange', 'red'])
        
        print(f"✓ Risco: {risco['nivel_risco']} - Tempo real: {risco['tempo_real_restante']} dias")
    
    def test_03_consumo_silencioso_normal(self):
        """Teste 3: Consumo silencioso normal"""
        print("\n🧪 Teste 3: Consumo silencioso normal")
        
        # Alerta criado há 3 dias
        alerta = {
            **self.alerta_exemplo,
            'data_criacao': (self.hoje - timedelta(days=3)).isoformat(),
            'estado': 'em_analise'
        }
        
        consumo = calcular_consumo_silencioso(alerta)
        
        self.assertEqual(consumo['severidade'], 'normal')
        self.assertIn('✅', consumo['status'])
        self.assertEqual(consumo['cor'], 'green')
        
        print(f"✓ Consumo: {consumo['consumo_silencioso']} dias - {consumo['status']}")
    
    def test_04_consumo_silencioso_excessivo(self):
        """Teste 4: Consumo silencioso excessivo"""
        print("\n🧪 Teste 4: Consumo silencioso excessivo")
        
        # Alerta criado há 30 dias em análise
        alerta = {
            **self.alerta_exemplo,
            'data_criacao': (self.hoje - timedelta(days=30)).isoformat(),
            'estado': 'em_analise'
        }
        
        consumo = calcular_consumo_silencioso(alerta)
        
        self.assertIn(consumo['severidade'], ['atencao', 'critico'])
        self.assertGreater(consumo['consumo_silencioso'], 0)
        
        print(f"✓ Consumo: {consumo['consumo_silencioso']} dias ({consumo['percentual_extra']}% extra)")
    
    def test_05_eficiencia_gestores(self):
        """Teste 5: Eficiência por gestor"""
        print("\n🧪 Teste 5: Eficiência por gestor")
        
        # Alertas de múltiplos gestores
        alertas = [
            {
                **self.alerta_exemplo,
                'id': f'ALT_{i}',
                'responsavel': 'gestor.silva' if i % 2 == 0 else 'gestor.costa',
                'estado': 'resolvido' if i < 5 else 'em_analise',
                'data_criacao': (self.hoje - timedelta(days=10)).isoformat(),
                'data_ultima_atualizacao': (self.hoje - timedelta(days=3)).isoformat()
            }
            for i in range(10)
        ]
        
        eficiencia = calcular_eficiencia_gestores(alertas)
        
        self.assertIsInstance(eficiencia, dict)
        self.assertIn('gestor.silva', eficiencia)
        self.assertIn('gestor.costa', eficiencia)
        
        for gestor, stats in eficiencia.items():
            self.assertIn('total_alertas', stats)
            self.assertIn('tempo_medio', stats)
            self.assertIn('classificacao', stats)
            self.assertGreaterEqual(stats['total_alertas'], 0)
            print(f"✓ {gestor}: {stats['total_alertas']} alertas - {stats['classificacao']}")
    
    def test_06_prever_rupturas(self):
        """Teste 6: Previsão de rupturas"""
        print("\n🧪 Teste 6: Previsão de rupturas")
        
        # Contratos com diferentes riscos
        contratos = [
            {
                'id': 'CNT_001',
                'numero': '100/2025',
                'objeto': 'Contrato crítico',
                'data_fim': (self.hoje + timedelta(days=30)).isoformat()
            },
            {
                'id': 'CNT_002',
                'numero': '200/2025',
                'objeto': 'Contrato médio',
                'data_fim': (self.hoje + timedelta(days=90)).isoformat()
            },
            {
                'id': 'CNT_003',
                'numero': '300/2025',
                'objeto': 'Contrato ok',
                'data_fim': (self.hoje + timedelta(days=365)).isoformat()
            }
        ]
        
        alertas_por_contrato = {
            'CNT_001': [{**self.alerta_exemplo, 'tipo': 'critico'}],
            'CNT_002': [{**self.alerta_exemplo, 'tipo': 'atencao'}],
            'CNT_003': []
        }
        
        previsoes = prever_rupturas(contratos, alertas_por_contrato)
        
        self.assertIsInstance(previsoes, list)
        # Deve ter pelo menos o contrato crítico
        self.assertGreater(len(previsoes), 0)
        
        # Primeiro da lista deve ser o mais urgente
        if len(previsoes) > 1:
            self.assertLessEqual(
                previsoes[0]['tempo_real_restante'],
                previsoes[1]['tempo_real_restante']
            )
        
        print(f"✓ {len(previsoes)} contratos em risco identificados")
    
    def test_07_kpis_dashboard(self):
        """Teste 7: KPIs consolidados do dashboard"""
        print("\n🧪 Teste 7: KPIs do dashboard")
        
        contratos = [self.contrato_exemplo]
        alertas = [self.alerta_exemplo]
        
        kpis = obter_kpis_dashboard(contratos, alertas)
        
        self.assertIsInstance(kpis, dict)
        self.assertIn('total_contratos', kpis)
        self.assertIn('contratos_risco_alto', kpis)
        self.assertIn('tempo_medio_resolucao_geral', kpis)
        self.assertIn('eficiencia_gestores', kpis)
        self.assertIn('previsoes_ruptura', kpis)
        
        self.assertEqual(kpis['total_contratos'], 1)
        self.assertGreaterEqual(kpis['contratos_risco_alto'], 0)
        
        print(f"✓ KPIs: {kpis['total_contratos']} contratos, {kpis['contratos_risco_alto']} em risco")
    
    def test_08_tendencia_temporal(self):
        """Teste 8: Análise de tendência temporal"""
        print("\n🧪 Teste 8: Tendência temporal")
        
        # Alertas em diferentes datas
        alertas = [
            {
                **self.alerta_exemplo,
                'id': f'ALT_{i}',
                'data_criacao': (self.hoje - timedelta(days=i)).isoformat(),
                'estado': 'resolvido' if i % 2 == 0 else 'em_analise',
                'data_ultima_atualizacao': (self.hoje - timedelta(days=i-1)).isoformat() if i % 2 == 0 else self.hoje.isoformat()
            }
            for i in range(10)
        ]
        
        tendencia = analisar_tendencia_temporal(alertas, dias=30)
        
        self.assertIsInstance(tendencia, dict)
        self.assertIn('total_criados', tendencia)
        self.assertIn('total_resolvidos', tendencia)
        self.assertIn('media_criados_dia', tendencia)
        self.assertIn('saldo', tendencia)
        
        self.assertGreater(tendencia['total_criados'], 0)
        
        print(f"✓ Tendência: {tendencia['total_criados']} criados, {tendencia['total_resolvidos']} resolvidos")
    
    def test_09_integracao_risco_e_consumo(self):
        """Teste 9: Integração entre risco e consumo"""
        print("\n🧪 Teste 9: Integração risco + consumo")
        
        # Contrato crítico com alerta com consumo
        contrato = {
            **self.contrato_exemplo,
            'data_fim': (self.hoje + timedelta(days=45)).isoformat()
        }
        
        alerta = {
            **self.alerta_exemplo,
            'data_criacao': (self.hoje - timedelta(days=20)).isoformat(),
            'tipo': 'critico'
        }
        
        risco = calcular_risco_ruptura(contrato, [alerta])
        consumo = calcular_consumo_silencioso(alerta)
        
        # Verificar correlação
        self.assertIn(risco['nivel_risco'], ['medio', 'alto', 'urgente'])
        
        # Se há risco alto e consumo excessivo, situação crítica
        if risco['nivel_risco'] in ['alto', 'urgente'] and consumo['severidade'] == 'critico':
            print("✓ ⚠️ SITUAÇÃO CRÍTICA DETECTADA: Risco alto + Consumo excessivo")
        else:
            print(f"✓ Risco: {risco['nivel_risco']}, Consumo: {consumo['severidade']}")
    
    def test_10_metricas_vazias(self):
        """Teste 10: Comportamento com dados vazios"""
        print("\n🧪 Teste 10: Dados vazios")
        
        # Testa com listas vazias
        eficiencia = calcular_eficiencia_gestores([])
        self.assertEqual(len(eficiencia), 0)
        
        previsoes = prever_rupturas([], {})
        self.assertEqual(len(previsoes), 0)
        
        kpis = obter_kpis_dashboard([], [])
        self.assertEqual(kpis['total_contratos'], 0)
        
        print("✓ Funções lidam corretamente com dados vazios")


def run_tests():
    """Executa todos os testes"""
    print("=" * 70)
    print("TESTES AUTOMATIZADOS - BI ALERTAS SERVICE")
    print("=" * 70)
    
    # Criar suite de testes
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBIAlertasService)
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    print(f"Total de testes: {result.testsRun}")
    print(f"✓ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"✗ Falhas: {len(result.failures)}")
    print(f"⚠ Erros: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM")
        return 1


if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
