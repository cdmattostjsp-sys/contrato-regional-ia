"""
Página de Configurações do Sistema
===================================
Configurações de notificações por email e preferências.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state
from services.email_service import get_email_service
from services.contract_service import get_todos_contratos
from services.alert_service import calcular_alertas


def main():
    st.set_page_config(
        page_title="TJSP - Configurações",
        page_icon="⚙️",
        layout="wide"
    )
    
    apply_tjsp_styles()
    initialize_session_state()
    
    # Cabeçalho padronizado institucional
    from components.layout_header import render_module_banner
    render_module_banner(
        title="Configurações do Sistema",
        subtitle="Notificações por Email e Preferências"
    )
    
    # Tabs de configurações
    tab1, tab2, tab3 = st.tabs(["📧 Notificações Email", "🧪 Testar Email", "📊 Histórico"])
    
    # ===== TAB 1: CONFIGURAÇÕES DE EMAIL =====
    with tab1:
        st.markdown("### 📧 Configurações de Notificações por Email")
        
        # Inicializa configurações no session_state se não existir
        if 'config_email' not in st.session_state:
            st.session_state.config_email = {
                'ativo': True,
                'email_principal': 'fiscal@tjsp.jus.br',
                'emails_copia': [],
                'alertas_criticos': True,
                'alertas_atencao': False,
                'resumo_semanal': True,
                'dia_resumo': 'Segunda-feira',
                'hora_resumo': '08:00'
            }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📮 Emails de Destino")
            
            email_principal = st.text_input(
                "Email Principal",
                value=st.session_state.config_email['email_principal'],
                help="Email principal para receber notificações"
            )
            
            emails_copia = st.text_area(
                "Emails em Cópia (um por linha)",
                value='\n'.join(st.session_state.config_email['emails_copia']),
                height=100,
                help="Outros emails que receberão cópia das notificações"
            )
            
            st.markdown("#### 🔔 Alertas Automáticos")
            
            alertas_criticos = st.checkbox(
                "🔴 Enviar alertas críticos imediatamente",
                value=st.session_state.config_email['alertas_criticos'],
                help="Envia email instantâneo quando houver alerta crítico"
            )
            
            alertas_atencao = st.checkbox(
                "⚠️ Enviar alertas de atenção",
                value=st.session_state.config_email['alertas_atencao'],
                help="Envia email diário com alertas de atenção"
            )
        
        with col2:
            st.markdown("#### 📊 Resumos Periódicos")
            
            resumo_semanal = st.checkbox(
                "📅 Enviar resumo semanal",
                value=st.session_state.config_email['resumo_semanal'],
                help="Envia relatório semanal com status de todos os contratos"
            )
            
            dia_resumo = st.selectbox(
                "Dia do resumo semanal",
                ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"],
                index=0 if st.session_state.config_email['dia_resumo'] == 'Segunda-feira' else 0,
                disabled=not resumo_semanal
            )
            
            hora_resumo = st.time_input(
                "Horário do envio",
                value=datetime.strptime(st.session_state.config_email['hora_resumo'], '%H:%M').time(),
                disabled=not resumo_semanal
            )
            
            st.markdown("#### 🎯 Modo de Operação")
            
            # Verifica modo piloto
            email_service = get_email_service()
            
            if email_service.modo_piloto:
                st.info("""
                    🧪 **Modo Piloto Ativado**
                    
                    Os emails estão sendo simulados (não enviados).
                    Para ativar envio real, configure as variáveis de ambiente:
                    - `EMAIL_MODO_PILOTO=false`
                    - `SMTP_SERVER`
                    - `SMTP_PORT`
                    - `SMTP_USER`
                    - `SMTP_PASSWORD`
                """)
            else:
                st.success("✅ **Modo Produção** - Emails sendo enviados")
        
        # Botão salvar
        st.markdown("---")
        col_save1, col_save2, col_save3 = st.columns([1, 1, 2])
        
        with col_save1:
            if st.button("💾 Salvar Configurações", type="primary", use_container_width=True):
                # Salva configurações
                st.session_state.config_email = {
                    'ativo': True,
                    'email_principal': email_principal,
                    'emails_copia': [e.strip() for e in emails_copia.split('\n') if e.strip()],
                    'alertas_criticos': alertas_criticos,
                    'alertas_atencao': alertas_atencao,
                    'resumo_semanal': resumo_semanal,
                    'dia_resumo': dia_resumo,
                    'hora_resumo': hora_resumo.strftime('%H:%M')
                }
                st.success("✅ Configurações salvas com sucesso!")
                st.rerun()
        
        with col_save2:
            if st.button("🏠 Voltar ao Dashboard", use_container_width=True):
                st.switch_page("Home.py")
    
    # ===== TAB 2: TESTAR EMAIL =====
    with tab2:
        st.markdown("### 🧪 Testar Envio de Email")
        
        st.info("""
            Use esta seção para testar o envio de emails e verificar se as configurações estão corretas.
            Em modo piloto, o email será simulado e registrado no histórico.
        """)
        
        col_test1, col_test2 = st.columns(2)
        
        with col_test1:
            tipo_teste = st.selectbox(
                "Tipo de Teste",
                [
                    "Email de Teste Simples",
                    "Alerta Crítico (Simulado)",
                    "Resumo Semanal (Simulado)"
                ]
            )
            
            email_teste = st.text_input(
                "Email de Destino",
                value=st.session_state.config_email.get('email_principal', 'teste@tjsp.jus.br')
            )
        
        with col_test2:
            st.markdown("#### Resultado do Teste")
            resultado_container = st.empty()
        
        if st.button("📤 Enviar Email de Teste", type="primary"):
            email_service = get_email_service()
            
            with st.spinner("Enviando email de teste..."):
                if tipo_teste == "Email de Teste Simples":
                    resultado = email_service.enviar_email(
                        destinatarios=[email_teste],
                        assunto="🧪 Teste - Sistema TJSP Contratos",
                        corpo=f"""
Este é um email de teste do Sistema de Gestão de Contratos TJSP.

Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Modo: {'Piloto (Simulado)' if email_service.modo_piloto else 'Produção'}

Se você recebeu este email, o sistema está funcionando corretamente.

TJSP - Tribunal de Justiça do Estado de São Paulo
"""
                    )
                
                elif tipo_teste == "Alerta Crítico (Simulado)":
                    alerta_mock = {
                        'contrato_numero': '2024/00070406',
                        'titulo': 'Vencimento Próximo',
                        'descricao': 'Contrato vence em 5 dias. Ação necessária.'
                    }
                    resultado = email_service.enviar_alerta_critico(
                        alerta=alerta_mock,
                        destinatarios=[email_teste]
                    )
                
                else:  # Resumo Semanal
                    contratos = get_todos_contratos()
                    resultado = email_service.enviar_resumo_semanal(
                        contratos=contratos[:10],  # Primeiros 10 para teste
                        destinatarios=[email_teste]
                    )
            
            # Mostra resultado
            with resultado_container:
                if resultado['sucesso']:
                    st.success(f"✅ {resultado['mensagem']}")
                    st.json(resultado)
                else:
                    st.error(f"❌ {resultado['mensagem']}")
                    st.json(resultado)
    
    # ===== TAB 3: HISTÓRICO =====
    with tab3:
        st.markdown("### 📊 Histórico de Emails Enviados")
        
        email_service = get_email_service()
        log = email_service.obter_log_envios()
        
        if log:
            st.info(f"📬 {len(log)} emails registrados nesta sessão")
            
            # Mostra últimos 20
            for idx, envio in enumerate(reversed(log[-20:])):
                with st.expander(
                    f"{envio['timestamp'][:16]} - {envio['assunto'][:50]}...",
                    expanded=idx == 0
                ):
                    col_h1, col_h2 = st.columns(2)
                    
                    with col_h1:
                        st.write("**Status:**", "✅ Sucesso" if envio['sucesso'] else "❌ Erro")
                        st.write("**Modo:**", "🧪 Piloto" if envio.get('modo') == 'piloto' else "🚀 Produção")
                        st.write("**Data/Hora:**", envio['timestamp'])
                    
                    with col_h2:
                        st.write("**Destinatários:**")
                        for dest in envio['destinatarios']:
                            st.write(f"  • {dest}")
                    
                    st.write("**Assunto:**", envio['assunto'])
                    
                    if not envio['sucesso']:
                        st.error(f"**Erro:** {envio.get('erro', 'Desconhecido')}")
            
            if st.button("🗑️ Limpar Histórico"):
                email_service.limpar_log()
                st.success("Histórico limpo!")
                st.rerun()
        else:
            st.info("📭 Nenhum email enviado nesta sessão")


if __name__ == "__main__":
    main()
