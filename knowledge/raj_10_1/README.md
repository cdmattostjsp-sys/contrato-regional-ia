# Base de Conhecimento RAJ 10.1

## 📚 Documentos Disponíveis

### 1. Manual de Contratos - TJSP - 2025.pdf
**Tipo:** Manual Institucional  
**Tamanho:** 1,7 MB  
**Status:** ✅ Disponível  
**Descrição:** Manual institucional oficial do TJSP para gestão e fiscalização de contratos, atualizado em 2025.

**Conteúdo esperado:**
- Conceitos fundamentais de contratos públicos
- Procedimentos de fiscalização
- Atribuições dos fiscais
- Rotinas de acompanhamento
- Gestão documental
- Modelos e templates

---

### 2. INSTRUÇÃO NORMATIVA Nº 12-2025 2 1.pdf
**Tipo:** Instrução Normativa  
**Tamanho:** 2,6 MB  
**Status:** ✅ Disponível  
**Descrição:** Instrução normativa institucional do TJSP sobre contratos administrativos.

**Conteúdo esperado:**
- Normas específicas do TJSP
- Procedimentos obrigatórios
- Fluxos administrativos
- Competências e responsabilidades
- Prazos institucionais

---

### 3. manual-de-boas-praticas-em-contratacoes-publicas.pdf
**Tipo:** Manual de Boas Práticas  
**Tamanho:** 24,3 MB  
**Status:** ✅ Disponível  
**Descrição:** Guia completo de boas práticas em contratações públicas.

**Conteúdo esperado:**
- Melhores práticas do setor público
- Casos de uso e exemplos
- Orientações técnicas
- Checklist de procedimentos
- Jurisprudência e precedentes

---

## 🎯 Uso no Sistema

### Integração com Agentes de IA

Estes documentos servirão como base de conhecimento para:

1. **Copilot de Contratos** (`agents/copilot_agent.py`)
   - Respostas contextuais enriquecidas
   - Citações de normas e procedimentos
   - Orientações baseadas em documentos oficiais

2. **Geração de Notificações** (`agents/notificacao_agent.py`)
   - Fundamentação legal automática
   - Templates baseados em modelos oficiais
   - Citação de artigos e cláusulas

3. **Página "Como Proceder"** (`pages/04_📖_Como_Proceder.py`)
   - Conteúdo extraído dos manuais
   - Procedimentos atualizados
   - Referências legais precisas

---

## 🚀 Implementação Futura

### Fase 1: Extração de Texto (Próxima)
```python
# Adicionar ao requirements.txt
PyPDF2==3.0.1  # ou
pdfplumber==0.10.3

# Implementar em services/document_service.py
def extrair_texto_pdf(caminho_pdf: str) -> str:
    # Extração real de texto
    pass
```

### Fase 2: Indexação e Busca
- Criar índice de palavras-chave
- Implementar busca full-text
- Adicionar busca por seção/capítulo

### Fase 3: IA Avançada
- Embeddings para busca semântica
- RAG (Retrieval Augmented Generation)
- Respostas geradas com contexto dos PDFs
- Citações automáticas com página e trecho

---

## 📊 Estatísticas

**Total de documentos:** 3  
**Tamanho total:** 28,6 MB  
**Status de extração:** Pendente (Fase 2)  
**Status de integração:** Em desenvolvimento

---

## 🔒 Observações Importantes

- ✅ Documentos institucionais oficiais
- ✅ Atualizados para 2025
- ✅ Armazenados localmente no repositório
- ⏳ Extração de conteúdo em desenvolvimento
- ⏳ Busca automática em desenvolvimento

---

## 📞 Manutenção

Para adicionar novos documentos:

1. Adicione o PDF neste diretório (`knowledge/raj_10_1/`)
2. Commit no Git
3. O sistema detectará automaticamente
4. Atualize este README com informações do documento

---

**Última atualização:** 16/12/2025  
**Versão:** 1.1.0 (Base de conhecimento expandida)
