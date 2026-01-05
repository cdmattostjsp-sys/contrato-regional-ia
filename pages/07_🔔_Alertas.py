"""
Página de Alertas Contratuais
==============================
Sistema automático de alertas baseado em regras de negócio.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import json

sys.path.append(str(Path(__file__).parent.parent))


from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state
from services.contract_service import get_todos_contratos
from services.alert_service import (
    calcular_alertas, 
    get_alertas_por_tipo, 
    get_alertas_por_categoria,
    registrar_resolucao_alerta,
    STATUS_ATIVO,
    STATUS_RESOLVIDO
)
from services.email_service import get_email_service
from services.history_service import log_event
from components.layout_header import render_module_banner


def render_alerta_card(alerta: dict, on_resolvido=None):
    """Renderiza card de alerta individual"""
    
    # Define cores e ícones por tipo
    config_tipos = {
        'critico': {
            'cor': '#DC3545',
            'cor_bg': '#F8D7DA',
            'icone': '🔴',
            'label': 'CRÍTICO'
        },
        'atencao': {
            'cor': '#FFC107',
            'cor_bg': '#FFF3CD',
            'icone': '🟡',
            'label': 'ATENÇÃO'
        },
        'info': {
            'cor': '#17A2B8',
            'cor_bg': '#D1ECF1',
            'icone': '🔵',
            'label': 'INFO'
        }
    }
    
    config = config_tipos.get(alerta.get('tipo', 'info'), config_tipos['info'])
    
    # Container do card
    container = st.container()
    
    with container:
        # Cabeçalho com badges e data
        col_badge, col_data = st.columns([3, 1])
        
        with col_badge:
            st.markdown(
                f"<span style='background: {config['cor']}; color: white; padding: 0.3rem 0.8rem; "
                f"border-radius: 15px; font-size: 0.75rem; font-weight: bold;'>"
                f"{config['icone']} {config['label']}</span>&nbsp;&nbsp;"
                f"<span style='background: #E9ECEF; color: #495057; padding: 0.3rem 0.8rem; "
                f"border-radius: 15px; font-size: 0.75rem; font-weight: bold;'>"
                f"{alerta.get('categoria', 'Geral')}</span>",
                unsafe_allow_html=True
            )
        
        with col_data:
            data_alerta = alerta.get('data_alerta', datetime.now())
            data_formatada = data_alerta.strftime('%d/%m/%Y %H:%M') if isinstance(data_alerta, datetime) else str(data_alerta)
            st.caption(data_formatada)
        
        # Título do alerta
        titulo = alerta.get('titulo', 'Sem título')
        st.markdown(f"### {config['icone']} {titulo}")
        
        # Descrição
        descricao = alerta.get('descricao', 'Sem descrição')
        st.write(descricao)
        
        # Informações do contrato
        contrato_numero = alerta.get('contrato_numero', 'N/A')
        st.caption(f"**Contrato:** {contrato_numero}")
        
        st.markdown("---")
    
    # Botões de ação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Ver Contrato", key=f"ver_{alerta['id']}", use_container_width=True):
            # Busca contrato
            contratos = get_todos_contratos()
            contrato = next((c for c in contratos if c['id'] == alerta['contrato_id']), None)
            if contrato:
                st.session_state.contrato_selecionado = contrato
                st.switch_page("pages/01_📄_Contrato.py")
    
    with col2:
        if st.button("📝 Gerar Notificação", key=f"notif_{alerta['id']}", use_container_width=True):
            contratos = get_todos_contratos()
            contrato = next((c for c in contratos if c['id'] == alerta['contrato_id']), None)
            if contrato:
                st.session_state.contrato_selecionado = contrato
                st.switch_page("pages/03_📝_Notificações.py")
    
    with col3:
        if st.button("✅ Marcar Resolvido", key=f"resolve_{alerta['id']}", use_container_width=True):
            if on_resolvido:
                on_resolvido(alerta['id'])


def load_alertas_resolvidos():
    """
    Carrega alertas resolvidos do arquivo de persistência.
    
    Retorna lista de dicionários com:
    - id: identificador do alerta
    - status: STATUS_RESOLVIDO
    - justificativa: texto da justificativa
    - data: data/hora da resolução
    - usuario: responsável pela resolução
    """
    try:
        with open("data/alertas_resolvidos.json", "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                if not data:
                    return []
                if isinstance(data[0], dict):
                    # Garante que todos tenham status RESOLVIDO
                    for item in data:
                        if 'status' not in item:
                            item['status'] = STATUS_RESOLVIDO
                    return data
                # Se vier lista de IDs (legado), converte para lista de dicts
                return [{
                    "id": id_antigo, 
                    "status": STATUS_RESOLVIDO,
                    "justificativa": "", 
                    "data": "",
                    "usuario": "Sistema"
                } for id_antigo in data if isinstance(id_antigo, str)]
            return []
    except Exception:
        return []

def save_alerta_resolvido(alerta_id):
    # Função não será mais usada diretamente, pois agora exige justificativa
    pass

def main():
    try:
        st.set_page_config(
            page_title="TJSP - Alertas Contratuais",
            page_icon="🔔",
            layout="wide"
        )
        apply_tjsp_styles()
        initialize_session_state()
        # Cabeçalho padronizado institucional
        render_module_banner(
            title="Alertas Contratuais",
            subtitle="Sistema Automático de Monitoramento e Alertas"
        )
        
        # Botão de retorno e configurações
        col_nav1, col_nav2 = st.columns([6, 1])
        
        with col_nav1:
            if st.button("🏛️ Voltar à Home", use_container_width=False):
                st.switch_page("Home.py")
        
        with col_nav2:
            if st.button("⚙️ Configurar Emails", use_container_width=True, type="secondary"):
                st.switch_page("pages/08_⚙️_Configurações.py")
        
        st.markdown("---")
        
        # Carrega contratos e calcula alertas
        with st.spinner("Calculando alertas..."):
            contratos = get_todos_contratos()
            alertas = calcular_alertas(contratos)
            alertas_resolvidos = load_alertas_resolvidos()
            # Lista de ids resolvidos
            ids_resolvidos = set(r["id"] for r in alertas_resolvidos)
            
            # Verifica se deve enviar notificações automáticas
            config_email = st.session_state.get('config_email', {})
            if config_email.get('alertas_criticos', False):
                email_service = get_email_service()
                alertas_criticos = [a for a in alertas if a.get('tipo') == 'critico']
                
                # Verifica alertas não notificados
                alertas_ja_notificados = st.session_state.get('alertas_notificados', set())
                
                for alerta in alertas_criticos:
                    alerta_id = alerta.get('id')
                    if alerta_id not in alertas_ja_notificados:
                        # Envia notificação
                        email_principal = config_email.get('email_principal', '')
                        if email_principal:
                            resultado = email_service.enviar_alerta_critico(
                                alerta=alerta,
                                destinatarios=[email_principal] + config_email.get('emails_copia', [])
                            )
                            
                            if resultado['sucesso']:
                                # Marca como notificado
                                alertas_ja_notificados.add(alerta_id)
                                st.session_state.alertas_notificados = alertas_ja_notificados
    except Exception as e:
        st.error(f"Erro ao carregar página de alertas: {e}")
        import traceback
        st.exception(e)
        return
    
    # Estatísticas de alertas
    contagens = get_alertas_por_tipo(alertas)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🔴 Críticos",
            value=contagens['critico'],
            delta="Requer ação imediata",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="🟡 Atenção",
            value=contagens['atencao'],
            delta="Acompanhamento necessário"
        )
    
    with col3:
        st.metric(
            label="🔵 Informativos",
            value=contagens['info'],
            delta="Monitoramento"
        )
    
    with col4:
        st.metric(
            label="📊 Total de Alertas",
            value=len(alertas),
            delta=f"{len(contratos)} contratos"
        )
    
    st.markdown("---")
    
    # Ação de envio de emails
    if contagens['critico'] > 0:
        col_email1, col_email2 = st.columns([3, 1])
        
        with col_email1:
            st.info(f"📧 {contagens['critico']} alertas críticos podem ser enviados por email")
        
        with col_email2:
            config_email = st.session_state.get('config_email', {})
            email_configurado = config_email.get('email_principal', '')
            
            if email_configurado:
                if st.button("📤 Enviar Alertas por Email", type="primary", use_container_width=True):
                    email_service = get_email_service()
                    alertas_criticos = [a for a in alertas if a.get('tipo') == 'critico']
                    
                    with st.spinner(f"Enviando {len(alertas_criticos)} alertas..."):
                        sucessos = 0
                        for alerta in alertas_criticos:
                            resultado = email_service.enviar_alerta_critico(
                                alerta=alerta,
                                destinatarios=[email_configurado] + config_email.get('emails_copia', [])
                            )
                            if resultado['sucesso']:
                                sucessos += 1
                        
                        if sucessos == len(alertas_criticos):
                            st.success(f"✅ {sucessos} emails enviados com sucesso!")
                        else:
                            st.warning(f"⚠️ {sucessos}/{len(alertas_criticos)} emails enviados")
            else:
                if st.button("⚙️ Configurar Email", use_container_width=True):
                    st.switch_page("pages/08_⚙️_Configurações.py")
    
    st.markdown("---")
    
    # Filtros
    col_filtro1, col_filtro2, col_filtro3 = st.columns([2, 2, 1])
    
    with col_filtro1:
        filtro_tipo = st.selectbox(
            "Filtrar por Tipo",
            ["Todos", "🔴 Críticos", "🟡 Atenção", "🔵 Informativos"],
            key="filtro_tipo_alerta"
        )
    
    with col_filtro2:
        categorias_disponiveis = ["Todas"] + list(get_alertas_por_categoria(alertas).keys())
        filtro_categoria = st.selectbox(
            "Filtrar por Categoria",
            categorias_disponiveis,
            key="filtro_categoria_alerta"
        )
    
    with col_filtro3:
        st.write("")
        st.write("")
        if st.button("🔄 Atualizar", use_container_width=True):
            st.rerun()
    
    # Aplica filtros e oculta resolvidos
    alertas_filtrados = [a for a in alertas if a.get('id') not in ids_resolvidos]

    if filtro_tipo != "Todos":
        tipo_map = {
            "🔴 Críticos": "critico",
            "🟡 Atenção": "atencao",
            "🔵 Informativos": "info"
        }
        tipo_busca = tipo_map.get(filtro_tipo)
        if tipo_busca:
            alertas_filtrados = [a for a in alertas_filtrados if a.get('tipo') == tipo_busca]

    if filtro_categoria != "Todas":
        alertas_filtrados = [a for a in alertas_filtrados if a.get('categoria') == filtro_categoria]

    # Define funções auxiliares antes de usar
    def marcar_resolvido(alerta_id):
        # Abre campo de justificativa obrigatória
        st.session_state["justificando_alerta"] = alerta_id
        st.rerun()

    def salvar_resolvido(alerta_id, justificativa):
        """
        Salva alerta como resolvido e registra evento formal no histórico.
        
        Este é um ATO ADMINISTRATIVO que será rastreado permanentemente.
        """
        from pathlib import Path
        
        # Busca o alerta completo
        alerta_atual = next((a for a in alertas_filtrados if a["id"] == alerta_id), None)
        if not alerta_atual:
            st.error("Alerta não encontrado")
            return
        
        # Busca contrato relacionado
        contratos = get_todos_contratos()
        contrato = next((c for c in contratos if c['id'] == alerta_atual['contrato_id']), None)
        if not contrato:
            st.error("Contrato não encontrado")
            return
        
        # Registra resolução formal
        try:
            usuario = st.session_state.get('usuario_atual', 'Gestor')
            resolucao = registrar_resolucao_alerta(
                alerta=alerta_atual,
                justificativa=justificativa,
                usuario=usuario
            )
            
            # Registra no histórico do contrato (ATO ADMINISTRATIVO FORMAL)
            log_event(
                contract=contrato,
                event_type="RESOLUCAO_ALERTA",
                title=f"Resolução de Alerta: {alerta_atual.get('titulo', 'Sem título')}",
                details=f"Justificativa: {justificativa}",
                source="Sistema de Alertas",
                actor=usuario,
                metadata=resolucao
            )
            
            # Persiste nos alertas resolvidos
            Path("data").mkdir(parents=True, exist_ok=True)
            resolvidos = load_alertas_resolvidos()
            if not any(r.get("id") == alerta_id for r in resolvidos):
                resolvidos.append({
                    "id": alerta_id,
                    "status": STATUS_RESOLVIDO,
                    "justificativa": justificativa,
                    "data": datetime.now().isoformat(timespec="seconds"),
                    "usuario": usuario,
                    "alerta_tipo": alerta_atual.get("tipo"),
                    "alerta_categoria": alerta_atual.get("categoria"),
                    "contrato_numero": alerta_atual.get("contrato_numero")
                })
                with open("data/alertas_resolvidos.json", "w") as f:
                    json.dump(resolvidos, f, indent=2, ensure_ascii=False)
            
            st.session_state.pop("justificando_alerta", None)
            st.rerun()
            
        except Exception as e:
            st.error(f"Erro ao registrar resolução: {e}")
            return

    # Mostra resultados
    st.markdown("---")

    # Verifica se há um alerta sendo justificado
    justificando = st.session_state.get("justificando_alerta")
    
    if justificando:
        # Mostra apenas o formulário de justificativa
        alerta_atual = next((a for a in alertas_filtrados if a["id"] == justificando), None)
        if alerta_atual:
            st.warning(f"⚠️ Resolução de alerta requer justificativa formal")
            st.markdown("---")
            
            # Informações do alerta
            st.markdown(f"### {alerta_atual.get('titulo', 'Alerta')}")
            st.write(alerta_atual.get('descricao', ''))
            st.caption(f"**Contrato:** {alerta_atual.get('contrato_numero', 'N/A')}")
            
            st.markdown("---")
            
            with st.form(f"form_justifica_{justificando}", clear_on_submit=False):
                st.write("**Registro de Ato Administrativo - Resolução de Alerta**")
                st.caption("A justificativa será registrada permanentemente no histórico do contrato.")
                justificativa = st.text_area(
                    "Justificativa da resolução (obrigatória):",
                    placeholder="Descreva as razões administrativas que fundamentam a resolução deste alerta...",
                    height=120,
                    key=f"just_{justificando}",
                    help="Este registro constitui ato administrativo rastreável para fins de auditoria."
                )
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    submitted = st.form_submit_button("✅ Registrar Resolução", type="primary", use_container_width=True)
                with col_btn2:
                    cancelado = st.form_submit_button("❌ Cancelar", use_container_width=True)
                
                if submitted:
                    if not justificativa.strip():
                        st.error("⚠️ A justificativa é obrigatória para registro formal do ato administrativo.")
                    else:
                        salvar_resolvido(justificando, justificativa.strip())
                        st.success("✅ Resolução registrada com sucesso no histórico do contrato!")
                        st.rerun()
                
                if cancelado:
                    st.session_state.pop("justificando_alerta", None)
                    st.rerun()
    else:
        # Mostra lista normal de alertas
        if not alertas_filtrados:
            st.success("✅ Nenhum alerta encontrado com os filtros aplicados!")
        else:
            if len(alertas_filtrados) != len(alertas):
                st.info(f"📊 Exibindo **{len(alertas_filtrados)}** de {len(alertas)} alertas")
            st.markdown("### 📋 Lista de Alertas")
            for alerta in alertas_filtrados:
                render_alerta_card(alerta, on_resolvido=marcar_resolvido)
    
    # Rodapé informativo
    st.markdown("---")
    with st.expander("ℹ️ Sobre o Sistema de Alertas e Governança"):
        st.markdown("""
        ### ⚙️ Sistema Automático de Alertas Contratuais
        
        Este módulo constitui **instrumento de governança administrativa**, 
        com rastreabilidade completa e registro formal de decisões.
        
        ---
        
        #### 🎯 Modelo de Funcionamento
        
        **O sistema APONTA alertas** baseados em regras de negócio pré-estabelecidas:
        
        **🔴 Alertas Críticos:**
        - Vigência inferior a 60 dias
        - Contratos vencidos
        - Status crítico identificado
        
        **🟡 Alertas de Atenção:**
        - Vigência entre 60-120 dias
        - Pendências contratuais identificadas
        
        **🔵 Alertas Informativos:**
        - Contratos de alto valor (> R$ 50 milhões)
        - Notificações gerais de acompanhamento
        
        ---
        
        #### 👤 Decisão Administrativa
        
        **O gestor RESOLVE** cada alerta através de análise e decisão fundamentada.
        
        A resolução de alertas:
        - É sempre uma **decisão humana**
        - Requer **justificativa obrigatória**
        - Identifica o **responsável pela decisão**
        - Registra **data e hora** do ato administrativo
        
        ---
        
        #### 📋 Rastreabilidade
        
        **O sistema REGISTRA** permanentemente cada ato administrativo:
        
        - Todos os alertas resolvidos ficam registrados
        - Justificativas são rastreáveis por auditoria
        - Histórico de decisões fica vinculado ao contrato
        - Eventos são consultáveis no módulo de Histórico
        
        ---
        
        #### 📊 Ações Disponíveis
        
        Para cada alerta identificado:
        - **Ver Contrato**: Acessar informações completas
        - **Gerar Notificação**: Criar documento formal com IA
        - **Marcar Resolvido**: Registrar decisão administrativa formal
        
        ---
        
        #### 🔄 Atualização de Alertas
        
        Os alertas são recalculados automaticamente:
        - A cada acesso à página
        - Ao clicar no botão "🔄 Atualizar"
        - Baseados no estado atual dos contratos
        
        ---
        
        #### 📧 Notificações Automáticas
        
        Quando configurado, alertas críticos podem ser enviados automaticamente 
        por email aos gestores responsáveis.
        
        Configure em: **⚙️ Configurações** → **Notificações por Email**
        """)



if __name__ == "__main__":
    main()
