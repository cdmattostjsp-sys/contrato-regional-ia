# Módulo de Alertas Contratuais

## Documento Técnico-Institucional

**Sistema:** Gestão Regional de Contratos - TJSP  
**Módulo:** Alertas Contratuais  
**Versão:** 1.0 (Consolidada)  
**Data:** Janeiro/2026  
**Status:** Produção (POC Institucional)

---

## 📋 Sumário Executivo

O **Módulo de Alertas Contratuais** constitui **instrumento de governança administrativa** que opera através de:

1. **Identificação Automática**: Sistema aponta alertas baseados em regras de negócio
2. **Decisão Humana**: Gestor analisa e resolve com justificativa obrigatória  
3. **Rastreabilidade Total**: Registro permanente de atos administrativos

---

## 🎯 Modelo de Governança

### Separação Conceitual

O sistema implementa **separação clara de responsabilidades**:

| Etapa | Responsável | Natureza |
|-------|-------------|----------|
| **Apontamento** | Sistema Automático | Cálculo algorítmico |
| **Resolução** | Gestor Administrativo | Decisão fundamentada |
| **Registro** | Sistema de Histórico | Rastreabilidade permanente |

> **Princípio fundamental**: O sistema **nunca decide** — apenas **aponta** situações que **requerem análise humana**.

---

## ⚙️ Funcionamento Técnico

### Estados do Alerta

Cada alerta possui um dos seguintes estados:

- **ATIVO**: Alerta gerado automaticamente, aguardando análise
- **RESOLVIDO**: Alerta analisado e resolvido por gestor, com justificativa formal
- **ARQUIVADO**: (Reservado para uso futuro)

### Regras de Negócio Implementadas

#### 🔴 Alertas Críticos

| Regra | Condição | Ação Sugerida |
|-------|----------|---------------|
| **Vigência Crítica** | Vencimento < 60 dias | Prorrogação urgente |
| **Contrato Vencido** | Vigência expirada | Verificação imediata |
| **Status Crítico** | Marcação manual | Atenção especial |

#### 🟡 Alertas de Atenção

| Regra | Condição | Ação Sugerida |
|-------|----------|---------------|
| **Vigência em Atenção** | Vencimento 60-120 dias | Planejamento renovação |
| **Pendências Contratuais** | Pendências identificadas | Resolução gradual |

#### 🔵 Alertas Informativos

| Regra | Condição | Ação Sugerida |
|-------|----------|---------------|
| **Alto Valor** | Valor > R$ 50 milhões | Acompanhamento especial |

---

## 📝 Resolução de Alertas

### Processo Formal

1. **Identificação**: Gestor acessa alerta na lista
2. **Análise**: Visualiza detalhes e contexto do contrato
3. **Decisão**: Marca alerta como resolvido
4. **Justificativa**: Fornece fundamentação obrigatória (mínimo razoável)
5. **Registro**: Sistema registra ato administrativo no histórico

### Dados Registrados

Cada resolução persiste **permanentemente**:

```json
{
  "alerta_id": "VIG_CRIT_123",
  "status": "RESOLVIDO",
  "justificativa": "Prorrogação formalizada via Termo Aditivo nº X",
  "usuario": "Nome do Gestor",
  "data": "2026-01-05T14:30:00",
  "contrato_numero": "45/2024",
  "alerta_tipo": "critico",
  "alerta_categoria": "Vigência"
}
```

---

## 🔍 Rastreabilidade e Auditoria

### Registro no Histórico do Contrato

Toda resolução gera **evento formal** no histórico:

- **Tipo**: `RESOLUCAO_ALERTA`
- **Título**: "Resolução de Alerta: [título do alerta]"
- **Detalhes**: Justificativa completa
- **Ator**: Nome do gestor responsável
- **Fonte**: Sistema de Alertas
- **Metadados**: JSON completo da resolução

### Consultas Disponíveis

O sistema permite consultar:

- Histórico de alertas resolvidos por contrato
- Estatísticas de resolução por tipo/categoria
- Últimas resoluções registradas
- Ações por usuário

### Funções de Auditoria

```python
# Listar alertas resolvidos de um contrato
carregar_alertas_resolvidos(contrato_id="123")

# Obter estatísticas gerais
obter_estatisticas_resolucoes()
```

---

## 🏛️ Arquitetura do Módulo

### Componentes

```
services/
├── alert_service.py          # Lógica de negócio e cálculo
├── history_service.py        # Rastreabilidade permanente
├── contract_service.py       # Fonte de dados

pages/
└── 07_🔔_Alertas.py         # Interface do usuário

data/
├── alertas_resolvidos.json   # Persistência de resoluções
└── history.db                # Banco de histórico SQLite
```

### Fluxo de Dados

```
[Contratos] → [Cálculo Automático] → [Alertas ATIVOS]
                                           ↓
                                    [Análise Humana]
                                           ↓
                        [Justificativa + Registro Formal]
                                           ↓
                        ┌──────────────────┴──────────────────┐
                        ↓                                      ↓
              [alertas_resolvidos.json]            [history.db (RESOLUCAO_ALERTA)]
```

---

## 📊 Interface do Usuário

### Recursos Disponíveis

- **Métricas Rápidas**: Contadores por tipo de alerta
- **Filtros Dinâmicos**: Por tipo e categoria
- **Cards Informativos**: Visual claro por criticidade
- **Ações Rápidas**: Ver contrato, gerar notificação, resolver
- **Envio de Emails**: Notificação automática de críticos
- **Formulário de Resolução**: Justificativa obrigatória

### Cores e Símbolos

| Tipo | Cor | Símbolo | Uso |
|------|-----|---------|-----|
| Crítico | Vermelho (#DC3545) | 🔴 | Ação imediata |
| Atenção | Amarelo (#FFC107) | 🟡 | Acompanhamento |
| Info | Azul (#17A2B8) | 🔵 | Monitoramento |

---

## 🔐 Segurança e Compliance

### Registro Permanente

- ✅ Alertas **nunca são excluídos**
- ✅ Resoluções ficam **permanentemente rastreáveis**
- ✅ Justificativas são **obrigatórias e imutáveis**
- ✅ Usuário responsável **sempre identificado**
- ✅ Data/hora de cada ato **registrada com precisão**

### Auditabilidade

O módulo permite responder:

- ❓ Quais alertas foram gerados para este contrato?
- ❓ Quem resolveu cada alerta e quando?
- ❓ Qual foi a justificativa administrativa?
- ❓ Quanto tempo levou entre apontamento e resolução?
- ❓ Quais gestores mais resolvem alertas?

---

## 📧 Notificações por Email

### Funcionamento

Quando configurado (⚙️ Configurações):

1. Alertas **críticos** podem ser enviados automaticamente
2. Email enviado ao gestor principal + cópias
3. Envio único por alerta (evita spam)
4. Mensagem formatada institucionalmente

### Configuração Necessária

- Email principal do gestor
- Emails de cópia (opcional)
- Ativação da notificação automática

---

## 🔄 Manutenção e Evolução

### Adição de Novas Regras

Para adicionar nova regra de alerta:

1. Editar `services/alert_service.py`
2. Adicionar lógica em `calcular_alertas()`
3. Garantir que campo `status: STATUS_ATIVO` seja incluído
4. Documentar regra neste documento

### Exemplo de Nova Regra

```python
# ALERTA: Saldo empenhado crítico
if contrato.get('saldo_empenhado', 0) < 10000:
    alertas.append({
        'id': f"SALDO_CRIT_{contrato['id']}",
        'status': STATUS_ATIVO,
        'tipo': 'critico',
        'categoria': 'Financeiro',
        'titulo': 'Saldo empenhado crítico',
        'descricao': f"Contrato {contrato['numero']} possui saldo baixo.",
        'contrato_id': contrato['id'],
        'contrato_numero': contrato['numero'],
        'data_alerta': hoje,
        'acao_sugerida': 'verificacao_saldo'
    })
```

---

## 🎓 Boas Práticas de Uso

### Para Gestores

1. **Revisar alertas diariamente** (especialmente críticos)
2. **Justificar com clareza** as resoluções
3. **Documentar ações tomadas** externamente ao sistema
4. **Usar notificações** para acompanhar contratos críticos

### Para Desenvolvedores

1. **Nunca excluir alertas** — apenas marcar como resolvidos
2. **Sempre registrar no histórico** eventos significativos
3. **Validar justificativas** como obrigatórias
4. **Testar regras** antes de adicionar novas

---

## 📈 Indicadores de Governança

O módulo permite acompanhar:

- **Taxa de resolução**: % de alertas resolvidos vs. ativos
- **Tempo médio de resolução**: Intervalo entre geração e resolução
- **Alertas recorrentes**: Contratos que geram alertas repetidos
- **Distribuição de responsabilidade**: Gestores mais atuantes

---

## 🧪 Status de Implementação

### ✅ Implementado e Funcional

- [x] Cálculo automático de alertas
- [x] Estados ATIVO/RESOLVIDO/ARQUIVADO
- [x] Justificativa obrigatória
- [x] Registro no histórico (RESOLUCAO_ALERTA)
- [x] Persistência em JSON
- [x] Interface completa com filtros
- [x] Envio de emails (quando configurado)
- [x] Rastreabilidade por usuário
- [x] Estatísticas de resolução

### 🔄 Evoluções Futuras (Pós-POC)

- [ ] Painel de auditoria dedicado
- [ ] Relatórios exportáveis (PDF/Excel)
- [ ] Dashboard executivo de alertas
- [ ] Integração com API do PNCP
- [ ] Alertas personalizados por contrato
- [ ] Workflow de aprovação multi-nível

---

## 📚 Referências Técnicas

### Arquivos-Chave

- `services/alert_service.py` — Lógica de negócio
- `services/history_service.py` — Rastreabilidade
- `pages/07_🔔_Alertas.py` — Interface principal
- `data/alertas_resolvidos.json` — Persistência

### Dependências

- `streamlit` — Framework de interface
- `sqlite3` — Banco de histórico
- `json` — Persistência de alertas
- `datetime` — Manipulação de datas

---

## 📞 Suporte e Contato

Para dúvidas sobre este módulo:

- **Documentação Técnica**: `DEVELOPER_GUIDE.md`
- **Histórico de Alterações**: Commits do repositório
- **Equipe Responsável**: Desenvolvimento TJSP

---

## 📜 Conclusão

O **Módulo de Alertas Contratuais** está consolidado como **ferramenta institucional de governança**, apto para:

✅ Demonstrações para áreas administrativas  
✅ Avaliação pela STI/SAAB  
✅ Auditoria futura  
✅ Expansão pós-POC  

> **Princípio institucional**: Sistema aponta, gestor decide, histórico registra.

---

**Documento preparado em**: Janeiro/2026  
**Última atualização**: Consolidação do módulo de alertas  
**Versão**: 1.0 — Produção POC
