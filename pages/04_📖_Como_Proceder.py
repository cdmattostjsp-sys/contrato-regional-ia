"""
Página Como Proceder
=====================
Orientações para fiscais de contrato sobre procedimentos administrativos.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state


def main():
    st.set_page_config(
        page_title="TJSP - Como Proceder",
        page_icon="📖",
        layout="wide"
    )
    
    apply_tjsp_styles()
    initialize_session_state()
    
    # Cabeçalho
    st.markdown("""
        <div style="background: linear-gradient(135deg, #003366 0%, #0066CC 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem; color: white;">
            <h1>📖 Como Proceder - Orientações ao Fiscal</h1>
            <p style="font-size: 1.1rem; opacity: 0.9;">
            Guia institucional de procedimentos para fiscalização de contratos
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Botão de navegação
    if st.button("🏠 Voltar ao Dashboard", use_container_width=False):
        st.switch_page("Home.py")
    
    st.markdown("---")
    
    # Tabs de orientações
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Atribuições",
        "📋 Acompanhamento",
        "⚠️ Irregularidades",
        "📝 Notificações",
        "📚 Base Legal"
    ])
    
    with tab1:
        st.markdown("## 🎯 Atribuições do Fiscal de Contrato")
        
        st.markdown("""
        ### Responsabilidades Principais
        
        O fiscal de contrato é responsável por:
        
        #### 1. Acompanhamento da Execução
        - Verificar o cumprimento de todas as cláusulas contratuais
        - Fiscalizar a qualidade dos serviços/produtos entregues
        - Conferir prazos estabelecidos no cronograma
        - Acompanhar a regularidade fiscal e trabalhista da contratada
        
        #### 2. Gestão Documental
        - Manter arquivo organizado de toda documentação do contrato
        - Elaborar relatórios mensais de acompanhamento
        - Atestar notas fiscais após conferência dos serviços
        - Registrar todas as ocorrências em sistema próprio
        
        #### 3. Comunicação Institucional
        - Comunicar imediatamente irregularidades ao gestor
        - Notificar a contratada quando necessário
        - Solicitar documentação complementar
        - Propor aplicação de penalidades quando cabível
        
        #### 4. Controle Financeiro
        - Conferir medições e quantitativos executados
        - Verificar adequação dos valores cobrados
        - Atestar documentos fiscais para pagamento
        - Acompanhar saldo contratual
        """)
        
        st.success("""
        **💡 Dica:** Mantenha um cronograma de fiscalização regular e documente 
        todas as ações em relatórios detalhados.
        """)
    
    with tab2:
        st.markdown("## 📋 Procedimentos de Acompanhamento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Rotina Diária
            
            - ✅ Verificar execução dos serviços do dia
            - ✅ Conferir presença de funcionários
            - ✅ Registrar ocorrências relevantes
            - ✅ Verificar equipamentos e materiais
            
            ### Rotina Semanal
            
            - 📊 Consolidar ocorrências da semana
            - 📋 Verificar documentação trabalhista
            - 🔍 Realizar vistoria técnica
            - 📝 Atualizar planilhas de controle
            """)
        
        with col2:
            st.markdown("""
            ### Rotina Mensal
            
            - 📄 Elaborar relatório mensal
            - 💰 Conferir e atestar notas fiscais
            - 📊 Analisar indicadores de desempenho
            - 🗂️ Organizar documentação do mês
            
            ### Rotina Trimestral
            
            - 📈 Avaliar cumprimento de metas
            - 🔄 Revisar procedimentos de fiscalização
            - 📋 Verificar validade de certidões
            - 💼 Reunião com gestor do contrato
            """)
        
        st.warning("""
        **⚠️ Atenção:** Todas as fiscalizações devem ser documentadas, 
        mesmo que não sejam identificadas irregularidades.
        """)
    
    with tab3:
        st.markdown("## ⚠️ Tratamento de Irregularidades")
        
        st.markdown("### Fluxo de Ação em Caso de Irregularidade")
        
        st.markdown("""
        ```
        1. IDENTIFICAÇÃO
           ↓
        2. REGISTRO FORMAL
           ↓
        3. NOTIFICAÇÃO À CONTRATADA
           ↓
        4. PRAZO PARA REGULARIZAÇÃO
           ↓
        5. VERIFICAÇÃO DA CORREÇÃO
           ↓
        6. COMUNICAÇÃO AO GESTOR
        ```
        """)
        
        st.markdown("### Tipos de Irregularidades e Procedimentos")
        
        with st.expander("🔴 IRREGULARIDADE GRAVE (Ação Imediata)"):
            st.markdown("""
            **Exemplos:**
            - Ausência total de serviço
            - Risco à segurança
            - Descumprimento grave de cláusula contratual
            
            **Procedimento:**
            1. Comunicar IMEDIATAMENTE ao gestor do contrato
            2. Registrar formalmente com fotos/evidências
            3. Emitir notificação urgente à contratada
            4. Prazo máximo: 24-48 horas para correção
            5. Se não corrigido: propor penalidade ou rescisão
            """)
        
        with st.expander("🟡 IRREGULARIDADE MÉDIA (Ação em 5 dias)"):
            st.markdown("""
            **Exemplos:**
            - Atraso na entrega de documentação
            - Qualidade inferior ao contratado
            - Falta de funcionários
            
            **Procedimento:**
            1. Registrar a ocorrência no sistema
            2. Notificar a contratada formalmente
            3. Estabelecer prazo de 5 dias úteis
            4. Acompanhar a regularização
            5. Se não corrigido: comunicar ao gestor
            """)
        
        with st.expander("🟢 IRREGULARIDADE LEVE (Orientação)"):
            st.markdown("""
            **Exemplos:**
            - Pequenos atrasos pontuais
            - Questões de organização
            - Falhas menores de procedimento
            
            **Procedimento:**
            1. Orientar verbalmente a contratada
            2. Registrar em relatório mensal
            3. Acompanhar se há recorrência
            4. Se reincidente: elevar para notificação formal
            """)
    
    with tab4:
        st.markdown("## 📝 Modelo de Notificações")
        
        st.info("""
        **💡 Use o módulo de Notificações do sistema para gerar documentos 
        automaticamente com IA!**
        
        Acesse: Dashboard → Selecione Contrato → Notificar
        """)
        
        st.markdown("### Elementos Obrigatórios de uma Notificação")
        
        st.markdown("""
        Toda notificação contratual deve conter:
        
        1. **Cabeçalho institucional** (TJSP)
        2. **Identificação do contrato** (número, objeto)
        3. **Destinatário** (empresa contratada)
        4. **Descrição clara da irregularidade**
        5. **Fundamentação legal** (cláusula contratual, lei)
        6. **Prazo para regularização**
        7. **Consequências do não atendimento**
        8. **Local, data e assinatura do fiscal**
        9. **Protocolo de envio/recebimento**
        """)
        
        st.markdown("### Prazos Recomendados")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Irregularidade Leve", "5 dias úteis")
        
        with col2:
            st.metric("Irregularidade Média", "3 dias úteis")
        
        with col3:
            st.metric("Irregularidade Grave", "24-48 horas")
    
    with tab5:
        st.markdown("## 📚 Base Legal e Normativa")
        
        st.markdown("### Legislação Aplicável")
        
        with st.expander("📜 Lei nº 8.666/1993"):
            st.markdown("""
            **Lei de Licitações e Contratos Administrativos**
            
            Principais artigos para fiscalização:
            - Art. 67: Da fiscalização e acompanhamento
            - Art. 77: Inexecução total ou parcial
            - Art. 78: Motivos de rescisão
            - Art. 87: Penalidades aplicáveis
            - Art. 88: Sanções previstas
            """)
        
        with st.expander("📜 Lei nº 14.133/2021"):
            st.markdown("""
            **Nova Lei de Licitações**
            
            Principais artigos:
            - Art. 117: Fiscalização técnica, administrativa e setorial
            - Art. 137: Inexecução contratual
            - Art. 155: Penalidades e sanções
            - Art. 156: Sanções administrativas
            """)
        
        with st.expander("📋 Normativas TJSP"):
            st.markdown("""
            **Resoluções e Atos Normativos Internos**
            
            - Resolução CNJ nº XXX/XXXX
            - Provimento CSM nº XXX/XXXX
            - Manual de Gestão de Contratos TJSP
            - Código de Ética do Servidor Público
            
            *(Consulte o departamento jurídico para normativas atualizadas)*
            """)
        
        st.warning("""
        **⚠️ Importante:** Esta seção contém orientações gerais. 
        Em caso de dúvidas, consulte sempre o departamento jurídico 
        e o gestor do contrato.
        """)
    
    # Rodapé
    st.markdown("---")
    st.markdown("""
        <div class="tjsp-footer">
            <p>📖 Guia de Procedimentos - TJSP</p>
            <p>Para dúvidas, entre em contato com a Coordenadoria de Gestão de Contratos</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
