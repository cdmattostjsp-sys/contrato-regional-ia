# 🧪 Checklist de Teste Manual - Alertas de Execução Físico-Financeira

## 📋 Objetivo dos Testes

Validar a integração completa de alertas de execução físico-financeira (FF) com:
- Cálculo de alertas baseado em registros reais
- Integração com alert_service
- Registro de eventos no history_service
- Exibição de dados reais na página do contrato

---

## ✅ Pré-requisitos

- [ ] Aplicação rodando (`streamlit run app.py`)
- [ ] Pelo menos 1 contrato cadastrado
- [ ] Arquivo `data/execution_financial_records.json` acessível

---

## 🧪 Testes de Integração

### Teste 1: Criar Registro Financeiro para Gerar Alerta

**Objetivo:** Criar um registro que vai gerar alerta crítico (ateste pendente)

**Passos:**
1. Acesse a aplicação
2. Selecione um contrato qualquer
3. Abra o terminal e execute:

```python
from services.execution_financial_service import criar_registro
from datetime import datetime, timedelta

# Cria registro com NF pendente de ateste (emitida há 6 dias)
data_emissao = (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d')

registro = {
    'contrato_id': 'CTR001',  # Ajuste para ID do seu contrato
    'nf_numero': 'NF-TEST-001',
    'nf_data_emissao': data_emissao,
    'competencia': 'Jan/2026',
    'valor_bruto': 15000.00,
    'iss_retido': 750.00,
    'incidencia_iss': True,
    'municipio_iss': 'São Paulo',
    'aliquota_iss': 5.0,
    'data_ateste': None,
    'responsavel': 'Fiscal Teste',
    'observacoes': 'Registro de teste para alerta FF',
    'status_fluxo': 'Pendente de Ateste'
}

result = criar_registro(registro)
print(f"Registro criado: {result}")
```

**Resultado Esperado:**
- ✅ Registro criado com sucesso
- ✅ ID retornado (contrato_id_nf_numero)

**Status:** [ ] Passou [ ] Falhou

---

### Teste 2: Verificar Alerta FF na Página de Alertas

**Objetivo:** Confirmar que alerta FF aparece na página principal de alertas

**Passos:**
1. Navegue para 🔔 Alertas
2. Aguarde cálculo de alertas
3. Procure por alertas com categoria "Execução Físico-Financeira"

**Resultado Esperado:**
- ✅ Aparece alerta crítico: "Ateste pendente: NF NF-TEST-001"
- ✅ Descrição menciona "aguarda ateste há X dias"
- ✅ Categoria é "Execução Físico-Financeira"
- ✅ Contador de críticos aumentou

**Status:** [ ] Passou [ ] Falhou

---

### Teste 3: Verificar Alertas FF no Componente de Execução

**Objetivo:** Confirmar exibição na UI de execução FF

**Passos:**
1. Acesse página do contrato (01_📄_Contrato)
2. Role até encontrar seção de Execução Físico-Financeira
3. Observe bloco de "Alertas e Pendências"

**Resultado Esperado:**
- ✅ Seção mostra "🔴 Críticos: 1"
- ✅ Alerta é renderizado com descrição
- ✅ Metadados (NF, competência, dias) aparecem

**Status:** [ ] Passou [ ] Falhou

---

### Teste 4: Verificar Dados Reais na Página do Contrato

**Objetivo:** Confirmar substituição de mocks por dados reais

**Passos:**
1. Na página 01_📄_Contrato
2. Expanda "📄 Histórico Detalhado de Atestes"
3. Verifique se aparece NF-TEST-001

**Resultado Esperado:**
- ✅ NF-TEST-001 aparece na lista
- ✅ Competência: Jan/2026
- ✅ Valor: R$ 15.000,00
- ✅ Status: Pendente (ícone ⏳)
- ✅ Sem data de ateste

**Status:** [ ] Passou [ ] Falhou

---

### Teste 5: Atualizar Status e Verificar Evento no Histórico

**Objetivo:** Confirmar registro de evento ao atualizar status

**Passos:**
1. Abra terminal Python
2. Execute:

```python
from services.execution_financial_service import atualizar_status

# Atualiza status do registro
result = atualizar_status('CTR001_NF-TEST-001', 'Atestado')
print(f"Status atualizado: {result}")
```

3. Acesse página do contrato
4. Vá para aba/seção de Histórico (se disponível)

**Resultado Esperado:**
- ✅ Status atualizado com sucesso (True)
- ✅ Evento "FF_STATUS_ATUALIZADO" registrado no histórico
- ✅ Título: "Status atualizado: NF NF-TEST-001"
- ✅ Detalhes: "Status alterado de 'Pendente de Ateste' para 'Atestado'"
- ✅ Metadados incluem nf_numero, competencia, status_anterior, status_novo

**Como verificar histórico via SQLite:**
```bash
sqlite3 data/history.db
SELECT * FROM contract_history WHERE event_type = 'FF_STATUS_ATUALIZADO' ORDER BY timestamp DESC LIMIT 1;
.quit
```

**Status:** [ ] Passou [ ] Falhou

---

### Teste 6: Verificar Alerta de Pagamento Atrasado

**Objetivo:** Criar cenário de pagamento atrasado

**Passos:**
1. Execute no terminal:

```python
from services.execution_financial_service import criar_registro
from datetime import datetime, timedelta

# NF atestada há 31 dias (gera alerta de pagamento atrasado)
data_ateste = (datetime.now() - timedelta(days=31)).strftime('%Y-%m-%d')
data_emissao = (datetime.now() - timedelta(days=35)).strftime('%Y-%m-%d')

registro = {
    'contrato_id': 'CTR001',
    'nf_numero': 'NF-TEST-002',
    'nf_data_emissao': data_emissao,
    'competencia': 'Dez/2025',
    'valor_bruto': 18000.00,
    'iss_retido': 900.00,
    'incidencia_iss': True,
    'municipio_iss': 'São Paulo',
    'aliquota_iss': 5.0,
    'data_ateste': data_ateste,
    'responsavel': 'Fiscal Teste',
    'observacoes': 'Teste pagamento atrasado',
    'status_fluxo': 'Atestado'
}

criar_registro(registro)
```

2. Acesse 🔔 Alertas
3. Clique em "🔄 Atualizar"

**Resultado Esperado:**
- ✅ Aparece alerta de atenção (🟡): "Pagamento atrasado: NF NF-TEST-002"
- ✅ Descrição menciona "atestada há 31 dias"
- ✅ Categoria: "Execução Físico-Financeira"

**Status:** [ ] Passou [ ] Falhou

---

### Teste 7: Verificar Alerta de ISS Inconsistente

**Objetivo:** Criar registro com ISS inconsistente

**Passos:**
1. Execute:

```python
from services.execution_financial_service import criar_registro
from datetime import datetime

registro = {
    'contrato_id': 'CTR001',
    'nf_numero': 'NF-TEST-003',
    'nf_data_emissao': datetime.now().strftime('%Y-%m-%d'),
    'competencia': 'Jan/2026',
    'valor_bruto': 20000.00,
    'iss_retido': 0.0,  # ISS zerado com incidência = True
    'incidencia_iss': True,
    'municipio_iss': 'São Paulo',
    'aliquota_iss': 5.0,
    'data_ateste': None,
    'responsavel': 'Fiscal Teste',
    'observacoes': 'Teste ISS inconsistente',
    'status_fluxo': 'Pendente'
}

criar_registro(registro)
```

2. Acesse 🔔 Alertas
3. Expanda "🔵 Alertas Informativos"

**Resultado Esperado:**
- ✅ Aparece alerta informativo: "ISS inconsistente: NF NF-TEST-003"
- ✅ Descrição menciona "incidência de ISS, mas valor retido é zero"
- ✅ Tipo: info (azul)

**Status:** [ ] Passou [ ] Falhou

---

### Teste 8: Verificar Evento de Alertas FF Gerados

**Objetivo:** Confirmar logging de alertas FF calculados

**Passos:**
1. Acesse componente de Execução FF na página do contrato
2. Observe seção de Alertas
3. Verifique histórico do contrato

**Resultado Esperado:**
- ✅ Evento "FF_ALERTA_GERADO" no histórico
- ✅ Título: "Alertas FF calculados: X alertas"
- ✅ Detalhes: contagem por tipo
- ✅ Metadados: total_alertas, criticos, atencao, informativos

**Status:** [ ] Passou [ ] Falhou

---

### Teste 9: Resolver Alerta FF

**Objetivo:** Validar resolução de alerta FF com justificativa

**Passos:**
1. Na página 🔔 Alertas
2. Localize alerta FF (ex: "Ateste pendente: NF NF-TEST-001")
3. Clique em "✅ Marcar Resolvido"
4. Preencha justificativa: "NF atestada manualmente - processo normalizado"
5. Clique em "Registrar Resolução"

**Resultado Esperado:**
- ✅ Formulário de justificativa aparece
- ✅ Após confirmar, alerta desaparece da lista
- ✅ Evento "RESOLUCAO_ALERTA" registrado no histórico
- ✅ Alerta salvo em `alertas_resolvidos.json` com status RESOLVIDO

**Status:** [ ] Passou [ ] Falhou

---

### Teste 10: Estado Vazio (Sem Registros)

**Objetivo:** Garantir que UI funciona sem registros

**Passos:**
1. Selecione contrato sem registros financeiros (ou crie um novo)
2. Acesse página do contrato
3. Expanda "📄 Histórico Detalhado de Atestes"
4. Acesse seção de Execução FF

**Resultado Esperado:**
- ✅ Mensagem: "📭 Nenhum registro de ateste/pagamento cadastrado"
- ✅ Alertas FF: "✅ Nenhum alerta de execução físico-financeira identificado"
- ✅ Não há erro ou exceção
- ✅ UI permanece funcional

**Status:** [ ] Passou [ ] Falhou

---

### Teste 11: Filtro por Categoria na Página de Alertas

**Objetivo:** Verificar filtro específico para alertas FF

**Passos:**
1. Na página 🔔 Alertas
2. No filtro "Filtrar por Categoria"
3. Selecione "Execução Físico-Financeira"

**Resultado Esperado:**
- ✅ Apenas alertas FF aparecem
- ✅ Outros alertas (vigência, status) ficam ocultos
- ✅ Contador mostra quantidade correta

**Status:** [ ] Passou [ ] Falhou

---

### Teste 12: Recálculo de Alertas ao Atualizar

**Objetivo:** Confirmar que alertas são recalculados dinamicamente

**Passos:**
1. Na página 🔔 Alertas, observe quantidade de alertas
2. Via terminal, atualize status de um registro pendente para "Pago"
3. Volte à página e clique em "🔄 Atualizar"

**Resultado Esperado:**
- ✅ Alertas são recalculados
- ✅ Alerta do registro resolvido desaparece
- ✅ Contadores são atualizados

**Status:** [ ] Passou [ ] Falhou

---

## 📊 Relatório de Testes

### Resumo Executivo

**Data dos testes:** _____________  
**Testador:** _____________  
**Versão testada:** Integração FF v1.0

**Resultados:**

| Categoria | Total | Passou | Falhou | N/A |
|-----------|-------|--------|--------|-----|
| Criação de dados | 1 | [ ] | [ ] | [ ] |
| Exibição de alertas | 4 | [ ] | [ ] | [ ] |
| Eventos histórico | 2 | [ ] | [ ] | [ ] |
| Regras de alerta | 3 | [ ] | [ ] | [ ] |
| UI e UX | 2 | [ ] | [ ] | [ ] |
| **TOTAL** | **12** | [ ] | [ ] | [ ] |

### Observações

_Registre aqui quaisquer observações, bugs ou sugestões:_

```
1. 

2. 

3. 

```

### Recomendação Final

- [ ] ✅ **APROVADO** - Integração completa e funcional
- [ ] ⚠️ **APROVADO COM RESSALVAS** - Ajustes menores necessários
- [ ] ❌ **REPROVADO** - Correções críticas necessárias

---

## 🚀 Próximos Passos

Após aprovação:

1. [ ] Commit das alterações
2. [ ] Documentar regras de alerta
3. [ ] Treinar usuários
4. [ ] Monitorar uso em produção
5. [ ] Coletar feedback para ajustes

---

## 📝 Notas Técnicas

### Arquivos Modificados

- `services/ff_alert_rules.py` (novo)
- `services/alert_service.py` (funções de merge)
- `services/execution_financial_service.py` (evento no histórico)
- `pages/01_📄_Contrato.py` (dados reais)
- `pages/07_🔔_Alertas.py` (integração FF)
- `components/execucao_ff.py` (renderização de alertas)

### Parâmetros Configuráveis

Em `services/ff_alert_rules.py`:

```python
DIAS_ALERTA_ATESTE_PENDENTE = 5
DIAS_ALERTA_PAGAMENTO_ATRASADO = 30
DIAS_ALERTA_STATUS_PARADO = 15
```

Ajuste conforme política institucional.

---

**Guia preparado em:** Janeiro/2026  
**Última atualização:** Integração de Alertas FF
