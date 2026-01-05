# Implementação de IA no Módulo COPILOTO

## 📋 Visão Geral

Implementação de integração com modelo de IA generativa (OpenAI) no módulo COPILOTO, mantendo governança, rastreabilidade e controle institucional.

**Status:** ✅ Implementado (Modo Híbrido)

---

## 🏗️ Arquitetura

### Componentes Implementados

```
┌─────────────────────────────────────────────────────────────┐
│                    PÁGINA COPILOTO                          │
│               (pages/02_💬_Copiloto.py)                     │
└───────────────────┬─────────────────────────────────────────┘
                    │ Entrada do usuário
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                   AGENTE COPILOTO                           │
│            (agents/copilot_agent.py)                        │
│                                                             │
│  • Recebe pergunta + contexto do contrato                  │
│  • Decide: usar IA ou modo padrão?                         │
└───────────────────┬─────────────────────────────────────────┘
                    │
        ┌───────────┴────────────┐
        ▼                        ▼
┌─────────────────┐      ┌──────────────────┐
│  SERVIÇO DE IA  │      │   MODO PADRÃO    │
│   (se config.)  │      │   (mockado)      │
└────────┬────────┘      └────────┬─────────┘
         │                        │
         ▼                        │
┌──────────────────┐              │
│  OpenAI API      │              │
│  (st.secrets)    │              │
└────────┬─────────┘              │
         │                        │
         └────────────┬───────────┘
                      ▼
          ┌─────────────────────┐
          │  RESPOSTA GERADA    │
          └─────────────────────┘
                      │
                      ▼
          ┌─────────────────────┐
          │  REGISTRO (optional)│
          │  history_service    │
          └─────────────────────┘
```

### Estrutura de Arquivos

```
services/
  └── copiloto_ai_service.py          # ⭐ NOVO: Serviço de integração com IA

agents/
  └── copilot_agent.py                # ✏️ ATUALIZADO: Modo híbrido (IA + padrão)

prompts/
  └── system_prompts.py               # ✏️ ATUALIZADO: Prompt institucional

pages/
  └── 02_💬_Copiloto.py               # ✅ SEM ALTERAÇÃO (compatível)

requirements.txt                      # ✏️ ATUALIZADO: + openai>=1.12.0
```

---

## 🔑 Configuração de Chaves (st.secrets)

### Como Ativar a IA

1. **Criar arquivo `.streamlit/secrets.toml`** (localmente ou no Streamlit Cloud):

```toml
[openai]
api_key = "sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

2. **Ou configurar no Streamlit Cloud**:
   - Vá em Settings → Secrets
   - Adicione:
     ```toml
     [openai]
     api_key = "sua-chave-aqui"
     ```

### Como Desativar a IA

- **Simplesmente remova a chave** do `secrets.toml` ou Streamlit Cloud
- O sistema automaticamente voltará ao modo padrão
- **Nenhuma quebra de funcionalidade**

---

## 🔒 Segurança e Governança

### Princípios Implementados

✅ **Chave NÃO hardcoded** - Usa exclusivamente `st.secrets`  
✅ **Modo degradado** - Funciona sem IA configurada  
✅ **Verificação explícita** - Testa disponibilidade antes de usar  
✅ **Respostas não vinculantes** - Rodapé institucional claro  
✅ **Rastreabilidade** - Registra uso (sem armazenar conteúdo)  
✅ **Tratamento de erros** - Fallback para modo padrão  
✅ **Sem ações automáticas** - IA apenas sugere, não executa  

### Leitura Segura de Credenciais

```python
import streamlit as st

def verificar_disponibilidade_ia() -> Tuple[bool, Optional[str]]:
    """Verifica se IA está disponível via st.secrets"""
    try:
        api_key = st.secrets.get("openai", {}).get("api_key")
        
        if not api_key:
            return False, None
        
        return True, api_key
        
    except Exception:
        return False, None
```

### Dados NÃO Enviados à IA

- ❌ Dados financeiros sensíveis (valores não essenciais)
- ❌ Dados pessoais identificáveis de fiscais
- ❌ Informações classificadas
- ❌ Histórico completo de interações

### Dados Enviados à IA (Contextualmente)

- ✅ Número do contrato
- ✅ Tipo de contratação
- ✅ Objeto (descrição pública)
- ✅ Vigência
- ✅ Pergunta do usuário

---

## 📊 Fluxo de Funcionamento

### 1. Entrada do Usuário

```python
# Página: 02_💬_Copiloto.py
user_input = st.chat_input("Digite sua pergunta sobre o contrato...")

if user_input:
    resposta = processar_pergunta_copilot(
        pergunta=user_input,
        contrato=contrato
    )
```

### 2. Processamento Híbrido

```python
# Agente: copilot_agent.py
def processar_pergunta_copilot(pergunta: str, contrato: Dict) -> str:
    try:
        # Tenta usar IA
        from services.copiloto_ai_service import processar_pergunta_com_ia
        
        resposta, metadata = processar_pergunta_com_ia(
            pergunta=pergunta,
            contrato=contrato,
            system_prompt=COPILOT_SYSTEM_PROMPT
        )
        
        return resposta
        
    except ImportError:
        # Fallback: modo padrão
        return _processar_pergunta_modo_padrao(pergunta, contrato)
```

### 3. Verificação de Disponibilidade

```python
# Serviço: copiloto_ai_service.py
disponivel, api_key = verificar_disponibilidade_ia()

if disponivel:
    # Usa OpenAI
    resposta_ia = consultar_ia_openai(...)
else:
    # Mensagem institucional de indisponibilidade
    resposta = "Recurso de apoio inteligente indisponível..."
```

### 4. Registro de Uso (Governança)

```python
# NÃO armazena conteúdo da pergunta/resposta
evento = {
    "tipo": "COPILOTO_CONSULTA_REALIZADA",
    "contrato_id": contrato_id,
    "modo": "IA_ATIVA" | "MODO_PADRAO" | "ERRO_IA",
    "timestamp": datetime.now(),
    "usuario": usuario
}

registrar_evento(evento)
```

---

## 🧪 Cenários de Uso

### Cenário 1: IA Disponível e Funcionando

```
✅ Chave configurada em st.secrets
✅ Biblioteca openai instalada
✅ API OpenAI respondendo

Resultado: Usuário recebe resposta da IA + rodapé institucional
```

### Cenário 2: IA Não Configurada

```
❌ Chave NÃO configurada em st.secrets

Resultado: Sistema usa modo padrão (regras mockadas)
+ mensagem "Recurso de apoio inteligente indisponível"
```

### Cenário 3: Erro na API OpenAI

```
✅ Chave configurada
❌ Erro na chamada API (timeout, limite excedido, etc.)

Resultado: Sistema usa modo padrão + mensagem de erro
```

### Cenário 4: Biblioteca openai Não Instalada

```
❌ Dependência não instalada

Resultado: Sistema usa modo padrão (fallback automático)
```

---

## 🎯 Parâmetros Recomendados

### Modelo OpenAI

```python
modelo = "gpt-4o-mini"  # Recomendado: bom custo-benefício
```

**Alternativas:**
- `gpt-4o` - Mais poderoso, mais caro
- `gpt-4-turbo` - Balanceado
- `gpt-3.5-turbo` - Mais barato, menos sofisticado

### Temperatura

```python
temperatura = 0.3  # Baixa criatividade, alta consistência
```

**Escala:**
- `0.0` - Completamente determinístico (sempre mesma resposta)
- `0.3` - **Recomendado para uso institucional** (consistente, mas não robótico)
- `0.7` - Mais criativo
- `1.0` - Muito criativo (não recomendado para contexto institucional)

### Limite de Tokens

```python
max_tokens = 1000  # Respostas concisas (aprox. 750 palavras)
```

---

## 🔍 Monitoramento e Logs

### Logs Implementados

```python
# Sucesso
logger.info(f"IA disponível: chave encontrada em st.secrets")
logger.info(f"Consultando OpenAI (modelo: {modelo})")
logger.info(f"Resposta recebida da IA ({len(resposta)} caracteres)")

# Avisos
logger.warning("IA indisponível: chave não configurada")

# Erros
logger.error(f"Erro ao consultar OpenAI: {e}")
```

### Onde Ver Logs

- **Localmente:** Terminal onde o Streamlit está rodando
- **Streamlit Cloud:** Logs → View logs

---

## 🚫 O Que NÃO Foi Implementado (Por Design)

❌ **Execução automática de ações administrativas**  
❌ **Assinatura digital de documentos**  
❌ **Tomada de decisões em nome do fiscal**  
❌ **Envio automático de notificações**  
❌ **Alteração de dados contratuais**  
❌ **Armazenamento de conversas completas**  
❌ **Personalização por usuário (histórico de IA)**  
❌ **Feedback/avaliação de respostas**  

**Justificativa:** Princípios institucionais de controle e governança.

---

## 📦 Dependências

### Nova Dependência

```txt
openai>=1.12.0
```

### Instalação

```bash
pip install openai
```

Ou:

```bash
pip install -r requirements.txt
```

---

## 🔄 Reversibilidade

### Como Reverter para Modo Padrão (Sem IA)

**Opção 1: Desativar IA (mantém código)**
```bash
# Remove chave do secrets.toml
# Sistema automaticamente volta ao modo padrão
```

**Opção 2: Remover integração completa**
```bash
# 1. Deletar services/copiloto_ai_service.py
# 2. Reverter agents/copilot_agent.py para versão anterior
# 3. Remover openai do requirements.txt
```

### Por Que a Arquitetura é Reversível?

1. **IA é opcional, não obrigatória**
   - Sistema funciona normalmente sem IA
   - Modo padrão preservado integralmente

2. **Separação de responsabilidades**
   - Serviço de IA isolado em arquivo próprio
   - Agente usa try/except para fallback

3. **Zero dependência hard-coded**
   - Nenhuma chave no código
   - Nenhum import obrigatório de openai

4. **Compatibilidade com páginas existentes**
   - Nenhuma alteração na UI
   - Interface do agente mantida

---

## 🏛️ Adequação a Ambientes Institucionais

### Por Que Esta Solução é Adequada?

#### 1. **Controle Total**
- Administrador decide se ativa IA (via secrets)
- Nenhuma dependência externa obrigatória
- Pode desligar a qualquer momento

#### 2. **Governança**
- Rastreabilidade de uso
- Logs detalhados
- Metadados registrados (sem conteúdo sensível)

#### 3. **Segurança**
- Chaves nunca no código
- Verificação explícita de disponibilidade
- Tratamento robusto de erros

#### 4. **Compliance**
- Respostas marcadas como "não vinculantes"
- Rodapé institucional em todas as respostas da IA
- Recomendação de validação com fontes oficiais

#### 5. **Custo Controlado**
- Usa modelo econômico (gpt-4o-mini)
- Limite de tokens configurável
- Pode desativar sem impacto

#### 6. **Auditável**
- Código aberto para revisão
- Logs de todas as operações
- Metadados de uso armazenados

---

## 📝 Exemplo de Uso

### Pergunta do Usuário

```
"Qual é o prazo de vigência do contrato?"
```

### Resposta da IA (Modo IA_ATIVA)

```markdown
📅 **Vigência do Contrato**

Com base nas informações fornecidas, o contrato nº 123/2025 
possui vigência de 12 meses, com início em 01/01/2025 e 
término previsto para 31/12/2025.

**Atenção:** Conforme previsto na Cláusula 2ª do contrato, 
é possível prorrogação mediante termo aditivo, desde que 
respeitado o prazo total de 60 meses previsto na Lei 14.133/2021.

ℹ️ *Fonte: Cláusula 2ª do contrato - Da Vigência*

💡 **Recomendação:** Valide esta informação consultando o 
documento original do contrato assinado.

---

⚠️ **IMPORTANTE:** Esta resposta foi gerada por IA como apoio textual. 
Não constitui orientação jurídica vinculante. Sempre valide as 
informações com fontes oficiais e consulte as cláusulas contratuais originais.
```

### Resposta (Modo MODO_PADRAO - IA Indisponível)

```markdown
🤖 **Recurso de Apoio Inteligente Indisponível**

No momento, o recurso de apoio inteligente não está disponível.

**Informações do Contrato:**
- Número: 123/2025
- Fornecedor: Empresa XYZ Ltda
- Objeto: Prestação de serviços de limpeza

**Como obter ajuda:**
- Consulte a página **"📖 Como Proceder"** para orientações gerais
- Acesse a **"📚 Biblioteca"** para consultar manuais institucionais
- Entre em contato com a equipe de suporte técnico

💡 *Administradores: Para ativar o recurso de IA, configure a 
chave da API em `st.secrets`*
```

---

## 🎓 Explicação Técnica da Arquitetura

### Por Que Service Layer?

**Centralização:**
- Toda lógica de IA em um único lugar
- Facilita manutenção e testes
- Evita duplicação de código

**Isolamento:**
- Páginas não conhecem OpenAI
- Agente não conhece detalhes da API
- Baixo acoplamento

**Testabilidade:**
- Pode mockar o serviço facilmente
- Testes unitários isolados
- CI/CD simplificado

### Por Que Modo Híbrido?

**Compatibilidade:**
- Sistema legado preservado
- Migração gradual possível
- Zero breaking changes

**Confiabilidade:**
- Se IA falhar, sistema continua
- Fallback automático
- Usuário sempre tem resposta

**Flexibilidade:**
- Ambientes sem IA funcionam
- Desenvolvimento local sem custos
- Testes sem API key

---

## 🚀 Próximos Passos (Futuro)

- [ ] Implementar cache de respostas (economia de custos)
- [ ] Adicionar feedback do usuário (👍/👎)
- [ ] Suporte a múltiplos provedores (Azure OpenAI, Anthropic)
- [ ] Personalização de prompts por perfil de usuário
- [ ] Dashboard de uso e custos
- [ ] Suporte a multimodalidade (anexar documentos)

---

## 📞 Suporte

**Dúvidas técnicas:**
- Consulte logs do sistema
- Verifique configuração de `st.secrets`
- Revise documentação do OpenAI

**Problemas comuns:**
1. "IA indisponível" → Verifique chave em secrets
2. "Erro ao consultar" → Verifique saldo da conta OpenAI
3. "Resposta vazia" → Verifique logs para detalhes

---

**Versão:** 1.0  
**Data:** Janeiro 2026  
**Autor:** Equipe de Desenvolvimento TJSP
