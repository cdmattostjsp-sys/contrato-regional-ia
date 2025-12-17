"""
Entrypoint para Streamlit Cloud
================================
Este arquivo existe apenas para compatibilidade com o Streamlit Cloud.
O código principal está em: Principal.py

Importa e executa todas as funções de Principal.py mantendo
a funcionalidade completa enquanto permite que o menu lateral
exiba "Principal" ao invés de "app".
"""

# Importa e executa tudo de Principal.py
import sys
from pathlib import Path

# Garante que o diretório raiz está no path
sys.path.insert(0, str(Path(__file__).parent))

# Importa o módulo Principal
import Principal

# Executa a função main do Principal
if __name__ == "__main__":
    Principal.main()
