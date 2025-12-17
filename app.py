"""
Entrypoint para Streamlit Cloud
================================
Este arquivo existe apenas para compatibilidade com o Streamlit Cloud,
que espera encontrar um arquivo 'app.py' na raiz.

O código principal está em: 🏠_Visão_Geral.py
"""

import streamlit as st
import sys
from pathlib import Path

# Redireciona para a página principal
st.switch_page("🏠_Visão_Geral.py")
