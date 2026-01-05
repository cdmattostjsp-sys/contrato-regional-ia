"""
Serviço de IA para o Módulo COPILOTO
=====================================
Centraliza toda integração com modelos de IA generativa.

PRINCÍPIOS INSTITUCIONAIS:
- IA atua apenas como apoio textual ao servidor
- Nenhuma ação administrativa é executada automaticamente
- Toda resposta é não vinculante e editável
- Sistema funciona normalmente mesmo sem IA configurada
- Nenhum dado sensível enviado sem controle explícito

GOVERNANÇA:
- Chaves lidas exclusivamente via st.secrets
- Modo degradado quando IA não disponível
- Rastreabilidade de uso (via history_service)
"""

import streamlit as st
from typing import Dict, Optional, Tuple
from datetime import datetime
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# VERIFICAÇÃO DE DISPONIBILIDADE DA IA
# ============================================================================

def verificar_disponibilidade_ia() -> Tuple[bool, Optional[str]]:
    """
    Verifica se a IA está disponível e retorna a chave da API.
    
    Aceita dois formatos de configuração em st.secrets:
    
    Formato 1 (estruturado):
        [openai]
        api_key = "sk-proj-..."
    
    Formato 2 (flat):
        OPENAI_API_KEY = "sk-proj-..."
    
    Returns:
        Tupla (disponivel: bool, api_key: Optional[str])
    """
    try:
        # Tenta formato estruturado: [openai] api_key = "..."
        api_key = st.secrets.get("openai", {}).get("api_key")
        
        # Se não encontrou, tenta formato flat: OPENAI_API_KEY = "..."
        if not api_key:
            api_key = st.secrets.get("OPENAI_API_KEY")
        
        if not api_key:
            logger.info("IA indisponível: chave não configurada em st.secrets")
            logger.info("Configure: [openai] api_key ou OPENAI_API_KEY")
            return False, None
        
        # Validação básica da chave
        if not isinstance(api_key, str) or len(api_key) < 20:
            logger.warning("IA indisponível: chave inválida")
            return False, None
        
        logger.info("IA disponível: chave encontrada em st.secrets")
        return True, api_key
        
    except Exception as e:
        logger.error(f"Erro ao verificar disponibilidade da IA: {e}")
        return False, None


def get_status_ia() -> Dict[str, any]:
    """
    Retorna informações sobre o status da IA.
    
    Returns:
        Dict com status, mensagem e metadados
    """
    disponivel, _ = verificar_disponibilidade_ia()
    
    if disponivel:
        return {
            "disponivel": True,
            "mensagem": "Recurso de apoio inteligente ativo",
            "modo": "IA_ATIVA",
            "timestamp": datetime.now()
        }
    else:
        return {
            "disponivel": False,
            "mensagem": "Recurso de apoio inteligente indisponível no momento",
            "modo": "MODO_PADRAO",
            "timestamp": datetime.now()
        }


# ============================================================================
# INTEGRAÇÃO COM OPENAI
# ============================================================================

def consultar_ia_openai(
    pergunta: str,
    contexto_contrato: str,
    system_prompt: str,
    modelo: str = "gpt-4o-mini",
    temperatura: float = 0.3,
    max_tokens: int = 1000
) -> Optional[str]:
    """
    Consulta o modelo OpenAI com a pergunta do usuário.
    
    IMPORTANTE: Esta função APENAS é chamada se a IA estiver disponível.
    
    Args:
        pergunta: Pergunta do usuário
        contexto_contrato: Contexto estruturado do contrato
        system_prompt: Prompt de sistema institucional
        modelo: Modelo OpenAI a ser usado
        temperatura: Controle de criatividade (0.0 = determinístico, 1.0 = criativo)
        max_tokens: Limite de tokens na resposta
        
    Returns:
        Resposta da IA ou None em caso de erro
    """
    try:
        from openai import OpenAI
        
        # Obtém chave (já validada previamente)
        _, api_key = verificar_disponibilidade_ia()
        if not api_key:
            return None
        
        # Inicializa cliente OpenAI
        client = OpenAI(api_key=api_key)
        
        # Monta mensagens
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{contexto_contrato}\n\n---\n\nPERGUNTA DO USUÁRIO:\n{pergunta}"}
        ]
        
        logger.info(f"Consultando OpenAI (modelo: {modelo})")
        
        # Chama API
        response = client.chat.completions.create(
            model=modelo,
            messages=messages,
            temperature=temperatura,
            max_tokens=max_tokens
        )
        
        # Extrai resposta
        resposta = response.choices[0].message.content
        
        logger.info(f"Resposta recebida da IA ({len(resposta)} caracteres)")
        
        return resposta
        
    except ImportError:
        logger.error("Biblioteca 'openai' não instalada. Execute: pip install openai")
        return None
        
    except Exception as e:
        logger.error(f"Erro ao consultar OpenAI: {e}")
        return None


# ============================================================================
# INTERFACE PRINCIPAL DO SERVIÇO
# ============================================================================

def processar_pergunta_com_ia(
    pergunta: str,
    contrato: Dict,
    system_prompt: str
) -> Tuple[str, Dict]:
    """
    Processa pergunta usando IA (se disponível) ou modo padrão.
    
    Esta é a função principal do serviço, chamada pelo agente.
    
    Args:
        pergunta: Pergunta do usuário
        contrato: Dados do contrato
        system_prompt: Prompt institucional
        
    Returns:
        Tupla (resposta: str, metadata: Dict)
        - resposta: Texto da resposta
        - metadata: Informações sobre o processamento
    """
    # Verifica disponibilidade
    disponivel, api_key = verificar_disponibilidade_ia()
    
    if not disponivel:
        # Modo degradado: retorna mensagem institucional
        metadata = {
            "modo": "MODO_PADRAO",
            "ia_disponivel": False,
            "timestamp": datetime.now(),
            "mensagem_sistema": "IA não configurada - operando em modo padrão"
        }
        
        resposta_padrao = """
🤖 **Recurso de Apoio Inteligente Indisponível**

No momento, o recurso de apoio inteligente não está disponível.

**Informações do Contrato:**
- Número: {numero}
- Fornecedor: {fornecedor}
- Objeto: {objeto}

**Como obter ajuda:**
- Consulte a página **"📖 Como Proceder"** para orientações gerais
- Acesse a **"📚 Biblioteca"** para consultar manuais institucionais
- Entre em contato com a equipe de suporte técnico

💡 *Administradores: Para ativar o recurso de IA, configure a chave da API em `st.secrets`*
        """.format(
            numero=contrato.get('numero', '(não informado)'),
            fornecedor=contrato.get('fornecedor', '(não informado)'),
            objeto=contrato.get('objeto', '(não informado)')
        )
        
        return resposta_padrao, metadata
    
    # Monta contexto do contrato
    from agents.copilot_agent import extrair_contexto_contrato
    contexto_contrato = extrair_contexto_contrato(contrato)
    
    # Consulta IA
    resposta_ia = consultar_ia_openai(
        pergunta=pergunta,
        contexto_contrato=contexto_contrato,
        system_prompt=system_prompt
    )
    
    if resposta_ia:
        # Sucesso: retorna resposta da IA
        metadata = {
            "modo": "IA_ATIVA",
            "ia_disponivel": True,
            "timestamp": datetime.now(),
            "mensagem_sistema": "Resposta gerada por IA generativa"
        }
        
        # Adiciona rodapé institucional
        resposta_final = f"""{resposta_ia}

---

⚠️ **IMPORTANTE:** Esta resposta foi gerada por IA como apoio textual. Não constitui orientação jurídica vinculante. Sempre valide as informações com fontes oficiais e consulte as cláusulas contratuais originais.
        """
        
        return resposta_final, metadata
    else:
        # Erro na IA: retorna mensagem de fallback
        metadata = {
            "modo": "ERRO_IA",
            "ia_disponivel": True,
            "timestamp": datetime.now(),
            "mensagem_sistema": "Erro ao processar com IA - consulte logs"
        }
        
        resposta_erro = """
⚠️ **Erro ao Processar Solicitação**

Não foi possível processar sua pergunta com o recurso de apoio inteligente no momento.

**Alternativas:**
- Reformule sua pergunta e tente novamente
- Consulte a página **"📖 Como Proceder"**
- Acesse a **"📚 Biblioteca"** para manuais institucionais
- Entre em contato com o suporte técnico

💡 *Se o problema persistir, entre em contato com os administradores do sistema.*
        """
        
        return resposta_erro, metadata


# ============================================================================
# REGISTRO DE USO (GOVERNANÇA)
# ============================================================================

def registrar_uso_copiloto(
    contrato_id: str,
    metadata: Dict,
    usuario: Optional[str] = None
) -> None:
    """
    Registra uso do COPILOTO para fins de governança.
    
    NÃO armazena conteúdo da pergunta ou resposta (privacidade).
    Armazena apenas metadados estatísticos.
    
    Args:
        contrato_id: ID do contrato consultado
        metadata: Metadados do processamento
        usuario: ID do usuário (opcional)
    """
    try:
        from services.history_service import registrar_evento
        
        evento = {
            "tipo": "COPILOTO_CONSULTA_REALIZADA",
            "contrato_id": contrato_id,
            "modo": metadata.get("modo", "DESCONHECIDO"),
            "ia_disponivel": metadata.get("ia_disponivel", False),
            "timestamp": metadata.get("timestamp", datetime.now()),
            "usuario": usuario or "não identificado"
        }
        
        registrar_evento(evento)
        logger.info(f"Uso do COPILOTO registrado: {evento['modo']}")
        
    except Exception as e:
        # Falha no registro não deve impedir funcionamento
        logger.warning(f"Erro ao registrar uso do COPILOTO: {e}")


# ============================================================================
# UTILITÁRIOS
# ============================================================================

def get_modelos_disponiveis() -> list:
    """
    Retorna lista de modelos OpenAI disponíveis para uso institucional.
    
    Returns:
        Lista de identificadores de modelos
    """
    return [
        "gpt-4o-mini",      # Recomendado: barato, rápido, bom custo-benefício
        "gpt-4o",           # Mais poderoso, mais caro
        "gpt-4-turbo",      # Balanceado
        "gpt-3.5-turbo"     # Mais barato, menos sofisticado
    ]


def get_parametros_recomendados() -> Dict[str, any]:
    """
    Retorna parâmetros recomendados para uso institucional.
    
    Returns:
        Dict com parâmetros
    """
    return {
        "modelo": "gpt-4o-mini",
        "temperatura": 0.3,      # Baixa criatividade, alta consistência
        "max_tokens": 1000,      # Respostas concisas
        "top_p": 0.9,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }
