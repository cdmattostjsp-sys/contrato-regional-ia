# ✅ Checklist de Testes - Contratos Regionais (FASE 3)

## 📋 Objetivo

Validar funcionalidade de **fiscais por comarca** para contratos regionais, garantindo:
- Cadastro correto
- Visualização adequada
- Integração com notificações
- Compatibilidade retroativa

---

## 🧪 Cenário 1: Cadastro de Contrato Regional

### Passos:
1. Acesse página **"📝 Cadastro de Contratos"**
2. Preencha dados básicos do contrato
3. ✅ **Marque checkbox** "Este contrato abrange múltiplas comarcas"
4. Adicione primeira comarca:
   - Comarca: Sorocaba
   - Fiscal Titular: João Silva Santos
   - Fiscal Suplente: Maria Oliveira Costa
5. Clique "➕ Adicionar"
6. Adicione segunda comarca:
   - Comarca: Itapetininga
   - Fiscal Titular: Carlos Eduardo Lima
   - Fiscal Suplente: Ana Paula Souza
7. Clique "➕ Adicionar"
8. Faça upload do PDF do contrato
9. Clique "Cadastrar Contrato"

### Resultado Esperado:
- ✅ Contrato cadastrado com sucesso
- ✅ Mensagem confirma cadastro
- ✅ Duas comarcas armazenadas

---

## 🧪 Cenário 2: Visualização de Contrato Regional

### Passos:
1. Na aba "📋 Contratos Cadastrados"
2. Localize contrato regional cadastrado
3. Expanda card do contrato

### Resultado Esperado:
- ✅ Campo "Tipo" indica "Contrato Regional (2 comarcas)"
- ✅ Seção "🏛️ Fiscais por Comarca" é exibida
- ✅ Cada comarca lista titular e suplente:
  - **Sorocaba:**
    - Titular: João Silva Santos
    - Suplente: Maria Oliveira Costa
  - **Itapetininga:**
    - Titular: Carlos Eduardo Lima
    - Suplente: Ana Paula Souza

---

## 🧪 Cenário 3: Contrato Simples (Compatibilidade)

### Passos:
1. Cadastre novo contrato
2. **NÃO marque** checkbox "modelo regional"
3. Preencha apenas:
   - Gestor Titular
   - Gestor Suplente
   - Fiscal Titular
   - Fiscal Substituto
4. Cadastre normalmente

### Resultado Esperado:
- ✅ Contrato cadastrado sem erros
- ✅ Visualização exibe fiscais no formato antigo
- ✅ Sistema trata como "comarca única"

---

## 🧪 Cenário 4: Notificação em Contrato Regional

### Passos:
1. Selecione contrato regional (com múltiplas comarcas)
2. Acesse página **"📝 Notificações"**
3. Observe campo de seleção de comarca

### Resultado Esperado:
- ✅ Info box aparece: "📍 Contrato Regional - Selecione a comarca..."
- ✅ Dropdown lista comarcas do contrato:
  - Sorocaba
  - Itapetininga
4. Selecione "Sorocaba"
5. Preencha motivo da notificação
6. Clique "✨ Gerar Sugestão com IA"

### Resultado Esperado:
- ✅ IA gera notificação
- ✅ Histórico registra comarca: "Comarca: Sorocaba"
- ✅ Fiscal responsável identificado (João Silva Santos)

---

## 🧪 Cenário 5: Notificação em Contrato Simples (Compatibilidade)

### Passos:
1. Selecione contrato simples (sem múltiplas comarcas)
2. Acesse página **"📝 Notificações"**

### Resultado Esperado:
- ✅ Campo de seleção de comarca **NÃO aparece**
- ✅ Fluxo de notificação funciona normalmente
- ✅ Nenhum erro ocorre

---

## 🧪 Cenário 6: Verificação de Histórico

### Passos:
1. Após gerar notificação em contrato regional
2. Acesse **"Histórico"** (se disponível) ou logs

### Resultado Esperado:
- ✅ Evento registrado: `NOTIFICACAO_GERADA_COM_IA`
- ✅ Metadados incluem:
  - `comarca`: "Sorocaba"
  - `tipo`: tipo da notificação
  - `modo`: "IA_ATIVA"
  - `fontes_usadas`: lista de documentos consultados

---

## 🧪 Cenário 7: Adicionar/Remover Comarcas Durante Cadastro

### Passos:
1. Durante cadastro de contrato regional
2. Adicione 3 comarcas
3. Clique "🗑️" na segunda comarca para remover

### Resultado Esperado:
- ✅ Comarca removida da lista
- ✅ Numeração das comarcas se ajusta
- ✅ Cadastro final inclui apenas 2 comarcas

---

## 🧪 Cenário 8: Validação de Campos Obrigatórios

### Passos:
1. Marque checkbox "modelo regional"
2. Tente adicionar comarca sem preencher todos os campos
3. Clique "➕ Adicionar"

### Resultado Esperado:
- ✅ Mensagem de erro: "⚠️ Preencha todos os campos da comarca!"
- ✅ Comarca não é adicionada

---

## 🧪 Cenário 9: Teste de Funções de Utilidade (Dev)

### Via Python REPL ou Jupyter:

```python
from services.contract_service import (
    obter_fiscais_do_contrato,
    obter_fiscal_por_comarca,
    obter_comarcas_do_contrato,
    eh_contrato_regional
)

# Contrato regional mock
contrato_regional = {
    "id": "CTR123",
    "numero": "56/2025",
    "fiscais_por_comarca": [
        {"comarca": "Sorocaba", "titular": "João", "suplente": "Maria"},
        {"comarca": "Itapetininga", "titular": "Carlos", "suplente": "Ana"}
    ]
}

# Testes
fiscais = obter_fiscais_do_contrato(contrato_regional)
assert len(fiscais) == 2

fiscal_sorocaba = obter_fiscal_por_comarca(contrato_regional, "Sorocaba")
assert fiscal_sorocaba["titular"] == "João"

comarcas = obter_comarcas_do_contrato(contrato_regional)
assert comarcas == ["Sorocaba", "Itapetininga"]

assert eh_contrato_regional(contrato_regional) == True

# Contrato antigo (compatibilidade)
contrato_antigo = {
    "id": "CTR456",
    "fiscal_titular": "Pedro",
    "fiscal_substituto": "Julia"
}

fiscais_antigo = obter_fiscais_do_contrato(contrato_antigo)
assert len(fiscais_antigo) == 1
assert fiscais_antigo[0]["titular"] == "Pedro"

assert eh_contrato_regional(contrato_antigo) == False
```

### Resultado Esperado:
- ✅ Todos os asserts passam
- ✅ Compatibilidade confirmada

---

## 🧪 Cenário 10: Stress Test - Muitas Comarcas

### Passos:
1. Cadastre contrato com 10 comarcas
2. Visualize o contrato
3. Gere notificação selecionando última comarca

### Resultado Esperado:
- ✅ Sistema suporta múltiplas comarcas
- ✅ Visualização não quebra layout
- ✅ Seleção de comarca funciona corretamente

---

## ✅ Critérios de Aprovação

Para considerar FASE 3 **validada**, todos os cenários devem:

- [ ] Executar sem erros
- [ ] Exibir resultados esperados
- [ ] Manter compatibilidade com contratos antigos
- [ ] Registrar eventos corretamente no histórico
- [ ] Não quebrar funcionalidades existentes

---

## 📊 Resultado do Teste

**Data:** ___/___/___  
**Testador:** __________________  
**Ambiente:** Dev / Staging / Produção

| Cenário | Status | Observações |
|---------|--------|-------------|
| 1. Cadastro Regional | ⬜ Pass / ⬜ Fail | |
| 2. Visualização Regional | ⬜ Pass / ⬜ Fail | |
| 3. Contrato Simples | ⬜ Pass / ⬜ Fail | |
| 4. Notificação Regional | ⬜ Pass / ⬜ Fail | |
| 5. Notificação Simples | ⬜ Pass / ⬜ Fail | |
| 6. Histórico | ⬜ Pass / ⬜ Fail | |
| 7. Adicionar/Remover | ⬜ Pass / ⬜ Fail | |
| 8. Validação Campos | ⬜ Pass / ⬜ Fail | |
| 9. Funções Utilidade | ⬜ Pass / ⬜ Fail | |
| 10. Stress Test | ⬜ Pass / ⬜ Fail | |

**Resultado Geral:** ⬜ **APROVADO** / ⬜ **REPROVADO**

---

**Fase 3 - Contratos Regionais com Fiscais por Comarca**  
**Status:** ✅ Implementado | 🧪 Em Teste
