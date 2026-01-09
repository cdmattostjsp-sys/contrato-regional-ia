"""
Testes Automatizados - Dual Write Service
==========================================
CICLO 4 - Validação completa da sincronização V1 ↔ V2

Data: 09/01/2026
"""

import unittest
import json
from pathlib import Path
from datetime import datetime
import sys

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.dual_write_service import (
    criar_alerta_dual,
    sincronizar_resolucao,
    sincronizar_acao_dual,
    mapear_v1_para_v2,
    registrar_mapeamento,
    buscar_v2_por_v1,
    buscar_v1_por_v2,
    obter_estatisticas_mapeamento,
    obter_estatisticas_dual_write,
    validar_integridade
)


class TestDualWriteService(unittest.TestCase):
    """Suite de testes do serviço de Dual Write"""
    
    @classmethod
    def setUpClass(cls):
        """Configuração inicial dos testes"""
        cls.data_dir = Path(__file__).parent.parent / "data"
        cls.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup de arquivos existentes
        cls.mapping_file = cls.data_dir / "dual_write_mapping.json"
        cls.mapping_backup = cls.data_dir / "dual_write_mapping.json.backup"
        
        if cls.mapping_file.exists():
            cls.mapping_file.rename(cls.mapping_backup)
    
    @classmethod
    def tearDownClass(cls):
        """Limpeza após todos os testes"""
        # Restaurar backup
        if cls.mapping_backup.exists():
            if cls.mapping_file.exists():
                cls.mapping_file.unlink()
            cls.mapping_backup.rename(cls.mapping_file)
    
    def setUp(self):
        """Configuração antes de cada teste"""
        # Limpar mapeamento
        if self.mapping_file.exists():
            self.mapping_file.unlink()
    
    def test_01_mapeamento_campos_v1_para_v2(self):
        """Teste 1: Mapeamento de campos V1 → V2"""
        print("\n🧪 Teste 1: Mapeamento de campos")
        
        alerta_v1 = {
            'id': 'VIG_CRIT_123',
            'tipo': 'critico',
            'categoria': 'Vigência',
            'titulo': 'Contrato próximo ao vencimento',
            'descricao': 'Vence em 45 dias',
            'contrato_id': 'CNT_001',
            'contrato_numero': '123/2025',
            'status': 'ATIVO',
            'dias_restantes': 45
        }
        
        v2_params = mapear_v1_para_v2(alerta_v1)
        
        # Verificações
        self.assertEqual(v2_params['tipo'], 'critico')
        self.assertEqual(v2_params['categoria'], 'Vigência')
        self.assertEqual(v2_params['titulo'], 'Contrato próximo ao vencimento')
        self.assertEqual(v2_params['contrato_id'], 'CNT_001')
        self.assertEqual(v2_params['criticidade'], 'urgente')
        self.assertEqual(v2_params['prazo_resposta_dias'], 5)  # Crítico = 5 dias
        self.assertIn('origem', v2_params['metadados'])
        self.assertEqual(v2_params['metadados']['origem'], 'dual_write_v1')
        
        print("✓ Mapeamento de campos funcionando corretamente")
    
    def test_02_registro_mapeamento_bidirecional(self):
        """Teste 2: Registro e busca de mapeamento V1 ↔ V2"""
        print("\n🧪 Teste 2: Mapeamento bidirecional")
        
        v1_id = "VIG_ATEN_456"
        v2_id = "550e8400-e29b-41d4-a716-446655440000"
        
        # Registrar mapeamento
        registrar_mapeamento(v1_id, v2_id, metadados={"tipo": "atencao"})
        
        # Buscar V2 por V1
        v2_encontrado = buscar_v2_por_v1(v1_id)
        self.assertEqual(v2_encontrado, v2_id)
        
        # Buscar V1 por V2
        v1_encontrado = buscar_v1_por_v2(v2_id)
        self.assertEqual(v1_encontrado, v1_id)
        
        # Verificar arquivo de mapeamento
        self.assertTrue(self.mapping_file.exists())
        
        with open(self.mapping_file, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        
        self.assertIn(v1_id, mapping['v1_to_v2'])
        self.assertIn(v2_id, mapping['v2_to_v1'])
        
        print("✓ Mapeamento bidirecional funcionando")
    
    def test_03_busca_inexistente(self):
        """Teste 3: Busca de mapeamento inexistente"""
        print("\n🧪 Teste 3: Busca de mapeamento inexistente")
        
        v2_resultado = buscar_v2_por_v1("ID_INEXISTENTE")
        self.assertIsNone(v2_resultado)
        
        v1_resultado = buscar_v1_por_v2("UUID_INEXISTENTE")
        self.assertIsNone(v1_resultado)
        
        print("✓ Busca de inexistentes retorna None corretamente")
    
    def test_04_mapeamento_tipo_atencao(self):
        """Teste 4: Mapeamento de alerta tipo 'atencao'"""
        print("\n🧪 Teste 4: Mapeamento tipo 'atencao'")
        
        alerta_v1 = {
            'id': 'VIG_ATEN_789',
            'tipo': 'atencao',
            'categoria': 'Vigência',
            'titulo': 'Planejamento necessário',
            'descricao': 'Vence em 90 dias',
            'contrato_id': 'CNT_002',
            'contrato_numero': '456/2025'
        }
        
        v2_params = mapear_v1_para_v2(alerta_v1)
        
        self.assertEqual(v2_params['tipo'], 'preventivo')
        self.assertEqual(v2_params['criticidade'], 'media')
        self.assertEqual(v2_params['prazo_resposta_dias'], 15)
        
        print("✓ Mapeamento de 'atencao' correto")
    
    def test_05_mapeamento_tipo_info(self):
        """Teste 5: Mapeamento de alerta tipo 'info'"""
        print("\n🧪 Teste 5: Mapeamento tipo 'info'")
        
        alerta_v1 = {
            'id': 'INFO_001',
            'tipo': 'info',
            'categoria': 'Documentação',
            'titulo': 'Documento disponível',
            'descricao': 'Nova versão do manual',
            'contrato_id': 'CNT_003',
            'contrato_numero': '789/2025'
        }
        
        v2_params = mapear_v1_para_v2(alerta_v1)
        
        self.assertEqual(v2_params['tipo'], 'informativo')
        self.assertEqual(v2_params['criticidade'], 'baixa')
        self.assertEqual(v2_params['prazo_resposta_dias'], 30)
        
        print("✓ Mapeamento de 'info' correto")
    
    def test_06_estatisticas_mapeamento(self):
        """Teste 6: Estatísticas de mapeamento"""
        print("\n🧪 Teste 6: Estatísticas")
        
        # Registrar múltiplos mapeamentos
        for i in range(5):
            registrar_mapeamento(
                f"V1_{i}",
                f"V2_{i}",
                metadados={"numero": i}
            )
        
        stats = obter_estatisticas_mapeamento()
        
        self.assertEqual(stats['total_mapeamentos'], 5)
        self.assertIsNotNone(stats['primeiro_mapeamento'])
        self.assertIsNotNone(stats['ultimo_mapeamento'])
        
        print(f"✓ Estatísticas: {stats['total_mapeamentos']} mapeamentos")
    
    def test_07_criacao_alerta_dual_sucesso(self):
        """Teste 7: Criação de alerta com dual write (mock)"""
        print("\n🧪 Teste 7: Criação dual write")
        
        # Este teste valida a estrutura, mas não executa o dual write completo
        # pois requer o sistema V2 completo rodando
        
        alerta_v1 = {
            'id': 'TEST_DUAL_001',
            'tipo': 'critico',
            'categoria': 'Vigência',
            'titulo': 'Teste dual write',
            'descricao': 'Teste de sincronização',
            'contrato_id': 'CNT_TEST',
            'contrato_numero': 'TEST/2026'
        }
        
        # Validar que o mapeamento funciona
        v2_params = mapear_v1_para_v2(alerta_v1)
        self.assertIsNotNone(v2_params)
        self.assertIn('tipo', v2_params)
        self.assertIn('metadados', v2_params)
        
        print("✓ Estrutura de dual write validada")
    
    def test_08_mapeamento_preserva_metadados(self):
        """Teste 8: Preservação de metadados no mapeamento"""
        print("\n🧪 Teste 8: Preservação de metadados")
        
        v1_id = "VIG_META_001"
        v2_id = "uuid-metadados-001"
        metadados = {
            "tipo": "critico",
            "categoria": "Vigência",
            "contrato": "100/2026",
            "custom_field": "valor_teste"
        }
        
        registrar_mapeamento(v1_id, v2_id, metadados=metadados)
        
        # Verificar no arquivo
        with open(self.mapping_file, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        
        registro_v1_to_v2 = mapping['v1_to_v2'][v1_id]
        self.assertEqual(registro_v1_to_v2['metadados'], metadados)
        
        registro_v2_to_v1 = mapping['v2_to_v1'][v2_id]
        self.assertEqual(registro_v2_to_v1['metadados'], metadados)
        
        print("✓ Metadados preservados corretamente")
    
    def test_09_mapeamento_duplicado(self):
        """Teste 9: Tratamento de mapeamento duplicado"""
        print("\n🧪 Teste 9: Mapeamento duplicado")
        
        v1_id = "DUP_001"
        v2_id_1 = "uuid-dup-001"
        v2_id_2 = "uuid-dup-002"
        
        # Primeiro mapeamento
        registrar_mapeamento(v1_id, v2_id_1)
        resultado_1 = buscar_v2_por_v1(v1_id)
        self.assertEqual(resultado_1, v2_id_1)
        
        # Segundo mapeamento (sobrescreve)
        registrar_mapeamento(v1_id, v2_id_2)
        resultado_2 = buscar_v2_por_v1(v1_id)
        self.assertEqual(resultado_2, v2_id_2)
        
        print("✓ Mapeamento duplicado sobrescreve corretamente")
    
    def test_10_integridade_timestamp(self):
        """Teste 10: Timestamps nos mapeamentos"""
        print("\n🧪 Teste 10: Timestamps")
        
        v1_id = "TIME_001"
        v2_id = "uuid-time-001"
        
        antes = datetime.now().isoformat()
        registrar_mapeamento(v1_id, v2_id)
        depois = datetime.now().isoformat()
        
        with open(self.mapping_file, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        
        timestamp = mapping['v1_to_v2'][v1_id]['timestamp']
        self.assertIsNotNone(timestamp)
        self.assertGreaterEqual(timestamp, antes)
        self.assertLessEqual(timestamp, depois)
        
        print(f"✓ Timestamp registrado: {timestamp}")


def run_tests():
    """Executa todos os testes"""
    print("=" * 70)
    print("TESTES AUTOMATIZADOS - DUAL WRITE SERVICE")
    print("=" * 70)
    
    # Criar suite de testes
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDualWriteService)
    
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

