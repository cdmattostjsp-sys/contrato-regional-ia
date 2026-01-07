# 📚 Contexto Enriquecido para Notificações com IA

## 📋 Visão Geral

Implementação de **contexto enriquecido com documentos contratuais e Base de Conhecimento** para o módulo de Notificações com IA.

**Versão:** 2.0  
**Status:** ✅ Implementado  
**Data:** Janeiro/2026

---

## 🎯 Objetivo Institucional

Permitir que a IA gere notificações fundamentadas em:
1. **Cláusulas do contrato** (PDF do contrato original)
2. **Aditivos contratuais** (PDFs de aditivos vinculados)
3. **Documentos institucionais** (Base de Conhecimento: manuais, portarias, INs, notas técnicas)

**Valor:** A IA não mais sugere cláusulas "genéricas" — ela cita trechos reais dos documentos disponíveis, aumentando a qualidade e a aderência institucional das notificações.

---

## 🏗️ Arquitetura da Solução

### Fluxo de Enriquecimento de Contexto

```
┌────────────────────────────────────────┐
│ Usuário preenche notificação          │
│ - Tipo, motivo, prazo, fundamentação  │
└───────────────┬────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│ Sistema enriquece contexto:            │
│                                        │
│ 1. Extrai palavras-chave do motivo    │
│ 2. Localiza PDFs do contrato          │
│ 3. Extrai texto dos PDFs               │
│ 4. Filtra trechos relevantes          │
│ 5. Consulta Base de Conhecimento      │
└───────────────┬────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│ Prompt enriquecido enviado à IA:      │
│ - Contexto básico do contrato         │
│ - Trechos do contrato original        │
│ - Trechos dos aditivos                │
│ - Documentos institucionais           │
│ - Motivo e fundamentação do usuário   │
└───────────────┬────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│ IA gera notificação CITANDO            │
│ cláusulas e trechos literais          │
└───────────────┬────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│ Registro de governança:                │
│ - Quais fontes foram consultadas       │
│ - Metadados completos no histórico    │
└────────────────────────────────────────┘
```

---

## 🔧 Componentes Implementados

### 1. Extração de Texto de PDF (PyMuPDF)

**Arquivo:** `services/document_service.py`

```python
def extrair_texto_pdf(caminho_pdf: str) -> str
```

- Usa PyMuPDF (fitz) para extrair texto de PDFs
- Retorna texto completo com marcação de páginas
- Trata erros com fallback seguro

### 2. Filtragem de Trechos Relevantes

**Arquivo:** `services/document_service.py`

```python
def filtrar_trechos_relevantes(
    texto_completo: str, 
    palavras_chave: List[str], 
    tamanho_janela: int = 800, 
    max_trechos: int = 5
) -> str
```

- Localiza palavras-chave no texto
- Extrai janelas de contexto (antes e depois)
- Evita sobreposição de trechos
- Limita quantidade para não exceder tokens

### 3. Localização de Documentos do Contrato

**Arquivo:** `services/contract_service.py`

```python
def obter_documentos_contrato(contrato_id: str) -> Dict[str, List[str]]
```

- Retorna caminho do PDF do contrato original
- Retorna lista de caminhos dos PDFs de aditivos
- Busca em `knowledge/contratos/{contrato_id}/`

### 4. Enriquecimento de Contexto

**Arquivo:** `services/notificacao_ai_service.py`

```python
def _enriquecer_contexto_com_documentos(
    contexto_contrato: Dict, 
    motivo: str
) -> Dict
```

**Processo:**
1. Extrai palavras-chave do motivo
2. Localiza PDFs do contrato (original + aditivos)
3. Extrai e filtra trechos relevantes
4. Consulta Base de Conhecimento institucional
5. Retorna contexto enriquecido + lista de fontes

**Retorno:**
```python
{
    'texto_contrato': str,        # Trechos do contrato
    'texto_aditivos': str,         # Trechos dos aditivos
    'texto_conhecimento': str,     # Documentos institucionais
    'fontes_usadas': List[str]     # Lista de fontes consultadas
}
```

### 5. Prompt Enriquecido

**Arquivo:** `services/notificacao_ai_service.py`

```python
def _montar_prompt_contexto(
    contexto: Dict, 
    dados: Dict, 
    contexto_enriquecido: Dict = None
) -> str
```

- Insere trechos documentais no prompt
- Instrui IA a citar LITERALMENTE
- Proíbe invenção de cláusulas

### 6. Governança com Fontes

**Arquivo:** `services/notificacao_ai_service.py`

```python
def registrar_geracao_notificacao(
    ...
    fontes_usadas: Optional[List[str]] = None
) -> None
```

- Registra no histórico quais fontes foram consultadas
- Metadados completos incluem lista de documentos
- Rastreabilidade total

---

## 📝 Exemplo de Uso

### Entrada do Usuário

**Contrato:** 56/2025 — Limpeza de caixas d'água  
**Motivo:** "Ausência de 3 funcionários durante 2 dias, sem reposição de postos"  
**Campo de fundamentação:** "POR FAVOR, VERIFIQUE A CLÁUSULA CONTRATUAL APLICÁVEL"

### Processamento Interno

1. **Palavras-chave extraídas:** `ausência`, `funcionários`, `reposição`, `postos`
2. **PDFs localizados:**
   - `knowledge/contratos/56_2025/56_2025.pdf` (contrato original)
   - Nenhum aditivo encontrado
3. **Texto extraído e filtrado:**
   - Trechos contendo "funcionário", "substituição", "ausência", "penalidade"
4. **Base de Conhecimento consultada:**
   - Manual de Contratos TJSP 2025
   - IN 12/2025 sobre fiscalização
5. **Fontes registradas:**
   - "Contrato 56/2025"
   - "Manual de Contratos - TJSP - 2025"
   - "IN TJSP nº 12/2025"

### Saída da IA (Exemplo)

```
Ao Sr. Representante Legal da HELENA MIRANDA MUNIZ-SANEAMENTO E SERVIÇOS

Ref.: Contrato nº 56/2025 — Serviços de limpeza e desinfecção de caixas d'água

NOTIFICAÇÃO DE ADVERTÊNCIA

CONSIDERANDO o disposto na Cláusula 8ª, § 2º do Contrato nº 56/2025, que 
estabelece: "A CONTRATADA deverá garantir a substituição imediata de 
funcionários ausentes, sob pena de glosa proporcional e aplicação das 
sanções previstas neste instrumento";

CONSIDERANDO que, conforme verificado nos dias 02/01/2026 e 03/01/2026, 
houve ausência de 03 (três) funcionários sem a devida reposição dos 
postos de trabalho, impactando a execução contratual;

COMUNICA-SE à CONTRATADA que a ausência injustificada de funcionários 
configura descumprimento contratual, sujeito à glosa proporcional e, 
conforme reincidência, à aplicação de penalidades previstas no art. 156 
da Lei 14.133/2021.

DETERMINA-SE:
1. Apresentação de justificativa formal para as ausências verificadas;
2. Comprovação de adoção de medidas corretivas imediatas;
3. Plano de ação para prevenir reincidências.

Prazo: 5 (cinco) dias úteis, contados do recebimento desta notificação.

FUNDAMENTAÇÃO LEGAL:
- Cláusula 8ª, § 2º do Contrato nº 56/2025
- Lei 14.133/2021, art. 156
- Manual de Contratos TJSP, item 7.2

Atenciosamente,
[Nome do Fiscal]
Fiscal do Contrato — RAJ 10.1
```

**Nota:** A IA citou a Cláusula 8ª, § 2º porque ela estava presente no texto extraído do PDF.

---

## ✅ Princípios de Segurança

### 1. Fallback Seguro
- Se não houver PDF, o sistema continua funcionando
- Se a extração falhar, usa contexto básico
- Se o texto for muito grande, limita automaticamente

### 2. Não Inventa Cláusulas
- IA instruída explicitamente a citar LITERALMENTE
- Se não houver cláusula específica, usa fundamentação genérica
- Prompt contém: "NÃO invente cláusulas ou números que não apareçam nos trechos fornecidos"

### 3. Controle de Tamanho (Tokens)
- Filtragem por palavras-chave reduz texto
- Máximo de trechos configurável
- Janelas de contexto limitadas

### 4. Governança Total
- Todas as fontes consultadas são registradas
- Metadados completos no histórico
- Não armazena conteúdo integral (apenas referências)

---

## 📊 Fluxo Técnico Detalhado

### Passo 1: Extração de Palavras-Chave

```python
motivo = "Ausência de 3 funcionários durante 2 dias, sem reposição"
palavras_chave = _extrair_palavras_chave(motivo)
# Resultado: ['ausência', 'funcionários', 'durante', 'dias', 'reposição']
```

### Passo 2: Localização de PDFs

```python
contrato_id = "56_2025"
docs = obter_documentos_contrato(contrato_id)
# Resultado: {
#   'contrato': 'knowledge/contratos/56_2025/56_2025.pdf',
#   'aditivos': []
# }
```

### Passo 3: Extração e Filtragem

```python
texto_completo = extrair_texto_pdf(docs['contrato'])
texto_filtrado = filtrar_trechos_relevantes(
    texto_completo, 
    palavras_chave, 
    tamanho_janela=1000,
    max_trechos=3
)
```

### Passo 4: Consulta à Base de Conhecimento

```python
docs_conhecimento = buscar_documentos_relevantes(
    pergunta=motivo,
    limite=3,
    tamanho_trecho=600
)
```

### Passo 5: Montagem do Prompt

```python
prompt = f"""
CONTEXTO DO CONTRATO:
- Número: 56/2025
- Contratada: HELENA MIRANDA MUNIZ
...

---
DOCUMENTAÇÃO DE APOIO:

TRECHOS DO CONTRATO:
[...] Cláusula 8ª, § 2º: A CONTRATADA deverá garantir a substituição 
imediata de funcionários ausentes, sob pena de glosa proporcional... [...]

DOCUMENTOS INSTITUCIONAIS RELEVANTES:
📄 Manual de Contratos - TJSP - 2025
Item 7.2 - Fiscalização e Controle de Pessoal
[...trecho relevante...]
---

TAREFA:
Gere notificação formal. CITE LITERALMENTE as cláusulas fornecidas.
NÃO invente cláusulas.
"""
```

---

## 🎯 Casos de Uso

### Caso 1: Contrato COM PDF cadastrado
✅ Sistema extrai trechos do contrato  
✅ IA cita cláusulas literais  
✅ Fontes registradas: "Contrato X/2025"

### Caso 2: Contrato SEM PDF cadastrado
⚠️ Sistema não localiza PDF  
✅ IA usa fundamentação genérica  
✅ Fontes registradas: apenas Base de Conhecimento

### Caso 3: Motivo SEM palavras-chave específicas
⚠️ Filtragem retorna início do documento  
✅ IA usa contexto limitado  
✅ Sistema continua funcionando

### Caso 4: PDF corrompido ou ilegível
⚠️ Extração retorna string vazia  
✅ Sistema usa contexto básico  
✅ Fallback seguro ativado

---

## 📚 Arquivos Modificados

### Novos Componentes
- `services/document_service.py` — Extração e filtragem de PDFs
- `services/contract_service.py` — Localização de documentos
- `services/notificacao_ai_service.py` — Enriquecimento de contexto
- `pages/03_📝_Notificações.py` — Integração com fontes

### Documentação
- `docs/CONTEXTO_ENRIQUECIDO_NOTIFICACOES.md` — Este documento

---

## 🔬 Checklist de Teste

### Teste 1: Contrato com PDF ✅
1. Cadastre contrato com PDF anexado
2. Gere notificação mencionando tema presente no contrato
3. **Esperado:** IA cita cláusula específica do PDF

### Teste 2: Contrato sem PDF ✅
1. Selecione contrato sem PDF cadastrado
2. Gere notificação
3. **Esperado:** IA usa fundamentação genérica, sem erro

### Teste 3: Motivo genérico ✅
1. Digite motivo sem palavras-chave específicas
2. Gere notificação
3. **Esperado:** Sistema funciona, IA usa contexto limitado

### Teste 4: Base de Conhecimento vazia ✅
1. Remova documentos da Base de Conhecimento
2. Gere notificação
3. **Esperado:** Sistema usa apenas PDF do contrato

### Teste 5: Verificar fontes no histórico ✅
1. Gere notificação
2. Acesse Histórico/Logs
3. **Esperado:** Evento registrado com lista de fontes consultadas

---

## 💡 Próximos Passos (Futuro)

### Fase 3: Embeddings e Busca Vetorial
- Usar Azure OpenAI Embeddings
- Indexar todos os documentos em vetor store
- Busca semântica mais precisa

### Fase 4: Cache de Extração
- Salvar texto extraído de PDFs
- Evitar reprocessamento a cada geração
- Atualizar cache quando PDF for substituído

### Fase 5: Citações com Página
- Incluir número da página na citação
- Facilitar verificação posterior

---

## 🔒 Segurança e Compliance

### Dados Não Armazenados
- ❌ Conteúdo integral das notificações
- ❌ Texto completo dos PDFs (apenas trechos no prompt)

### Dados Armazenados (Governança)
- ✅ Metadados: tipo, categoria, modo
- ✅ Lista de fontes consultadas (referências)
- ✅ Timestamp e usuário

### Dados Enviados à IA
- ✅ Contexto sanitizado (sem valores, CPFs, etc.)
- ✅ Trechos relevantes (não o PDF inteiro)
- ✅ Motivo e fundamentação do usuário

---

## 📞 Suporte

**Dúvidas técnicas:** Consulte este documento  
**Problemas de extração:** Verifique se PyMuPDF está instalado  
**Base de Conhecimento:** Página "📚 Biblioteca de Conhecimento"

---

## 🎯 Valor Institucional

Esta implementação representa um **salto de qualidade** no sistema:

1. **Antes:** IA gerava texto genérico, sem citar cláusulas específicas
2. **Agora:** IA lê o contrato e cita cláusulas literais

**Impacto:**
- ✅ Notificações mais fundamentadas
- ✅ Redução de retrabalho (menos revisões)
- ✅ Padronização institucional (Base de Conhecimento)
- ✅ Rastreabilidade total (governança)

---

**Versão:** 2.0  
**Data:** Janeiro/2026  
**Status:** ✅ Implementado e Testado
