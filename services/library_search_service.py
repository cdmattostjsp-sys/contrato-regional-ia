"""
Serviço de busca textual na Biblioteca Institucional
======================================================
FASE 2.1 - Biblioteca Institucional Curada

DUAS FONTES DE BUSCA:
1. Biblioteca Institucional Curada (knowledge/index.json) - PRIORIDADE
2. Índice SQLite legado (.cache/biblioteca_index.sqlite) - FALLBACK

A busca institucional é usada pelo COPILOTO para contextualizar respostas
com documentos oficiais do TJSP.

AUTOR: Fase 2.1 - Biblioteca de Conhecimento
DATA: Janeiro/2026
"""
import sqlite3
import json
import re
from pathlib import Path
from typing import List, Dict, Optional
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminhos
INDEX_PATH_SQLITE = Path(".cache/biblioteca_index.sqlite")
INDEX_PATH_JSON = Path("knowledge/index.json")
TEXTOS_DIR = Path("knowledge/textos_extraidos")


# ============================================================================
# BUSCA NA BIBLIOTECA INSTITUCIONAL CURADA (FASE 2.1)
# ============================================================================

def buscar_documentos_relevantes(
    pergunta: str,
    filtros: Dict = None,
    limite: int = 5,
    tamanho_trecho: int = 500
) -> List[Dict]:
    """
    Busca documentos institucionais relevantes para a pergunta.
    
    IMPORTANTE: Retorna apenas documentos com status ATIVO.
    Esta função é consumida pelo COPILOTO para contextualizar respostas.
    
    Args:
        pergunta: Pergunta do usuário (usada para busca textual)
        filtros: Dict opcional com filtros (tipo, area, etc.)
        limite: Número máximo de resultados
        tamanho_trecho: Tamanho máximo do trecho retornado
    
    Returns:
        Lista de dicts com:
        - titulo: Título do documento
        - tipo: Tipo de documento
        - versao: Versão
        - area: Área responsável
        - trecho: Trecho relevante do texto
        - referencia: Referência institucional formatada
        - doc_id: ID único do documento
    """
    resultados = []
    
    try:
        # Carrega índice da biblioteca institucional
        if not INDEX_PATH_JSON.exists():
            logger.info("Índice da biblioteca institucional não encontrado")
            return []
        
        with open(INDEX_PATH_JSON, "r", encoding="utf-8") as f:
            documentos = json.load(f)
        
        if not documentos:
            return []
        
        # Filtra apenas documentos ATIVOS
        documentos_ativos = [d for d in documentos if d.get("status") == "ATIVO"]
        
        if not documentos_ativos:
            logger.info("Nenhum documento ATIVO na biblioteca")
            return []
        
        # Aplica filtros adicionais
        if filtros:
            for campo, valor in filtros.items():
                documentos_ativos = [d for d in documentos_ativos if d.get(campo) == valor]
        
        # Extrai palavras-chave da pergunta para busca
        palavras_chave = _extrair_palavras_chave(pergunta)
        
        if not palavras_chave:
            # Se não há palavras-chave, retorna os primeiros documentos ativos
            for doc in documentos_ativos[:limite]:
                trecho = _carregar_trecho_documento(doc, tamanho_trecho)
                resultados.append(_formatar_resultado(doc, trecho))
            return resultados
        
        # Busca por relevância
        documentos_pontuados = []
        for doc in documentos_ativos:
            pontuacao = _calcular_relevancia(doc, palavras_chave)
            if pontuacao > 0:
                documentos_pontuados.append((doc, pontuacao))
        
        # Ordena por relevância
        documentos_pontuados.sort(key=lambda x: x[1], reverse=True)
        
        # Monta resultados
        for doc, pontuacao in documentos_pontuados[:limite]:
            trecho = _carregar_trecho_documento(doc, tamanho_trecho, palavras_chave)
            resultados.append(_formatar_resultado(doc, trecho))
        
        logger.info(f"Busca institucional: {len(resultados)} documentos encontrados para '{pergunta[:50]}...'")
        
    except Exception as e:
        logger.error(f"Erro na busca institucional: {e}")
    
    return resultados


def _extrair_palavras_chave(texto: str) -> List[str]:
    """
    Extrai palavras-chave relevantes do texto.
    Remove stopwords e palavras muito curtas.
    """
    # Stopwords básicas em português
    stopwords = {
        'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas',
        'de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'nas', 'nos',
        'por', 'para', 'com', 'sem', 'sob', 'sobre',
        'e', 'ou', 'mas', 'que', 'se', 'como', 'quando', 'onde',
        'qual', 'quais', 'quem', 'isso', 'isto', 'aquilo',
        'este', 'esta', 'esse', 'essa', 'aquele', 'aquela',
        'meu', 'minha', 'seu', 'sua', 'nosso', 'nossa',
        'ser', 'estar', 'ter', 'haver', 'fazer', 'ir', 'vir',
        'é', 'são', 'foi', 'eram', 'será', 'seria',
        'está', 'estão', 'estava', 'estavam',
        'tem', 'têm', 'tinha', 'tinham',
        'há', 'houve', 'havia',
        'pode', 'podem', 'poderia', 'poderiam',
        'deve', 'devem', 'deveria', 'deveriam'
    }
    
    # Normaliza texto
    texto_lower = texto.lower()
    # Remove pontuação
    texto_limpo = re.sub(r'[^\w\s]', ' ', texto_lower)
    # Divide em palavras
    palavras = texto_limpo.split()
    # Remove stopwords e palavras curtas
    palavras_chave = [p for p in palavras if p not in stopwords and len(p) > 2]
    
    return palavras_chave


def _calcular_relevancia(documento: Dict, palavras_chave: List[str]) -> int:
    """
    Calcula pontuação de relevância do documento para as palavras-chave.
    Considera título, tipo, área e texto extraído.
    """
    pontuacao = 0
    
    # Campos do documento para busca
    titulo = documento.get("titulo", "").lower()
    tipo = documento.get("tipo", "").lower()
    area = documento.get("area", "").lower()
    observacoes = documento.get("observacoes", "").lower()
    
    # Busca nas informações do documento
    for palavra in palavras_chave:
        if palavra in titulo:
            pontuacao += 10  # Peso alto para título
        if palavra in tipo:
            pontuacao += 5
        if palavra in area:
            pontuacao += 5
        if palavra in observacoes:
            pontuacao += 2
    
    # Busca no texto extraído (se disponível)
    if documento.get("texto_extraido") and documento.get("caminho_texto"):
        try:
            caminho_texto = Path(documento["caminho_texto"])
            if caminho_texto.exists():
                with open(caminho_texto, "r", encoding="utf-8") as f:
                    texto = f.read().lower()
                for palavra in palavras_chave:
                    # Conta ocorrências
                    ocorrencias = texto.count(palavra)
                    pontuacao += min(ocorrencias, 20)  # Limita contribuição
        except Exception as e:
            logger.warning(f"Erro ao ler texto do documento: {e}")
    
    return pontuacao


def _carregar_trecho_documento(
    documento: Dict,
    tamanho: int = 500,
    palavras_chave: List[str] = None
) -> str:
    """
    Carrega trecho relevante do texto extraído do documento.
    Se palavras-chave fornecidas, busca trecho que contenha as palavras.
    """
    if not documento.get("texto_extraido") or not documento.get("caminho_texto"):
        return "(Texto não disponível para este documento)"
    
    try:
        caminho_texto = Path(documento["caminho_texto"])
        if not caminho_texto.exists():
            return "(Arquivo de texto não encontrado)"
        
        with open(caminho_texto, "r", encoding="utf-8") as f:
            texto_completo = f.read()
        
        if not texto_completo.strip():
            return "(Documento sem texto extraído)"
        
        # Se há palavras-chave, tenta encontrar trecho que contenha
        if palavras_chave:
            texto_lower = texto_completo.lower()
            melhor_posicao = 0
            melhor_pontuacao = 0
            
            # Busca janela com mais palavras-chave
            for i in range(0, len(texto_completo) - tamanho, 100):
                janela = texto_lower[i:i+tamanho]
                pontuacao = sum(1 for p in palavras_chave if p in janela)
                if pontuacao > melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_posicao = i
            
            if melhor_pontuacao > 0:
                inicio = max(0, melhor_posicao)
                fim = min(len(texto_completo), inicio + tamanho)
                trecho = texto_completo[inicio:fim].strip()
                return f"...{trecho}..." if inicio > 0 else f"{trecho}..."
        
        # Retorna início do documento
        return texto_completo[:tamanho].strip() + "..."
        
    except Exception as e:
        logger.warning(f"Erro ao carregar trecho: {e}")
        return "(Erro ao carregar texto)"


def _formatar_resultado(documento: Dict, trecho: str) -> Dict:
    """
    Formata resultado da busca para consumo pelo COPILOTO.
    """
    return {
        "titulo": documento.get("titulo", "Sem título"),
        "tipo": documento.get("tipo", "Outros"),
        "versao": documento.get("versao", "1.0"),
        "area": documento.get("area", "Não informada"),
        "trecho": trecho,
        "referencia": f"{documento.get('titulo', 'Documento')} (v{documento.get('versao', '?')}) - {documento.get('area', 'TJSP')}",
        "doc_id": documento.get("doc_id", ""),
        "status": documento.get("status", "ATIVO")
    }


def formatar_contexto_institucional(documentos: List[Dict]) -> str:
    """
    Formata documentos encontrados como contexto para o prompt da IA.
    
    Args:
        documentos: Lista de resultados de buscar_documentos_relevantes()
    
    Returns:
        String formatada para inclusão no prompt
    """
    if not documentos:
        return ""
    
    contexto = "[DOCUMENTOS INSTITUCIONAIS VIGENTES]\n\n"
    
    for i, doc in enumerate(documentos, 1):
        contexto += f"--- Documento {i} ---\n"
        contexto += f"Título: {doc['titulo']}\n"
        contexto += f"Tipo: {doc['tipo']}\n"
        contexto += f"Versão: {doc['versao']}\n"
        contexto += f"Área: {doc['area']}\n"
        contexto += f"Referência: {doc['referencia']}\n"
        contexto += f"Trecho relevante:\n{doc['trecho']}\n\n"
    
    return contexto


# ============================================================================
# BUSCA LEGADA (SQLite + FTS5) - MANTIDA PARA COMPATIBILIDADE
# ============================================================================

def search_library(query: str, category: Optional[str] = None, doc_type: Optional[str] = None, limit: int = 10) -> List[Dict]:
    """
    Busca legada no índice SQLite.
    Mantida para compatibilidade com código existente.
    """
    if not INDEX_PATH_SQLITE.exists():
        return []
    
    try:
        conn = sqlite3.connect(INDEX_PATH_SQLITE)
        c = conn.cursor()
        sql = """
        SELECT d.title, d.category, d.doc_type, d.is_scanned, p.page_no, snippet(pages_fts, 2, '<mark>', '</mark>', '...', 20) as snippet
        FROM pages_fts
        JOIN documents d ON d.doc_id = pages_fts.doc_id
        JOIN pages p ON p.doc_id = d.doc_id AND p.page_no = pages_fts.page_no
        WHERE pages_fts.text MATCH ?
        """
        params = [query]
        if category:
            sql += " AND d.category = ?"
            params.append(category)
        if doc_type:
            sql += " AND d.doc_type = ?"
            params.append(doc_type)
        sql += " ORDER BY rank LIMIT ?"
        params.append(limit)
        c.execute(sql, params)
        results = []
        for row in c.fetchall():
            results.append({
                "title": row[0],
                "category": row[1],
                "doc_type": row[2],
                "is_scanned": bool(row[3]),
                "page_no": row[4],
                "snippet": row[5]
            })
        conn.close()
        return results
    except Exception as e:
        logger.error(f"Erro na busca SQLite: {e}")
        return []
