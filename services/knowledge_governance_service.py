"""
Serviço de Governança da Biblioteca de Conhecimento Institucional
==================================================================
FASE 2.1 - Biblioteca Institucional Curada

RESPONSABILIDADES:
- Validar perfil de usuário para upload
- Persistir documentos com versionamento
- Gerenciar metadados institucionais
- Extrair e indexar texto de documentos
- Registrar eventos de auditoria

PRINCÍPIOS:
- Governança explícita e rastreável
- Versionamento imutável (sem sobrescrita)
- Apenas documentos ATIVOS são consumidos pela IA
- Auditoria de todas as operações

AUTOR: Fase 2.1 - Biblioteca de Conhecimento
DATA: Janeiro/2026
"""

import os
import json
import re
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import streamlit as st
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# CONSTANTES E CONFIGURAÇÃO
# ============================================================================

# Diretórios base
KNOWLEDGE_BASE_DIR = Path("knowledge")
DOCUMENTOS_DIR = KNOWLEDGE_BASE_DIR / "documentos"
TEXTOS_DIR = KNOWLEDGE_BASE_DIR / "textos_extraidos"
INDEX_PATH = KNOWLEDGE_BASE_DIR / "index.json"

# Tipos de documento permitidos
TIPOS_DOCUMENTO = [
    "Manual",
    "Nota Técnica",
    "Orientação Jurídica",
    "Caderno Técnico",
    "Instrução Normativa",
    "Guia de Boas Práticas"
]

# Status permitidos
STATUS_DOCUMENTO = ["ATIVO", "REVOGADO"]

# Perfis autorizados para upload
PERFIS_AUTORIZADOS = ["ADMIN", "CURADOR", "JURIDICO"]

# Extensões permitidas
EXTENSOES_PERMITIDAS = [".pdf", ".docx"]


# ============================================================================
# INICIALIZAÇÃO E ESTRUTURA
# ============================================================================

def inicializar_estrutura():
    """
    Inicializa a estrutura de diretórios da biblioteca.
    Cria pastas e index.json se não existirem.
    """
    # Cria diretórios base
    DOCUMENTOS_DIR.mkdir(parents=True, exist_ok=True)
    TEXTOS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Cria subpastas por tipo de documento
    for tipo in TIPOS_DOCUMENTO:
        tipo_slug = _normalizar_nome(tipo)
        (DOCUMENTOS_DIR / tipo_slug).mkdir(exist_ok=True)
    
    # Cria index.json se não existir
    if not INDEX_PATH.exists():
        _salvar_indice([])
        logger.info("Índice da biblioteca inicializado")


def _normalizar_nome(nome: str) -> str:
    """
    Normaliza nome para uso em sistema de arquivos.
    Remove acentos, espaços e caracteres especiais.
    """
    # Remove acentos
    substituicoes = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e',
        'í': 'i',
        'ó': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'ü': 'u',
        'ç': 'c',
        ' ': '_'
    }
    nome_lower = nome.lower()
    for original, substituto in substituicoes.items():
        nome_lower = nome_lower.replace(original, substituto)
    
    # Remove caracteres especiais
    nome_limpo = re.sub(r'[^a-z0-9_]', '', nome_lower)
    return nome_limpo


# ============================================================================
# CONTROLE DE PERFIL
# ============================================================================

def verificar_perfil_autorizado() -> Tuple[bool, str]:
    """
    Verifica se o usuário atual tem perfil autorizado para upload.
    
    Returns:
        Tupla (autorizado: bool, mensagem: str)
    """
    perfil_atual = st.session_state.get("perfil", "").upper()
    
    # Normaliza perfil para comparação
    perfil_normalizado = perfil_atual.replace(" ", "_").upper()
    
    # Verifica se é um perfil autorizado ou contém palavras-chave
    for perfil_permitido in PERFIS_AUTORIZADOS:
        if perfil_permitido in perfil_normalizado:
            return True, f"Perfil autorizado: {perfil_atual}"
    
    # Verifica também se contém palavras-chave de autorização
    palavras_autorizadas = ["ADMIN", "CURADOR", "JURIDICO", "GESTOR", "COORDENADOR"]
    for palavra in palavras_autorizadas:
        if palavra in perfil_normalizado:
            return True, f"Perfil autorizado: {perfil_atual}"
    
    return False, f"Perfil '{perfil_atual}' não autorizado. Perfis permitidos: {', '.join(PERFIS_AUTORIZADOS)}"


def get_usuario_atual() -> str:
    """Retorna o usuário atual da sessão."""
    return st.session_state.get("usuario", "Sistema")


# ============================================================================
# GESTÃO DO ÍNDICE
# ============================================================================

def _carregar_indice() -> List[Dict]:
    """Carrega o índice de documentos."""
    if not INDEX_PATH.exists():
        return []
    try:
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        logger.warning("Erro ao carregar índice, retornando lista vazia")
        return []


def _salvar_indice(documentos: List[Dict]):
    """Salva o índice de documentos."""
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(documentos, f, ensure_ascii=False, indent=2, default=str)


def listar_documentos(filtros: Dict = None) -> List[Dict]:
    """
    Lista documentos do índice com filtros opcionais.
    
    Args:
        filtros: Dict com campos para filtrar (tipo, area, status, etc.)
    
    Returns:
        Lista de documentos que atendem aos filtros
    """
    documentos = _carregar_indice()
    
    if not filtros:
        return documentos
    
    resultado = []
    for doc in documentos:
        match = True
        for campo, valor in filtros.items():
            if campo in doc and doc[campo] != valor:
                match = False
                break
        if match:
            resultado.append(doc)
    
    return resultado


def listar_documentos_ativos() -> List[Dict]:
    """Lista apenas documentos com status ATIVO."""
    return listar_documentos({"status": "ATIVO"})


def buscar_documento_por_id(doc_id: str) -> Optional[Dict]:
    """Busca documento pelo ID único."""
    documentos = _carregar_indice()
    for doc in documentos:
        if doc.get("doc_id") == doc_id:
            return doc
    return None


# ============================================================================
# EXTRAÇÃO DE TEXTO
# ============================================================================

def extrair_texto_documento(caminho_arquivo: str, extensao: str) -> Tuple[bool, str, str]:
    """
    Extrai texto de documento PDF ou DOCX.
    
    Args:
        caminho_arquivo: Caminho do arquivo físico
        extensao: Extensão do arquivo (.pdf ou .docx)
    
    Returns:
        Tupla (sucesso: bool, texto: str, mensagem: str)
    """
    try:
        if extensao.lower() == ".pdf":
            from services.pdf_text_extractor import extract_pdf_pages
            pages, is_scanned, total_chars = extract_pdf_pages(caminho_arquivo)
            
            if is_scanned:
                return False, "", "Documento digitalizado (sem texto pesquisável). OCR não implementado na Fase 2.1."
            
            # Concatena texto de todas as páginas
            texto_completo = "\n\n".join([p["text"] for p in pages])
            return True, texto_completo, f"Texto extraído: {total_chars} caracteres de {len(pages)} páginas"
            
        elif extensao.lower() == ".docx":
            from docx import Document
            doc = Document(caminho_arquivo)
            paragrafos = [p.text for p in doc.paragraphs if p.text.strip()]
            texto_completo = "\n\n".join(paragrafos)
            return True, texto_completo, f"Texto extraído: {len(texto_completo)} caracteres"
            
        else:
            return False, "", f"Extensão não suportada: {extensao}"
            
    except Exception as e:
        logger.error(f"Erro ao extrair texto: {e}")
        return False, "", f"Erro na extração: {str(e)}"


# ============================================================================
# PUBLICAÇÃO DE DOCUMENTOS
# ============================================================================

def validar_metadados(metadados: Dict) -> Tuple[bool, List[str]]:
    """
    Valida metadados obrigatórios do documento.
    
    Args:
        metadados: Dict com campos do formulário
    
    Returns:
        Tupla (valido: bool, erros: List[str])
    """
    erros = []
    
    # Campos obrigatórios
    campos_obrigatorios = ["titulo", "tipo", "area", "versao"]
    for campo in campos_obrigatorios:
        if not metadados.get(campo):
            erros.append(f"Campo obrigatório não preenchido: {campo}")
    
    # Valida tipo de documento
    if metadados.get("tipo") and metadados["tipo"] not in TIPOS_DOCUMENTO:
        erros.append(f"Tipo de documento inválido: {metadados['tipo']}")
    
    # Valida formato da versão (ex: 1.0, 2.1)
    versao = metadados.get("versao", "")
    if versao and not re.match(r'^\d+\.\d+$', versao):
        erros.append(f"Formato de versão inválido: '{versao}'. Use formato X.Y (ex: 1.0, 2.1)")
    
    return len(erros) == 0, erros


def verificar_versao_existente(titulo: str, versao: str) -> bool:
    """
    Verifica se já existe documento com mesmo título e versão.
    Evita sobrescrita silenciosa.
    """
    documentos = _carregar_indice()
    titulo_normalizado = _normalizar_nome(titulo)
    
    for doc in documentos:
        if _normalizar_nome(doc.get("titulo", "")) == titulo_normalizado:
            if doc.get("versao") == versao:
                return True
    
    return False


def publicar_documento(
    arquivo_bytes: bytes,
    nome_arquivo: str,
    metadados: Dict
) -> Tuple[bool, str, Optional[Dict]]:
    """
    Publica documento na biblioteca institucional.
    
    FLUXO:
    1. Valida perfil do usuário
    2. Valida metadados
    3. Verifica duplicidade de versão
    4. Salva arquivo físico
    5. Extrai texto
    6. Salva texto extraído
    7. Atualiza índice
    8. Registra evento no histórico
    
    Args:
        arquivo_bytes: Conteúdo binário do arquivo
        nome_arquivo: Nome original do arquivo
        metadados: Dict com metadados do documento
    
    Returns:
        Tupla (sucesso: bool, mensagem: str, documento: Optional[Dict])
    """
    # 1. Valida perfil
    autorizado, msg_perfil = verificar_perfil_autorizado()
    if not autorizado:
        return False, msg_perfil, None
    
    # 2. Valida metadados
    valido, erros = validar_metadados(metadados)
    if not valido:
        return False, "Metadados inválidos:\n- " + "\n- ".join(erros), None
    
    # 3. Verifica duplicidade
    if verificar_versao_existente(metadados["titulo"], metadados["versao"]):
        return False, f"Já existe documento '{metadados['titulo']}' na versão {metadados['versao']}. Use uma versão diferente.", None
    
    # Inicializa estrutura
    inicializar_estrutura()
    
    # Extrai extensão do arquivo
    extensao = Path(nome_arquivo).suffix.lower()
    if extensao not in EXTENSOES_PERMITIDAS:
        return False, f"Extensão não permitida: {extensao}. Use: {', '.join(EXTENSOES_PERMITIDAS)}", None
    
    # Gera identificadores únicos
    doc_id = str(uuid.uuid4())[:8]
    titulo_slug = _normalizar_nome(metadados["titulo"])
    tipo_slug = _normalizar_nome(metadados["tipo"])
    versao_slug = metadados["versao"].replace(".", "_")
    
    # 4. Salva arquivo físico
    nome_arquivo_final = f"{titulo_slug}_v{versao_slug}{extensao}"
    caminho_arquivo = DOCUMENTOS_DIR / tipo_slug / nome_arquivo_final
    
    try:
        with open(caminho_arquivo, "wb") as f:
            f.write(arquivo_bytes)
        logger.info(f"Arquivo salvo: {caminho_arquivo}")
    except Exception as e:
        return False, f"Erro ao salvar arquivo: {str(e)}", None
    
    # 5. Extrai texto
    sucesso_extracao, texto_extraido, msg_extracao = extrair_texto_documento(
        str(caminho_arquivo), extensao
    )
    
    # 6. Salva texto extraído
    caminho_texto = TEXTOS_DIR / f"{doc_id}.txt"
    if sucesso_extracao and texto_extraido:
        try:
            with open(caminho_texto, "w", encoding="utf-8") as f:
                f.write(texto_extraido)
            logger.info(f"Texto extraído salvo: {caminho_texto}")
        except Exception as e:
            logger.warning(f"Erro ao salvar texto extraído: {e}")
    
    # 7. Atualiza índice
    usuario_atual = get_usuario_atual()
    data_publicacao = datetime.now().isoformat()
    
    documento = {
        "doc_id": doc_id,
        "titulo": metadados["titulo"],
        "tipo": metadados["tipo"],
        "area": metadados["area"],
        "versao": metadados["versao"],
        "status": metadados.get("status", "ATIVO"),
        "data_vigencia": metadados.get("data_vigencia", ""),
        "observacoes": metadados.get("observacoes", ""),
        "caminho_arquivo": str(caminho_arquivo),
        "caminho_texto": str(caminho_texto) if sucesso_extracao else "",
        "texto_extraido": sucesso_extracao,
        "data_publicacao": data_publicacao,
        "usuario_responsavel": usuario_atual,
        "nome_arquivo_original": nome_arquivo
    }
    
    documentos = _carregar_indice()
    documentos.append(documento)
    _salvar_indice(documentos)
    
    # 8. Registra evento no histórico
    try:
        _registrar_evento_publicacao(documento)
    except Exception as e:
        logger.warning(f"Erro ao registrar evento: {e}")
    
    # Mensagem de sucesso
    msg_sucesso = f"✅ Documento publicado com sucesso!\n"
    msg_sucesso += f"- ID: {doc_id}\n"
    msg_sucesso += f"- Título: {metadados['titulo']}\n"
    msg_sucesso += f"- Versão: {metadados['versao']}\n"
    msg_sucesso += f"- {msg_extracao}"
    
    return True, msg_sucesso, documento


def _registrar_evento_publicacao(documento: Dict):
    """Registra evento de publicação no histórico institucional."""
    try:
        from services.history_service import log_event
        
        # Cria contexto mínimo para o evento
        contrato_contexto = {
            "id": f"BIBLIOTECA_{documento['doc_id']}",
            "numero": documento["titulo"]
        }
        
        log_event(
            contract=contrato_contexto,
            event_type="BIBLIOTECA_DOCUMENTO_PUBLICADO",
            title=f"Documento publicado: {documento['titulo']}",
            details=f"Versão: {documento['versao']} | Tipo: {documento['tipo']} | Área: {documento['area']}",
            source="Biblioteca Institucional",
            actor=documento["usuario_responsavel"],
            metadata={
                "doc_id": documento["doc_id"],
                "versao": documento["versao"],
                "tipo": documento["tipo"],
                "area": documento["area"],
                "status": documento["status"]
            }
        )
        logger.info(f"Evento de publicação registrado para doc_id: {documento['doc_id']}")
    except Exception as e:
        logger.error(f"Erro ao registrar evento de publicação: {e}")


# ============================================================================
# REVOGAÇÃO DE DOCUMENTOS
# ============================================================================

def revogar_documento(doc_id: str, motivo: str = "") -> Tuple[bool, str]:
    """
    Revoga documento (muda status para REVOGADO).
    Documento revogado não é mais consumido pela IA.
    
    Args:
        doc_id: ID do documento
        motivo: Motivo da revogação (opcional)
    
    Returns:
        Tupla (sucesso: bool, mensagem: str)
    """
    autorizado, msg_perfil = verificar_perfil_autorizado()
    if not autorizado:
        return False, msg_perfil
    
    documentos = _carregar_indice()
    
    for doc in documentos:
        if doc.get("doc_id") == doc_id:
            if doc.get("status") == "REVOGADO":
                return False, "Documento já está revogado"
            
            doc["status"] = "REVOGADO"
            doc["data_revogacao"] = datetime.now().isoformat()
            doc["motivo_revogacao"] = motivo
            doc["usuario_revogacao"] = get_usuario_atual()
            
            _salvar_indice(documentos)
            
            # Registra evento
            try:
                _registrar_evento_revogacao(doc)
            except Exception as e:
                logger.warning(f"Erro ao registrar evento de revogação: {e}")
            
            return True, f"Documento revogado: {doc['titulo']} v{doc['versao']}"
    
    return False, f"Documento não encontrado: {doc_id}"


def _registrar_evento_revogacao(documento: Dict):
    """Registra evento de revogação no histórico."""
    try:
        from services.history_service import log_event
        
        contrato_contexto = {
            "id": f"BIBLIOTECA_{documento['doc_id']}",
            "numero": documento["titulo"]
        }
        
        log_event(
            contract=contrato_contexto,
            event_type="BIBLIOTECA_DOCUMENTO_REVOGADO",
            title=f"Documento revogado: {documento['titulo']}",
            details=f"Versão: {documento['versao']} | Motivo: {documento.get('motivo_revogacao', 'Não informado')}",
            source="Biblioteca Institucional",
            actor=documento.get("usuario_revogacao", "Sistema"),
            metadata={
                "doc_id": documento["doc_id"],
                "versao": documento["versao"],
                "motivo": documento.get("motivo_revogacao", "")
            }
        )
    except Exception as e:
        logger.error(f"Erro ao registrar evento de revogação: {e}")


# ============================================================================
# ESTATÍSTICAS E RELATÓRIOS
# ============================================================================

def get_estatisticas_biblioteca() -> Dict:
    """
    Retorna estatísticas da biblioteca.
    
    Returns:
        Dict com contadores e métricas
    """
    documentos = _carregar_indice()
    
    total = len(documentos)
    ativos = len([d for d in documentos if d.get("status") == "ATIVO"])
    revogados = len([d for d in documentos if d.get("status") == "REVOGADO"])
    com_texto = len([d for d in documentos if d.get("texto_extraido")])
    
    # Contagem por tipo
    por_tipo = {}
    for doc in documentos:
        tipo = doc.get("tipo", "Outros")
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
    
    # Contagem por área
    por_area = {}
    for doc in documentos:
        area = doc.get("area", "Outros")
        por_area[area] = por_area.get(area, 0) + 1
    
    return {
        "total": total,
        "ativos": ativos,
        "revogados": revogados,
        "com_texto_extraido": com_texto,
        "por_tipo": por_tipo,
        "por_area": por_area
    }


# Inicialização automática ao importar
inicializar_estrutura()
