"""
Serviço de Contratos
====================
Gerencia operações relacionadas a contratos regionais.

Nota: Atualmente utiliza dados mockados.
Preparado para futura integração com API REST corporativa.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional


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


def get_contrato_by_id(contrato_id: str) -> Optional[Dict]:
    """
    Busca contrato por ID.
    
    Args:
        contrato_id: ID do contrato
        
    Returns:
        Dados do contrato ou None se não encontrado
    """
    contratos = get_contratos_mock()
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
    
    return contrato
