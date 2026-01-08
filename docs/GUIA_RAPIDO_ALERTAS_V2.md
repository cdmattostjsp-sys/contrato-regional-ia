# 🚀 Guia Rápido: Novo Sistema de Alertas V2

## 📋 Como Usar o Novo Modelo

### 🎯 Passo 1: Ativar o Modo V2

1. Acesse a página **🔔 Alertas** no menu lateral
2. No topo da página, você verá um toggle: **"🚀 Novo Modelo (V2)"**
3. Ative o toggle
4. O sistema irá:
   - Importar automaticamente alguns alertas como exemplo
   - Exibir a nova interface com métricas avançadas

### 🔄 Passo 2: Escolher Modo de Visualização

Após ativar o V2, você pode escolher:

- **"Apenas V2"** - Ver somente os alertas no novo formato
- **"Comparar V1 vs V2"** - Ver ambos os sistemas lado a lado

### 📊 Passo 3: Explorar um Alerta V2

Cada card de alerta V2 mostra:

```
┌─────────────────────────────────────────────────┐
│ 🔵 PREVENTIVO   EM_ANALISE   ▲ ALTA            │
│                                                 │
│ ### Título do Alerta                            │
│ Descrição detalhada...                         │
│                                                 │
│ Contrato: 123/2025                             │
│ Responsável: gestor.silva                      │
│ Geração: 🌱 1 (raiz)                           │
│                                                 │
│ ⏱️ Prazo: 30d     🛡️ Janela: 10d    ⚠️ Risco: 45% │
│                                                 │
│ [📄 Contrato] [📝 Ação] [📊 Histórico] [✅]    │
└─────────────────────────────────────────────────┘
```

**Métricas explicadas:**

- **⏱️ Prazo:** Dias restantes para resposta
- **🛡️ Janela:** Tempo real disponível (prazo - tempo médio de execução)
- **⚠️ Risco:** Score calculado automaticamente (0-100%)

### 📝 Passo 4: Registrar uma Ação

1. Clique no botão **"📝 Registrar Ação"** no card
2. Selecione o tipo de ação:
   - ✅ Decisão: Renovar contrato
   - ❌ Decisão: Não renovar
   - 📢 Decisão: Nova licitação
   - ⚙️ Providência: Iniciar processo
   - 📄 Providência: Solicitar documentação
   - ⏱️ Justificativa: Adiamento
   - 🔍 Verificação realizada

3. Preencha a **justificativa** (obrigatória, mín. 10 caracteres)
4. Opcionalmente:
   - Defina um novo prazo
   - Anexe documentos relacionados
5. Clique em **"✅ Registrar Ação"**

**O sistema irá:**
- Criar registro permanente da ação
- Vincular ao alerta
- Atualizar o estado automaticamente
- Registrar data, hora e usuário

### 📊 Passo 5: Ver Histórico Completo

1. Clique no botão **"📊 Histórico"** no card
2. Você verá:
   - **Timeline de estados** - Todas as transições com datas
   - **Ações registradas** - Lista de decisões tomadas
   - **Análise de risco** - Fatores que compõem o score

**Exemplo de timeline:**

```
🆕 NOVO - 08/01/2026 10:00
└─ Usuário: sistema
   Observação: Alerta criado automaticamente

🔍 EM_ANALISE - 08/01/2026 14:30
└─ Usuário: gestor.silva
   Observação: Iniciando análise do contrato
```

### ✅ Passo 6: Resolver um Alerta

1. Clique no botão **"✅ Resolver"** no card
2. Preencha a **justificativa de resolução**
3. Clique em **"✅ Confirmar"**

**O sistema irá:**
- Transicionar estado para "resolvido"
- Registrar justificativa no histórico
- Remover da lista de alertas ativos
- Manter registro permanente para auditoria

---

## 🔄 Como Comparar V1 vs V2

### Modo Comparação

1. Ative o toggle V2
2. Selecione **"Comparar V1 vs V2"**
3. Você verá:

```
┌──────────────────┬──────────────────┐
│ Sistema V1       │ Sistema V2       │
│ (Tradicional)    │ (Ciclo de Vida)  │
├──────────────────┼──────────────────┤
│ • Notificação    │ • Processo       │
│ • Status simples │ • 7 estados      │
│ • Sem histórico  │ • Timeline       │
│ • Sem métricas   │ • Risco/Janela   │
└──────────────────┴──────────────────┘
```

### Estatísticas Comparativas

**V1 mostra:**
- 🔴 Críticos
- 🟡 Atenção
- 🔵 Informativos

**V2 mostra:**
- 📊 Total de alertas
- 🔴 Alertas em risco alto
- ⚠️ Score de risco médio
- 📋 Total de ações registradas

---

## 💡 Dicas de Uso

### ✅ Boas Práticas

1. **Sempre registre justificativas completas**
   - Inclua fundamentação legal quando aplicável
   - Mencione documentos relacionados
   - Descreva o contexto da decisão

2. **Use os tipos de ação corretos**
   - Decisões para escolhas finais
   - Providências para ações em andamento
   - Justificativas para adiamentos

3. **Monitore o score de risco**
   - Score > 70% = Atenção urgente
   - Score 40-70% = Acompanhamento necessário
   - Score < 40% = Situação controlada

4. **Observe a janela de segurança**
   - Janela negativa = Risco de ruptura
   - Janela < 5 dias = Situação apertada
   - Janela > 10 dias = Tempo adequado

### ⚠️ O Que Evitar

❌ Não registre ações sem justificativa completa  
❌ Não ignore alertas com janela negativa  
❌ Não resolva alertas sem documentar a solução  
❌ Não deixe alertas críticos sem resposta  

---

## 🔧 Funcionalidades Avançadas

### Encadeamento de Alertas

Quando você registra uma ação de decisão (ex: "renovar"), o sistema pode criar automaticamente um **alerta derivado** para a próxima etapa (ex: "iniciar processo de renovação").

**Identificação:**
- Alertas raiz: 🌱 Geração 1
- Alertas derivados: 🔗 Geração 2, 3, 4...

### Cálculo Automático de Risco

O score de risco é calculado com base em 4 fatores:

1. **Urgência temporal (35%)** - Dias restantes vs prazo total
2. **Criticidade (30%)** - Nível declarado (baixa/média/alta/urgente)
3. **Histórico de adiamentos (20%)** - Quantas vezes foi adiado
4. **Geração no encadeamento (15%)** - Alertas derivados são mais arriscados

### Janela de Segurança

Conceito inovador que calcula o **tempo real disponível**:

```
Janela = Dias Restantes - Tempo Médio de Execução

Exemplo:
- Prazo nominal: 120 dias
- Tempo médio para renovar: 30 dias
- Janela de segurança: 90 dias (tempo real)
```

---

## 🆘 Resolução de Problemas

### Problema: Toggle V2 não aparece

**Solução:** Atualize a página (F5)

### Problema: Nenhum alerta V2 após ativar

**Solução:** O sistema importa automaticamente. Se não aparecer:
1. Desative e reative o toggle
2. Clique em "🔄 Atualizar"

### Problema: Formulário de ação não abre

**Solução:** 
1. Feche qualquer formulário aberto
2. Atualize a página
3. Tente novamente

### Problema: Quero voltar ao V1

**Solução:** 
1. Desative o toggle "Novo Modelo (V2)"
2. O sistema volta imediatamente ao V1
3. Seus dados V2 são preservados

---

## 📞 Suporte

Para dúvidas ou problemas:
- Consulte a documentação em `docs/FASE2_UI_FEATURE_FLAG_CONCLUIDA.md`
- Veja a arquitetura em `docs/ARQUITETURA_CICLO_VIDA_ALERTAS.md`
- Entre em contato com a equipe de TI

---

## 🎓 Glossário

| Termo | Significado |
|-------|-------------|
| **Alerta raiz** | Primeiro alerta de uma cadeia (geração 1) |
| **Alerta derivado** | Alerta criado a partir de outro (geração 2+) |
| **Ciclo de vida** | Sequência de estados por qual o alerta passa |
| **Estado** | Situação atual do alerta (novo, em análise, resolvido, etc.) |
| **Janela de segurança** | Tempo real disponível após considerar execução |
| **Score de risco** | Valor de 0 a 1 (0-100%) indicando urgência |
| **Transição** | Mudança de um estado para outro |
| **Encadeamento** | Ligação entre alerta origem e derivados |

---

**Versão:** 2.0  
**Data:** 8 de janeiro de 2026  
**Status:** ✅ Documentação completa
