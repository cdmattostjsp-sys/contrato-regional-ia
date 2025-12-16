"""
Agente de Geração de Notificações
==================================
Gera notificações contratuais formais baseadas em templates e contexto.
"""

from typing import Dict
from datetime import datetime, timedelta


def gerar_notificacao_contratual(contrato: Dict, dados_notificacao: Dict) -> str:
    """
    Gera notificação contratual formal.
    
    IMPORTANTE: Esta é uma implementação mockada para o MVP.
    Em produção, integrar com modelo LLM para geração mais sofisticada.
    
    Args:
        contrato: Dados do contrato
        dados_notificacao: Dados da notificação (tipo, motivo, prazo, etc.)
        
    Returns:
        Notificação formatada
    """
    
    # Calcula data limite para resposta
    data_notificacao = datetime.now()
    data_limite = data_notificacao + timedelta(days=dados_notificacao['prazo'])
    
    # Número de protocolo (mockado)
    numero_protocolo = f"NOT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Template base da notificação
    notificacao = f"""
═══════════════════════════════════════════════════════════════════
                    TRIBUNAL DE JUSTIÇA DO ESTADO DE SÃO PAULO
                          COORDENADORIA REGIONAL - RAJ 10.1
═══════════════════════════════════════════════════════════════════

NOTIFICAÇÃO CONTRATUAL
Protocolo: {numero_protocolo}

Data: {data_notificacao.strftime('%d/%m/%Y')}


DESTINATÁRIO:
{dados_notificacao['destinatario']}


REFERÊNCIA:
Contrato: {contrato['numero']}
Objeto: {contrato['objeto']}
Fiscal: {contrato['fiscal_titular']}


TIPO DE NOTIFICAÇÃO:
{dados_notificacao['tipo']}


MOTIVO:
{dados_notificacao['motivo']}


"""
    
    # Adiciona fundamentação se fornecida
    if dados_notificacao.get('fundamentacao'):
        notificacao += f"""
FUNDAMENTAÇÃO LEGAL:
{dados_notificacao['fundamentacao']}


"""
    else:
        notificacao += """
FUNDAMENTAÇÃO LEGAL:
Em conformidade com a Cláusula 7ª do contrato (Da Fiscalização) e com os 
artigos 67 e 77 da Lei nº 8.666/1993, que estabelecem as obrigações da 
contratada e as competências da fiscalização contratual.


"""
    
    # Adiciona solicitação e prazo
    notificacao += f"""
SOLICITAÇÃO:
A empresa contratada deverá providenciar a regularização da situação descrita
acima, apresentando as devidas justificativas e/ou correções necessárias.


PRAZO PARA ATENDIMENTO:
{dados_notificacao['prazo']} ({"dia útil" if dados_notificacao['prazo'] == 1 else "dias úteis"})
Data limite: {data_limite.strftime('%d/%m/%Y')}


"""
    
    # Adiciona advertências conforme tipo de notificação
    if dados_notificacao['tipo'] == "Notificação Prévia de Penalidade":
        notificacao += """
ADVERTÊNCIA:
O não atendimento desta notificação no prazo estabelecido poderá acarretar a
aplicação das penalidades previstas na Cláusula 6ª do contrato, incluindo:
- Advertência formal
- Multa contratual
- Suspensão temporária de participação em licitações
- Rescisão contratual

"""
    elif dados_notificacao['tipo'] == "Comunicado de Irregularidade":
        notificacao += """
ADVERTÊNCIA:
A persistência da irregularidade apontada implicará na instauração de 
procedimento administrativo para apuração de responsabilidades e eventual
aplicação de sanções contratuais.

"""
    else:
        notificacao += """
OBSERVAÇÕES:
Esta notificação visa exclusivamente a regularização da situação apontada,
garantindo a adequada execução contratual e o interesse público.

"""
    
    # Rodapé institucional
    notificacao += f"""
RESPOSTA:
A resposta a esta notificação deverá ser encaminhada ao fiscal do contrato
por meio dos canais oficiais de comunicação, devidamente protocolada.


═══════════════════════════════════════════════════════════════════

{contrato['fiscal_titular']}
Fiscal Titular do Contrato
RAJ 10.1 - TJSP

{contrato['fiscal_substituto']}
Fiscal Substituto do Contrato
RAJ 10.1 - TJSP

═══════════════════════════════════════════════════════════════════
Este documento foi gerado pelo Sistema de Gestão de Contratos Regionais - TJSP
Protocolo: {numero_protocolo}
Data/Hora: {data_notificacao.strftime('%d/%m/%Y %H:%M:%S')}
═══════════════════════════════════════════════════════════════════
"""
    
    return notificacao


def validar_dados_notificacao(dados: Dict) -> tuple[bool, str]:
    """
    Valida dados antes de gerar notificação.
    
    Args:
        dados: Dados da notificação
        
    Returns:
        Tupla (válido, mensagem_erro)
    """
    if not dados.get('tipo'):
        return False, "Tipo de notificação é obrigatório"
    
    if not dados.get('motivo'):
        return False, "Motivo da notificação é obrigatório"
    
    if not dados.get('prazo') or dados['prazo'] < 1:
        return False, "Prazo deve ser maior que zero"
    
    if not dados.get('destinatario'):
        return False, "Destinatário é obrigatório"
    
    return True, ""


def gerar_historico_notificacao(contrato_id: str, dados_notificacao: Dict) -> Dict:
    """
    Gera registro histórico da notificação para log.
    
    Args:
        contrato_id: ID do contrato
        dados_notificacao: Dados da notificação
        
    Returns:
        Registro estruturado para histórico
    """
    return {
        "timestamp": datetime.now(),
        "contrato_id": contrato_id,
        "tipo": dados_notificacao['tipo'],
        "motivo": dados_notificacao['motivo'],
        "prazo": dados_notificacao['prazo'],
        "status": "gerada",
        "usuario": "Sistema"  # Em produção, pegar do session_state
    }
