"""
Agente Copilot de Contratos
============================
Processa perguntas sobre contratos usando contexto específico.

Padrão: Responde EXCLUSIVAMENTE com base no contrato carregado.
Não inventa informações. Se não souber, admite.

Base de Conhecimento:
- Manual de Contratos TJSP 2025
- Instrução Normativa 12/2025
- Manual de Boas Práticas em Contratações Públicas
"""

from typing import Dict
from datetime import datetime
from pathlib import Path


def processar_pergunta_copilot(pergunta: str, contrato: Dict) -> str:
    """
    Processa pergunta do usuário sobre o contrato.
    
    IMPORTANTE: Esta é uma implementação mockada para o MVP.
    Em produção, integrar com modelo LLM (OpenAI, Azure OpenAI, etc.)
    
    Args:
        pergunta: Pergunta do usuário
        contrato: Dados do contrato
        
    Returns:
        Resposta baseada no contrato
    """
    
    # Normaliza pergunta para análise
    pergunta_lower = pergunta.lower()
    
    # === PERGUNTAS SOBRE VIGÊNCIA E PRAZO ===
    if any(palavra in pergunta_lower for palavra in ["vigência", "prazo", "quando", "até quando", "validade"]):
        return f"""
📅 **Vigência do Contrato**

O contrato **{contrato['numero']}** possui a seguinte vigência:
- **Período:** {contrato['vigencia']}
- **Data de início:** {contrato['data_inicio'].strftime('%d/%m/%Y')}
- **Data de término:** {contrato['data_fim'].strftime('%d/%m/%Y')}

ℹ️ *Fonte: Cláusula 2ª do contrato*
"""
    
    # === PERGUNTAS SOBRE VALOR ===
    elif any(palavra in pergunta_lower for palavra in ["valor", "preço", "quanto", "custo", "orçamento"]):
        return f"""
💰 **Informações Financeiras**

O **{contrato['numero']}** possui:
- **Valor total:** R$ {contrato['valor']:,.2f}
- **Tipo de contratação:** {contrato['tipo']}

ℹ️ *Fonte: Cláusula 3ª do contrato - Do Valor*
"""
    
    # === PERGUNTAS SOBRE FISCALIZAÇÃO ===
    elif any(palavra in pergunta_lower for palavra in ["fiscal", "responsável", "quem", "fiscalização"]):
        return f"""
👥 **Equipe de Fiscalização**

A fiscalização do **{contrato['numero']}** é realizada por:
- **Fiscal Titular:** {contrato['fiscal_titular']}
- **Fiscal Substituto:** {contrato['fiscal_substituto']}

📋 A fiscalização é exercida conforme previsto na Cláusula 7ª do contrato.

ℹ️ *Fonte: Termo de Designação de Fiscais*
"""
    
    # === PERGUNTAS SOBRE OBJETO ===
    elif any(palavra in pergunta_lower for palavra in ["objeto", "qual", "o que", "serviço", "fornecimento"]):
        return f"""
📋 **Objeto do Contrato**

**{contrato['numero']}**
- **Tipo:** {contrato['tipo']}
- **Objeto:** {contrato['objeto']}
- **Contratada:** {contrato['fornecedor']}

ℹ️ *Fonte: Cláusula 1ª do contrato - Do Objeto*
"""
    
    # === PERGUNTAS SOBRE FORNECEDOR/CONTRATADA ===
    elif any(palavra in pergunta_lower for palavra in ["fornecedor", "empresa", "contratada", "fornece"]):
        return f"""
🏢 **Empresa Contratada**

**{contrato['fornecedor']}**

Contrato: {contrato['numero']}
Objeto: {contrato['objeto']}

ℹ️ Para mais informações sobre a contratada, consulte o processo licitatório.
"""
    
    # === PERGUNTAS SOBRE PENDÊNCIAS ===
    elif any(palavra in pergunta_lower for palavra in ["pendência", "problema", "irregularidade", "alerta"]):
        if "pendencias" in contrato and contrato["pendencias"]:
            pendencias_texto = "\n".join([f"- {p}" for p in contrato["pendencias"]])
            ultima_atualizacao = contrato.get('ultima_atualizacao')
            if ultima_atualizacao:
                ultima_atualizacao_str = ultima_atualizacao.strftime('%d/%m/%Y %H:%M')
            else:
                ultima_atualizacao_str = '(data não informada)'
            return f"""
⚠️ **Pendências Identificadas**

O contrato **{contrato['numero']}** possui as seguintes pendências:

{pendencias_texto}

🔔 Recomenda-se notificar a contratada e estabelecer prazo para regularização.

ℹ️ *Fonte: Relatório de fiscalização - Última atualização: {ultima_atualizacao_str}*
"""
        else:
            ultima_atualizacao = contrato.get('ultima_atualizacao')
            if ultima_atualizacao:
                ultima_atualizacao_str = ultima_atualizacao.strftime('%d/%m/%Y %H:%M')
            else:
                ultima_atualizacao_str = '(data não informada)'
            return f"""
✅ **Situação Regular**

O contrato **{contrato['numero']}** não possui pendências registradas no momento.

Status: **{contrato.get('status', 'indefinido').upper()}**

ℹ️ *Última atualização: {ultima_atualizacao_str}*
"""
    
    # === PERGUNTAS SOBRE STATUS ===
    elif any(palavra in pergunta_lower for palavra in ["status", "situação", "como está"]):
        status_msg = {
            "ativo": "✅ O contrato está **ATIVO** e em execução regular.",
            "atencao": "🟡 O contrato requer **ATENÇÃO** - há pontos a serem observados.",
            "critico": "🔴 O contrato está em situação **CRÍTICA** - ação imediata necessária."
        }
        status_val = contrato.get('status', 'indefinido')
        ultima_atualizacao = contrato.get('ultima_atualizacao')
        if ultima_atualizacao:
            ultima_atualizacao_str = ultima_atualizacao.strftime('%d/%m/%Y %H:%M')
        else:
            ultima_atualizacao_str = '(data não informada)'
        return f"""
📊 **Status do Contrato**

{status_msg.get(status_val, 'Status não identificado')}

**{contrato['numero']}**
- Fornecedor: {contrato['fornecedor']}
- Última atualização: {ultima_atualizacao_str}

ℹ️ Para detalhes, acesse a página de visualização do contrato.
"""
    
    # === PERGUNTAS SOBRE DOCUMENTOS ===
    elif any(palavra in pergunta_lower for palavra in ["documento", "arquivo", "anexo", "papelada"]):
        return f"""
📁 **Documentação do Contrato**

O **{contrato['numero']}** possui os seguintes documentos:
- Termo de Referência
- Edital de Licitação
- Proposta da Contratada
- Contrato Assinado
- Garantias Contratuais
- Certidões de Regularidade

📄 Acesse a aba "Documentos" na página do contrato para visualizar todos os arquivos.
"""
    
    # === PERGUNTAS SOBRE CLÁUSULAS ===
    elif any(palavra in pergunta_lower for palavra in ["cláusula", "obrigação", "dever", "direito"]):
        return f"""
📜 **Cláusulas Contratuais**

O **{contrato['numero']}** contém as seguintes cláusulas principais:

1. **Do Objeto** - Define o escopo da contratação
2. **Do Prazo** - Estabelece a vigência
3. **Do Valor** - Define valores e forma de pagamento
4. **Das Obrigações da Contratada** - Lista deveres da empresa
5. **Das Obrigações da Contratante** - Lista deveres do TJSP
6. **Das Penalidades** - Prevê sanções aplicáveis
7. **Da Fiscalização** - Define fiscalização
8. **Da Rescisão** - Estabelece condições de rescisão

📄 Para ler as cláusulas completas, acesse a aba "Cláusulas" na página do contrato.
"""
    
    # === RESPOSTA PADRÃO ===
    else:
        return f"""
🤖 **Entendi sua pergunta sobre o contrato {contrato['numero']}**

Posso fornecer informações sobre:
- 📅 Vigência e prazos
- 💰 Valores e custos
- 👥 Fiscais responsáveis
- 📋 Objeto do contrato
- 🏢 Empresa contratada
- ⚠️ Pendências e irregularidades
- 📊 Status atual
- 📁 Documentos anexados
- 📜 Cláusulas contratuais

**Tente perguntar:**
- "Qual é o prazo de vigência?"
- "Quem são os fiscais responsáveis?"
- "Existem pendências?"
- "Qual o valor do contrato?"

💡 Estou aqui para ajudar com informações específicas deste contrato!

---

📚 **Base de Conhecimento Disponível:**
- Manual de Contratos TJSP 2025
- Instrução Normativa 12/2025
- Manual de Boas Práticas em Contratações

*Consulte a página "Biblioteca" para mais informações sobre os manuais institucionais.*
"""


def extrair_contexto_contrato(contrato: Dict) -> str:
    """
    Extrai contexto estruturado do contrato para uso em prompts.
    
    Args:
        contrato: Dados do contrato
        
    Returns:
        String formatada com contexto do contrato
    """
    contexto = f"""
CONTEXTO DO CONTRATO:
====================
Número: {contrato['numero']}
Tipo: {contrato['tipo']}
Fornecedor: {contrato['fornecedor']}
Objeto: {contrato['objeto']}
Vigência: {contrato['vigencia']}
Valor: R$ {contrato['valor']:,.2f}
Status: {contrato['status']}
Fiscal Titular: {contrato['fiscal_titular']}
Fiscal Substituto: {contrato['fiscal_substituto']}
Última Atualização: {contrato['ultima_atualizacao'].strftime('%d/%m/%Y %H:%M')}
"""
    
    if "pendencias" in contrato and contrato["pendencias"]:
        contexto += "\nPendências:\n"
        for pendencia in contrato["pendencias"]:
            contexto += f"- {pendencia}\n"
    
    return contexto
