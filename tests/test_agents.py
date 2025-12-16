"""
Testes dos Agentes de IA
=========================
"""

import unittest
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from agents.copilot_agent import processar_pergunta_copilot, extrair_contexto_contrato
from agents.notificacao_agent import gerar_notificacao_contratual, validar_dados_notificacao
from services.contract_service import get_contrato_by_id


class TestCopilotAgent(unittest.TestCase):
    """Testes para o agente Copilot"""
    
    def setUp(self):
        """Setup dos testes"""
        self.contrato = get_contrato_by_id("CTR001")
    
    def test_processar_pergunta_sobre_valor(self):
        """Testa pergunta sobre valor do contrato"""
        resposta = processar_pergunta_copilot("Qual é o valor do contrato?", self.contrato)
        self.assertIn("valor", resposta.lower())
        # Verifica se contém alguma representação do valor
        self.assertTrue(
            "450" in resposta or "450000" in resposta,
            f"Valor não encontrado na resposta: {resposta}"
        )
    
    def test_processar_pergunta_sobre_fiscal(self):
        """Testa pergunta sobre fiscal"""
        resposta = processar_pergunta_copilot("Quem é o fiscal?", self.contrato)
        self.assertIn(self.contrato['fiscal_titular'], resposta)
    
    def test_extrair_contexto_contrato(self):
        """Testa extração de contexto"""
        contexto = extrair_contexto_contrato(self.contrato)
        self.assertIn("CONTEXTO DO CONTRATO", contexto)
        self.assertIn(self.contrato['numero'], contexto)


class TestNotificacaoAgent(unittest.TestCase):
    """Testes para o agente de notificações"""
    
    def setUp(self):
        """Setup dos testes"""
        self.contrato = get_contrato_by_id("CTR001")
        self.dados_notificacao = {
            "tipo": "Advertência",
            "motivo": "Teste de motivo",
            "prazo": 5,
            "fundamentacao": "Lei 8.666/93",
            "destinatario": self.contrato['fornecedor']
        }
    
    def test_gerar_notificacao_contratual(self):
        """Testa geração de notificação"""
        notificacao = gerar_notificacao_contratual(self.contrato, self.dados_notificacao)
        self.assertIn("TRIBUNAL DE JUSTIÇA", notificacao)
        self.assertIn(self.contrato['numero'], notificacao)
        self.assertIn(self.dados_notificacao['motivo'], notificacao)
    
    def test_validar_dados_notificacao_validos(self):
        """Testa validação de dados válidos"""
        valido, mensagem = validar_dados_notificacao(self.dados_notificacao)
        self.assertTrue(valido)
        self.assertEqual(mensagem, "")
    
    def test_validar_dados_notificacao_invalidos(self):
        """Testa validação de dados inválidos"""
        dados_invalidos = {"tipo": "", "motivo": ""}
        valido, mensagem = validar_dados_notificacao(dados_invalidos)
        self.assertFalse(valido)
        self.assertNotEqual(mensagem, "")


if __name__ == '__main__':
    unittest.main()
