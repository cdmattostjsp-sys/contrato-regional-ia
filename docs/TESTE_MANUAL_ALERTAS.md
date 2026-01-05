# 🧪 Guia de Teste Manual - Módulo de Alertas Consolidado

## 📋 Objetivo dos Testes

Validar que o módulo de alertas funciona conforme especificado como **instrumento de governança administrativa**, com rastreabilidade completa.

---

## ✅ Checklist de Validação

### Pré-requisitos

- [ ] Aplicação rodando localmente (`streamlit run app.py`)
- [ ] Pelo menos 2 contratos cadastrados
- [ ] Um contrato com vigência < 60 dias (para gerar alerta crítico)

---

## 🧪 Testes Funcionais

### Teste 1: Geração Automática de Alertas

**Objetivo:** Verificar que alertas são calculados automaticamente

**Passos:**
1. Acesse Home e visualize contratos
2. Navegue para 🔔 Alertas
3. Aguarde carregamento

**Resultado Esperado:**
- ✅ Alertas são exibidos em cards coloridos
- ✅ Métricas aparecem no topo (Críticos, Atenção, Info, Total)
- ✅ Cada alerta mostra: tipo, categoria, data, título, descrição, contrato

**Status:** [ ] Passou [ ] Falhou

---

### Teste 2: Verificação de Status ATIVO

**Objetivo:** Confirmar que alertas gerados têm status ATIVO

**Passos:**
1. Na página de alertas, observe os alertas listados
2. Inspecione via browser dev tools (opcional)

**Resultado Esperado:**
- ✅ Todos os alertas novos aparecem na lista
- ✅ Nenhum alerta gerado automaticamente está oculto

**Status:** [ ] Passou [ ] Falhou

---

### Teste 3: Filtros de Alertas

**Objetivo:** Validar funcionalidade de filtros

**Passos:**
1. Selecione filtro "🔴 Críticos"
2. Observe lista atualizada
3. Selecione filtro por categoria
4. Clique em "🔄 Atualizar"

**Resultado Esperado:**
- ✅ Filtro por tipo funciona corretamente
- ✅ Filtro por categoria funciona corretamente
- ✅ Botão atualizar recalcula alertas

**Status:** [ ] Passou [ ] Falhou

---

### Teste 4: Ações do Alerta

**Objetivo:** Verificar botões de ação

**Passos:**
1. Em um alerta qualquer, clique "📄 Ver Contrato"
2. Volte e clique "📝 Gerar Notificação"
3. Volte aos alertas

**Resultado Esperado:**
- ✅ "Ver Contrato" redireciona para página do contrato
- ✅ "Gerar Notificação" redireciona para notificações
- ✅ Contrato correto é selecionado automaticamente

**Status:** [ ] Passou [ ] Falhou

---

### Teste 5: Resolução de Alerta - Validação

**Objetivo:** Verificar que justificativa é obrigatória

**Passos:**
1. Clique "✅ Marcar Resolvido" em um alerta
2. Observe formulário que aparece
3. Tente submeter sem preencher justificativa
4. Clique "Registrar Resolução"

**Resultado Esperado:**
- ✅ Formulário modal aparece
- ✅ Texto institucional visível ("Ato Administrativo")
- ✅ Campo de justificativa é obrigatório
- ✅ Erro é exibido se justificativa vazia
- ✅ Não permite registro sem justificativa

**Status:** [ ] Passou [ ] Falhou

---

### Teste 6: Resolução de Alerta - Registro Completo

**Objetivo:** Validar resolução com justificativa válida

**Passos:**
1. Clique "✅ Marcar Resolvido" em um alerta crítico
2. Preencha justificativa: "Teste de resolução - prorrogação formalizada"
3. Clique "Registrar Resolução"
4. Aguarde confirmação

**Resultado Esperado:**
- ✅ Mensagem de sucesso aparece
- ✅ Página recarrega
- ✅ Alerta não aparece mais na lista
- ✅ Contadores são atualizados

**Status:** [ ] Passou [ ] Falhou

---

### Teste 7: Persistência da Resolução

**Objetivo:** Verificar que resolução foi salva permanentemente

**Passos:**
1. Após resolver alerta (Teste 6)
2. Feche e reabra a página de alertas
3. Verifique que alerta continua não visível

**Resultado Esperado:**
- ✅ Alerta resolvido NÃO reaparece após reload
- ✅ Sistema "lembra" que foi resolvido

**Status:** [ ] Passou [ ] Falhou

---

### Teste 8: Histórico do Contrato

**Objetivo:** Verificar integração com history_service

**Passos:**
1. Após resolver um alerta (Teste 6)
2. Navegue para a página do contrato relacionado
3. Acesse aba/seção de "Histórico" (se disponível)
4. Ou verifique `data/history.db` via SQLite

**Resultado Esperado:**
- ✅ Evento "RESOLUCAO_ALERTA" registrado
- ✅ Título contém nome do alerta
- ✅ Detalhes contêm justificativa
- ✅ Ator identifica usuário
- ✅ Metadata JSON está completo

**Como verificar history.db:**
```bash
sqlite3 data/history.db
SELECT * FROM contract_history WHERE event_type = 'RESOLUCAO_ALERTA';
.quit
```

**Status:** [ ] Passou [ ] Falhou

---

### Teste 9: Persistência JSON

**Objetivo:** Validar estrutura do arquivo de alertas resolvidos

**Passos:**
1. Após resolver alerta (Teste 6)
2. Abra arquivo `data/alertas_resolvidos.json`
3. Verifique estrutura

**Resultado Esperado:**
- ✅ Arquivo existe
- ✅ Formato JSON válido
- ✅ Contém objeto do alerta resolvido
- ✅ Campos presentes: id, status, justificativa, data, usuario
- ✅ Status = "RESOLVIDO"

**Exemplo esperado:**
```json
[
  {
    "id": "VIG_CRIT_123",
    "status": "RESOLVIDO",
    "justificativa": "Teste de resolução - prorrogação formalizada",
    "data": "2026-01-05T14:30:00",
    "usuario": "Gestor",
    "alerta_tipo": "critico",
    "alerta_categoria": "Vigência",
    "contrato_numero": "45/2024"
  }
]
```

**Status:** [ ] Passou [ ] Falhou

---

### Teste 10: Cancelamento de Resolução

**Objetivo:** Validar botão cancelar

**Passos:**
1. Clique "✅ Marcar Resolvido" em alerta
2. Formulário abre
3. Clique "❌ Cancelar"

**Resultado Esperado:**
- ✅ Formulário fecha
- ✅ Alerta permanece na lista
- ✅ Nada é salvo

**Status:** [ ] Passou [ ] Falhou

---

### Teste 11: Linguagem Institucional

**Objetivo:** Verificar adequação do texto da interface

**Passos:**
1. Expanda "ℹ️ Sobre o Sistema de Alertas e Governança"
2. Leia conteúdo

**Resultado Esperado:**
- ✅ Texto claro e institucional
- ✅ Explica modelo de governança
- ✅ Separação conceitual clara (aponta/resolve/registra)
- ✅ Não menciona "em desenvolvimento"
- ✅ Linguagem formal e defensável

**Status:** [ ] Passou [ ] Falhou

---

### Teste 12: Envio de Email (Se Configurado)

**Objetivo:** Validar notificações automáticas

**Pré-requisito:** Email configurado em ⚙️ Configurações

**Passos:**
1. Configure email em Configurações
2. Gere alerta crítico (ou aguarde sistema recalcular)
3. Verifique envio automático

**Resultado Esperado:**
- ✅ Email enviado para gestor
- ✅ Mensagem formatada institucionalmente
- ✅ Não envia duplicados

**Status:** [ ] Passou [ ] Falhou [ ] Não testado (sem config)

---

## 🔍 Testes de Rastreabilidade

### Teste 13: Auditoria Completa

**Objetivo:** Validar rastreabilidade de ponta a ponta

**Cenário:**
1. Sistema gera alerta automático (registro 1)
2. Gestor resolve com justificativa (registro 2)
3. Sistema registra no histórico (registro 3)

**Verificações:**

| Item | Local | Status |
|------|-------|--------|
| Alerta gerado | Tela de alertas | [ ] OK |
| Status inicial = ATIVO | `calcular_alertas()` | [ ] OK |
| Justificativa capturada | Formulário UI | [ ] OK |
| Resolução salva | `alertas_resolvidos.json` | [ ] OK |
| Status = RESOLVIDO | JSON | [ ] OK |
| Evento registrado | `history.db` | [ ] OK |
| Tipo = RESOLUCAO_ALERTA | SQLite | [ ] OK |
| Usuário identificado | JSON + DB | [ ] OK |
| Data/hora registrada | JSON + DB | [ ] OK |
| Alerta não reaparece | UI após reload | [ ] OK |

**Status Geral:** [ ] Passou [ ] Falhou

---

## 📊 Testes de Estatísticas

### Teste 14: Funções de Auditoria

**Objetivo:** Validar funções auxiliares

**Método:** Console Python ou Jupyter

```python
from services.alert_service import (
    carregar_alertas_resolvidos,
    obter_estatisticas_resolucoes
)

# Teste 1: Carregar todos os resolvidos
resolvidos = carregar_alertas_resolvidos()
print(f"Total resolvidos: {len(resolvidos)}")
print(resolvidos)

# Teste 2: Filtrar por contrato
resolvidos_contrato = carregar_alertas_resolvidos(contrato_id="123")
print(f"Resolvidos do contrato 123: {len(resolvidos_contrato)}")

# Teste 3: Estatísticas
stats = obter_estatisticas_resolucoes()
print(f"Total: {stats['total']}")
print(f"Por tipo: {stats['por_tipo']}")
print(f"Por categoria: {stats['por_categoria']}")
print(f"Por usuário: {stats['por_usuario']}")
print(f"Últimas 10: {len(stats['ultimas_resolucoes'])}")
```

**Resultado Esperado:**
- ✅ Todas as funções retornam dados válidos
- ✅ Filtro por contrato funciona
- ✅ Estatísticas calculadas corretamente

**Status:** [ ] Passou [ ] Falhou

---

## 🛡️ Testes de Segurança e Compliance

### Teste 15: Imutabilidade

**Objetivo:** Garantir que resoluções não podem ser alteradas

**Passos:**
1. Resolva um alerta
2. Tente editar `alertas_resolvidos.json` manualmente
3. Recarregue aplicação

**Resultado Esperado:**
- ✅ Sistema não oferece opção de editar resolução via UI
- ✅ Edição manual não tem reflexo (sistema ignora)
- ✅ Princípio de imutabilidade é respeitado

**Status:** [ ] Passou [ ] Falhou

---

### Teste 16: Não Exclusão de Alertas

**Objetivo:** Verificar que alertas resolvidos nunca são excluídos

**Passos:**
1. Resolva vários alertas
2. Verifique `alertas_resolvidos.json`
3. Aguarde recálculo automático

**Resultado Esperado:**
- ✅ Alertas resolvidos permanecem no arquivo JSON
- ✅ Não são excluídos automaticamente
- ✅ Histórico é preservado permanentemente

**Status:** [ ] Passou [ ] Falhou

---

## 📝 Checklist Final de Consolidação

### Funcionalidades Core

- [ ] Geração automática de alertas (5 regras)
- [ ] Estados ATIVO/RESOLVIDO implementados
- [ ] Justificativa obrigatória validada
- [ ] Registro no histórico (RESOLUCAO_ALERTA)
- [ ] Persistência JSON enriquecida
- [ ] Interface de resolução funcional
- [ ] Filtros por tipo/categoria operacionais
- [ ] Linguagem institucional adequada

### Rastreabilidade

- [ ] Usuário identificado em cada resolução
- [ ] Data/hora registrada com precisão
- [ ] Justificativas capturadas corretamente
- [ ] Eventos no histórico consultáveis
- [ ] Alertas resolvidos não reaparecem
- [ ] Funções de auditoria operacionais

### Documentação

- [ ] `docs/MODULO_ALERTAS.md` completo
- [ ] `README.md` atualizado
- [ ] `DEVELOPER_GUIDE.md` atualizado
- [ ] Sumário executivo criado

### Compliance

- [ ] Alertas nunca são excluídos
- [ ] Resoluções são imutáveis
- [ ] Princípio de governança respeitado
- [ ] Código sem erros de lint

---

## 📊 Relatório de Testes

### Resumo Executivo

**Data dos testes:** _____________  
**Testador:** _____________  
**Versão testada:** Consolidação v1.0

**Resultados:**

| Categoria | Total | Passou | Falhou | N/A |
|-----------|-------|--------|--------|-----|
| Funcionais | 12 | [ ] | [ ] | [ ] |
| Rastreabilidade | 1 | [ ] | [ ] | [ ] |
| Estatísticas | 1 | [ ] | [ ] | [ ] |
| Segurança | 2 | [ ] | [ ] | [ ] |
| **TOTAL** | **16** | [ ] | [ ] | [ ] |

### Observações

_Registre aqui quaisquer observações, bugs ou sugestões de melhoria:_

```
1. 

2. 

3. 

```

### Recomendação Final

- [ ] ✅ **APROVADO** - Sistema pronto para demonstração institucional
- [ ] ⚠️ **APROVADO COM RESSALVAS** - Ajustes menores necessários
- [ ] ❌ **REPROVADO** - Correções críticas necessárias

---

## 🚀 Próximos Passos

Após aprovação nos testes:

1. [ ] Commit das alterações
2. [ ] Demonstração para stakeholders internos
3. [ ] Coleta de feedback
4. [ ] Ajustes finos (se necessário)
5. [ ] Preparação para avaliação STI/SAAB

---

**Guia preparado em:** Janeiro/2026  
**Última atualização:** Consolidação do módulo
