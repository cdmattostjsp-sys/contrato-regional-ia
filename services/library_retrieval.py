"""
Serviço de retrieval para Copiloto/IA: busca trechos relevantes na Biblioteca.
"""
from services.library_search_service import search_library

def retrieve_passages(query, category=None, k=5):
    """
    Retorna até k trechos relevantes para o Copiloto, com doc, página, snippet.
    """
    return search_library(query, category=category, limit=k)
