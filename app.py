"""
Entrypoint para Streamlit Cloud
================================
Redireciona para Home.py seguindo padrão SAAB-Tech
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import Home

if __name__ == "__main__":
    Home.main()
