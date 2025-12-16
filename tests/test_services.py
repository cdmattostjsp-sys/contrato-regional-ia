"""
Testes do Módulo de Serviços
=============================
"""

import unittest
from datetime import datetime
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from services.contract_service import get_contratos_mock, get_contrato_by_id


class TestContractService(unittest.TestCase):
    """Testes para o serviço de contratos"""
    
    def test_get_contratos_mock_returns_list(self):
        """Testa se get_contratos_mock retorna uma lista"""
        contratos = get_contratos_mock()
        self.assertIsInstance(contratos, list)
        self.assertGreater(len(contratos), 0)
    
    def test_contrato_tem_campos_obrigatorios(self):
        """Testa se cada contrato tem os campos obrigatórios"""
        contratos = get_contratos_mock()
        campos_obrigatorios = [
            'id', 'numero', 'tipo', 'fornecedor', 'objeto',
            'vigencia', 'valor', 'status'
        ]
        
        for contrato in contratos:
            for campo in campos_obrigatorios:
                self.assertIn(campo, contrato)
    
    def test_get_contrato_by_id_existente(self):
        """Testa busca de contrato existente"""
        contrato = get_contrato_by_id("CTR001")
        self.assertIsNotNone(contrato)
        self.assertEqual(contrato['id'], "CTR001")
    
    def test_get_contrato_by_id_inexistente(self):
        """Testa busca de contrato inexistente"""
        contrato = get_contrato_by_id("CTR999")
        self.assertIsNone(contrato)


if __name__ == '__main__':
    unittest.main()
