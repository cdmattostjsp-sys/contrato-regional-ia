"""
Serviço de Notificações por Email - SMTP
=========================================
Sistema de envio de emails automáticos para alertas e notificações.

Instituição: TJSP
Projeto: SAAB-Tech / Synapse.IA
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict, Optional
import os


class EmailService:
    """Serviço de envio de emails SMTP"""
    
    def __init__(self):
        """Inicializa o serviço de email com configurações"""
        # Configurações SMTP (em produção, usar variáveis de ambiente)
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.tjsp.jus.br")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "contratos@tjsp.jus.br")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "contratos@tjsp.jus.br")
        self.from_name = "TJSP - Gestão de Contratos"
        
        # Modo mockado para piloto (não envia emails reais)
        self.modo_piloto = os.getenv("EMAIL_MODO_PILOTO", "true").lower() == "true"
        
        # Log de emails enviados
        self.log_envios = []
    
    def enviar_email(
        self,
        destinatarios: List[str],
        assunto: str,
        corpo: str,
        corpo_html: Optional[str] = None,
        cc: Optional[List[str]] = None,
        anexos: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Envia email para destinatários
        
        Args:
            destinatarios: Lista de emails destinatários
            assunto: Assunto do email
            corpo: Corpo do email em texto plano
            corpo_html: Corpo do email em HTML (opcional)
            cc: Lista de emails em cópia (opcional)
            anexos: Lista de anexos (opcional)
        
        Returns:
            Dict com resultado do envio
        """
        
        # Modo piloto: apenas simula o envio
        if self.modo_piloto:
            resultado = {
                'sucesso': True,
                'modo': 'piloto',
                'timestamp': datetime.now().isoformat(),
                'destinatarios': destinatarios,
                'assunto': assunto,
                'mensagem': '📧 Email simulado (Modo Piloto)'
            }
            self.log_envios.append(resultado)
            return resultado
        
        try:
            # Cria mensagem
            msg = MIMEMultipart('alternative')
            msg['Subject'] = assunto
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = ', '.join(destinatarios)
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            
            # Adiciona corpo texto plano
            parte_texto = MIMEText(corpo, 'plain', 'utf-8')
            msg.attach(parte_texto)
            
            # Adiciona corpo HTML se fornecido
            if corpo_html:
                parte_html = MIMEText(corpo_html, 'html', 'utf-8')
                msg.attach(parte_html)
            
            # Conecta ao servidor SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                
                # Autentica se credenciais estiverem configuradas
                if self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                
                # Envia email
                todos_destinatarios = destinatarios + (cc or [])
                server.send_message(msg, self.from_email, todos_destinatarios)
            
            resultado = {
                'sucesso': True,
                'modo': 'producao',
                'timestamp': datetime.now().isoformat(),
                'destinatarios': destinatarios,
                'assunto': assunto,
                'mensagem': '✅ Email enviado com sucesso'
            }
            self.log_envios.append(resultado)
            return resultado
            
        except Exception as e:
            resultado = {
                'sucesso': False,
                'erro': str(e),
                'timestamp': datetime.now().isoformat(),
                'destinatarios': destinatarios,
                'assunto': assunto,
                'mensagem': f'❌ Erro ao enviar email: {str(e)}'
            }
            self.log_envios.append(resultado)
            return resultado
    
    def enviar_alerta_critico(self, alerta: Dict, destinatarios: List[str]) -> Dict:
        """
        Envia notificação de alerta crítico
        
        Args:
            alerta: Dicionário com dados do alerta
            destinatarios: Lista de emails para notificar
        
        Returns:
            Resultado do envio
        """
        contrato_num = alerta.get('contrato_numero', 'N/A')
        tipo_alerta = alerta.get('titulo', 'Alerta')
        descricao = alerta.get('descricao', '')
        
        assunto = f"🔴 ALERTA CRÍTICO - Contrato {contrato_num}"
        
        corpo = f"""
ALERTA CRÍTICO - AÇÃO IMEDIATA NECESSÁRIA
==========================================

Contrato: {contrato_num}
Tipo de Alerta: {tipo_alerta}

Descrição:
{descricao}

Criticidade: ALTA
Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}

---
Este é um alerta automático do Sistema de Gestão de Contratos TJSP.
Acesse o sistema para mais detalhes e ações necessárias.

TJSP - Tribunal de Justiça do Estado de São Paulo
Sistema SAAB-Tech / Synapse.IA
"""
        
        corpo_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #DC3545; color: white; padding: 20px; border-radius: 5px; }}
        .content {{ background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px; }}
        .footer {{ text-align: center; color: #6c757d; font-size: 0.9em; padding: 20px 0; }}
        .badge {{ display: inline-block; padding: 5px 10px; background: #DC3545; 
                  color: white; border-radius: 3px; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🔴 ALERTA CRÍTICO</h2>
            <p>Ação Imediata Necessária</p>
        </div>
        
        <div class="content">
            <p><strong>Contrato:</strong> {contrato_num}</p>
            <p><strong>Tipo:</strong> {tipo_alerta}</p>
            <p><strong>Descrição:</strong></p>
            <p>{descricao}</p>
            <p><span class="badge">CRITICIDADE: ALTA</span></p>
            <p><strong>Data/Hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
        
        <div class="footer">
            <p>Este é um alerta automático do Sistema de Gestão de Contratos TJSP</p>
            <p><strong>TJSP - Tribunal de Justiça do Estado de São Paulo</strong></p>
            <p>Sistema SAAB-Tech / Synapse.IA</p>
        </div>
    </div>
</body>
</html>
"""
        
        return self.enviar_email(
            destinatarios=destinatarios,
            assunto=assunto,
            corpo=corpo,
            corpo_html=corpo_html
        )
    
    def enviar_resumo_semanal(self, contratos: List[Dict], destinatarios: List[str]) -> Dict:
        """
        Envia resumo semanal de contratos
        
        Args:
            contratos: Lista de contratos para incluir no resumo
            destinatarios: Lista de emails para notificar
        
        Returns:
            Resultado do envio
        """
        total_contratos = len(contratos)
        ativos = len([c for c in contratos if c.get('status') == 'ativo'])
        atencao = len([c for c in contratos if c.get('status') == 'atencao'])
        criticos = len([c for c in contratos if c.get('status') == 'critico'])
        
        assunto = f"📊 Resumo Semanal de Contratos - {datetime.now().strftime('%d/%m/%Y')}"
        
        corpo = f"""
RESUMO SEMANAL DE CONTRATOS
============================

Data: {datetime.now().strftime('%d/%m/%Y')}

RESUMO GERAL:
-------------
Total de Contratos: {total_contratos}
✅ Ativos: {ativos}
⚠️ Atenção: {atencao}
🔴 Críticos: {criticos}

{f"CONTRATOS QUE REQUEREM ATENÇÃO ({atencao + criticos}):" if atencao + criticos > 0 else ""}
{'=' * 40}

"""
        
        # Adiciona contratos que requerem atenção
        for c in contratos:
            if c.get('status') in ['atencao', 'critico']:
                status_icon = '🔴' if c.get('status') == 'critico' else '⚠️'
                corpo += f"""
{status_icon} {c.get('numero', 'N/A')}
   Fornecedor: {c.get('fornecedor', 'N/A')}
   Status: {c.get('status', 'N/A').upper()}
   
"""
        
        corpo += f"""
---
Para mais detalhes, acesse o Sistema de Gestão de Contratos.

TJSP - Tribunal de Justiça do Estado de São Paulo
Sistema SAAB-Tech / Synapse.IA
"""
        
        return self.enviar_email(
            destinatarios=destinatarios,
            assunto=assunto,
            corpo=corpo
        )
    
    def enviar_notificacao_contratual(
        self,
        contrato: Dict,
        tipo_notificacao: str,
        destinatarios: List[str],
        corpo_notificacao: str
    ) -> Dict:
        """
        Envia notificação contratual formal
        
        Args:
            contrato: Dados do contrato
            tipo_notificacao: Tipo de notificação
            destinatarios: Emails destinatários
            corpo_notificacao: Corpo da notificação
        
        Returns:
            Resultado do envio
        """
        contrato_num = contrato.get('numero', 'N/A')
        fornecedor = contrato.get('fornecedor', 'N/A')
        
        assunto = f"📝 {tipo_notificacao} - Contrato {contrato_num}"
        
        corpo = f"""
{tipo_notificacao.upper()}
{'=' * 60}

DADOS DO CONTRATO:
------------------
Número: {contrato_num}
Fornecedor: {fornecedor}
Objeto: {contrato.get('objeto', 'N/A')}

NOTIFICAÇÃO:
------------
{corpo_notificacao}

---
Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Sistema: TJSP - Gestão de Contratos Regionais

TJSP - Tribunal de Justiça do Estado de São Paulo
"""
        
        return self.enviar_email(
            destinatarios=destinatarios,
            assunto=assunto,
            corpo=corpo
        )
    
    def obter_log_envios(self) -> List[Dict]:
        """Retorna log de todos os emails enviados"""
        return self.log_envios.copy()
    
    def limpar_log(self):
        """Limpa o log de envios"""
        self.log_envios.clear()


# Instância global do serviço
_email_service = None

def get_email_service() -> EmailService:
    """Retorna instância singleton do serviço de email"""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service
