# Alert Lifecycle Service V2 - Guia de Uso

## 📚 Visão Geral

O `alert_lifecycle_service.py` implementa o **modelo evolutivo de alertas com ciclo de vida completo** para o SAAB-Tech, transformando alertas de simples notificações em processos estruturados com estados, ações e encadeamento.

## 🎯 Conceito Principal

**ANTES (V1)**: Alerta = notificação isolada  
**AGORA (V2)**: Alerta = processo com ciclo de vida

- ✅ Estados rastreados (novo → em análise → resolvido)
- ✅ Decisões registradas com justificativa
- ✅ Encadeamento automático de alertas derivados
- ✅ Cálculo de risco e janela de segurança
- ✅ Histórico completo e auditável

## 🏗️ Estrutura de Dados

### Alerta V2

```python
{
    # Identificação
    'id': 'uuid',
    'tipo': 'preventivo|operacional|critico|escalonado|informativo',
    'categoria': 'Vigência|Execução Físico-Financeira|...',
    'titulo': 'Descrição curta',
    'descricao': 'Descrição detalhada',
    
    # Vinculação
    'contrato_id': 'id_do_contrato',
    'contrato_numero': '123/2025',
    'responsavel': 'usuario_gestor',
    
    # Ciclo de vida
    'estado': 'novo|em_analise|providencia_em_curso|...',
    'estado_anterior': 'estado_anterior',
    'data_criacao': 'ISO timestamp',
    'data_ultima_atualizacao': 'ISO timestamp',
    
    # Prazos e criticidade
    'prazo_resposta': 'ISO timestamp',
    'prazo_resposta_dias': 30,
    'criticidade': 'baixa|media|alta|urgente',
    'dias_restantes': 30,
    'janela_seguranca_dias': 10,  # dias - tempo_medio_execucao
    
    # Encadeamento
    'alerta_origem_id': 'id_alerta_pai',
    'geracao': 1,  # 1=raiz, 2=derivado, 3=derivado do derivado...
    'alertas_derivados': ['id1', 'id2'],
    
    # Análise e risco
    'score_risco': 0.75,  # 0.0 a 1.0
    'fatores_risco': {...},
    'recomendacao_ia': 'texto gerado por IA',
    
    # Ações e histórico
    'acoes_ids': ['acao1', 'acao2'],
    'historico_estados': [{...}, {...}],
    
    # Metadados
    'metadados': {...},
    'versao': 2
}
```

### Ação Registrada

```python
{
    'id': 'uuid',
    'alerta_id': 'id_do_alerta',
    'tipo_acao': 'decisao_renovar|providencia_iniciar_processo|...',
    'usuario': 'gestor.nome',
    'data_acao': 'ISO timestamp',
    'justificativa': 'Texto da justificativa',
    'decisao': 'RENOVAR|NÃO_RENOVAR|LICITAR|...',
    'prazo_novo_dias': 60,
    'documentos': ['url1', 'url2'],
    'metadados': {...}
}
```

## 🔧 Funções Principais

### 1. Criar Alerta V2

```python
from services.alert_lifecycle_service import (
    criar_alerta_v2,
    TIPO_PREVENTIVO,
    CATEGORIA_VIGENCIA,
    CRITICIDADE_ALTA
)

alerta = criar_alerta_v2(
    tipo=TIPO_PREVENTIVO,
    categoria=CATEGORIA_VIGENCIA,
    titulo="Contrato próximo ao vencimento",
    descricao="Contrato 123/2025 vence em 90 dias. Necessário planejar renovação.",
    contrato_id="cont_001",
    contrato_numero="123/2025",
    responsavel="gestor.silva",
    prazo_resposta_dias=30,
    criticidade=CRITICIDADE_ALTA
)

print(f"Alerta criado: {alerta['id']}")
```

### 2. Transicionar Estado

```python
from services.alert_lifecycle_service import transicionar_estado, ESTADO_EM_ANALISE

sucesso = transicionar_estado(
    alerta_id=alerta['id'],
    novo_estado=ESTADO_EM_ANALISE,
    usuario="gestor.silva",
    observacao="Iniciando análise do contrato"
)
```

### 3. Registrar Ação Administrativa

```python
from services.alert_lifecycle_service import registrar_acao, ACAO_DECISAO_RENOVAR

acao = registrar_acao(
    alerta_id=alerta['id'],
    tipo_acao=ACAO_DECISAO_RENOVAR,
    usuario="gestor.silva",
    justificativa="Necessidade de continuidade do serviço conforme Art. 57, II da Lei 8.666/93",
    decisao="RENOVAR",
    prazo_novo_dias=60,
    documentos=["parecer_juridico_2025_001.pdf"],
    metadados_acao={
        'fundamentacao_legal': 'Art. 57, II, Lei 8.666/93',
        'parecer_juridico': 'PAJ-2025-001'
    }
)

print(f"Ação registrada: {acao['id']}")
```

### 4. Criar Alerta Derivado (Encadeamento)

```python
from services.alert_lifecycle_service import criar_alerta_derivado, TIPO_OPERACIONAL

# Após decidir renovar, criar alerta para iniciar o processo
alerta_derivado = criar_alerta_derivado(
    alerta_origem_id=alerta['id'],
    tipo=TIPO_OPERACIONAL,
    titulo="Iniciar processo de renovação",
    descricao="Elaborar termo aditivo e submeter à aprovação",
    prazo_resposta_dias=45,
    criticidade=CRITICIDADE_ALTA
)

print(f"Alerta derivado criado (geração {alerta_derivado['geracao']})")
```

### 5. Calcular Risco

```python
from services.alert_lifecycle_service import calcular_score_risco

score = calcular_score_risco(alerta['id'])
print(f"Score de risco: {score} (0.0 a 1.0)")

# Fatores considerados:
# - Urgência temporal (peso 35%)
# - Criticidade (peso 30%)
# - Histórico de adiamentos (peso 20%)
# - Geração no encadeamento (peso 15%)
```

### 6. Calcular Janela de Segurança

```python
from services.alert_lifecycle_service import calcular_janela_seguranca

tempo_medio_renovacao = 20  # dias (histórico institucional)
janela = calcular_janela_seguranca(alerta['id'], tempo_medio_renovacao)

if janela < 0:
    print(f"⚠️  ALERTA: Prazo insuficiente! Faltam {abs(janela)} dias.")
else:
    print(f"✓ Janela de segurança: {janela} dias")
```

### 7. Obter Cadeia de Alertas

```python
from services.alert_lifecycle_service import get_cadeia_alertas

raiz, cadeia = get_cadeia_alertas(alerta_derivado['id'])

print(f"Alerta raiz: {raiz['titulo']}")
print(f"Cadeia completa: {len(cadeia)} alertas")
for a in cadeia:
    print(f"  - Geração {a['geracao']}: {a['titulo']} ({a['estado']})")
```

### 8. Estatísticas e BI

```python
from services.alert_lifecycle_service import get_estatisticas_alertas_v2

stats = get_estatisticas_alertas_v2()

print(f"Total de alertas: {stats['total_alertas']}")
print(f"Risco médio: {stats['risco_medio']:.2f}")
print(f"Alertas risco alto: {stats['alertas_risco_alto']}")
print(f"Por estado: {stats['por_estado']}")
```

### 9. Importar Alerta V1 para V2

```python
from services.alert_lifecycle_service import importar_alerta_v1_para_v2

# Lê alerta V1 (do sistema antigo)
alerta_v1 = {
    'id': 'VIG_CRIT_001',
    'tipo': 'critico',
    'contrato_id': 'cont_001',
    # ... outros campos V1
}

# Converte para V2 (não modifica o V1)
alerta_v2 = importar_alerta_v1_para_v2(alerta_v1)
print(f"Alerta V1 migrado para V2: {alerta_v2['id']}")
```

## 📊 Exemplo Completo: Fluxo de Renovação

```python
from services.alert_lifecycle_service import *

# 1. Sistema detecta contrato próximo ao vencimento
alerta_preventivo = criar_alerta_v2(
    tipo=TIPO_PREVENTIVO,
    categoria=CATEGORIA_VIGENCIA,
    titulo="Contrato 123/2025 vence em 90 dias",
    descricao="Necessário decidir sobre renovação",
    contrato_id="cont_001",
    contrato_numero="123/2025",
    responsavel="gestor.silva",
    prazo_resposta_dias=30,
    criticidade=CRITICIDADE_ALTA
)

# 2. Gestor analisa o alerta
transicionar_estado(
    alerta_preventivo['id'],
    ESTADO_EM_ANALISE,
    "gestor.silva",
    "Analisando viabilidade de renovação"
)

# 3. Gestor registra decisão de renovar
acao_decisao = registrar_acao(
    alerta_preventivo['id'],
    ACAO_DECISAO_RENOVAR,
    "gestor.silva",
    "Serviço essencial, renovação justificada pelo Art. 57, II da Lei 8.666/93",
    decisao="RENOVAR",
    prazo_novo_dias=60
)

# 4. Sistema cria alerta derivado automaticamente
alerta_operacional = criar_alerta_derivado(
    alerta_preventivo['id'],
    TIPO_OPERACIONAL,
    "Iniciar processo de renovação do contrato 123/2025",
    "Elaborar termo aditivo e submeter à aprovação",
    prazo_resposta_dias=45,
    criticidade=CRITICIDADE_ALTA
)

# 5. Gestor registra que iniciou o processo
acao_providencia = registrar_acao(
    alerta_operacional['id'],
    ACAO_PROVIDENCIA_INICIAR_PROCESSO,
    "gestor.silva",
    "Processo SEI 2025.1.0001 aberto para tramitação",
    metadados_acao={'processo_sei': '2025.1.0001'}
)

# 6. Calcula risco e janela de segurança
score_risco = calcular_score_risco(alerta_operacional['id'])
janela = calcular_janela_seguranca(alerta_operacional['id'], tempo_medio_execucao_dias=20)

if janela < 0:
    # Sistema escalona automaticamente
    alerta_escalonado = criar_alerta_derivado(
        alerta_operacional['id'],
        TIPO_ESCALONADO,
        "URGENTE: Prazo insuficiente para renovação",
        f"Janela de segurança negativa ({janela} dias). Risco de ruptura.",
        prazo_resposta_dias=7,
        criticidade=CRITICIDADE_URGENTE
    )
```

## 🔄 Estados do Ciclo de Vida

```
novo                    → Alerta recém-criado pelo sistema
  ↓
em_analise             → Gestor está analisando
  ↓
providencia_em_curso   → Ação sendo executada
  ↓
aguardando_prazo       → Aguardando vencimento de prazo
  ↓
resolvido              → Alerta resolvido com sucesso
  ↓
encerrado              → Processo concluído

escalonado             → Alerta crítico não atendido (paralelo)
```

## 🎯 Tipos de Alerta

- **preventivo**: Antecipa riscos (ex: contrato vence em 180 dias)
- **operacional**: Monitora execução de ação decidida
- **critico**: Indica risco iminente
- **escalonado**: Sinaliza não cumprimento de prazo
- **informativo**: Registra evento sem requerer ação

## ⚙️ Compatibilidade com V1

O service V2 **NÃO modifica** dados V1. A função `importar_alerta_v1_para_v2()` apenas **lê** alertas V1 e cria novos alertas V2, preservando referência ao original.

## 📁 Arquivos de Dados

- `data/alertas_ciclo_vida.json` - Alertas V2
- `data/acoes_alertas.json` - Ações registradas
- `data/alertas_resolvidos.json` - Alertas V1 (não modificado)

## 🧪 Testes

Execute a suite de testes:

```bash
python tests/test_alert_lifecycle_service.py
```

## 🚀 Próximos Passos

1. ✅ **Fase 1 Concluída**: Estrutura de dados V2 criada
2. ⏳ **Fase 2**: Criar interface UI com feature flag
3. ⏳ **Fase 3**: Modo "dual write" (V1 + V2)
4. ⏳ **Fase 4**: Migração gradual de dados
5. ⏳ **Fase 5**: Desativação do V1

## 📞 Suporte

Para dúvidas sobre implementação, consulte:
- `docs/ARQUITETURA_CICLO_VIDA_ALERTAS.md` - Arquitetura completa
- `services/alert_service.py` - Sistema V1 (referência)
