"""
Serviço de Processamento de Documentos PDF
===========================================
Extrai e processa conteúdo dos manuais institucionais.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
import re


def listar_documentos_disponiveis() -> List[Dict]:
    """
    Lista todos os documentos PDF disponíveis na base de conhecimento.
    
    Returns:
        Lista de dicionários com informações dos documentos
    """
    knowledge_path = Path(__file__).parent.parent / "knowledge" / "raj_10_1"
    documentos = []
    
    if knowledge_path.exists():
        for pdf_file in knowledge_path.glob("*.pdf"):
            tamanho_mb = pdf_file.stat().st_size / (1024 * 1024)
            documentos.append({
                "nome": pdf_file.name,
                "caminho": str(pdf_file),
                "tamanho_mb": round(tamanho_mb, 2),
                "tipo": classificar_documento(pdf_file.name)
            })
    
    return documentos


def classificar_documento(nome_arquivo: str) -> str:
    """
    Classifica o tipo de documento baseado no nome.
    
    Args:
        nome_arquivo: Nome do arquivo
        
    Returns:
        Tipo do documento
    """
    nome_lower = nome_arquivo.lower()
    
    if "manual" in nome_lower and "contratos" in nome_lower and "tjsp" in nome_lower:
        return "Manual Institucional TJSP"
    elif "instrução" in nome_lower or "normativa" in nome_lower:
        return "Instrução Normativa"
    elif "boas práticas" in nome_lower or "boas-praticas" in nome_lower:
        return "Manual de Boas Práticas"
    else:
        return "Documento Institucional"


def extrair_texto_pdf(caminho_pdf: str) -> str:
    """
    Extrai texto de um arquivo PDF.
    
    NOTA: Esta é uma implementação placeholder para o MVP.
    Em produção, usar biblioteca como PyPDF2, pdfplumber ou pypdf.
    
    Args:
        caminho_pdf: Caminho completo do arquivo PDF
        
    Returns:
        Texto extraído do PDF
    """
    # TODO: Implementar extração real com PyPDF2 ou pdfplumber
    # Para isso, adicionar ao requirements.txt:
    # - PyPDF2==3.0.1 ou
    # - pdfplumber==0.10.3
    
    return """
    [PLACEHOLDER - Extração de PDF não implementada no MVP]
    
    Para implementar:
    1. Adicionar dependência: pip install PyPDF2
    2. Implementar extração real de texto
    3. Tratar erros de leitura
    4. Fazer cache do conteúdo extraído
    
    Os documentos estão disponíveis em:
    - Manual de Contratos - TJSP - 2025.pdf
    - INSTRUÇÃO NORMATIVA Nº 12-2025 2 1.pdf
    - manual-de-boas-praticas-em-contratacoes-publicas.pdf
    """


def buscar_em_documento(query: str, documento_nome: str) -> List[Dict]:
    """
    Busca termos específicos em um documento.
    
    Args:
        query: Termo de busca
        documento_nome: Nome do documento
        
    Returns:
        Lista de trechos encontrados
    """
    # TODO: Implementar busca real após extração de PDF
    return [
        {
            "documento": documento_nome,
            "trecho": f"Trecho relacionado a '{query}' será extraído aqui",
            "pagina": "N/A",
            "relevancia": 0.0
        }
    ]


def obter_contexto_para_copilot(contrato: Dict) -> str:
    """
    Obtém contexto relevante dos manuais para o Copilot.
    
    Args:
        contrato: Dados do contrato
        
    Returns:
        Contexto estruturado dos manuais
    """
    documentos = listar_documentos_disponiveis()
    
    contexto = """
DOCUMENTOS INSTITUCIONAIS DISPONÍVEIS:
======================================

"""
    
    for doc in documentos:
        contexto += f"""
📄 {doc['nome']}
   Tipo: {doc['tipo']}
   Tamanho: {doc['tamanho_mb']} MB
   
"""
    
    contexto += """
NOTA: A extração automática de conteúdo destes PDFs será implementada
na próxima fase. Por enquanto, consulte os documentos diretamente.

Para implementação futura:
- Instalar PyPDF2 ou pdfplumber
- Extrair texto dos PDFs
- Criar índice de busca
- Integrar com respostas do Copilot
"""
    
    return contexto


def obter_referencias_legais() -> Dict:
    """
    Retorna referências legais principais dos manuais.
    
    Returns:
        Dicionário com referências estruturadas
    """
    return {
        "lei_8666_93": {
            "nome": "Lei 8.666/1993",
            "descricao": "Lei de Licitações e Contratos",
            "artigos_importantes": [67, 77, 78, 87, 88]
        },
        "lei_14133_21": {
            "nome": "Lei 14.133/2021",
            "descricao": "Nova Lei de Licitações",
            "artigos_importantes": [117, 137, 155, 156]
        },
        "instrucao_normativa": {
            "nome": "Instrução Normativa TJSP 12/2025",
            "descricao": "Norma institucional de contratos",
            "arquivo": "INSTRUÇÃO NORMATIVA Nº 12-2025 2 1.pdf"
        },
        "manual_tjsp": {
            "nome": "Manual de Contratos TJSP 2025",
            "descricao": "Manual institucional atualizado",
            "arquivo": "Manual de Contratos - TJSP - 2025.pdf"
        },
        "boas_praticas": {
            "nome": "Manual de Boas Práticas",
            "descricao": "Guia de boas práticas em contratações",
            "arquivo": "manual-de-boas-praticas-em-contratacoes-publicas.pdf"
        }
    }


def gerar_resumo_documentos() -> str:
    """
    Gera resumo dos documentos disponíveis.
    
    Returns:
        Resumo formatado em markdown
    """
    documentos = listar_documentos_disponiveis()
    referencias = obter_referencias_legais()
    
    resumo = """
# 📚 Base de Conhecimento - RAJ 10.1

## Documentos Disponíveis

"""
    
    for doc in documentos:
        resumo += f"""
### {doc['tipo']}
**Arquivo:** `{doc['nome']}`  
**Tamanho:** {doc['tamanho_mb']} MB  
**Status:** ✅ Disponível

"""
    
    resumo += """
## Referências Legais Principais

"""
    
    for key, ref in referencias.items():
        if "arquivo" in ref:
            resumo += f"- **{ref['nome']}**: {ref['descricao']} → `{ref['arquivo']}`\n"
        else:
            resumo += f"- **{ref['nome']}**: {ref['descricao']}\n"
    
    resumo += """

## Próximas Implementações

- [ ] Extração automática de texto dos PDFs
- [ ] Índice de busca por palavra-chave
- [ ] Integração com Copilot para respostas baseadas nos manuais
- [ ] Cache de conteúdo extraído
- [ ] Busca semântica com embeddings
- [ ] Citação automática de fontes nas respostas

## Como Usar

Os documentos estão armazenados em `knowledge/raj_10_1/` e serão
automaticamente consultados pelos agentes de IA quando a extração
de PDF for implementada.

**Para desenvolvedores:** Adicione ao requirements.txt:
```
PyPDF2==3.0.1
# ou
pdfplumber==0.10.3
```

Depois implemente a extração real em `extrair_texto_pdf()`.
"""
    
    return resumo
