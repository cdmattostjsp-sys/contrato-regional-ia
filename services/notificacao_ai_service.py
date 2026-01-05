"""
Serviço de IA para o Módulo de Notificações
============================================
Centraliza geração assistida de notificações contratuais via IA generativa.

PRINCÍPIOS INSTITUCIONAIS:
- IA sugere textos; servidor é o autor final
- Nenhuma notificação enviada automaticamente
- Toda sugestão é editável antes de salvar/enviar
- Sistema funciona normalmente sem IA
- Contexto mínimo e sanitizado

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

def is_ai_enabled() -> bool:
    """
    Verifica se a IA está disponível para geração de notificações.
    
    Aceita dois formatos de configuração em st.secrets:
    - Formato estruturado: [openai] api_key = "..."
    - Formato flat: OPENAI_API_KEY = "..."
    
    Returns:
        bool: True se IA disponível, False caso contrário
    """
    try:
        # Tenta formato estruturado
        api_key = st.secrets.get("openai", {}).get("api_key")
        
        # Se não encontrou, tenta formato flat
        if not api_key:
            api_key = st.secrets.get("OPENAI_API_KEY")
        
        if not api_key:
            logger.info("IA indisponível: chave não configurada")
            return False
        
        # Validação básica
        if not isinstance(api_key, str) or len(api_key) < 20:
            logger.warning("IA indisponível: chave inválida")
            return False
        
        logger.info("IA disponível para geração de notificações")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao verificar disponibilidade da IA: {e}")
        return False


def _get_api_key() -> Optional[str]:
    """
    Obtém a chave da API de forma segura.
    
    Returns:
        Chave da API ou None se não disponível
    """
    try:
        # Tenta formato estruturado
        api_key = st.secrets.get("openai", {}).get("api_key")
        
        # Se não encontrou, tenta formato flat
        if not api_key:
            api_key = st.secrets.get("OPENAI_API_KEY")
        
        return api_key
    except:
        return None


# ============================================================================
# SANITIZAÇÃO DE CONTEXTO
# ============================================================================

def _sanitizar_contexto_contrato(contrato: Dict) -> Dict:
    """
    Sanitiza contexto do contrato, removendo dados sensíveis.
    
    Args:
        contrato: Dados completos do contrato
        
    Returns:
        Contexto sanitizado (apenas dados não sensíveis)
    """
    return {
        "numero": contrato.get("numero", "(não informado)"),
        "fornecedor": contrato.get("fornecedor", "(não informado)"),
        "objeto": contrato.get("objeto", "(não informado)")[:200],  # Limita tamanho
        "vigencia": contrato.get("vigencia", "(não informada)"),
        "status": contrato.get("status", "indefinido"),
        "tipo": contrato.get("tipo", "(não informado)")
    }


# ============================================================================
# PROMPTS INSTITUCIONAIS
# ============================================================================

PROMPT_SYSTEM_NOTIFICACAO = """
Você é um assistente especializado em redação de notificações contratuais formais 
para o Tribunal de Justiça do Estado de São Paulo (TJSP).

NATUREZA DO SERVIÇO:
Você atua como APOIO TEXTUAL ao servidor público. Suas sugestões são NÃO VINCULANTES
e servem apenas como rascunho inicial que será revisado e editado pelo servidor.

REGRAS OBRIGATÓRIAS:
1. Use linguagem formal e institucional (tom administrativo, não chatbot)
2. Seja objetivo e direto, sem floreios
3. NÃO invente normas, prazos ou fatos não fornecidos
4. Se faltar informação essencial, indique claramente onde o servidor deve complementar
5. Use estrutura clara: considerandos, determinações, advertências (se aplicável), fechamento
6. Cite fundamentação legal apenas se fornecida; caso contrário, use termos genéricos
7. Mantenha tom respeitoso mas firme
8. NÃO tome decisões administrativas - apenas sugira texto

CONTEXTO INSTITUCIONAL:
Você está auxiliando fiscais e gestores de contrato do TJSP a redigir notificações 
contratuais. O texto gerado será SEMPRE revisado e editado pelo servidor antes de uso.

ESTILO DE REDAÇÃO:
- Formal e institucional
- Claro e objetivo
- Sem ambiguidades
- Baseado em fatos fornecidos
- Respeitoso e técnico

ESTRUTURA ESPERADA (quando aplicável):
1. Identificação do destinatário
2. Assunto/Referência do contrato
3. Considerandos (contexto)
4. Comunicação/Determinação principal
5. Prazo (se aplicável)
6. Fundamentação legal (se fornecida)
7. Advertências/Consequências (se aplicável)
8. Fechamento institucional

LIMITAÇÕES EXPLÍCITAS:
- NÃO crie obrigações não previstas
- NÃO invente prazos; use o fornecido
- NÃO assine documentos
- Suas sugestões são RASCUNHOS, não documentos finais
- Sempre oriente revisão humana

FORMATO DE RESPOSTA:
Texto corrido, formatado para cópia direta, sem markdown excessivo.
Use quebras de linha para separar seções.
"""


# ============================================================================
# GERAÇÃO DE SUGESTÃO VIA IA
# ============================================================================

def gerar_sugestao_notificacao(
    contexto_contrato: Dict,
    dados_notificacao: Dict
) -> Dict:
    """
    Gera sugestão de texto de notificação via IA generativa.
    
    Esta é a função principal do serviço, chamada pela página.
    
    Args:
        contexto_contrato: Dados sanitizados do contrato
        dados_notificacao: Dados do formulário (tipo, motivo, prazo, fundamentação)
        
    Returns:
        Dict com:
        - "sucesso": bool
        - "texto_sugerido": str (se sucesso)
        - "resumo_criterios": str (metadados da geração)
        - "mensagem": str (mensagem para o usuário)
        - "modo": str (IA_ATIVA | MODO_PADRAO | ERRO_IA)
    """
    
    # Verifica disponibilidade
    if not is_ai_enabled():
        return {
            "sucesso": False,
            "texto_sugerido": "",
            "resumo_criterios": "IA não disponível",
            "mensagem": _get_mensagem_ia_indisponivel(),
            "modo": "MODO_PADRAO"
        }
    
    # Sanitiza contexto
    contexto_sanitizado = _sanitizar_contexto_contrato(contexto_contrato)
    
    # Monta prompt contextual
    prompt_contexto = _montar_prompt_contexto(contexto_sanitizado, dados_notificacao)
    
    # Consulta IA
    try:
        texto_ia = _consultar_openai_notificacao(prompt_contexto)
        
        if texto_ia:
            return {
                "sucesso": True,
                "texto_sugerido": texto_ia,
                "resumo_criterios": f"Gerado por IA | Tipo: {dados_notificacao.get('tipo')} | Prazo: {dados_notificacao.get('prazo')} dias",
                "mensagem": "✅ Sugestão gerada com sucesso. Revise e ajuste conforme necessário.",
                "modo": "IA_ATIVA"
            }
        else:
            return {
                "sucesso": False,
                "texto_sugerido": "",
                "resumo_criterios": "Erro ao consultar IA",
                "mensagem": "⚠️ Erro ao gerar sugestão. Tente novamente ou use modo manual.",
                "modo": "ERRO_IA"
            }
            
    except Exception as e:
        logger.error(f"Erro ao gerar sugestão: {e}")
        return {
            "sucesso": False,
            "texto_sugerido": "",
            "resumo_criterios": f"Erro: {str(e)[:100]}",
            "mensagem": "⚠️ Erro inesperado ao gerar sugestão. Use modo manual.",
            "modo": "ERRO_IA"
        }


def _montar_prompt_contexto(contexto: Dict, dados: Dict) -> str:
    """
    Monta prompt contextualizado para a IA.
    
    Args:
        contexto: Contexto sanitizado do contrato
        dados: Dados do formulário
        
    Returns:
        Prompt completo para enviar à IA
    """
    prompt = f"""
CONTEXTO DO CONTRATO:
- Número: {contexto['numero']}
- Contratada: {contexto['fornecedor']}
- Objeto: {contexto['objeto']}
- Vigência: {contexto['vigencia']}
- Status: {contexto['status']}

TIPO DE NOTIFICAÇÃO:
{dados.get('tipo', '(não especificado)')}

CATEGORIA:
{dados.get('categoria', '(não especificada)')}

MOTIVO DA NOTIFICAÇÃO:
{dados.get('motivo', '(não especificado)')}

PRAZO PARA RESPOSTA:
{dados.get('prazo', 5)} dias úteis

FUNDAMENTAÇÃO LEGAL (se fornecida):
{dados.get('fundamentacao', '(não fornecida - usar referência genérica ao contrato e legislação aplicável)')}

---

TAREFA:
Gere um texto formal de notificação contratual seguindo a estrutura institucional do TJSP.
O texto será revisado e ajustado pelo servidor antes do envio.

Inclua:
1. Cabeçalho com destinatário
2. Assunto/Referência
3. Considerandos (contexto legal e contratual)
4. Comunicação/Determinação clara e objetiva
5. Prazo especificado
6. Fundamentação (baseada no fornecido ou genérica)
7. Advertências (se aplicável ao tipo)
8. Fechamento institucional com espaço para assinatura

NÃO invente dados não fornecidos.
Se faltar informação, indique onde o servidor deve complementar com [A COMPLEMENTAR].
"""
    return prompt


def _consultar_openai_notificacao(prompt_contexto: str) -> Optional[str]:
    """
    Consulta o modelo OpenAI para gerar texto de notificação.
    
    Args:
        prompt_contexto: Prompt contextualizado
        
    Returns:
        Texto gerado ou None em caso de erro
    """
    try:
        from openai import OpenAI
        
        api_key = _get_api_key()
        if not api_key:
            return None
        
        client = OpenAI(api_key=api_key)
        
        logger.info("Consultando OpenAI para geração de notificação")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Modelo econômico e eficiente
            messages=[
                {"role": "system", "content": PROMPT_SYSTEM_NOTIFICACAO},
                {"role": "user", "content": prompt_contexto}
            ],
            temperature=0.3,  # Baixa criatividade, alta consistência
            max_tokens=2000,  # Notificações podem ser mais longas
        )
        
        texto = response.choices[0].message.content
        
        logger.info(f"Texto gerado com sucesso ({len(texto)} caracteres)")
        
        # Adiciona rodapé institucional
        texto_final = f"""{texto}

---

⚠️ IMPORTANTE: Este texto foi gerado por IA como sugestão inicial. 
REVISE INTEGRALMENTE antes de salvar/enviar. Ajuste conforme necessário 
e valide a adequação legal e técnica. O servidor é o autor final do documento.
"""
        
        return texto_final
        
    except ImportError:
        logger.error("Biblioteca 'openai' não instalada")
        return None
        
    except Exception as e:
        logger.error(f"Erro ao consultar OpenAI: {e}")
        return None


def _get_mensagem_ia_indisponivel() -> str:
    """
    Retorna mensagem institucional quando IA não está disponível.
    
    Returns:
        Mensagem formatada
    """
    return """
ℹ️ **Recurso de Apoio Inteligente Indisponível**

A geração assistida por IA não está disponível no momento.

**Alternativas:**
- Use os templates padrão do sistema (pré-visualização abaixo)
- Consulte a página "📖 Como Proceder" para orientações
- Entre em contato com o suporte técnico

💡 *Administradores: Para ativar o recurso de IA, configure a chave 
da API em `st.secrets` (Streamlit Cloud Settings → Secrets)*
"""


# ============================================================================
# REGISTRO DE USO (GOVERNANÇA)
# ============================================================================

def registrar_geracao_notificacao(
    contrato_id: str,
    tipo_notificacao: str,
    categoria: str,
    modo: str,
    usuario: Optional[str] = None
) -> None:
    """
    Registra geração de notificação para fins de governança.
    
    NÃO armazena conteúdo da notificação (apenas metadados).
    
    Args:
        contrato_id: ID do contrato
        tipo_notificacao: Tipo de notificação
        categoria: Categoria (Gestor/Fiscal)
        modo: Modo de geração (IA_ATIVA | MODO_PADRAO | ERRO_IA)
        usuario: ID do usuário (opcional)
    """
    try:
        from services.history_service import log_event
        
        # Prepara metadados
        details = f"{categoria} - {tipo_notificacao} | Modo: {modo}"
        
        # Registra evento
        log_event(
            contrato={"id": contrato_id},
            event_type="NOTIFICACAO_GERADA_COM_IA",
            title="Notificação gerada com assistência de IA",
            details=details,
            source="Notificações IA",
            metadata={
                "categoria": categoria,
                "tipo": tipo_notificacao,
                "modo": modo,
                "timestamp": datetime.now().isoformat(),
                "usuario": usuario or "não identificado"
            }
        )
        
        logger.info(f"Geração registrada: {modo} - {tipo_notificacao}")
        
    except Exception as e:
        # Falha no registro não deve impedir funcionamento
        logger.warning(f"Erro ao registrar geração de notificação: {e}")


# ============================================================================
# UTILITÁRIOS
# ============================================================================

def get_status_ia_notificacoes() -> Dict:
    """
    Retorna status da IA para o módulo de notificações.
    
    Returns:
        Dict com status e informações
    """
    disponivel = is_ai_enabled()
    
    return {
        "disponivel": disponivel,
        "mensagem": "IA ativa para geração de notificações" if disponivel else "IA indisponível",
        "modo": "IA_ATIVA" if disponivel else "MODO_PADRAO",
        "timestamp": datetime.now()
    }
