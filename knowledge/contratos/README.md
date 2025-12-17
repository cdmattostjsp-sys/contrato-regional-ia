# Diretório de Contratos (PDFs)

Este diretório armazena os arquivos PDF dos contratos cadastrados via sistema.

## 📁 Estrutura

```
knowledge/contratos/
├── CTR20251217120000/              # Diretório do contrato
│   ├── CTR20251217120000_PRINCIPAL.pdf     # Contrato principal
│   ├── CTR20251217120000_ADITIVO_01.pdf    # 1º Aditivo
│   ├── CTR20251217120000_ADITIVO_02.pdf    # 2º Aditivo
│   └── ...                                 # N aditivos
├── CTR20251217120001/              # Outro contrato
│   └── CTR20251217120001_PRINCIPAL.pdf
└── ...
```

## 📝 Nomenclatura

**Diretórios:**
- Um diretório por contrato
- Nome = ID do contrato (timestamp único)

**Arquivos:**
- **Contrato:** `{ID}_PRINCIPAL.pdf`
- **Aditivos:** `{ID}_ADITIVO_{NN}.pdf` (numeração sequencial 01, 02, 03...)

## 🔄 Fluxo de Upload

### Cadastro Inicial
1. Usuário acessa **Gestão de Contratos** (página 06)
2. Preenche formulário com dados estruturados
3. Faz upload do PDF do contrato principal
4. **NOVO:** Pode fazer upload de múltiplos aditivos de uma vez
5. Sistema salva:
   - **Diretório** → `knowledge/contratos/{ID}/`
   - **Contrato** → `{ID}_PRINCIPAL.pdf`
   - **Aditivos** → `{ID}_ADITIVO_01.pdf`, `{ID}_ADITIVO_02.pdf`, ...
   - **Metadados** → `data/contratos_cadastrados.json`

### Adicionar Aditivos Posteriormente
(Funcionalidade futura - preparada na estrutura)

## 🎯 Uso dos PDFs

Os PDFs são utilizados para:

### 1. Armazenamento Oficial
Repositório dos documentos contratuais completos.

### 2. Extração de Texto (Futuro)
Integração com PyPDF2 ou pdfplumber para:
- Alimentar o Copiloto com texto completo do contrato
- Busca semântica em cláusulas
- Análise automatizada

### 3. Download pelo Usuário
Os fiscais/gestores podem baixar os PDFs diretamente do sistema.

## 📊 Integração com Dados Estruturados

**Relação entre PDF e Metadados:**

```
knowledge/contratos/CTR20251217120530.pdf  ←→  data/contratos_cadastrados.json
           (Documento completo)                    (Dados estruturados)
```

**Dados Estruturados incluem:**
- Número, fornecedor, objeto
- Datas, valor, fiscais
- Status, vigência
- **Referência ao PDF** (`pdf_path`, `pdf_filename`)

## 🚀 Próximos Passos (Evolução)

### Fase 1 - MVP Atual ✅
- Upload de PDF único por contrato
- Armazenamento simples
- Listagem

### Fase 2 - Aditivos (Futuro)
- Upload de múltiplos aditivos
- Versionamento de contratos
- Histórico de alterações

### Fase 3 - Análise Inteligente (Futuro)
- Extração automática de cláusulas
- RAG (Retrieval Augmented Generation)
- Copiloto lê PDF completo

### Fase 4 - Integração SGF (Produção)
- Sincronização automática com SGF
- Importação em lote
- API REST

## ⚠️ Importante

- **Tamanho máximo:** 200MB por arquivo (limite Streamlit Cloud)
- **Formato:** Apenas PDF
- **Segurança:** Os PDFs não são expostos publicamente
- **Backup:** Considerar backup periódico desta pasta

## 📞 Suporte

Para dúvidas sobre cadastro de contratos, consulte:
- Página: **06_📂_Gestao_Contratos.py**
- Serviço: **services/contract_service.py**
