# Guia de Configuração - Chaves de API

## 🔑 Como Configurar a IA no Módulo COPILOTO

### Passo 1: Obter Chave da OpenAI

1. Acesse: https://platform.openai.com/
2. Faça login ou crie uma conta
3. Vá em: **API Keys** → **Create new secret key**
4. Copie a chave (começa com `sk-proj-...`)
5. **IMPORTANTE:** Guarde a chave em local seguro (só aparece uma vez)

### Passo 2: Configurar Localmente

#### Opção A: Arquivo de Secrets (Recomendado)

1. Crie o diretório `.streamlit/` na raiz do projeto (se não existir):
   ```bash
   mkdir -p .streamlit
   ```

2. Crie o arquivo `.streamlit/secrets.toml`:
   ```bash
   touch .streamlit/secrets.toml
   ```

3. Adicione a chave:
   ```toml
   # .streamlit/secrets.toml
   
   [openai]
   api_key = "sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
   ```

4. **IMPORTANTE:** Adicione ao `.gitignore`:
   ```bash
   echo ".streamlit/secrets.toml" >> .gitignore
   ```

### Passo 3: Configurar no Streamlit Cloud

1. Acesse seu app no Streamlit Cloud
2. Vá em: **Settings** → **Secrets**
3. Cole o conteúdo:
   ```toml
   [openai]
   api_key = "sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
   ```
4. Clique em **Save**
5. O app será reiniciado automaticamente

---

## ✅ Verificar Configuração

Execute o app e:

1. Acesse a página **💬 Copiloto**
2. Selecione um contrato
3. Faça uma pergunta

**Se configurado corretamente:**
- ✅ Resposta gerada pela IA
- ✅ Rodapé: "Esta resposta foi gerada por IA como apoio textual..."

**Se NÃO configurado:**
- ℹ️ Mensagem: "Recurso de apoio inteligente indisponível no momento"
- ℹ️ Sistema funciona normalmente em modo padrão

---

## 🔒 Segurança

### ✅ FAÇA:
- Mantenha chaves em `secrets.toml` (nunca no código)
- Adicione `.streamlit/secrets.toml` ao `.gitignore`
- Use chaves com permissões restritas
- Monitore uso e custos no dashboard OpenAI
- Rotacione chaves periodicamente

### ❌ NÃO FAÇA:
- Nunca commite chaves no Git
- Nunca compartilhe chaves publicamente
- Nunca hardcode chaves no código
- Nunca use chaves em logs

---

## 💰 Custos Estimados

### Modelo Recomendado: gpt-4o-mini

**Preços (Jan 2026):**
- Input: $0.150 / 1M tokens
- Output: $0.600 / 1M tokens

**Estimativa por pergunta:**
- Contexto: ~500 tokens (contrato)
- Pergunta: ~50 tokens
- Resposta: ~300 tokens
- **Total: ~850 tokens ≈ $0.0003 por interação**

**Uso mensal estimado:**
- 1.000 perguntas/mês ≈ $0.30
- 10.000 perguntas/mês ≈ $3.00
- 50.000 perguntas/mês ≈ $15.00

💡 **Dica:** Configure alertas de limite no dashboard OpenAI

---

## 🧪 Testar Localmente (Sem Custos)

### Modo de Desenvolvimento (Sem IA)

1. **NÃO configure** a chave em `secrets.toml`
2. Execute o app normalmente
3. Sistema funcionará em **modo padrão** (mockado)
4. Perfeito para desenvolvimento e testes

### Quando Usar Cada Modo

**Modo Padrão (sem IA):**
- ✅ Desenvolvimento de features
- ✅ Testes de UI/UX
- ✅ CI/CD pipelines
- ✅ Ambientes sem orçamento

**Modo IA (com chave):**
- ✅ Produção
- ✅ Homologação
- ✅ Demonstrações
- ✅ Validação de respostas

---

## 🔧 Troubleshooting

### Erro: "openai module not found"

**Solução:**
```bash
pip install openai
```

Ou:
```bash
pip install -r requirements.txt
```

### Erro: "Invalid API key"

**Causas:**
1. Chave incorreta ou expirada
2. Formato errado em `secrets.toml`
3. Chave não ativada na conta OpenAI

**Solução:**
1. Verifique a chave no dashboard OpenAI
2. Confirme formato: `api_key = "sk-proj-..."`
3. Gere uma nova chave se necessário

### Erro: "Rate limit exceeded"

**Causas:**
- Muitas requisições em pouco tempo
- Limite de conta atingido

**Solução:**
1. Aguarde alguns minutos
2. Verifique limites no dashboard OpenAI
3. Considere upgrade do plano

### Erro: "Insufficient credits"

**Solução:**
1. Adicione créditos na conta OpenAI
2. Configure método de pagamento
3. Ou desative IA (remove chave)

---

## 📊 Monitoramento

### Dashboard OpenAI

1. Acesse: https://platform.openai.com/usage
2. Monitore:
   - Requisições por dia
   - Tokens consumidos
   - Custo acumulado
   - Erros e falhas

### Logs do Sistema

**Verificar logs:**
```bash
# Localmente
# Aparece no terminal onde o Streamlit está rodando

# Streamlit Cloud
# Settings → Logs → View logs
```

**O que procurar:**
```
INFO:copiloto_ai_service:IA disponível: chave encontrada
INFO:copiloto_ai_service:Consultando OpenAI (modelo: gpt-4o-mini)
INFO:copiloto_ai_service:Resposta recebida da IA (542 caracteres)
```

---

## 🎯 Exemplo Completo

### Arquivo `.streamlit/secrets.toml`

```toml
# =============================================================================
# Configuração de Secrets - Módulo COPILOTO
# =============================================================================
# IMPORTANTE: Este arquivo NÃO deve ser commitado no Git
# Adicione ao .gitignore: .streamlit/secrets.toml
# =============================================================================

# -----------------------------------------------------------------------------
# OpenAI API (Módulo COPILOTO - IA Generativa)
# -----------------------------------------------------------------------------
# Obtenha sua chave em: https://platform.openai.com/api-keys
# Monitore uso em: https://platform.openai.com/usage
# -----------------------------------------------------------------------------
[openai]
api_key = "sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# -----------------------------------------------------------------------------
# Outras configurações (futuro)
# -----------------------------------------------------------------------------
# [azure_openai]
# endpoint = "https://sua-instancia.openai.azure.com/"
# api_key = "sua-chave-azure"
# api_version = "2024-02-15-preview"

# [anthropic]
# api_key = "sk-ant-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

### Estrutura de Diretórios

```
contrato-regional-ia/
├── .streamlit/
│   ├── secrets.toml           # ⚠️ NÃO COMMITAR
│   └── config.toml            # Configurações gerais (pode commitar)
├── .gitignore                 # Deve conter: .streamlit/secrets.toml
├── services/
│   └── copiloto_ai_service.py # Serviço de IA
├── agents/
│   └── copilot_agent.py       # Agente híbrido
├── pages/
│   └── 02_💬_Copiloto.py      # Interface
└── requirements.txt           # Inclui: openai>=1.12.0
```

---

## 📚 Referências

**OpenAI:**
- Documentação: https://platform.openai.com/docs
- Preços: https://openai.com/pricing
- Status: https://status.openai.com/

**Streamlit:**
- Secrets: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
- Configuração: https://docs.streamlit.io/library/advanced-features/configuration

---

## 📞 Suporte

**Problemas técnicos:**
- Verifique logs do sistema
- Revise configuração de secrets
- Consulte documentação OpenAI

**Dúvidas sobre configuração:**
- Consulte: [COPILOTO_IA_IMPLEMENTACAO.md](COPILOTO_IA_IMPLEMENTACAO.md)
- Entre em contato com a equipe de desenvolvimento

---

**Última atualização:** Janeiro 2026
