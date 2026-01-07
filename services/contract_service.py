"""
Serviço de Contratos
====================
Gerencia operações relacionadas a contratos regionais.

Nota: Atualmente utiliza dados mockados + contratos cadastrados via upload.
Preparado para futura integração com API REST corporativa.

EVOLUÇÃO FASE 3 - Contratos Regionais com Fiscais por Comarca:
- Suporte a múltiplas comarcas por contrato
- Cada comarca possui fiscal titular e suplente
- Compatibilidade total com contratos simples (modelo antigo)
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


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
    
    # Consolida dados do contrato aplicando aditivos sequencialmente
    contrato = consolidar_contrato_com_aditivos(contrato)
    
    return contrato


def consolidar_contrato_com_aditivos(contrato: dict) -> dict:
    """
    Aplica aditivos sequencialmente sobre dados originais do contrato.
    
    Esta função é crítica para refletir a realidade dos contratos do TJSP:
    - Prorrogações de prazo alteram data_fim e vigência
    - Acréscimos/supressões alteram valor total
    - Alterações qualitativas são registradas no histórico
    
    Args:
        contrato: Dados originais do contrato
        
    Returns:
        Contrato consolidado com todas as modificações dos aditivos aplicadas
    """
    # Se não tem aditivos, retorna contrato original
    if 'aditivos' not in contrato or not contrato['aditivos']:
        contrato['valor_original'] = contrato.get('valor', 0.0)
        contrato['data_fim_original'] = contrato.get('data_fim')
        return contrato
    
    # Salva valores originais
    contrato['valor_original'] = contrato.get('valor', 0.0)
    contrato['data_fim_original'] = contrato.get('data_fim')
    
    # Ordena aditivos por número (aplicação sequencial)
    aditivos_ordenados = sorted(
        contrato['aditivos'],
        key=lambda x: x.get('numero', 0)
    )
    
    # Valores acumulados
    valor_atual = contrato['valor_original']
    data_fim_atual = contrato['data_fim_original']
    
    # Histórico de modificações
    contrato['historico_aditivos'] = []
    
    # Aplica cada aditivo sequencialmente
    for aditivo in aditivos_ordenados:
        modificacao = {
            'numero': aditivo.get('numero'),
            'data': aditivo.get('data_aditivo', ''),
            'tipos': aditivo.get('tipo_modificacao', []),
            'alteracoes': []
        }
        
        # Aplica prorrogação de prazo
        if 'Prorrogação de Prazo' in aditivo.get('tipo_modificacao', []):
            nova_data = aditivo.get('nova_data_fim', '')
            if nova_data:
                # Converte string ISO para datetime se necessário
                if isinstance(nova_data, str):
                    from datetime import date
                    nova_data = datetime.fromisoformat(nova_data)
                elif isinstance(nova_data, date):
                    nova_data = datetime.combine(nova_data, datetime.min.time())
                
                dias_prorrogados = aditivo.get('prorrogacao_dias', 0)
                data_fim_atual = nova_data
                
                modificacao['alteracoes'].append({
                    'tipo': 'Prorrogação de Prazo',
                    'descricao': f'Prazo prorrogado em {dias_prorrogados} dias',
                    'nova_data_fim': nova_data.strftime('%d/%m/%Y') if hasattr(nova_data, 'strftime') else str(nova_data)
                })
        
        # Aplica acréscimo de valor
        if 'Acréscimo de Valor' in aditivo.get('tipo_modificacao', []):
            valor_acrescimo = aditivo.get('valor_acrescimo', 0.0)
            percentual = aditivo.get('percentual_acrescimo', 0.0)
            
            if valor_acrescimo > 0:
                valor_atual += valor_acrescimo
                
                modificacao['alteracoes'].append({
                    'tipo': 'Acréscimo de Valor',
                    'descricao': f'Acréscimo de {percentual:.1f}%',
                    'valor': valor_acrescimo,
                    'novo_valor_total': valor_atual
                })
        
        # Aplica supressão de valor
        if 'Supressão de Valor' in aditivo.get('tipo_modificacao', []):
            valor_supressao = aditivo.get('valor_supressao', 0.0)
            percentual = aditivo.get('percentual_supressao', 0.0)
            
            if valor_supressao > 0:
                valor_atual -= valor_supressao
                
                modificacao['alteracoes'].append({
                    'tipo': 'Supressão de Valor',
                    'descricao': f'Supressão de {percentual:.1f}%',
                    'valor': -valor_supressao,
                    'novo_valor_total': valor_atual
                })
        
        # Registra alterações qualitativas
        if 'Alteração Qualitativa' in aditivo.get('tipo_modificacao', []):
            alteracoes = aditivo.get('alteracoes_qualitativas', '')
            if alteracoes:
                modificacao['alteracoes'].append({
                    'tipo': 'Alteração Qualitativa',
                    'descricao': alteracoes[:200] + ('...' if len(alteracoes) > 200 else '')
                })
        
        # Adiciona justificativa
        if aditivo.get('justificativa'):
            modificacao['justificativa'] = aditivo['justificativa']
        
        # Adiciona ao histórico
        contrato['historico_aditivos'].append(modificacao)
    
    # Atualiza valores consolidados no contrato
    contrato['valor'] = valor_atual
    contrato['data_fim'] = data_fim_atual
    
    # Atualiza string de vigência
    if contrato.get('data_inicio') and data_fim_atual:
        data_inicio_fmt = contrato['data_inicio'].strftime('%d/%m/%Y') if hasattr(contrato['data_inicio'], 'strftime') else str(contrato['data_inicio'])
        data_fim_fmt = data_fim_atual.strftime('%d/%m/%Y') if hasattr(data_fim_atual, 'strftime') else str(data_fim_atual)
        contrato['vigencia'] = f"{data_inicio_fmt} a {data_fim_fmt}"
    
    # Recalcula vigência detalhada com data consolidada
    if 'vigencia_detalhada' in contrato:
        dias_restantes = (data_fim_atual - datetime.now()).days
        contrato['vigencia_detalhada']['data_fim'] = data_fim_atual
        contrato['vigencia_detalhada']['dias_restantes'] = dias_restantes
        contrato['vigencia_detalhada']['status_semaforo'] = "verde" if dias_restantes > 120 else ("amarelo" if dias_restantes >= 60 else "vermelho")
    
    # Marca que o contrato foi consolidado
    contrato['consolidado_com_aditivos'] = True
    contrato['total_aditivos_aplicados'] = len(aditivos_ordenados)
    
    return contrato


def adicionar_aditivo_contrato(contrato_id: str, arquivo_pdf, dados_aditivo: dict) -> bool:
    """
    Adiciona um novo aditivo a um contrato existente.
    
    Args:
        contrato_id: ID do contrato
        arquivo_pdf: Arquivo PDF do aditivo
        dados_aditivo: Dicionário com dados do aditivo (tipo, impactos, datas, valores, etc)
    
    Returns:
        True se sucesso, False caso contrário
    """
    try:
        # Carrega contratos cadastrados
        json_path = Path("data/contratos_cadastrados.json")
        
        if not json_path.exists():
            return False
        
        with open(json_path, 'r', encoding='utf-8') as f:
            contratos = json.load(f)
        
        # Encontra o contrato
        contrato = None
        indice_contrato = None
        for i, c in enumerate(contratos):
            if c.get('id') == contrato_id:
                contrato = c
                indice_contrato = i
                break
        
        if not contrato:
            return False
        
        # Garante que aditivos existe
        if 'aditivos' not in contrato:
            contrato['aditivos'] = []
        
        # Define próximo número do aditivo
        proximo_numero = len(contrato['aditivos']) + 1
        
        # Salva PDF do aditivo
        contratos_dir = Path("knowledge/contratos")
        contrato_dir = contratos_dir / contrato_id
        contrato_dir.mkdir(exist_ok=True)
        
        aditivo_filename = f"{contrato_id}_ADITIVO_{proximo_numero:02d}.pdf"
        aditivo_path = contrato_dir / aditivo_filename
        
        with open(aditivo_path, 'wb') as f:
            f.write(arquivo_pdf.getbuffer())
        
        # Adiciona aditivo ao contrato
        novo_aditivo = {
            'numero': proximo_numero,
            'filename': aditivo_filename,
            'path': str(aditivo_path),
            'data_upload': datetime.now().isoformat(),
            'nome_original': arquivo_pdf.name,
            'tipo_modificacao': dados_aditivo.get('tipo_modificacao', []),
            'data_aditivo': dados_aditivo.get('data_aditivo', ''),
            'justificativa': dados_aditivo.get('justificativa', ''),
            'prorrogacao_dias': dados_aditivo.get('prorrogacao_dias', 0),
            'nova_data_fim': dados_aditivo.get('nova_data_fim', ''),
            'percentual_acrescimo': dados_aditivo.get('percentual_acrescimo', 0.0),
            'percentual_supressao': dados_aditivo.get('percentual_supressao', 0.0),
            'valor_acrescimo': dados_aditivo.get('valor_acrescimo', 0.0),
            'valor_supressao': dados_aditivo.get('valor_supressao', 0.0),
            'alteracoes_qualitativas': dados_aditivo.get('alteracoes_qualitativas', '')
        }
        
        contrato['aditivos'].append(novo_aditivo)
        contrato['total_aditivos'] = len(contrato['aditivos'])
        contrato['ultima_atualizacao'] = datetime.now().isoformat()
        
        # Atualiza contrato na lista
        contratos[indice_contrato] = contrato
        
        # Salva de volta no JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(contratos, f, ensure_ascii=False, indent=2, default=str)
        
        return True
        
    except Exception as e:
        print(f"Erro ao adicionar aditivo: {e}")
        return False


def obter_documentos_contrato(contrato_id: str) -> Dict[str, List[str]]:
    """
    Retorna caminhos dos PDFs vinculados ao contrato (contrato original + aditivos).
    
    Args:
        contrato_id: ID do contrato
        
    Returns:
        Dict com:
        - 'contrato': caminho do PDF do contrato original (ou None)
        - 'aditivos': lista de caminhos dos PDFs de aditivos
    """
    contrato_dir = Path("knowledge/contratos") / contrato_id
    
    resultado = {
        'contrato': None,
        'aditivos': []
    }
    
    if not contrato_dir.exists():
        return resultado
    
    # Busca PDF do contrato original
    for arquivo in contrato_dir.glob(f"{contrato_id}.pdf"):
        resultado['contrato'] = str(arquivo)
        break
    
    # Busca PDFs de aditivos
    for arquivo in sorted(contrato_dir.glob(f"{contrato_id}_ADITIVO_*.pdf")):
        resultado['aditivos'].append(str(arquivo))
    
    return resultado


# ============================================================================
# FASE 3: CONTRATOS REGIONAIS - FISCAIS POR COMARCA
# ============================================================================

def obter_fiscais_do_contrato(contrato: Dict) -> List[Dict]:
    """
    Retorna lista normalizada de fiscais do contrato, com suporte a:
    - Contratos regionais (múltiplas comarcas): fiscais_por_comarca
    - Contratos simples (modelo antigo): fiscal_titular + fiscal_substituto
    
    Esta função garante COMPATIBILIDADE RETROATIVA com contratos antigos.
    
    Args:
        contrato: Dict com dados do contrato
        
    Returns:
        Lista de dicts com estrutura:
        [
            {
                "comarca": str,
                "titular": str,
                "suplente": str,
                "email_titular": str (opcional),
                "email_suplente": str (opcional)
            }
        ]
        
    Exemplos:
        # Contrato regional (novo modelo):
        contrato = {
            "fiscais_por_comarca": [
                {"comarca": "Sorocaba", "titular": "João", "suplente": "Maria"}
            ]
        }
        
        # Contrato simples (modelo antigo):
        contrato = {
            "fiscal_titular": "João",
            "fiscal_substituto": "Maria"
        }
    """
    # PRIORIDADE 1: Novo modelo (fiscais por comarca)
    if 'fiscais_por_comarca' in contrato and contrato['fiscais_por_comarca']:
        return contrato['fiscais_por_comarca']
    
    # PRIORIDADE 2: Modelo antigo (compatibilidade)
    # Trata como contrato de comarca única
    titular = contrato.get('fiscal_titular', '')
    suplente = contrato.get('fiscal_substituto', '')
    
    if titular or suplente:
        return [{
            "comarca": contrato.get('comarca', '(Comarca Única)'),
            "titular": titular,
            "suplente": suplente
        }]
    
    # FALLBACK: Sem fiscais cadastrados
    return []


def obter_fiscal_por_comarca(contrato: Dict, comarca: str) -> Optional[Dict]:
    """
    Retorna fiscal específico de uma comarca do contrato.
    
    Args:
        contrato: Dict com dados do contrato
        comarca: Nome da comarca
        
    Returns:
        Dict com titular/suplente ou None se não encontrado
    """
    fiscais = obter_fiscais_do_contrato(contrato)
    
    for fiscal in fiscais:
        if fiscal.get('comarca', '').lower() == comarca.lower():
            return fiscal
    
    return None


def obter_comarcas_do_contrato(contrato: Dict) -> List[str]:
    """
    Retorna lista de comarcas abrangidas pelo contrato.
    
    Args:
        contrato: Dict com dados do contrato
        
    Returns:
        Lista de nomes de comarcas
    """
    fiscais = obter_fiscais_do_contrato(contrato)
    return [f.get('comarca', '') for f in fiscais if f.get('comarca')]


def eh_contrato_regional(contrato: Dict) -> bool:
    """
    Verifica se o contrato é regional (múltiplas comarcas).
    
    Args:
        contrato: Dict com dados do contrato
        
    Returns:
        True se contrato regional, False caso contrário
    """
    return len(obter_comarcas_do_contrato(contrato)) > 1
