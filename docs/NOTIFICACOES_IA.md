# 📝 Módulo de Notificações com IA - Documentação

## 📋 Visão Geral

Implementação de **geração assistida por IA** no módulo de Notificações Contratuais, permitindo que fiscais e gestores obtenham sugestões de textos formais institucionais via IA generativa.

**Versão:** 1.1.0  
**Status:** ✅ Implementado

---

## 🎯 Funcionalidade

### O Que Foi Implementado

**Botão "✨ Gerar Sugestão com IA"** na página de notificações:
1. Coleta contexto do contrato (sanitizado)
2. Coleta dados do formulário (tipo, motivo, prazo, fundamentação)
3. Envia à IA para gerar sugestão de texto formal
4. Exibe texto sugerido em área editável
5. Permite revisão e ajuste antes de usar
6. Servidor é sempre o autor final

---

## 🔒 Princípios Institucionais Atendidos

✅ **IA sugere; servidor é o autor final**  
✅ **Nenhuma notificação enviada automaticamente**  
✅ **Toda sugestão é editável**  
✅ **Sistema funciona sem IA** (templates padrão)  
✅ **IA pode ser desativada** (remove chave)  
✅ **Contexto mínimo e sanitizado** (sem dados sensíveis)  

---

## 🏗️ Arquitetura

### Service Layer

```
services/notificacao_ai_service.py
│
├── is_ai_enabled()                     # Verifica disponibilidade
├── gerar_sugestao_notificacao()        # ⭐ Função principal
├── registrar_geracao_notificacao()     # Governança
└── _consultar_openai_notificacao()     # Integração OpenAI
```

### Integração na UI

```
pages/03_📝_Notificações.py
│
├── Botão "✨ Gerar Sugestão com IA"
├── Área de exibição da sugestão (editável)
├── Botões: Usar / Gerar Nova / Descartar
└── Pré-visualização (template padrão mantido)
```

---

## 🔑 Como Ativar

### Passo 1: Configurar Chave OpenAI

**No Streamlit Cloud:**
```
Settings → Secrets → Adicionar:

[openai]
api_key = "sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

**OU (formato flat):**
```
OPENAI_API_KEY = "sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

### Passo 2: Instalar Dependência

```bash
pip install openai
```

### Passo 3: Testar

1. Acesse página **📝 Notificações**
2. Selecione um contrato
3. Preencha: tipo, motivo, prazo
4. Clique em **"✨ Gerar Sugestão com IA"**

**Com IA ativa:**
- ✅ Sugestão gerada
- ✅ Texto editável exibido
- ✅ Botões de ação disponíveis

**Sem IA (modo degradado):**
- ℹ️ Mensagem: "Recurso de apoio inteligente indisponível"
- ✅ Templates padrão continuam funcionando normalmente

---

## 🔒 Dados Sanitizados (Segurança)

### O Que É Enviado à IA

✅ **Enviado:**
- Número do contrato
- Nome do fornecedor
- Objeto do contrato (primeiros 200 caracteres)
- Vigência
- Status
- Tipo de notificação
- Categoria (Gestor/Fiscal)
- Motivo descrito pelo usuário
- Prazo selecionado
- Fundamentação fornecida (opcional)

❌ **NÃO Enviado:**
- CPF de pessoas
- Emails pessoais
- Números de documentos sensíveis
- Dados financeiros detalhados
- Histórico completo

---

## 📊 Fluxo de Funcionamento

```
┌──────────────────────────────────────────┐
│ Usuário preenche formulário             │
│ • Tipo, motivo, prazo, fundamentação    │
└───────────────┬──────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────┐
│ Clica "✨ Gerar Sugestão com IA"       │
└───────────────┬──────────────────────────┘
                │
                ▼
        ┌───────────────┐
        │ IA disponível?│
        └───┬───────┬───┘
         SIM│       │NÃO
            ▼       ▼
    ┌──────────┐  ┌──────────────┐
    │ Consulta │  │ Mensagem     │
    │ OpenAI   │  │ institucional│
    └────┬─────┘  └──────┬───────┘
         │               │
         └───────┬───────┘
                 ▼
    ┌────────────────────────┐
    │ Exibe sugestão editável│
    │ + Botões de ação       │
    └────────┬───────────────┘
             │
             ▼
    ┌────────────────────────┐
    │ Usuário revisa e edita │
    └────────┬───────────────┘
             │
             ▼
    ┌────────────────────────┐
    │ "✅ Usar Este Texto"   │
    │ Aplica à pré-visualiza│
    └────────────────────────┘
```

---

## 🎓 Prompt Institucional

### Diretrizes para a IA

O serviço usa um prompt específico que instrui a IA a:

✅ Usar linguagem formal e institucional  
✅ Ser objetiva e direta  
✅ NÃO inventar normas, prazos ou fatos  
✅ Indicar onde falta informação: `[A COMPLEMENTAR]`  
✅ Estrutura clara: considerandos → determinações → prazo → fechamento  
✅ Tom respeitoso mas firme  
✅ NÃO tomar decisões administrativas  

### Estrutura Esperada da Sugestão

1. Identificação do destinatário
2. Assunto/Referência do contrato
3. Considerandos (contexto legal)
4. Comunicação/Determinação principal
5. Prazo para atendimento
6. Fundamentação legal
7. Advertências/Consequências (se aplicável)
8. Fechamento institucional

---

## 📝 Exemplo de Uso

### Entrada do Usuário

**Tipo:** Solicitação de Correção  
**Motivo:** Atraso recorrente na execução do serviço de limpeza no setor administrativo durante o mês de janeiro/2026  
**Prazo:** 5 dias úteis  
**Fundamentação:** Cláusula 7ª do contrato; Lei 14.133/2021  

### Saída da IA (Exemplo)

```
À EMPRESA ABC LTDA – CNPJ 00.000.000/0001-00
Endereço: Rua Exemplo, 123 - São Paulo/SP
Assunto: Solicitação de correção – Contrato nº 123/2025
São Paulo, 05 de janeiro de 2026

Prezado(a) Senhor(a),

CONSIDERANDO o Contrato nº 123/2025, relativo a "Prestação de 
Serviços de Limpeza e Conservação Predial";

CONSIDERANDO a obrigação da CONTRATADA de manter a execução regular 
e conforme especificações pactuadas;

CONSIDERANDO a ocorrência registrada: Atraso recorrente na execução 
do serviço de limpeza no setor administrativo durante o mês de 
janeiro/2026;

DETERMINA-SE que a CONTRATADA promova a correção/adequação do item 
apontado, com apresentação de evidências de regularização (relatório, 
fotos, checklist ou outros meios idôneos), no prazo de 5 dias úteis.

Se houver impedimento ou necessidade de alinhamento operacional, a 
CONTRATADA deve informar formalmente, justificando e propondo plano 
de correção no mesmo prazo.

FUNDAMENTAÇÃO LEGAL:
Cláusula 7ª do contrato; Lei 14.133/2021

Atenciosamente,

[Nome do Fiscal]
Fiscal do Contrato
RAJ 10.1 - TJSP

---
⚠️ IMPORTANTE: Este texto foi gerado por IA como sugestão inicial.
REVISE INTEGRALMENTE antes de salvar/enviar. O servidor é o autor final.
```

---

## 🔧 Como Desativar

### Opção 1: Temporária (Remove Chave)

No Streamlit Cloud:
```
Settings → Secrets → Remover seção [openai]
```

✅ Sistema volta ao modo padrão (templates)  
✅ Nenhuma quebra de funcionalidade  

### Opção 2: Permanente (Remove Código)

```bash
# 1. Remover serviço
rm services/notificacao_ai_service.py

# 2. Reverter página (remover importações e botão IA)
git checkout pages/03_📝_Notificações.py

# 3. Remover dependência (opcional)
# Editar requirements.txt e remover openai
```

---

## 📊 Governança e Rastreabilidade

### O Que É Registrado

Evento: `NOTIFICACAO_GERADA_COM_IA`

**Metadados armazenados:**
- ✅ Contrato ID
- ✅ Tipo de notificação
- ✅ Categoria (Gestor/Fiscal)
- ✅ Modo (IA_ATIVA | MODO_PADRAO | ERRO_IA)
- ✅ Timestamp
- ✅ Usuário (se disponível)

**NÃO armazenado:**
- ❌ Texto completo da notificação
- ❌ Motivo descrito
- ❌ Conteúdo sensível

---

## ✅ Checklist de Teste Manual

### Teste 1: IA Disponível ✅
1. Configure chave em `st.secrets`
2. Acesse página de Notificações
3. Selecione contrato
4. Preencha tipo, motivo, prazo
5. Clique "✨ Gerar Sugestão com IA"
6. **Esperado:** Sugestão exibida em área editável

### Teste 2: Editar Sugestão ✅
1. Após gerar sugestão
2. Edite o texto na área editável
3. Clique "✅ Usar Este Texto"
4. **Esperado:** Texto aplicado à pré-visualização

### Teste 3: IA Indisponível ✅
1. Remova chave de `st.secrets`
2. Clique "✨ Gerar Sugestão com IA"
3. **Esperado:** Mensagem "Recurso indisponível" + template padrão funciona

### Teste 4: Descartar Sugestão ✅
1. Gere sugestão com IA
2. Clique "❌ Descartar"
3. **Esperado:** Sugestão removida, template padrão exibido

### Teste 5: Gerar Nova Sugestão ✅
1. Gere primeira sugestão
2. Clique "🔄 Gerar Nova Sugestão"
3. **Esperado:** Nova consulta à IA, texto diferente

### Teste 6: Limpar Formulário ✅
1. Preencha formulário
2. Gere sugestão
3. Clique "🗑️ Limpar"
4. **Esperado:** Todos os campos limpos, incluindo sugestão

### Teste 7: Diferentes Tipos de Notificação ✅
1. Teste com: Advertência, Solicitação de Correção, Notificação Prévia de Penalidade
2. **Esperado:** Textos diferentes, apropriados a cada tipo

### Teste 8: Histórico Registrado ✅
1. Gere notificação com IA
2. Verifique logs/histórico
3. **Esperado:** Evento `NOTIFICACAO_GERADA_COM_IA` registrado

---

## 💰 Custos Estimados

### Modelo: gpt-4o-mini

**Por notificação:** ~$0.0005  
**100 notificações/mês:** ~$0.05  
**1.000 notificações/mês:** ~$0.50  
**10.000 notificações/mês:** ~$5.00  

💡 **Custo desprezível para uso institucional**

---

## 📚 Arquivos Criados/Modificados

### ✨ Novo (1)
- `services/notificacao_ai_service.py` (~450 linhas)

### ✏️ Modificado (1)
- `pages/03_📝_Notificações.py` (integração com IA)

### 📄 Documentação (1)
- `docs/NOTIFICACOES_IA.md` (este arquivo)

---

## 🔒 Segurança

✅ Chave via `st.secrets` (nunca hardcoded)  
✅ Contexto sanitizado (sem dados sensíveis)  
✅ Validação de disponibilidade  
✅ Tratamento de erros  
✅ Logs sem conteúdo  
✅ Modo degradado automático  
✅ Usuário sempre é autor final  

---

## 🎯 Compatibilidade

✅ **Zero breaking changes**  
✅ **Templates padrão preservados**  
✅ **Funciona com ou sem IA**  
✅ **Mesma interface do usuário**  
✅ **Mesmos fluxos de salvamento/envio**  

---

## 📞 Suporte

**Ativar IA:**
- Configure `st.secrets` (ver seção "Como Ativar")

**Desativar IA:**
- Remova chave de `st.secrets`

**Problemas:**
- Verifique logs: `INFO:notificacao_ai_service:...`
- Teste disponibilidade: `is_ai_enabled()`

---

**Última atualização:** Janeiro 2026  
**Versão:** 1.0  
**Status:** ✅ Produção
