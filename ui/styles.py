"""
Estilos CSS Institucionais TJSP
================================
Design System aplicado conforme padrão homologado SAAB-Tech.

Referência: DESIGN_SYSTEM_TJSP.md
"""

import streamlit as st


def apply_tjsp_styles():
    """
    Aplica o CSS institucional do TJSP em todas as páginas.
    Cores oficiais e identidade visual padronizada.
    """
    st.markdown("""
        <style>
        /* =====================================================
           CORES INSTITUCIONAIS TJSP
           ===================================================== */
        :root {
            --tjsp-azul-primario: #003366;
            --tjsp-azul-secundario: #0066CC;
            --tjsp-azul-claro: #E6F2FF;
            --tjsp-dourado: #B8860B;
            --tjsp-cinza-escuro: #333333;
            --tjsp-cinza-medio: #666666;
            --tjsp-cinza-claro: #F5F5F5;
            --tjsp-branco: #FFFFFF;
            --tjsp-verde: #28A745;
            --tjsp-amarelo: #FFC107;
            --tjsp-vermelho: #DC3545;
        }
        
        /* =====================================================
           TIPOGRAFIA INSTITUCIONAL
           ===================================================== */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
        
        * {
            font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        /* =====================================================
           CABEÇALHO TJSP
           ===================================================== */
        .tjsp-header {
            background: linear-gradient(135deg, var(--tjsp-azul-primario) 0%, var(--tjsp-azul-secundario) 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .tjsp-header h1 {
            color: var(--tjsp-branco);
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
        }
        
        .tjsp-subtitle {
            color: var(--tjsp-azul-claro);
            margin: 0.5rem 0 0 0;
            font-size: 1rem;
            font-weight: 300;
        }
        
        /* =====================================================
           CARDS DE CONTRATO
           ===================================================== */
        .contract-card {
            background: var(--tjsp-branco);
            border-left: 4px solid var(--tjsp-azul-primario);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
        }
        
        .contract-card:hover {
            box-shadow: 0 4px 12px rgba(0, 51, 102, 0.15);
            transform: translateY(-2px);
        }
        
        .contract-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--tjsp-cinza-claro);
        }
        
        .contract-header h3 {
            margin: 0;
            color: var(--tjsp-azul-primario);
            font-size: 1.2rem;
        }
        
        .contract-badge {
            background: var(--tjsp-azul-claro);
            color: var(--tjsp-azul-primario);
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        .contract-card p {
            margin: 0.5rem 0;
            color: var(--tjsp-cinza-escuro);
            font-size: 0.95rem;
        }
        
        /* =====================================================
           BOTÕES INSTITUCIONAIS
           ===================================================== */
        .stButton>button {
            background-color: var(--tjsp-azul-primario);
            color: var(--tjsp-branco);
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: var(--tjsp-azul-secundario);
            box-shadow: 0 2px 8px rgba(0, 51, 102, 0.3);
        }
        
            /* =====================================================
               BOTÃO DE NOTIFICAÇÃO CONTRATUAL (DESTAQUE)
               ===================================================== */
            .notificacao-btn {
                background: linear-gradient(90deg, var(--tjsp-dourado) 0%, var(--tjsp-azul-primario) 100%);
                color: var(--tjsp-branco) !important;
                border: 2px solid var(--tjsp-dourado);
                border-radius: 8px;
                font-size: 1.15rem !important;
                font-weight: 700;
                padding: 0.7rem 1.5rem !important;
                box-shadow: 0 4px 16px rgba(184, 134, 11, 0.10);
                display: flex;
                align-items: center;
                gap: 0.7rem;
            }
        
            .notificacao-btn .notificacao-icon {
                background: var(--tjsp-dourado);
                color: var(--tjsp-branco);
                border-radius: 50%;
                padding: 0.35rem 0.55rem;
                font-size: 1.5rem;
                margin-right: 0.5rem;
                box-shadow: 0 2px 8px rgba(184, 134, 11, 0.15);
            }
        
            .notificacao-btn .notificacao-title {
                font-size: 1.1rem;
                font-weight: 700;
                letter-spacing: 0.5px;
            }
        
            .notificacao-btn .notificacao-desc {
                font-size: 0.95rem;
                font-weight: 400;
                color: var(--tjsp-branco);
                opacity: 0.85;
            }
        
            .notificacao-btn:hover, .notificacao-btn:focus {
                box-shadow: 0 6px 24px rgba(184, 134, 11, 0.18);
                transform: translateY(-2px) scale(1.04);
                cursor: pointer;
                filter: brightness(1.08);
            }
        
        /* =====================================================
           MÉTRICAS
           ===================================================== */
        [data-testid="stMetricValue"] {
            color: var(--tjsp-azul-primario);
            font-size: 2rem;
            font-weight: 700;
        }
        
        [data-testid="stMetricLabel"] {
            color: var(--tjsp-cinza-medio);
            font-weight: 500;
        }
        
        /* =====================================================
           SIDEBAR
           ===================================================== */
        [data-testid="stSidebar"] {
            background-color: var(--tjsp-cinza-claro);
        }
        
        [data-testid="stSidebar"] .stMarkdown {
            color: var(--tjsp-cinza-escuro);
        }
        
        /* =====================================================
           CHAT / COPILOT
           ===================================================== */
        .chat-message {
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        .chat-message.user {
            background-color: var(--tjsp-azul-claro);
            border-left: 4px solid var(--tjsp-azul-primario);
        }
        
        .chat-message.assistant {
            background-color: var(--tjsp-cinza-claro);
            border-left: 4px solid var(--tjsp-dourado);
        }
        
        /* =====================================================
           ALERTAS E NOTIFICAÇÕES
           ===================================================== */
        .alert-success {
            background-color: #d4edda;
            border-left: 4px solid var(--tjsp-verde);
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .alert-warning {
            background-color: #fff3cd;
            border-left: 4px solid var(--tjsp-amarelo);
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .alert-danger {
            background-color: #f8d7da;
            border-left: 4px solid var(--tjsp-vermelho);
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        /* =====================================================
           RODAPÉ INSTITUCIONAL
           ===================================================== */
        .tjsp-footer {
            text-align: center;
            padding: 2rem 0;
            color: var(--tjsp-cinza-medio);
            font-size: 0.85rem;
        }
        
        .tjsp-footer p {
            margin: 0.25rem 0;
        }
        
        /* =====================================================
           CONTAINERS E DIVISORES
           ===================================================== */
        .stContainer {
            border-radius: 8px;
        }
        
        hr {
            border: none;
            border-top: 1px solid var(--tjsp-cinza-claro);
            margin: 2rem 0;
        }
        
        /* =====================================================
           INPUTS E FORMULÁRIOS
           ===================================================== */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea,
        .stSelectbox>div>div>select {
            border: 1px solid var(--tjsp-cinza-claro);
            border-radius: 5px;
            padding: 0.5rem;
        }
        
        .stTextInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus,
        .stSelectbox>div>div>select:focus {
            border-color: var(--tjsp-azul-primario);
            box-shadow: 0 0 0 1px var(--tjsp-azul-primario);
        }
        
        /* =====================================================
           TABS
           ===================================================== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: var(--tjsp-cinza-claro);
            border-radius: 5px 5px 0 0;
            color: var(--tjsp-cinza-medio);
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--tjsp-azul-primario);
            color: var(--tjsp-branco);
        }
        
        /* =====================================================
           EXPANDERS
           ===================================================== */
        .streamlit-expanderHeader {
            background-color: var(--tjsp-azul-claro);
            border-radius: 5px;
            font-weight: 500;
            color: var(--tjsp-azul-primario);
        }
        
        /* =====================================================
           HIERARQUIA DE TÍTULOS INSTITUCIONAL
           ===================================================== */
        /* Título principal da página - mantém destaque */
        h1 {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            color: var(--tjsp-azul-primario) !important;
            margin-bottom: 1rem !important;
        }
        
        /* Subtítulos principais (seções) - REDUZIDO */
        h2 {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: var(--tjsp-azul-primario) !important;
            margin-top: 1.5rem !important;
            margin-bottom: 0.8rem !important;
        }
        
        /* Subtítulos secundários (subseções) - AINDA MENOR */
        h3 {
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            color: var(--tjsp-cinza-escuro) !important;
            margin-top: 1rem !important;
            margin-bottom: 0.6rem !important;
        }
        
        /* Subtítulos terciários */
        h4 {
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            color: var(--tjsp-cinza-medio) !important;
            margin-top: 0.8rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* =====================================================
           RESPONSIVIDADE
           ===================================================== */
        @media (max-width: 768px) {
            .tjsp-header h1 {
                font-size: 1.5rem;
            }
            
            h1 {
                font-size: 1.5rem !important;
            }
            
            h2 {
                font-size: 1rem !important;
            }
            
            h3 {
                font-size: 0.9rem !important;
            }
            
            h4 {
                font-size: 0.85rem !important;
            }
            
            .contract-header {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .contract-badge {
                margin-top: 0.5rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)
