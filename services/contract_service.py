"""
Serviço de Contratos
====================
Gerencia operações relacionadas a contratos regionais.

Nota: Atualmente utiliza dados mockados + contratos cadastrados via upload.
Preparado para futura integração com API REST corporativa.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
from pathlib import Path


def get_contratos_cadastrados() -> List[Dict]:
    """
    Retorna contratos cadastrados via upload (sistema de gestão).
    
    Returns:
        Lista de contratos cadastrados pelos usuários
    """
    json_path = Path("data/contratos_cadastrados.json")
    
    if not json_path.exists():
        return []
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            contratos = json.load(f)
        
        # Converte strings ISO de data para datetime
        for contrato in contratos:
            if 'data_inicio' in contrato and isinstance(contrato['data_inicio'], str):
                contrato['data_inicio'] = datetime.fromisoformat(contrato['data_inicio'])
            if 'data_fim' in contrato and isinstance(contrato['data_fim'], str):
                contrato['data_fim'] = datetime.fromisoformat(contrato['data_fim'])
            if 'ultima_atualizacao' in contrato and isinstance(contrato['ultima_atualizacao'], str):
                contrato['ultima_atualizacao'] = datetime.fromisoformat(contrato['ultima_atualizacao'])
        
        return contratos
    except Exception as e:
        print(f"Erro ao carregar contratos cadastrados: {e}")
        return []


def get_contratos_mock() -> List[Dict]:
    """
    Retorna lista de contratos mockados para o MVP.
    
    Returns:
        Lista de contratos com dados simulados
    """
    contratos = [
        {
            "id": "CTR001",
            "numero": "Contrato 001/2024 - RAJ 10.1",
            "tipo": "Serviços",
            "fornecedor": "Tech Solutions Ltda",
            "objeto": "Prestação de serviços de manutenção predial",
            "vigencia": "01/01/2024 a 31/12/2024",
            "valor": 450000.00,
            "status": "ativo",
            "data_inicio": datetime(2024, 1, 1),
            "data_fim": datetime(2024, 12, 31),
            "fiscal_titular": "João Silva Santos",
            "fiscal_substituto": "Maria Oliveira Costa",
            "ultima_atualizacao": datetime.now() - timedelta(days=2)
        },
        {
            "id": "CTR002",
            "numero": "Contrato 002/2024 - RAJ 10.1",
            "tipo": "Fornecimento",
            "fornecedor": "Office Supply SA",
            "objeto": "Fornecimento de material de expediente",
            "vigencia": "15/02/2024 a 14/02/2025",
            "valor": 180000.00,
            "status": "ativo",
            "data_inicio": datetime(2024, 2, 15),
            "data_fim": datetime(2025, 2, 14),
            "fiscal_titular": "Carlos Eduardo Lima",
            "fiscal_substituto": "Ana Paula Ferreira",
            "ultima_atualizacao": datetime.now() - timedelta(days=5)
        },
        {
            "id": "CTR003",
            "numero": "Contrato 003/2024 - RAJ 10.1",
            "tipo": "Serviços",
            "fornecedor": "Clean Services Eireli",
            "objeto": "Serviços de limpeza e conservação",
            "vigencia": "01/03/2024 a 28/02/2025",
            "valor": 320000.00,
            "status": "atencao",
            "data_inicio": datetime(2024, 3, 1),
            "data_fim": datetime(2025, 2, 28),
            "fiscal_titular": "Pedro Henrique Alves",
            "fiscal_substituto": "Juliana Rodrigues",
            "ultima_atualizacao": datetime.now() - timedelta(days=1),
            "pendencias": ["Atraso na entrega do relatório mensal", "Falta de atestação de nota fiscal"]
        },
        {
            "id": "CTR004",
            "numero": "Contrato 004/2024 - RAJ 10.1",
            "tipo": "Serviços",
            "fornecedor": "Segurança Total Ltda",
            "objeto": "Serviços de segurança patrimonial",
            "vigencia": "01/01/2024 a 31/12/2024",
            "valor": 680000.00,
            "status": "ativo",
            "data_inicio": datetime(2024, 1, 1),
            "data_fim": datetime(2024, 12, 31),
            "fiscal_titular": "Roberto Carlos Souza",
            "fiscal_substituto": "Fernanda Gomes",
            "ultima_atualizacao": datetime.now() - timedelta(hours=12)
        },
        {
            "id": "CTR005",
            "numero": "Contrato 005/2024 - RAJ 10.1",
            "tipo": "Serviços",
            "fornecedor": "InfoTech Sistemas SA",
            "objeto": "Manutenção e suporte de sistemas informatizados",
            "vigencia": "15/03/2024 a 14/03/2025",
            "valor": 540000.00,
            "status": "ativo",
            "data_inicio": datetime(2024, 3, 15),
            "data_fim": datetime(2025, 3, 14),
            "fiscal_titular": "Marcos Antonio Silva",
            "fiscal_substituto": "Luciana Martins",
            "ultima_atualizacao": datetime.now() - timedelta(days=3)
        },
        {
            "id": "CTR006",
            "numero": "Contrato 006/2024 - RAJ 10.1",
            "tipo": "Obras",
            "fornecedor": "Construções Rápidas Ltda",
            "objeto": "Reforma de salas de audiência",
            "vigencia": "01/04/2024 a 31/10/2024",
            "valor": 850000.00,
            "status": "critico",
            "data_inicio": datetime(2024, 4, 1),
            "data_fim": datetime(2024, 10, 31),
            "fiscal_titular": "Eng. José Mendes",
            "fiscal_substituto": "Arq. Paula Costa",
            "ultima_atualizacao": datetime.now() - timedelta(hours=6),
            "pendencias": ["Atraso de 15 dias no cronograma", "Não conformidade em vistoria técnica", "Pendência documental"]
        },
        {
            "id": "CTR007",
            "numero": "Contrato 007/2024 - RAJ 10.1",
            "tipo": "Fornecimento",
            "fornecedor": "TI Solutions Distribuidora",
            "objeto": "Fornecimento de equipamentos de informática",
            "vigencia": "10/05/2024 a 09/05/2025",
            "valor": 420000.00,
            "status": "ativo",
            "data_inicio": datetime(2024, 5, 10),
            "data_fim": datetime(2025, 5, 9),
            "fiscal_titular": "André Luiz Santos",
            "fiscal_substituto": "Camila Ribeiro",
            "ultima_atualizacao": datetime.now() - timedelta(days=4)
        },
        {
            "id": "CTR008",
            "numero": "Contrato 008/2024 - RAJ 10.1",
            "tipo": "Serviços",
            "fornecedor": "Jardinagem Verde Ltda",
            "objeto": "Serviços de jardinagem e paisagismo",
            "vigencia": "01/06/2024 a 31/05/2025",
            "valor": 95000.00,
            "status": "ativo",
            "data_inicio": datetime(2024, 6, 1),
            "data_fim": datetime(2025, 5, 31),
            "fiscal_titular": "Ricardo Oliveira",
            "fiscal_substituto": "Beatriz Almeida",
            "ultima_atualizacao": datetime.now() - timedelta(days=7)
        }
    ]
    
    return contratos


def get_todos_contratos() -> List[Dict]:
    """
    Retorna TODOS os contratos: mockados + cadastrados via upload.
    
    Esta é a função principal para listar contratos no sistema.
    Combina contratos de exemplo (mock) com contratos reais cadastrados.
    
    Returns:
        Lista completa de contratos disponíveis
    """
    contratos_mock = get_contratos_mock()
    contratos_cadastrados = get_contratos_cadastrados()
    
    # Combina as duas listas
    todos_contratos = contratos_mock + contratos_cadastrados
    
    # Ordena por data de atualização (mais recentes primeiro)
    todos_contratos.sort(
        key=lambda x: x.get('ultima_atualizacao', datetime.now()),
        reverse=True
    )
    
    return todos_contratos


def get_contrato_by_id(contrato_id: str) -> Optional[Dict]:
    """
    Busca contrato por ID (em ambas as fontes: mock e cadastrados).
    
    Args:
        contrato_id: ID do contrato
        
    Returns:
        Dados do contrato ou None se não encontrado
    """
    contratos = get_todos_contratos()
    for contrato in contratos:
        if contrato["id"] == contrato_id:
            return contrato
    return None


def get_contrato_detalhes(contrato_id: str) -> Optional[Dict]:
    """
    Retorna detalhes completos de um contrato, incluindo cláusulas e documentação.
    
    Args:
        contrato_id: ID do contrato
        
    Returns:
        Detalhes completos do contrato
    """
    contrato = get_contrato_by_id(contrato_id)
    
    if not contrato:
        return None
    
    # Adiciona informações detalhadas (mockadas)
    contrato["clausulas_principais"] = [
        "Cláusula 1ª - Do Objeto: O presente contrato tem por objeto...",
        "Cláusula 2ª - Do Prazo: O prazo de vigência será de 12 (doze) meses...",
        "Cláusula 3ª - Do Valor: O valor total do contrato é de...",
        "Cláusula 4ª - Das Obrigações da Contratada: São obrigações da contratada...",
        "Cláusula 5ª - Das Obrigações da Contratante: São obrigações da contratante...",
        "Cláusula 6ª - Das Penalidades: O descumprimento das obrigações sujeitará...",
        "Cláusula 7ª - Da Fiscalização: A fiscalização será exercida por...",
        "Cláusula 8ª - Da Rescisão: O contrato poderá ser rescindido..."
    ]
    
    contrato["documentos"] = [
        {"tipo": "Termo de Referência", "data": "15/11/2023", "status": "Aprovado"},
        {"tipo": "Edital", "data": "20/11/2023", "status": "Publicado"},
        {"tipo": "Proposta Vencedora", "data": "05/12/2023", "status": "Homologada"},
        {"tipo": "Contrato Assinado", "data": contrato["vigencia"].split(" a ")[0], "status": "Vigente"}
    ]
    
    contrato["historico_eventos"] = [
        {"data": datetime.now() - timedelta(days=30), "evento": "Contrato iniciado", "responsavel": contrato["fiscal_titular"]},
        {"data": datetime.now() - timedelta(days=15), "evento": "Primeira vistoria realizada", "responsavel": contrato["fiscal_titular"]},
        {"data": datetime.now() - timedelta(days=7), "evento": "Atestação de nota fiscal", "responsavel": contrato["fiscal_titular"]},
        {"data": datetime.now() - timedelta(days=2), "evento": "Relatório mensal recebido", "responsavel": contrato["fiscal_titular"]}
    ]
    
    # Informações de vigência detalhadas
    dias_restantes = (contrato["data_fim"] - datetime.now()).days
    contrato["vigencia_detalhada"] = {
        "data_inicio": contrato["data_inicio"],
        "data_fim": contrato["data_fim"],
        "dias_restantes": dias_restantes,
        "status_semaforo": "verde" if dias_restantes > 120 else ("amarelo" if dias_restantes >= 60 else "vermelho")
    }
    
    # Dados de pagamentos e atestes (mockados)
    contrato["pagamentos"] = [
        {
            "competencia": "11/2024",
            "nota_fiscal": "NF-001234",
            "valor": contrato["valor"] / 12,
            "status": "Atestado",
            "unidade_ateste": "RAJ 10.1 - Comarca de São Paulo",
            "data_ateste": datetime(2024, 12, 5),
            "responsavel_ateste": contrato["fiscal_titular"]
        },
        {
            "competencia": "10/2024",
            "nota_fiscal": "NF-001189",
            "valor": contrato["valor"] / 12,
            "status": "Atestado",
            "unidade_ateste": "RAJ 10.1 - Comarca de São Paulo",
            "data_ateste": datetime(2024, 11, 8),
            "responsavel_ateste": contrato["fiscal_titular"]
        },
        {
            "competencia": "12/2024",
            "nota_fiscal": "NF-001278",
            "valor": contrato["valor"] / 12,
            "status": "Pendente",
            "unidade_ateste": "-",
            "data_ateste": None,
            "responsavel_ateste": "-"
        }
    ]
    
    # Informações de tributação ISS
    contrato["tributacao"] = {
        "retem_iss": True,
        "base_legal_iss": "Lei Municipal nº 13.701/2003 - Art. 9º, § 3º",
        "observacao_iss": "Retenção na fonte conforme legislação municipal de São Paulo. Alíquota: 5%"
    }
    
    # Informações trabalhistas (para modo gestor)
    contrato["info_trabalhista"] = {
        "possui_mao_obra_residente": True if "Serviços" in contrato["tipo"] else False,
        "aplica_convencao_coletiva": True if "Serviços" in contrato["tipo"] else False,
        "categoria_profissional": "Trabalhadores em Edifícios e Condomínios" if "limpeza" in contrato["objeto"].lower() else "Serviços Gerais",
        "sindicato": "SIEMACO - Sindicato dos Empregados em Edifícios e Condomínios de SP"
    }
    
    return contrato
