"""
Serviço de Ciclo de Vida de Alertas V2
========================================
Implementa o modelo evolutivo de alertas com ciclo de vida completo.

MODELO V2: Alerta como Processo
- Alerta não é apenas notificação, é um PROCESSO com estados
- Cada decisão gera consequências estruturadas
- Encadeamento automático de alertas derivados
- Rastreamento completo de ações e transições
- Cálculo de risco e janela de segurança

COMPATIBILIDADE:
- Lê dados V1 sem modificá-los
- Permite migração gradual
- Mantém integridade referencial
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import json
import uuid

# ========================================
# CONSTANTES
# ========================================

# Estados do ciclo de vida (V2)
ESTADO_NOVO = "novo"
ESTADO_EM_ANALISE = "em_analise"
ESTADO_PROVIDENCIA_EM_CURSO = "providencia_em_curso"
ESTADO_AGUARDANDO_PRAZO = "aguardando_prazo"
ESTADO_RESOLVIDO = "resolvido"
ESTADO_ENCERRADO = "encerrado"
ESTADO_ESCALONADO = "escalonado"

# Tipos de alerta (expandido)
TIPO_PREVENTIVO = "preventivo"
TIPO_OPERACIONAL = "operacional"
TIPO_CRITICO = "critico"
TIPO_ESCALONADO = "escalonado"
TIPO_INFORMATIVO = "informativo"

# Categorias
CATEGORIA_VIGENCIA = "Vigência"
CATEGORIA_EXECUCAO_FF = "Execução Físico-Financeira"
CATEGORIA_DOCUMENTACAO = "Documentação"
CATEGORIA_CONFORMIDADE = "Conformidade"

# Tipos de ação
ACAO_DECISAO_RENOVAR = "decisao_renovar"
ACAO_DECISAO_NAO_RENOVAR = "decisao_nao_renovar"
ACAO_DECISAO_LICITAR = "decisao_licitar"
ACAO_PROVIDENCIA_INICIAR_PROCESSO = "providencia_iniciar_processo"
ACAO_PROVIDENCIA_SOLICITAR_DOC = "providencia_solicitar_doc"
ACAO_JUSTIFICATIVA_ADIAMENTO = "justificativa_adiamento"
ACAO_VERIFICACAO_REALIZADA = "verificacao_realizada"

# Níveis de criticidade
CRITICIDADE_BAIXA = "baixa"
CRITICIDADE_MEDIA = "media"
CRITICIDADE_ALTA = "alta"
CRITICIDADE_URGENTE = "urgente"

# Caminhos dos arquivos
DATA_DIR = Path(__file__).parent.parent / "data"
ALERTAS_V2_FILE = DATA_DIR / "alertas_ciclo_vida.json"
ACOES_FILE = DATA_DIR / "acoes_alertas.json"


# ========================================
# FUNÇÕES DE PERSISTÊNCIA
# ========================================

def _load_alertas_v2() -> List[Dict]:
    """Carrega alertas V2 do arquivo JSON"""
    if ALERTAS_V2_FILE.exists():
        with open(ALERTAS_V2_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def _save_alertas_v2(alertas: List[Dict]):
    """Salva alertas V2 no arquivo JSON"""
    ALERTAS_V2_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ALERTAS_V2_FILE, 'w', encoding='utf-8') as f:
        json.dump(alertas, f, indent=2, ensure_ascii=False, default=str)


def _load_acoes() -> List[Dict]:
    """Carrega ações registradas do arquivo JSON"""
    if ACOES_FILE.exists():
        with open(ACOES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def _save_acoes(acoes: List[Dict]):
    """Salva ações no arquivo JSON"""
    ACOES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ACOES_FILE, 'w', encoding='utf-8') as f:
        json.dump(acoes, f, indent=2, ensure_ascii=False, default=str)


# ========================================
# CRIAÇÃO E GERENCIAMENTO DE ALERTAS V2
# ========================================

def criar_alerta_v2(
    tipo: str,
    categoria: str,
    titulo: str,
    descricao: str,
    contrato_id: str,
    contrato_numero: str,
    responsavel: str,
    prazo_resposta_dias: int,
    criticidade: str = CRITICIDADE_MEDIA,
    alerta_origem_id: Optional[str] = None,
    geracao: int = 1,
    metadados: Optional[Dict] = None
) -> Dict:
    """
    Cria um novo alerta V2 com estrutura completa de ciclo de vida.
    
    Args:
        tipo: Tipo do alerta (preventivo, operacional, crítico, escalonado, informativo)
        categoria: Categoria do alerta (Vigência, Execução FF, etc.)
        titulo: Título descritivo do alerta
        descricao: Descrição detalhada
        contrato_id: ID do contrato relacionado
        contrato_numero: Número do contrato
        responsavel: Identificador do gestor responsável
        prazo_resposta_dias: Prazo em dias para resposta
        criticidade: Nível de criticidade (baixa, media, alta, urgente)
        alerta_origem_id: ID do alerta que originou este (encadeamento)
        geracao: Número da geração no encadeamento (1 = alerta raiz)
        metadados: Metadados adicionais específicos do contexto
        
    Returns:
        Dicionário com o alerta criado
    """
    agora = datetime.now()
    prazo_resposta = agora + timedelta(days=prazo_resposta_dias)
    
    alerta = {
        # Identificação
        'id': str(uuid.uuid4()),
        'tipo': tipo,
        'categoria': categoria,
        'titulo': titulo,
        'descricao': descricao,
        
        # Vinculação
        'contrato_id': contrato_id,
        'contrato_numero': contrato_numero,
        'responsavel': responsavel,
        
        # Ciclo de vida
        'estado': ESTADO_NOVO,
        'estado_anterior': None,
        'data_criacao': agora.isoformat(),
        'data_ultima_atualizacao': agora.isoformat(),
        
        # Prazos e criticidade
        'prazo_resposta': prazo_resposta.isoformat(),
        'prazo_resposta_dias': prazo_resposta_dias,
        'criticidade': criticidade,
        'dias_restantes': prazo_resposta_dias,
        'janela_seguranca_dias': None,  # Será calculado
        
        # Encadeamento
        'alerta_origem_id': alerta_origem_id,
        'geracao': geracao,
        'alertas_derivados': [],
        
        # Análise e risco
        'score_risco': None,  # Será calculado
        'fatores_risco': {},
        'recomendacao_ia': None,
        
        # Ações e histórico
        'acoes_ids': [],
        'historico_estados': [
            {
                'estado': ESTADO_NOVO,
                'data': agora.isoformat(),
                'usuario': 'sistema',
                'observacao': 'Alerta criado automaticamente'
            }
        ],
        
        # Metadados
        'metadados': metadados or {},
        'versao': 2
    }
    
    # Salva o alerta
    alertas = _load_alertas_v2()
    alertas.append(alerta)
    _save_alertas_v2(alertas)
    
    return alerta


def get_alerta_v2_por_id(alerta_id: str) -> Optional[Dict]:
    """Busca um alerta V2 pelo ID"""
    alertas = _load_alertas_v2()
    for alerta in alertas:
        if alerta['id'] == alerta_id:
            return alerta
    return None


def listar_alertas_v2(
    contrato_id: Optional[str] = None,
    estado: Optional[str] = None,
    tipo: Optional[str] = None,
    responsavel: Optional[str] = None
) -> List[Dict]:
    """
    Lista alertas V2 com filtros opcionais.
    
    Args:
        contrato_id: Filtrar por contrato
        estado: Filtrar por estado
        tipo: Filtrar por tipo
        responsavel: Filtrar por responsável
        
    Returns:
        Lista de alertas filtrados
    """
    alertas = _load_alertas_v2()
    
    # Aplica filtros
    if contrato_id:
        alertas = [a for a in alertas if a['contrato_id'] == contrato_id]
    if estado:
        alertas = [a for a in alertas if a['estado'] == estado]
    if tipo:
        alertas = [a for a in alertas if a['tipo'] == tipo]
    if responsavel:
        alertas = [a for a in alertas if a['responsavel'] == responsavel]
    
    # Atualiza dias_restantes e ordena por criticidade
    return _ordenar_por_criticidade(_atualizar_dias_restantes(alertas))


def _atualizar_dias_restantes(alertas: List[Dict]) -> List[Dict]:
    """Atualiza o campo dias_restantes de cada alerta"""
    agora = datetime.now()
    for alerta in alertas:
        prazo = datetime.fromisoformat(alerta['prazo_resposta'])
        alerta['dias_restantes'] = (prazo - agora).days
    return alertas


def _ordenar_por_criticidade(alertas: List[Dict]) -> List[Dict]:
    """Ordena alertas por criticidade e dias restantes"""
    ordem_criticidade = {
        CRITICIDADE_URGENTE: 0,
        CRITICIDADE_ALTA: 1,
        CRITICIDADE_MEDIA: 2,
        CRITICIDADE_BAIXA: 3
    }
    
    return sorted(
        alertas,
        key=lambda a: (
            ordem_criticidade.get(a['criticidade'], 99),
            a['dias_restantes']
        )
    )


# ========================================
# TRANSIÇÕES DE ESTADO
# ========================================

def transicionar_estado(
    alerta_id: str,
    novo_estado: str,
    usuario: str,
    observacao: Optional[str] = None
) -> bool:
    """
    Realiza transição de estado de um alerta.
    
    Args:
        alerta_id: ID do alerta
        novo_estado: Novo estado desejado
        usuario: Usuário que está fazendo a transição
        observacao: Observação opcional sobre a transição
        
    Returns:
        True se transição foi bem-sucedida
    """
    alertas = _load_alertas_v2()
    alerta_encontrado = False
    
    for alerta in alertas:
        if alerta['id'] == alerta_id:
            alerta_encontrado = True
            estado_anterior = alerta['estado']
            agora = datetime.now()
            
            # Atualiza o alerta
            alerta['estado_anterior'] = estado_anterior
            alerta['estado'] = novo_estado
            alerta['data_ultima_atualizacao'] = agora.isoformat()
            
            # Adiciona entrada no histórico
            alerta['historico_estados'].append({
                'estado': novo_estado,
                'estado_anterior': estado_anterior,
                'data': agora.isoformat(),
                'usuario': usuario,
                'observacao': observacao or f'Transição de {estado_anterior} para {novo_estado}'
            })
            
            break
    
    if alerta_encontrado:
        _save_alertas_v2(alertas)
        return True
    return False


# ========================================
# REGISTRO DE AÇÕES
# ========================================

def registrar_acao(
    alerta_id: str,
    tipo_acao: str,
    usuario: str,
    justificativa: str,
    decisao: Optional[str] = None,
    prazo_novo_dias: Optional[int] = None,
    documentos: Optional[List[str]] = None,
    metadados_acao: Optional[Dict] = None
) -> Dict:
    """
    Registra uma ação administrativa vinculada a um alerta.
    
    Args:
        alerta_id: ID do alerta
        tipo_acao: Tipo da ação (decisão, providência, justificativa, etc.)
        usuario: Usuário que realizou a ação
        justificativa: Justificativa textual da ação
        decisao: Decisão tomada (se aplicável)
        prazo_novo_dias: Novo prazo definido (se aplicável)
        documentos: Lista de URLs/IDs de documentos anexados
        metadados_acao: Metadados adicionais da ação
        
    Returns:
        Dicionário com a ação registrada
    """
    agora = datetime.now()
    
    acao = {
        'id': str(uuid.uuid4()),
        'alerta_id': alerta_id,
        'tipo_acao': tipo_acao,
        'usuario': usuario,
        'data_acao': agora.isoformat(),
        'justificativa': justificativa,
        'decisao': decisao,
        'prazo_novo_dias': prazo_novo_dias,
        'documentos': documentos or [],
        'metadados': metadados_acao or {},
        
        # Análise IA (será preenchido posteriormente)
        'justificativa_categoria': None,
        'justificativa_completude': None,
        'fundamentacao_legal': None
    }
    
    # Salva a ação
    acoes = _load_acoes()
    acoes.append(acao)
    _save_acoes(acoes)
    
    # Vincula ação ao alerta
    alertas = _load_alertas_v2()
    for alerta in alertas:
        if alerta['id'] == alerta_id:
            alerta['acoes_ids'].append(acao['id'])
            alerta['data_ultima_atualizacao'] = agora.isoformat()
            break
    _save_alertas_v2(alertas)
    
    return acao


def get_acoes_por_alerta(alerta_id: str) -> List[Dict]:
    """Retorna todas as ações de um alerta"""
    acoes = _load_acoes()
    return [a for a in acoes if a['alerta_id'] == alerta_id]


# ========================================
# ENCADEAMENTO DE ALERTAS
# ========================================

def criar_alerta_derivado(
    alerta_origem_id: str,
    tipo: str,
    titulo: str,
    descricao: str,
    prazo_resposta_dias: int,
    criticidade: str = CRITICIDADE_MEDIA,
    metadados: Optional[Dict] = None
) -> Optional[Dict]:
    """
    Cria um alerta derivado a partir de outro alerta (encadeamento).
    
    Args:
        alerta_origem_id: ID do alerta que originou este
        tipo: Tipo do novo alerta
        titulo: Título do novo alerta
        descricao: Descrição
        prazo_resposta_dias: Prazo em dias
        criticidade: Nível de criticidade
        metadados: Metadados adicionais
        
    Returns:
        Alerta derivado criado ou None se alerta origem não existe
    """
    alerta_origem = get_alerta_v2_por_id(alerta_origem_id)
    if not alerta_origem:
        return None
    
    # Cria o alerta derivado
    alerta_derivado = criar_alerta_v2(
        tipo=tipo,
        categoria=alerta_origem['categoria'],
        titulo=titulo,
        descricao=descricao,
        contrato_id=alerta_origem['contrato_id'],
        contrato_numero=alerta_origem['contrato_numero'],
        responsavel=alerta_origem['responsavel'],
        prazo_resposta_dias=prazo_resposta_dias,
        criticidade=criticidade,
        alerta_origem_id=alerta_origem_id,
        geracao=alerta_origem['geracao'] + 1,
        metadados=metadados
    )
    
    # Atualiza o alerta origem para incluir referência ao derivado
    alertas = _load_alertas_v2()
    for alerta in alertas:
        if alerta['id'] == alerta_origem_id:
            alerta['alertas_derivados'].append(alerta_derivado['id'])
            alerta['data_ultima_atualizacao'] = datetime.now().isoformat()
            break
    _save_alertas_v2(alertas)
    
    return alerta_derivado


def get_cadeia_alertas(alerta_id: str) -> Tuple[Optional[Dict], List[Dict]]:
    """
    Retorna a cadeia completa de alertas (origem + derivados).
    
    Returns:
        Tupla (alerta_raiz, lista_de_alertas_na_cadeia)
    """
    alerta = get_alerta_v2_por_id(alerta_id)
    if not alerta:
        return None, []
    
    # Encontra a raiz
    alerta_raiz = alerta
    while alerta_raiz['alerta_origem_id']:
        alerta_raiz = get_alerta_v2_por_id(alerta_raiz['alerta_origem_id'])
        if not alerta_raiz:
            break
    
    # Coleta todos os derivados recursivamente
    def _coletar_derivados(alerta_id: str) -> List[Dict]:
        alerta_atual = get_alerta_v2_por_id(alerta_id)
        if not alerta_atual:
            return []
        
        resultado = [alerta_atual]
        for derivado_id in alerta_atual['alertas_derivados']:
            resultado.extend(_coletar_derivados(derivado_id))
        return resultado
    
    cadeia = _coletar_derivados(alerta_raiz['id']) if alerta_raiz else []
    
    return alerta_raiz, cadeia


# ========================================
# CÁLCULO DE RISCO E MÉTRICAS
# ========================================

def calcular_score_risco(alerta_id: str) -> float:
    """
    Calcula score de risco multifatorial para um alerta.
    
    Fatores considerados:
    - Dias restantes vs prazo total (urgência)
    - Criticidade declarada
    - Histórico de adiamentos
    - Geração no encadeamento (alertas derivados são mais arriscados)
    
    Returns:
        Score de 0.0 a 1.0 (quanto maior, maior o risco)
    """
    alerta = get_alerta_v2_por_id(alerta_id)
    if not alerta:
        return 0.0
    
    score = 0.0
    fatores = {}
    
    # Fator 1: Urgência temporal (peso 0.35)
    dias_restantes = alerta['dias_restantes']
    prazo_total = alerta['prazo_resposta_dias']
    
    if dias_restantes <= 0:
        fator_tempo = 1.0
    elif prazo_total > 0:
        fator_tempo = 1.0 - (dias_restantes / prazo_total)
        fator_tempo = max(0.0, min(1.0, fator_tempo))
    else:
        fator_tempo = 0.5
    
    fatores['urgencia_temporal'] = fator_tempo
    score += fator_tempo * 0.35
    
    # Fator 2: Criticidade (peso 0.30)
    map_criticidade = {
        CRITICIDADE_BAIXA: 0.2,
        CRITICIDADE_MEDIA: 0.5,
        CRITICIDADE_ALTA: 0.8,
        CRITICIDADE_URGENTE: 1.0
    }
    fator_criticidade = map_criticidade.get(alerta['criticidade'], 0.5)
    fatores['criticidade'] = fator_criticidade
    score += fator_criticidade * 0.30
    
    # Fator 3: Histórico de ações (peso 0.20)
    acoes = get_acoes_por_alerta(alerta_id)
    adiamentos = sum(1 for a in acoes if a['tipo_acao'] == ACAO_JUSTIFICATIVA_ADIAMENTO)
    fator_adiamentos = min(1.0, adiamentos * 0.25)
    fatores['historico_adiamentos'] = fator_adiamentos
    score += fator_adiamentos * 0.20
    
    # Fator 4: Profundidade no encadeamento (peso 0.15)
    geracao = alerta['geracao']
    fator_geracao = min(1.0, (geracao - 1) * 0.3)
    fatores['geracao_alerta'] = fator_geracao
    score += fator_geracao * 0.15
    
    # Atualiza o alerta com o score
    alertas = _load_alertas_v2()
    for a in alertas:
        if a['id'] == alerta_id:
            a['score_risco'] = round(score, 3)
            a['fatores_risco'] = fatores
            break
    _save_alertas_v2(alertas)
    
    return round(score, 3)


def calcular_janela_seguranca(alerta_id: str, tempo_medio_execucao_dias: int) -> int:
    """
    Calcula a janela de segurança real para execução de uma ação.
    
    Janela de segurança = dias_restantes - tempo_médio_execução
    
    Se janela < 0, indica que o prazo nominal é insuficiente.
    
    Args:
        alerta_id: ID do alerta
        tempo_medio_execucao_dias: Tempo médio histórico para executar este tipo de ação
        
    Returns:
        Janela de segurança em dias (pode ser negativa)
    """
    alerta = get_alerta_v2_por_id(alerta_id)
    if not alerta:
        return 0
    
    janela = alerta['dias_restantes'] - tempo_medio_execucao_dias
    
    # Atualiza o alerta
    alertas = _load_alertas_v2()
    for a in alertas:
        if a['id'] == alerta_id:
            a['janela_seguranca_dias'] = janela
            a['metadados']['tempo_medio_execucao_dias'] = tempo_medio_execucao_dias
            break
    _save_alertas_v2(alertas)
    
    return janela


# ========================================
# ESTATÍSTICAS E BI
# ========================================

def get_estatisticas_alertas_v2() -> Dict:
    """
    Retorna estatísticas gerais dos alertas V2.
    
    Returns:
        Dicionário com métricas agregadas
    """
    alertas = _load_alertas_v2()
    acoes = _load_acoes()
    
    # Contadores por estado
    por_estado = {}
    for alerta in alertas:
        estado = alerta['estado']
        por_estado[estado] = por_estado.get(estado, 0) + 1
    
    # Contadores por tipo
    por_tipo = {}
    for alerta in alertas:
        tipo = alerta['tipo']
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
    
    # Contadores por criticidade
    por_criticidade = {}
    for alerta in alertas:
        crit = alerta['criticidade']
        por_criticidade[crit] = por_criticidade.get(crit, 0) + 1
    
    # Risco médio
    scores = [a['score_risco'] for a in alertas if a['score_risco'] is not None]
    risco_medio = sum(scores) / len(scores) if scores else 0.0
    
    # Alertas em risco alto (score > 0.7)
    alertas_risco_alto = len([s for s in scores if s > 0.7])
    
    return {
        'total_alertas': len(alertas),
        'total_acoes': len(acoes),
        'por_estado': por_estado,
        'por_tipo': por_tipo,
        'por_criticidade': por_criticidade,
        'risco_medio': round(risco_medio, 3),
        'alertas_risco_alto': alertas_risco_alto
    }


# ========================================
# COMPATIBILIDADE COM V1
# ========================================

def importar_alerta_v1_para_v2(alerta_v1: Dict) -> Dict:
    """
    Converte um alerta V1 para o formato V2.
    NÃO modifica o alerta V1 original.
    
    Args:
        alerta_v1: Alerta no formato antigo
        
    Returns:
        Alerta no formato V2
    """
    # Mapeia tipo V1 para V2
    map_tipo = {
        'critico': TIPO_CRITICO,
        'atencao': TIPO_PREVENTIVO,
        'info': TIPO_INFORMATIVO
    }
    
    tipo_v2 = map_tipo.get(alerta_v1.get('tipo', 'info'), TIPO_PREVENTIVO)
    
    # Mapeia criticidade baseada no tipo
    map_criticidade = {
        'critico': CRITICIDADE_ALTA,
        'atencao': CRITICIDADE_MEDIA,
        'info': CRITICIDADE_BAIXA
    }
    criticidade = map_criticidade.get(alerta_v1.get('tipo', 'info'), CRITICIDADE_MEDIA)
    
    # Define prazo baseado em dias_restantes
    dias_restantes = alerta_v1.get('dias_restantes', 30)
    prazo = max(7, dias_restantes)  # Mínimo 7 dias
    
    # Cria alerta V2
    return criar_alerta_v2(
        tipo=tipo_v2,
        categoria=alerta_v1.get('categoria', CATEGORIA_VIGENCIA),
        titulo=alerta_v1.get('titulo', 'Alerta importado'),
        descricao=alerta_v1.get('descricao', ''),
        contrato_id=alerta_v1.get('contrato_id', ''),
        contrato_numero=alerta_v1.get('contrato_numero', ''),
        responsavel='não_definido',
        prazo_resposta_dias=prazo,
        criticidade=criticidade,
        metadados={
            'importado_de_v1': True,
            'id_v1': alerta_v1.get('id'),
            'data_alerta_v1': str(alerta_v1.get('data_alerta', ''))
        }
    )
