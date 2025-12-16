# 📚 Cadernos Técnicos de Contratação - TJSP

Estrutura organizada dos Cadernos Técnicos do TJSP para referência do sistema.

## 📋 Estrutura de Organização

Cada tipo de serviço possui seu próprio diretório com:
- **Caderno Técnico** (PDF) - Especificações técnicas completas
- **Planilha de Composição de Custos** (XLSX/PDF) - Detalhamento financeiro

---

## 🗂️ Cadernos Disponíveis

### 1. Limpeza Predial
**Diretório:** `limpeza_predial/`

**Documentos:**
- [ ] Caderno Técnico de Composição de Custos.pdf
- [ ] Planilha de Composição de Custos.xlsx

**Aplicação:**
- Contratos de limpeza e conservação
- Cálculo de custos operacionais
- Definição de postos de trabalho

---

### 2. Garçom/Garçonete e Copeiro/Copeira
**Diretório:** `garcom_copeiro/`

**Documentos:**
- [ ] Caderno Técnico de Composição de Custos.pdf
- [ ] Planilha de Composição de Custos.xlsx

**Aplicação:**
- Contratos de copa e cozinha
- Eventos e serviços de alimentação
- Cálculo de mão de obra

---

### 3. Mão de Obra Braçal
**Diretório:** `mao_obra_bracal/`

**Documentos:**
- [ ] Caderno Técnico de Composição de Custos.pdf
- [ ] Planilha de Composição de Custos.xlsx

**Aplicação:**
- Serviços gerais
- Apoio operacional
- Movimentação de materiais

---

### 4. Vigilância Patrimonial
**Diretório:** `vigilancia_patrimonial/`

**Documentos:**
- [ ] Caderno Técnico de Composição de Custos.pdf
- [ ] Planilha de Composição de Custos.xlsx

**Aplicação:**
- Contratos de segurança
- Definição de postos de vigilância
- Cálculo de custos com encargos

---

### 5. Ascensorista ou Cabineiros
**Diretório:** `ascensorista_cabineiro/`

**Documentos:**
- [ ] Caderno Técnico de Composição de Custos.pdf
- [ ] Planilha de Composição de Custos.xlsx

**Aplicação:**
- Operação de elevadores
- Controle de acesso vertical
- Composição de custos específicos

---

## 📥 Como Adicionar os Documentos

### Método 1: Upload via GitHub
1. Acesse: https://github.com/cdmattostjsp-sys/contrato-regional-ia
2. Navegue até: `knowledge/cadernos_tecnicos/[nome_servico]/`
3. Clique em **"Add file" → "Upload files"**
4. Arraste os arquivos (PDF e XLSX)
5. Commit: "docs: adicionar caderno técnico de [serviço]"

### Método 2: Upload via VS Code (Codespaces)
1. Clique com botão direito em `knowledge/cadernos_tecnicos/[nome_servico]/`
2. Selecione **"Upload Files..."**
3. Escolha os documentos
4. Commit e push

---

## 🎯 Benefícios da Integração

### Para o Copilot
- ✅ Respostas técnicas sobre composição de custos
- ✅ Orientações específicas por tipo de serviço
- ✅ Cálculos e referências de mercado

### Para Notificações
- ✅ Fundamentação técnica em irregularidades
- ✅ Citação de parâmetros oficiais
- ✅ Referências de custos esperados

### Para Fiscalização
- ✅ Consulta rápida a especificações
- ✅ Validação de planilhas da contratada
- ✅ Comparação com padrões TJSP

---

## 🔧 Integração no Sistema

Após adicionar os documentos, o sistema automaticamente:

1. **Detectará** os novos PDFs e planilhas
2. **Classificará** por tipo de serviço
3. **Disponibilizará** na página Biblioteca
4. **Indexará** para busca futura

### Atualização do document_service.py

Os cadernos serão reconhecidos e classificados como:
```python
"Caderno Técnico - [Nome do Serviço]"
```

---

## 📊 Nomenclatura Recomendada

Para facilitar a identificação automática:

```
limpeza_predial/
├── caderno_tecnico_limpeza.pdf
└── planilha_custos_limpeza.xlsx

garcom_copeiro/
├── caderno_tecnico_garcom_copeiro.pdf
└── planilha_custos_garcom_copeiro.xlsx

mao_obra_bracal/
├── caderno_tecnico_mao_obra_bracal.pdf
└── planilha_custos_mao_obra_bracal.xlsx

vigilancia_patrimonial/
├── caderno_tecnico_vigilancia.pdf
└── planilha_custos_vigilancia.xlsx

ascensorista_cabineiro/
├── caderno_tecnico_ascensorista.pdf
└── planilha_custos_ascensorista.xlsx
```

---

## 🚀 Próximas Implementações

Com esses cadernos técnicos, poderemos:

1. **Validação Automática de Custos**
   - Comparar valores do contrato com parâmetros TJSP
   - Alertar sobre divergências significativas

2. **Gerador de TR (Termo de Referência)**
   - Templates baseados nos cadernos técnicos
   - Especificações técnicas automatizadas

3. **Calculadora de Custos**
   - Baseada nas planilhas oficiais
   - Simulação de valores contratuais

4. **Análise de Conformidade**
   - Verificar se contrato atende especificações técnicas
   - Sugerir adequações

---

## 📞 Download dos Documentos

Os cadernos técnicos estão disponíveis no site do TJSP:
- Portal de Compras do TJSP
- Seção de Cadernos Técnicos
- Área de Licitações e Contratos

Ou solicite à área responsável por contratações do TJSP.

---

**Estrutura criada e pronta para receber os documentos!** 📚✨

Aguardando upload dos PDFs e planilhas para enriquecer ainda mais o sistema.
