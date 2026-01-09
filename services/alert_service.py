"""
Serviço de Alertas Contratuais
===============================
Gera e gerencia alertas automáticos baseados em regras de negócio.

MODELO DE GOVERNANÇA:
- Sistema APONTA alertas automaticamente
- Gestor RESOLVE com justificativa obrigatória
- Sistema REGISTRA ato administrativo no histórico

Estados do alerta:
- ATIVO: Alerta gerado pelo sistema, aguardando análise
- RESOLVIDO: Alerta analisado e resolvido por gestor
- ARQUIVADO: Alerta não mais relevante (uso futuro)
"""

from datetime import datetime, timedelta
from typing import List, Dict
import json
from pathlib import Path

# Importação condicional para evitar dependência circular
try:
    from services.dual_write_service import criar_alerta_dual
except ImportError:
    criar_alerta_dual = None

# Estados possíveis do alerta
STATUS_ATIVO = "ATIVO"
STATUS_RESOLVIDO = "RESOLVIDO"
STATUS_ARQUIVADO = "ARQUIVADO"


def calcular_alertas(contratos: List[Dict]) -> List[Dict]:
    """
    Calcula alertas automáticos para contratos.
    
    IMPORTANTE: Esta função APENAS APONTA alertas com base em regras.
    A resolução é sempre uma DECISÃO ADMINISTRATIVA HUMANA.
    
    Args:
        contratos: Lista de contratos
        
    Returns:
        Lista de alertas ordenados por criticidade, todos com status ATIVO
    """
    alertas = []
    hoje = datetime.now()
    
    for contrato in contratos:
        # Verifica vigência
        data_fim = contrato.get('data_fim')
        if isinstance(data_fim, str):
            data_fim = datetime.fromisoformat(data_fim)
        
        if data_fim:
            dias_restantes = (data_fim - hoje).days
            
            # ALERTA CRÍTICO: Vigência < 60 dias
            if dias_restantes < 60 and dias_restantes >= 0:
                alertas.append({
                    'id': f"VIG_CRIT_{contrato['id']}",
                    'status': STATUS_ATIVO,
                    'tipo': 'critico',
                    'categoria': 'Vigência',
                    'titulo': f'Vigência crítica: {dias_restantes} dias',
                    'descricao': f"Contrato {contrato['numero']} vence em {dias_restantes} dias. Providenciar prorrogação ou nova licitação urgentemente.",
                    'contrato_id': contrato['id'],
                    'contrato_numero': contrato['numero'],
                    'dias_restantes': dias_restantes,
                    'data_alerta': hoje,
                    'acao_sugerida': 'prorrogacao'
                })
            
            elif dias_restantes >= 60 and dias_restantes <= 120:
                alerta = {
                    'id': f"VIG_ATEN_{contrato['id']}",
                    'status': STATUS_ATIVO,
                    'tipo': 'atencao',
                    'categoria': 'Vigência',
                    'titulo': f'Vigência requer atenção: {dias_restantes} dias',
                    'descricao': f"Contrato {contrato['numero']} vence em {dias_restantes} dias. Planejar renovação ou nova contratação.",
                    'contrato_id': contrato['id'],
                    'contrato_numero': contrato['numero'],
                    'dias_restantes': dias_restantes,
                    'data_alerta': hoje,
                    'acao_sugerida': 'planejamento'
                }
                alertas.append(alerta)
                if criar_alerta_dual:
                    criar_alerta_dual(alerta)
            
            # ALERTA VENCIDO
            elif dias_restantes < 0:
                alerta = {
                    'id': f"VIG_VENC_{contrato['id']}",
                    'status': STATUS_ATIVO,
                    'tipo': 'critico',
                    'categoria': 'Vigência',
                    'titulo': f'Contrato VENCIDO há {abs(dias_restantes)} dias',
                    'descricao': f"Contrato {contrato['numero']} está VENCIDO. Verificar situação imediatamente.",
                    'contrato_id': contrato['id'],
                    'contrato_numero': contrato['numero'],
                    'dias_restantes': dias_restantes,
                    'data_alerta': hoje,
                    'acao_sugerida': 'verificacao'
                }
                alertas.append(alerta)
                if criar_alerta_dual:
                    criar_alerta_dual(alerta)
        
        # ALERTA STATUS CRÍTICO
        if contrato.get('status') == 'critico':
            alerta = {
                'id': f"STATUS_CRIT_{contrato['id']}",
                'status': STATUS_ATIVO,
                'tipo': 'critico',
                'categoria': 'Status',
                'titulo': 'Contrato com status CRÍTICO',
                'descricao': f"Contrato {contrato['numero']} está marcado como crítico. Requer atenção imediata.",
                'contrato_id': contrato['id'],
                'contrato_numero': contrato['numero'],
                'data_alerta': hoje
            }
            alertas.append(alerta)
            if criar_alerta_dual:
                criar_alerta_dual(alerta)
        
        # ALERTA PENDÊNCIAS
        pendencias = contrato.get('pendencias', [])
        if pendencias:
            alerta = {
                'id': f"PEND_{contrato['id']}",
                'status': STATUS_ATIVO,
                'tipo': 'atencao',
                'categoria': 'Pendências',
                'titulo': f'{len(pendencias)} pendência(s) identificada(s)',
                'descricao': f"Contrato {contrato['numero']}: {', '.join(pendencias[:2])}{'...' if len(pendencias) > 2 else ''}",
                'contrato_id': contrato['id'],
                'contrato_numero': contrato['numero'],
                'total_pendencias': len(pendencias),
                'data_alerta': hoje,
                'acao_sugerida': 'resolucao'
            }
            alertas.append(alerta)
            if criar_alerta_dual:
                criar_alerta_dual(alerta)
        
        # ALERTA VALOR ALTO (> R$ 50M)
        valor = contrato.get('valor', 0)
        if valor > 50_000_000:
            alerta = {
                'id': f"VALOR_ALTO_{contrato['id']}",
                'status': STATUS_ATIVO,
                'tipo': 'info',
                'categoria': 'Valor',
                'titulo': f'Contrato de alto valor: R$ {valor/1_000_000:.1f}M',
                'descricao': f"Contrato {contrato['numero']} possui valor elevado. Acompanhamento especial recomendado.",
                'contrato_id': contrato['id'],
                'contrato_numero': contrato['numero'],
                'valor': valor,
                'data_alerta': hoje,
                'acao_sugerida': 'acompanhamento'
            }
            alertas.append(alerta)
            if criar_alerta_dual:
                criar_alerta_dual(alerta)
    
    # Ordena por criticidade e dias restantes
    prioridade = {'critico': 0, 'atencao': 1, 'info': 2}
    alertas.sort(key=lambda x: (prioridade.get(x['tipo'], 3), x.get('dias_restantes', 999)))
    
    return alertas


def get_alertas_por_tipo(alertas: List[Dict]) -> Dict[str, int]:
    """
    Conta alertas por tipo.
    
    Args:
        alertas: Lista de alertas
        
    Returns:
        Dicionário com contagens por tipo
    """
    contagens = {
        'critico': 0,
        'atencao': 0,
        'info': 0
    }
    
    for alerta in alertas:
        tipo = alerta.get('tipo', 'info')
        contagens[tipo] = contagens.get(tipo, 0) + 1
    
    return contagens


def get_alertas_por_categoria(alertas: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Agrupa alertas por categoria.
    
    Args:
        alertas: Lista de alertas
        
    Returns:
        Dicionário com alertas agrupados por categoria
    """
    agrupados = {}
    
    for alerta in alertas:
        categoria = alerta.get('categoria', 'Outros')
        if categoria not in agrupados:
            agrupados[categoria] = []
        agrupados[categoria].append(alerta)
    
    return agrupados


def upsert_ff_alerts(alertas_ff: List[Dict], contrato: Dict) -> List[Dict]:
    """
    Insere ou atualiza alertas de execução físico-financeira.
    
    Garante que:
    - Alertas FF são adicionados aos alertas do contrato
    - Não há duplicatas (baseado em ID estável)
    - Metadados do contrato são preenchidos corretamente
    
    Args:
        alertas_ff: Lista de alertas FF calculados
        contrato: Dicionário do contrato para preencher metadados
        
    Returns:
        Lista de alertas FF processados
    """
    # Enriquece alertas com dados do contrato
    for alerta in alertas_ff:
        alerta['contrato_numero'] = contrato.get('numero', contrato.get('id'))
        alerta['status'] = STATUS_ATIVO
    
    return alertas_ff


def merge_alertas_contratuais_e_ff(alertas_contratuais: List[Dict], alertas_ff: List[Dict]) -> List[Dict]:
    """
    Mescla alertas contratuais (vigência, status, etc.) com alertas FF.
    
    Remove duplicatas baseadas no ID do alerta.
    
    Args:
        alertas_contratuais: Alertas gerados por calcular_alertas()
        alertas_ff: Alertas de execução físico-financeira
        
    Returns:
        Lista unificada de alertas sem duplicatas
    """
    # Cria dicionário por ID para evitar duplicatas
    alertas_dict = {}
    
    for alerta in alertas_contratuais:
        alertas_dict[alerta['id']] = alerta
    
    for alerta in alertas_ff:
        # Sobrescreve se já existir (prioriza FF)
        alertas_dict[alerta['id']] = alerta
    
    # Ordena por criticidade
    alertas_merged = list(alertas_dict.values())
    prioridade = {'critico': 0, 'atencao': 1, 'info': 2}
    alertas_merged.sort(key=lambda x: (prioridade.get(x['tipo'], 3), x.get('dias_restantes', 999)))
    
    return alertas_merged


def registrar_resolucao_alerta(alerta: Dict, justificativa: str, usuario: str = "Gestor") -> Dict:
    """
    Registra formalmente a resolução de um alerta.
    
    IMPORTANTE: Este registro constitui ATO ADMINISTRATIVO.
    A resolução é sempre uma DECISÃO HUMANA rastreável.
    
    Args:
        alerta: Alerta a ser resolvido
        justificativa: Justificativa obrigatória da resolução
        usuario: Usuário responsável pela resolução
        
    Returns:
        Dicionário com dados da resolução para histórico
    """
    from datetime import datetime
    
    if not justificativa or not justificativa.strip():
        raise ValueError("Justificativa obrigatória para resolução de alerta")
    
    resolucao = {
        "alerta_id": alerta.get("id"),
        "alerta_tipo": alerta.get("tipo"),
        "alerta_categoria": alerta.get("categoria"),
        "alerta_titulo": alerta.get("titulo"),
        "status_anterior": alerta.get("status", STATUS_ATIVO),
        "status_novo": STATUS_RESOLVIDO,
        "justificativa": justificativa.strip(),
        "usuario": usuario,
        "data_resolucao": datetime.now().isoformat(),
        "contrato_id": alerta.get("contrato_id"),
        "contrato_numero": alerta.get("contrato_numero")
    }
    
    return resolucao


def carregar_alertas_resolvidos(contrato_id: str = None) -> List[Dict]:
    """
    Carrega histórico de alertas resolvidos para auditoria.
    
    Args:
        contrato_id: Se informado, filtra por contrato específico
        
    Returns:
        Lista de alertas resolvidos com metadados completos
    """
    import json
    from pathlib import Path
    
    arquivo = Path("data/alertas_resolvidos.json")
    if not arquivo.exists():
        return []
    
    try:
        with open(arquivo, "r") as f:
            dados = json.load(f)
            
        if not isinstance(dados, list):
            return []
        
        # Filtra por contrato se especificado
        if contrato_id:
            dados = [a for a in dados if a.get("contrato_id") == contrato_id]
        
        return dados
        
    except Exception:
        return []


def obter_estatisticas_resolucoes() -> Dict:
    """
    Gera estatísticas de alertas resolvidos para relatórios.
    
    Returns:
        Dicionário com estatísticas agregadas
    """
    resolvidos = carregar_alertas_resolvidos()
    
    stats = {
        "total": len(resolvidos),
        "por_tipo": {},
        "por_categoria": {},
        "por_usuario": {},
        "ultimas_resolucoes": []
    }
    
    for alerta in resolvidos:
        # Contagem por tipo
        tipo = alerta.get("alerta_tipo", "Desconhecido")
        stats["por_tipo"][tipo] = stats["por_tipo"].get(tipo, 0) + 1
        
        # Contagem por categoria
        categoria = alerta.get("alerta_categoria", "Desconhecido")
        stats["por_categoria"][categoria] = stats["por_categoria"].get(categoria, 0) + 1
        
        # Contagem por usuário
        usuario = alerta.get("usuario", "Desconhecido")
        stats["por_usuario"][usuario] = stats["por_usuario"].get(usuario, 0) + 1
    
    # Ordena por data (mais recentes primeiro)
    resolvidos_ordenados = sorted(
        resolvidos, 
        key=lambda x: x.get("data", ""), 
        reverse=True
    )
    stats["ultimas_resolucoes"] = resolvidos_ordenados[:10]
    
    return stats
