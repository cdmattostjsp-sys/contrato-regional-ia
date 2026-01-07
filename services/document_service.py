"""
Serviço de Processamento de Documentos PDF
===========================================
Extrai e processa conteúdo dos manuais institucionais.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
import re
import logging

logger = logging.getLogger(__name__)


def listar_documentos_disponiveis() -> List[Dict]:
    """
    Lista todos os documentos PDF disponíveis na base de conhecimento.
    
    Returns:
        Lista de dicionários com informações dos documentos
    """
    base_path = Path(__file__).parent.parent / "knowledge"
    documentos = []
    
    # RAJ 10.1 - Manuais institucionais
    raj_path = base_path / "raj_10_1"
    if raj_path.exists():
        for pdf_file in raj_path.glob("*.pdf"):
            tamanho_mb = pdf_file.stat().st_size / (1024 * 1024)
            documentos.append({
                "nome": pdf_file.name,
                "caminho": str(pdf_file),
                "tamanho_mb": round(tamanho_mb, 2),
                "tipo": classificar_documento(pdf_file.name),
                "categoria": "Manuais Institucionais"
            })
    
    # Cadernos Técnicos
    cadernos_path = base_path / "cadernos_tecnicos"
    if cadernos_path.exists():
        for servico_dir in cadernos_path.iterdir():
            if servico_dir.is_dir():
                servico_nome = servico_dir.name.replace("_", " ").title()
                for doc_file in servico_dir.glob("*.*"):
                    if doc_file.suffix.lower() in ['.pdf', '.xlsx', '.xls']:
                        tamanho_mb = doc_file.stat().st_size / (1024 * 1024)
                        documentos.append({
                            "nome": doc_file.name,
                            "caminho": str(doc_file),
                            "tamanho_mb": round(tamanho_mb, 2),
                            "tipo": f"Caderno Técnico - {servico_nome}",
                            "categoria": "Cadernos Técnicos",
                            "servico": servico_nome
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
    Extrai texto de um arquivo PDF usando PyMuPDF (fitz).
    
    Args:
        caminho_pdf: Caminho completo do arquivo PDF
        
    Returns:
        Texto extraído do PDF ou string vazia em caso de erro
    """
    try:
        import fitz  # PyMuPDF
        
        texto_completo = []
        
        # Abre o PDF
        doc = fitz.open(caminho_pdf)
        
        # Extrai texto de cada página
        for pagina_num in range(len(doc)):
            pagina = doc[pagina_num]
            texto = pagina.get_text("text")
            if texto.strip():
                texto_completo.append(f"\n--- Página {pagina_num + 1} ---\n{texto}")
        
        doc.close()
        
        return "\n".join(texto_completo)
        
    except ImportError:
        logger.warning("⚠️ PyMuPDF (fitz) não instalado. Instale com: pip install pymupdf")
        return ""
    except Exception as e:
        logger.error(f"Erro ao extrair texto do PDF {caminho_pdf}: {e}")
        return ""


def filtrar_trechos_relevantes(texto_completo: str, palavras_chave: List[str], tamanho_janela: int = 800, max_trechos: int = 5) -> str:
    """
    Filtra trechos relevantes de um texto longo baseado em palavras-chave.
    
    Args:
        texto_completo: Texto completo extraído
        palavras_chave: Lista de palavras-chave para buscar
        tamanho_janela: Tamanho da janela de contexto (caracteres antes e depois)
        max_trechos: Número máximo de trechos a retornar
        
    Returns:
        Texto com os trechos mais relevantes
    """
    if not texto_completo or not palavras_chave:
        return texto_completo[:5000]  # Retorna início se não houver filtro
    
    texto_lower = texto_completo.lower()
    palavras_lower = [p.lower() for p in palavras_chave]
    
    # Encontra posições onde palavras-chave aparecem
    ocorrencias = []
    for palavra in palavras_lower:
        pos = 0
        while True:
            pos = texto_lower.find(palavra, pos)
            if pos == -1:
                break
            ocorrencias.append(pos)
            pos += 1
    
    if not ocorrencias:
        # Se não encontrou palavras-chave, retorna início
        return texto_completo[:5000]
    
    # Ordena ocorrências
    ocorrencias.sort()
    
    # Extrai trechos com janela de contexto
    trechos = []
    usado = set()
    
    for pos in ocorrencias:
        if len(trechos) >= max_trechos:
            break
        
        inicio = max(0, pos - tamanho_janela)
        fim = min(len(texto_completo), pos + tamanho_janela)
        
        # Evita sobreposição
        if any(i in usado for i in range(inicio, fim)):
            continue
        
        trecho = texto_completo[inicio:fim]
        trechos.append(f"\n[...]{trecho}[...]\n")
        usado.update(range(inicio, fim))
    
    return "\n".join(trechos) if trechos else texto_completo[:5000]


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
    
    # Agrupa por categoria
    por_categoria = {}
    for doc in documentos:
        categoria = doc.get('categoria', 'Outros')
        if categoria not in por_categoria:
            por_categoria[categoria] = []
        por_categoria[categoria].append(doc)
    
    resumo = """
# 📚 Base de Conhecimento Completa

## Documentos por Categoria

"""
    
    for categoria, docs in por_categoria.items():
        resumo += f"\n### {categoria}\n\n"
        for doc in docs:
            resumo += f"""
**{doc['tipo']}**  
Arquivo: `{doc['nome']}`  
Tamanho: {doc['tamanho_mb']} MB  
Status: ✅ Disponível

"""
    
    resumo += """
## Referências Legais Principais

"""
    
    for key, ref in referencias.items():
        if "arquivo" in ref:
            resumo += f"- **{ref['nome']}**: {ref['descricao']} → `{ref['arquivo']}`\n"
        else:
            resumo += f"- **{ref['nome']}**: {ref['descricao']}\n"
    
    total_docs = len(documentos)
    total_mb = sum(d['tamanho_mb'] for d in documentos)
    
    resumo += f"""

## 📊 Estatísticas

- **Total de documentos:** {total_docs}
- **Tamanho total:** {total_mb:.1f} MB
- **Categorias:** {len(por_categoria)}

## Próximas Implementações

- [ ] Extração automática de texto dos PDFs
- [ ] Índice de busca por palavra-chave
- [ ] Integração com Copilot para respostas baseadas nos manuais
- [ ] Cache de conteúdo extraído
- [ ] Busca semântica com embeddings
- [ ] Citação automática de fontes nas respostas
- [ ] Análise de planilhas XLSX (Cadernos Técnicos)

## Como Usar

Os documentos estão armazenados em `knowledge/` e serão
automaticamente consultados pelos agentes de IA quando a extração
de PDF for implementada.

**Para desenvolvedores:** Adicione ao requirements.txt:
```
PyPDF2==3.0.1
# ou
pdfplumber==0.10.3
openpyxl==3.1.2  # Para planilhas Excel
```

Depois implemente a extração real em `extrair_texto_pdf()`.
"""
    
    return resumo
