# 🎯 Guia Rápido - IA no COPILOTO

**5 minutos para entender e ativar**

---

## 🤔 O Que É?

IA generativa integrada ao módulo COPILOTO para **ajudar** fiscais de contrato com perguntas sobre contratos.

**⚠️ IMPORTANTE:**
- IA apenas **sugere** (não decide)
- Você sempre valida a resposta
- Sistema funciona **com ou sem** IA

---

## 🚀 Como Ativar (3 passos)

### 1️⃣ Obter Chave OpenAI

```
1. Vá em: https://platform.openai.com/
2. Faça login
3. API Keys → Create new secret key
4. Copie a chave (começa com sk-proj-...)
```

### 2️⃣ Configurar no Sistema

**Localmente:**
```bash
# Criar arquivo de secrets
mkdir -p .streamlit
echo '[openai]
api_key = "sk-proj-SUA-CHAVE-AQUI"' > .streamlit/secrets.toml
```

**Streamlit Cloud:**
```
Settings → Secrets → Cole:
[openai]
api_key = "sua-chave-aqui"
```

### 3️⃣ Instalar e Executar

```bash
pip install openai
streamlit run Home.py
```

✅ **Pronto!** A IA está ativa.

---

## 🧪 Como Testar

1. Abra a página **💬 Copiloto**
2. Selecione um contrato
3. Digite: *"Qual é o prazo de vigência?"*

**✅ Com IA ativa:**
```
📅 Vigência do Contrato

Com base nas informações fornecidas, o contrato vigora de...

[resposta detalhada]

---
⚠️ Esta resposta foi gerada por IA como apoio textual...
```

**ℹ️ Sem IA (modo padrão):**
```
🤖 Recurso de apoio inteligente indisponível no momento.

Informações do Contrato:
- Número: 123/2025
- Fornecedor: Empresa XYZ

Como obter ajuda:
- Consulte a página "Como Proceder"
- Acesse a "Biblioteca"...
```

---

## 💰 Quanto Custa?

**Modelo usado:** gpt-4o-mini (mais econômico)

| Uso | Custo/mês |
|-----|-----------|
| 1.000 perguntas | $0.30 |
| 10.000 perguntas | $3.00 |
| 50.000 perguntas | $15.00 |

💡 **Custo desprezível para uso institucional**

---

## 🔒 É Seguro?

✅ **SIM.** A implementação segue padrões institucionais:

- Chave **nunca** no código (usa `st.secrets`)
- Sistema funciona **sem IA** se necessário
- IA **não toma decisões** administrativas
- Respostas **não são vinculantes**
- Uso é **rastreado** (sem gravar perguntas)

---

## 🔄 Como Desativar

**Opção 1:** Remove chave (temporário)
```bash
rm .streamlit/secrets.toml
```
Sistema volta ao modo padrão. **Sem quebra.**

**Opção 2:** Remove integração (permanente)
```bash
rm services/copiloto_ai_service.py
# Reverter agents/copilot_agent.py
```

---

## ❓ Perguntas Frequentes

### A IA vai tomar decisões por mim?
**NÃO.** A IA apenas sugere. Você sempre valida e decide.

### E se a IA errar?
Por isso toda resposta tem rodapé: "Valide com fontes oficiais".

### O sistema para de funcionar sem IA?
**NÃO.** Ele volta ao modo padrão automaticamente.

### Quem tem acesso à chave?
Apenas administradores do sistema.

### As perguntas são gravadas?
NÃO. Apenas metadados estatísticos (data, contrato ID).

### Posso usar em produção?
SIM. Está pronto para produção.

---

## 📚 Quer Saber Mais?

**Guias Completos:**
- 📖 Implementação: `docs/COPILOTO_IA_IMPLEMENTACAO.md`
- 🔧 Configuração: `docs/CONFIGURACAO_CHAVES_API.md`
- 📊 Resumo: `docs/RESUMO_EXECUTIVO_IA.md`
- 📦 Entrega: `docs/ENTREGA_TECNICA.md`

**Scripts:**
- Setup: `scripts/setup_copiloto_ia.sh`
- Validação: `scripts/validar_copiloto_ia.py`

---

## 🎯 Resumo em 3 Pontos

1. **IA ajuda, você decide** - Apoio textual não vinculante
2. **Funciona com ou sem IA** - Modo degradado automático
3. **Seguro e reversível** - Padrões institucionais

---

## ✅ Checklist de Ativação

- [ ] Obter chave OpenAI
- [ ] Configurar em `st.secrets`
- [ ] Instalar `pip install openai`
- [ ] Executar `streamlit run Home.py`
- [ ] Testar no módulo COPILOTO
- [ ] Verificar rodapé "gerado por IA"

---

**Tempo total:** ~5 minutos  
**Dificuldade:** Fácil  
**Impacto:** Alto  

**Dúvidas?** Consulte a documentação completa em `docs/`

---

**Versão:** 1.0  
**Data:** Janeiro 2026  
**Status:** ✅ Pronto para uso
