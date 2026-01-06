# ⚖️ TJSP - Gestão de Contratos Regionais IA

**Aplicativo Piloto Institucional para Fiscalização e Gestão de Contratos Regionais**

<div align="center">

![TJSP](https://img.shields.io/badge/TJSP-Institucional-003366?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red?style=for-the-badge&logo=streamlit)
![Status](https://img.shields.io/badge/Status-MVP-yellow?style=for-the-badge)

</div>

---

## 📋 Sobre o Projeto

Este é um **aplicativo piloto institucional** desenvolvido para o **Tribunal de Justiça do Estado de São Paulo (TJSP)**, especificamente para a **Coordenadoria Regional - RAJ 10.1**.

O sistema é satélite ao ecossistema **SAAB-Tech / Synapse.IA** e tem como objetivo auxiliar coordenadores regionais e fiscais de contrato em suas atividades de fiscalização, acompanhamento e gestão de contratos administrativos.

### 🎯 Objetivos Principais

- ✅ Centralizar informações sobre contratos regionais
- ✅ Fornecer assistência por IA (Copilot) baseada em contexto contratual
- ✅ Gerar notificações contratuais de forma assistida
- ✅ Orientar fiscais sobre procedimentos administrativos
- ✅ Facilitar o acompanhamento de pendências e irregularidades

---

## 🏗️ Arquitetura

O projeto segue o **padrão arquitetural institucional homologado** do SAAB-Tech:

```
contrato-regional-ia/
├── app.py                      # Aplicação principal (Dashboard)
├── pages/                      # Páginas do aplicativo
│   ├── 01_📄_Contrato.py      # Visualização de contrato
│   ├── 02_🤖_Copilot.py       # Assistente conversacional
│   ├── 03_📝_Notificações.py  # Geração de notificações
│   └── 04_📖_Como_Proceder.py # Orientações ao fiscal
├── agents/                     # Agentes de IA
│   ├── copilot_agent.py       # Processamento de perguntas
│   └── notificacao_agent.py   # Geração de notificações
├── services/                   # Serviços de negócio
│   ├── session_manager.py     # Gerenciamento de sessão
│   └── contract_service.py    # Operações com contratos
├── prompts/                    # Biblioteca de prompts
│   └── system_prompts.py      # Prompts dos agentes
├── knowledge/                  # Base de conhecimento
│   └── raj_10_1/              # Documentos RAJ 10.1
├── ui/                         # Interface e estilos
│   └── styles.py              # CSS institucional TJSP
├── exports/                    # Documentos exportados
├── logs/                       # Logs do sistema
├── tests/                      # Testes automatizados
├── requirements.txt            # Dependências Python
├── runtime.txt                 # Versão do Python
└── README.md                   # Este arquivo
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.11+
- pip (gerenciador de pacotes Python)
- GitHub Codespaces (recomendado) ou ambiente local

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/cdmattostjsp-sys/contrato-regional-ia.git
   cd contrato-regional-ia
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o aplicativo:**
   ```bash
   streamlit run app.py
   ```

4. **Acesse no navegador:**
   ```
   http://localhost:8501
   ```

---

## 📱 Funcionalidades

### 🏠 Dashboard Principal
- Visualização de cards de contratos regionais
- Métricas consolidadas (contratos ativos, pendências, conformidade)
- Filtros por status e tipo de contrato
- Acesso rápido às ações de cada contrato

### 📄 Visualização de Contrato
- Dados gerais do contrato
- Cláusulas principais
- Documentos anexados
- Histórico de eventos

### 🤖 Copilot de Contrato
- Assistente conversacional contextual
- Responde perguntas **exclusivamente** sobre o contrato carregado
- Interface de chat intuitiva
- Histórico de conversação

### 📝 Geração de Notificações
- Formulário assistido para notificações contratuais
- Geração automática com IA
- Pré-visualização da notificação
- Templates institucionais padronizados

### 📖 Como Proceder
- Guia de atribuições do fiscal de contrato
- Procedimentos de acompanhamento (diário, semanal, mensal)
- Fluxos de tratamento de irregularidades
- Base legal e normativa aplicável

### 📚 Biblioteca de Manuais
- Consulta aos manuais institucionais em PDF
- Manual de Contratos TJSP 2025 (1,7 MB)
- Instrução Normativa 12/2025 (2,6 MB)
- Manual de Boas Práticas em Contratações (24,3 MB)
- Referências legais estruturadas

### 🔔 Alertas Contratuais
- Sistema automático de identificação de alertas
- Monitoramento de vigência, status e pendências
- Resolução formal com justificativa obrigatória
- Rastreabilidade completa (ato administrativo)
- Integração com histórico do contrato
- Notificações por email (configurável)
- **Documentação completa:** `docs/MODULO_ALERTAS.md`

### 📚 Biblioteca de Conhecimento Institucional (Fase 2.1)

A **Biblioteca de Conhecimento Institucional** é um repositório curado de documentos orientativos do TJSP, consumido automaticamente pela IA do COPILOTO.

#### Funcionalidades

- **Upload controlado** de documentos PDF/DOCX (restrito por perfil)
- **Metadados obrigatórios**: título, tipo, área, versão, status
- **Versionamento simples**: controle de versões sem sobrescrita
- **Indexação textual**: extração automática de texto para busca
- **Consumo pela IA**: COPILOTO consulta documentos ativos como referência

#### Governança

- **Perfis autorizados**: ADMIN, CURADOR, JURIDICO
- **Status de documentos**: ATIVO (usado pela IA) / REVOGADO (histórico)
- **Rastreabilidade**: eventos registrados no histórico institucional
- **Referenciação**: respostas da IA citam fontes institucionais

#### Tipos de Documentos Suportados

- Manual
- Nota Técnica
- Orientação Jurídica
- Caderno Técnico
- Instrução Normativa
- Guia de Boas Práticas

#### Estrutura de Arquivos

```
knowledge/
├── documentos/           # Arquivos originais por tipo
│   ├── manual/
│   ├── nota_tecnica/
│   ├── orientacao_juridica/
│   ├── caderno_tecnico/
│   ├── instrucao_normativa/
│   └── guia_de_boas_praticas/
├── textos_extraidos/     # Textos extraídos para indexação
└── index.json            # Índice de metadados
```

#### Como Usar

1. Acesse a página **📚 Gestão de Conhecimento**
2. Faça upload do documento (PDF/DOCX)
3. Preencha os metadados obrigatórios
4. Clique em **Publicar Documento**
5. O COPILOTO passará a consultar o documento em suas respostas

#### Princípio Fundamental

> **A IA não substitui normas. Ela opera subordinada ao conhecimento institucional validado.**

---

## 🎨 Design System

O aplicativo segue rigorosamente o **Design System Institucional TJSP**, incluindo:

- **Cores oficiais:** Azul primário (#003366), Azul secundário (#0066CC)
- **Tipografia:** Roboto (família institucional)
- **Componentes:** Cards, botões, formulários padronizados
- **Identidade visual:** Brasão, cores e elementos gráficos oficiais

Referência: `DESIGN_SYSTEM_TJSP.md` (repositório synapse-next-homologacao)

---

## 🔧 Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| **Python** | 3.11+ | Linguagem principal |
| **Streamlit** | 1.31.0 | Framework web |
| **Pandas** | 2.2.0 | Manipulação de dados |
| **NumPy** | 1.26.3 | Computação numérica |

---

## 📊 Status do Projeto

**Fase Atual:** MVP (Minimum Viable Product)

### ✅ Implementado
- [x] Estrutura base do projeto
- [x] Dashboard com cards de contratos
- [x] Página de visualização de contrato
- [x] Copilot com respostas contextuais (mockado)
- [x] Geração de notificações (mockado)
- [x] Área "Como Proceder"
- [x] CSS institucional TJSP
- [x] Navegação entre páginas
- [x] Session state management
- [x] **Módulo de Alertas consolidado (governança)**

### � Base de Conhecimento
- [x] Manual de Contratos TJSP 2025
- [x] Instrução Normativa 12/2025
- [x] Manual de Boas Práticas em Contratações Públicas
- [x] Página de Biblioteca de Manuais
- [ ] Extração automática de texto PDF
- [ ] Busca nos documentos

### �🔄 Em Desenvolvimento
- [ ] Integração com API REST corporativa
- [ ] Integração com modelo LLM real (OpenAI/Azure)
- [ ] Upload de documentos contratuais
- [ ] Exportação de notificações em DOCX/PDF
- [ ] Sistema de autenticação
- [ ] Logs e auditoria completos
- [ ] Testes automatizados

### 📅 Roadmap Futuro
- [ ] Integração com sistemas TJSP (e-SAJ, etc.)
- [ ] Dashboard analytics avançado
- [ ] Painel de auditoria de alertas resolvidos
- [ ] Workflow de aprovação de notificações
- [ ] Assinatura digital de documentos
- [ ] App mobile (Progressive Web App)

---

## 👥 Perfis de Usuário

O sistema atende aos seguintes perfis:

1. **Coordenador Regional**
   - Visão geral de todos os contratos
   - Aprovação de notificações
   - Relatórios gerenciais

2. **Fiscal de Contrato (Titular/Substituto)**
   - Acompanhamento diário de contratos
   - Geração de notificações
   - Registro de ocorrências

3. **Administrador do Sistema**
   - Configurações gerais
   - Gestão de usuários
   - Acesso a logs e auditoria

---

## 📚 Referências Institucionais

Este projeto segue os padrões definidos em:

- **ARCHITECTURE_PATTERNS.md** - Padrões arquiteturais SAAB-Tech
- **DESIGN_SYSTEM_TJSP.md** - Design system institucional
- **CODE_STANDARDS.md** - Padrões de código
- **INTEGRATION_BLUEPRINT.md** - Blueprint de integrações
- **docs/MODULO_ALERTAS.md** - Documentação técnica do módulo de alertas

Repositório de referência: [synapse-next-homologacao](https://github.com/cdmattostjsp-sys/synapse-next-homologacao)

---

## 🔒 Segurança e Compliance

- Dados mockados para ambiente de desenvolvimento
- Preparado para integração segura com APIs corporativas
- Seguirá políticas de segurança da informação do TJSP
- Auditoria de todas as ações sensíveis
- LGPD compliance (em implementação)

---

## 🤝 Contribuição

Este é um projeto institucional interno do TJSP. Contribuições devem seguir:

1. Padrões de código definidos no CODE_STANDARDS.md
2. Aprovação prévia da equipe SAAB-Tech
3. Testes obrigatórios antes de merge
4. Documentação atualizada

---

## 📞 Contato

**Tribunal de Justiça do Estado de São Paulo**  
Coordenadoria Regional - RAJ 10.1  
Projeto SAAB-Tech / Synapse.IA

Para dúvidas ou suporte, entre em contato com a equipe de desenvolvimento institucional.

---

## 📄 Licença

Projeto de uso **exclusivamente institucional** do TJSP.  
Todos os direitos reservados © 2025 TJSP.

---

<div align="center">

**Desenvolvido com ⚖️ pelo TJSP**

![TJSP Logo](https://img.shields.io/badge/TJSP-Justiça%20para%20Todos-003366?style=for-the-badge)

</div>
