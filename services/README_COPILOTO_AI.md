# Serviço de IA do Módulo COPILOTO

## 📁 Arquivo: `services/copiloto_ai_service.py`

Este serviço centraliza **toda** a integração com modelos de IA generativa no módulo COPILOTO.

---

## 🎯 Responsabilidades

1. **Verificar disponibilidade da IA** (chave em `st.secrets`)
2. **Consultar modelo OpenAI** (quando disponível)
3. **Fornecer fallback institucional** (quando indisponível)
4. **Registrar uso** (governança, sem dados sensíveis)
5. **Tratar erros** (robustez)

---

## 🔑 Funções Principais

### `verificar_disponibilidade_ia()`

Verifica se a IA está disponível via `st.secrets`.

**Retorna:**
```python
(disponivel: bool, api_key: Optional[str])
```

**Exemplo:**
```python
disponivel, api_key = verificar_disponibilidade_ia()

if disponivel:
    print("✅ IA disponível")
else:
    print("❌ IA não configurada")
```

---

### `get_status_ia()`

Retorna informações sobre o status da IA.

**Retorna:**
```python
{
    "disponivel": bool,
    "mensagem": str,
    "modo": str,  # "IA_ATIVA" | "MODO_PADRAO"
    "timestamp": datetime
}
```

**Exemplo:**
```python
status = get_status_ia()
print(status["mensagem"])
# "Recurso de apoio inteligente ativo"
```

---

### `consultar_ia_openai()`

Consulta o modelo OpenAI com a pergunta do usuário.

**Parâmetros:**
- `pergunta` (str): Pergunta do usuário
- `contexto_contrato` (str): Contexto estruturado do contrato
- `system_prompt` (str): Prompt institucional
- `modelo` (str): Modelo OpenAI (default: "gpt-4o-mini")
- `temperatura` (float): Controle de criatividade (default: 0.3)
- `max_tokens` (int): Limite de tokens (default: 1000)

**Retorna:**
```python
Optional[str]  # Resposta da IA ou None em caso de erro
```

**Exemplo:**
```python
resposta = consultar_ia_openai(
    pergunta="Qual é o prazo de vigência?",
    contexto_contrato=contexto,
    system_prompt=COPILOT_SYSTEM_PROMPT,
    modelo="gpt-4o-mini",
    temperatura=0.3,
    max_tokens=1000
)
```

---

### `processar_pergunta_com_ia()` ⭐

**Função principal do serviço.**

Processa pergunta usando IA (se disponível) ou modo padrão.

**Parâmetros:**
- `pergunta` (str): Pergunta do usuário
- `contrato` (Dict): Dados do contrato
- `system_prompt` (str): Prompt institucional

**Retorna:**
```python
Tuple[str, Dict]
# (resposta: str, metadata: Dict)
```

**Exemplo:**
```python
resposta, metadata = processar_pergunta_com_ia(
    pergunta="Quem são os fiscais?",
    contrato=contrato,
    system_prompt=COPILOT_SYSTEM_PROMPT
)

print(resposta)  # Texto da resposta
print(metadata["modo"])  # "IA_ATIVA" | "MODO_PADRAO" | "ERRO_IA"
```

---

### `registrar_uso_copiloto()`

Registra uso do COPILOTO para fins de governança.

**NÃO armazena:**
- ❌ Conteúdo da pergunta
- ❌ Conteúdo da resposta
- ❌ Dados sensíveis

**Armazena:**
- ✅ Timestamp
- ✅ Contrato ID
- ✅ Modo de processamento
- ✅ Disponibilidade da IA
- ✅ Usuário (opcional)

**Exemplo:**
```python
registrar_uso_copiloto(
    contrato_id="123",
    metadata={"modo": "IA_ATIVA", "ia_disponivel": True},
    usuario="servidor@tjsp.jus.br"
)
```

---

## 📊 Fluxo de Decisão

```
┌─────────────────────────────────────┐
│  processar_pergunta_com_ia()        │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  verificar_disponibilidade_ia()     │
└────────────┬────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
[Disponível]    [Indisponível]
    │                 │
    ▼                 ▼
┌─────────┐     ┌──────────────┐
│ Consulta│     │ Mensagem     │
│ OpenAI  │     │ Institucional│
└────┬────┘     └──────┬───────┘
     │                 │
     ├─────────────────┤
     │                 │
     ▼                 ▼
┌─────────────────────────────────────┐
│  Adiciona Rodapé Institucional      │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  registrar_uso_copiloto()           │
│  (opcional, metadados apenas)       │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Retorna: (resposta, metadata)      │
└─────────────────────────────────────┘
```

---

## 🔒 Segurança

### Leitura Segura de Chaves

```python
# ✅ CORRETO: Via st.secrets
api_key = st.secrets.get("openai", {}).get("api_key")

# ❌ ERRADO: Hardcoded
api_key = "sk-proj-XXXX"  # NUNCA FAÇA ISSO

# ❌ ERRADO: Variável de ambiente sem controle
api_key = os.getenv("OPENAI_API_KEY")  # Não recomendado para Streamlit
```

### Validação de Chave

```python
if not api_key:
    return False, None

if not isinstance(api_key, str) or len(api_key) < 20:
    logger.warning("Chave inválida")
    return False, None

return True, api_key
```

### Tratamento de Erros

```python
try:
    # Tentativa de consultar IA
    resposta = consultar_ia_openai(...)
except ImportError:
    # Biblioteca não instalada
    return None
except Exception as e:
    # Qualquer outro erro
    logger.error(f"Erro: {e}")
    return None
```

---

## 📈 Monitoramento

### Logs Implementados

**Nível INFO:**
```python
logger.info("IA disponível: chave encontrada em st.secrets")
logger.info(f"Consultando OpenAI (modelo: {modelo})")
logger.info(f"Resposta recebida da IA ({len(resposta)} caracteres)")
logger.info(f"Uso do COPILOTO registrado: {modo}")
```

**Nível WARNING:**
```python
logger.warning("IA indisponível: chave não configurada")
logger.warning(f"Erro ao registrar uso do COPILOTO: {e}")
```

**Nível ERROR:**
```python
logger.error(f"Erro ao verificar disponibilidade da IA: {e}")
logger.error(f"Erro ao consultar OpenAI: {e}")
```

---

## 🧪 Testes

### Teste Manual 1: IA Disponível

**Setup:**
```toml
# .streamlit/secrets.toml
[openai]
api_key = "sk-proj-XXXXX"  # Chave válida
```

**Execução:**
```python
from services.copiloto_ai_service import processar_pergunta_com_ia

resposta, metadata = processar_pergunta_com_ia(
    pergunta="Qual é o prazo?",
    contrato={"numero": "123/2025", ...},
    system_prompt=COPILOT_SYSTEM_PROMPT
)

print(metadata["modo"])  # Deve ser: "IA_ATIVA"
```

### Teste Manual 2: IA Indisponível

**Setup:**
```toml
# .streamlit/secrets.toml
# (sem chave configurada)
```

**Execução:**
```python
resposta, metadata = processar_pergunta_com_ia(
    pergunta="Qual é o prazo?",
    contrato={"numero": "123/2025", ...},
    system_prompt=COPILOT_SYSTEM_PROMPT
)

print(metadata["modo"])  # Deve ser: "MODO_PADRAO"
```

### Teste Manual 3: Erro na API

**Setup:**
```toml
# .streamlit/secrets.toml
[openai]
api_key = "sk-proj-INVALIDA"  # Chave inválida
```

**Execução:**
```python
resposta, metadata = processar_pergunta_com_ia(...)

print(metadata["modo"])  # Deve ser: "ERRO_IA"
```

---

## 💰 Parâmetros Recomendados

### Uso Institucional

```python
PARAMETROS_INSTITUCIONAIS = {
    "modelo": "gpt-4o-mini",     # Custo-benefício
    "temperatura": 0.3,           # Consistência
    "max_tokens": 1000,           # Concisão
    "top_p": 0.9,                 # Foco
    "frequency_penalty": 0.0,     # Sem penalidade
    "presence_penalty": 0.0       # Sem penalidade
}
```

### Uso Experimental (Não Recomendado para Produção)

```python
PARAMETROS_EXPERIMENTAIS = {
    "modelo": "gpt-4o",          # Mais poderoso
    "temperatura": 0.7,           # Mais criativo
    "max_tokens": 2000,           # Mais longo
}
```

---

## 🔄 Manutenção

### Adicionar Novo Provedor (Ex: Azure OpenAI)

1. **Adicionar função de verificação:**
```python
def verificar_disponibilidade_azure() -> Tuple[bool, Optional[Dict]]:
    endpoint = st.secrets.get("azure_openai", {}).get("endpoint")
    api_key = st.secrets.get("azure_openai", {}).get("api_key")
    
    if endpoint and api_key:
        return True, {"endpoint": endpoint, "api_key": api_key}
    return False, None
```

2. **Adicionar função de consulta:**
```python
def consultar_ia_azure(...):
    # Implementação específica do Azure
    pass
```

3. **Atualizar função principal:**
```python
def processar_pergunta_com_ia(...):
    # Tenta OpenAI
    if verificar_disponibilidade_ia()[0]:
        return consultar_ia_openai(...)
    
    # Tenta Azure
    if verificar_disponibilidade_azure()[0]:
        return consultar_ia_azure(...)
    
    # Fallback
    return modo_padrao()
```

---

## 📚 Dependências

```python
import streamlit as st        # Para st.secrets
from typing import Dict, Optional, Tuple
from datetime import datetime
import logging
from openai import OpenAI     # pip install openai>=1.12.0
```

---

## 📞 Suporte

**Dúvidas sobre o serviço:**
- Consulte logs do sistema
- Revise documentação: `docs/COPILOTO_IA_IMPLEMENTACAO.md`
- Verifique configuração de secrets

**Problemas comuns:**
1. "openai not found" → `pip install openai`
2. "IA indisponível" → Verifique `st.secrets`
3. "Erro ao consultar" → Verifique saldo OpenAI

---

**Última atualização:** Janeiro 2026
