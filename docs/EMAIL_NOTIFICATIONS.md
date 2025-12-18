# 📧 Sistema de Notificações por Email - TJSP

## Visão Geral

Sistema integrado de notificações por email SMTP para alertas contratuais automáticos e manuais.

## 🎯 Funcionalidades Implementadas

### 1. **Configurações de Email** (`pages/08_⚙️_Configurações.py`)

#### 📮 Destinatários
- **Email Principal**: Destinatário primário das notificações
- **Emails em Cópia**: Lista de destinatários secundários (um por linha)

#### 🔔 Alertas Automáticos
- **Alertas Críticos**: Envio imediato quando detectado alerta crítico
- **Alertas de Atenção**: Envio diário agregado (em desenvolvimento)

#### 📊 Resumos Periódicos
- **Resumo Semanal**: Relatório com status de todos os contratos
- **Dia da Semana**: Configurável (Segunda a Sexta)
- **Horário**: Configurável (HH:MM)

#### 🎯 Modos de Operação

**Modo Piloto (Padrão)**
```bash
EMAIL_MODO_PILOTO=true  # Emails simulados, não enviados
```
- ✅ Registra logs de envio
- ✅ Valida lógica de notificações
- ❌ Não envia emails reais
- 💰 Sem custos SMTP

**Modo Produção**
```bash
EMAIL_MODO_PILOTO=false
SMTP_SERVER=smtp.tjsp.jus.br
SMTP_PORT=587
SMTP_USER=contratos@tjsp.jus.br
SMTP_PASSWORD=sua_senha_aqui
FROM_EMAIL=contratos@tjsp.jus.br
```

### 2. **Página de Alertas Integrada** (`pages/07_🔔_Alertas.py`)

#### Notificações Automáticas
- Monitora alertas críticos em tempo real
- Envia email automaticamente se configurado
- Evita duplicação (rastreamento de alertas já notificados)

#### Notificações Manuais
- Botão "📤 Enviar Alertas por Email"
- Envia todos os alertas críticos sob demanda
- Feedback de sucesso/erro por alerta

#### Interface
```
┌─────────────────────────────────────────┐
│ 🏠 Voltar   |   ⚙️ Configurar Emails │
├─────────────────────────────────────────┤
│ 📧 5 alertas críticos podem ser         │
│    enviados por email                   │
│                 [📤 Enviar por Email]   │
└─────────────────────────────────────────┘
```

### 3. **Serviço de Email** (`services/email_service.py`)

#### Classe `EmailService`

##### Métodos Principais

**`enviar_email()`** - Envio genérico
```python
email_service.enviar_email(
    destinatarios=["fiscal@tjsp.jus.br"],
    assunto="Teste",
    corpo="Mensagem em texto plano",
    corpo_html="<p>Mensagem em HTML</p>",  # Opcional
    cc=["copia@tjsp.jus.br"],  # Opcional
    anexos=[]  # Opcional
)
```

**`enviar_alerta_critico()`** - Template para alertas
```python
email_service.enviar_alerta_critico(
    alerta={
        'contrato_numero': '2024/00070406',
        'titulo': 'Vencimento Próximo',
        'descricao': 'Contrato vence em 5 dias'
    },
    destinatarios=["fiscal@tjsp.jus.br"]
)
```

**`enviar_resumo_semanal()`** - Relatório periódico
```python
email_service.enviar_resumo_semanal(
    contratos=lista_contratos,
    destinatarios=["coordenador@tjsp.jus.br"]
)
```

**`enviar_notificacao_contratual()`** - Notificação formal
```python
email_service.enviar_notificacao_contratual(
    contrato=dados_contrato,
    tipo_notificacao="Advertência",
    destinatarios=["fornecedor@empresa.com"],
    corpo_notificacao="Texto da notificação..."
)
```

#### Singleton Pattern
```python
from services.email_service import get_email_service

email_service = get_email_service()  # Sempre a mesma instância
```

#### Histórico e Logs
```python
# Obter histórico de envios
log = email_service.obter_log_envios()

# Limpar histórico
email_service.limpar_log()
```

## 📋 Templates de Email

### Alerta Crítico

**Assunto:** `🔴 ALERTA CRÍTICO - Contrato {numero}`

**HTML:**
- Cabeçalho vermelho (#DC3545)
- Badge de criticidade
- Dados do contrato
- Descrição do alerta
- Rodapé institucional TJSP

### Resumo Semanal

**Assunto:** `📊 Resumo Semanal de Contratos - DD/MM/YYYY`

**Conteúdo:**
- Total de contratos
- Distribuição por status (✅⚠️🔴)
- Lista de contratos que requerem atenção
- Resumo executivo

### Notificação Contratual

**Assunto:** `📝 {Tipo} - Contrato {numero}`

**Conteúdo:**
- Dados completos do contrato
- Corpo da notificação
- Data/hora oficial
- Identificação institucional

## 🧪 Testes

### Interface de Testes (`Configurações > Testar Email`)

#### Tipos de Teste
1. **Email de Teste Simples**: Valida conectividade SMTP
2. **Alerta Crítico (Simulado)**: Testa template de alerta
3. **Resumo Semanal (Simulado)**: Testa relatório com dados reais

#### Resultado
```json
{
  "sucesso": true,
  "modo": "piloto",
  "timestamp": "2025-12-18T10:30:00",
  "destinatarios": ["teste@tjsp.jus.br"],
  "assunto": "...",
  "mensagem": "📧 Email simulado (Modo Piloto)"
}
```

### Histórico de Envios
- Últimos 20 emails na tab "📊 Histórico"
- Status (✅ Sucesso / ❌ Erro)
- Modo (🧪 Piloto / 🚀 Produção)
- Destinatários, assunto, timestamp
- Detalhes de erros se aplicável

## ⚙️ Configuração em Produção

### Variáveis de Ambiente

```bash
# .env ou configuração do sistema
EMAIL_MODO_PILOTO=false
SMTP_SERVER=smtp.tjsp.jus.br
SMTP_PORT=587
SMTP_USER=contratos@tjsp.jus.br
SMTP_PASSWORD=senha_segura_aqui
FROM_EMAIL=contratos@tjsp.jus.br
```

### Segurança

#### ✅ Boas Práticas
- Senhas em variáveis de ambiente (nunca no código)
- TLS/STARTTLS obrigatório (porta 587)
- Autenticação SMTP configurável
- Validação de destinatários

#### ⚠️ Recomendações
- Use conta de serviço dedicada (`contratos@tjsp.jus.br`)
- Configure SPF/DKIM no domínio TJSP
- Implemente rate limiting em produção
- Monitore logs de envio
- Configure whitelist de domínios permitidos

### Servidor SMTP TJSP

**Contato TI TJSP para:**
- Endpoint SMTP institucional
- Credenciais de conta de serviço
- Configuração de firewall/ACL
- Limites de envio (quota)

## 🔄 Fluxo de Notificações Automáticas

```
┌─────────────────────┐
│ Sistema calcula     │
│ alertas a cada      │
│ visualização        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Alertas Críticos    │
│ detectados?         │
└──────────┬──────────┘
           │ Sim
           ▼
┌─────────────────────┐
│ Config email ativa? │
│ Alertas automáticos?│
└──────────┬──────────┘
           │ Sim
           ▼
┌─────────────────────┐
│ Alerta já foi       │
│ notificado?         │
└──────────┬──────────┘
           │ Não
           ▼
┌─────────────────────┐
│ 📧 Envia email      │
│ para destinatários  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Marca alerta como   │
│ notificado          │
│ (session_state)     │
└─────────────────────┘
```

## 📊 Métricas e Monitoramento

### Dados Coletados
- Total de emails enviados
- Taxa de sucesso/erro
- Tempo médio de envio
- Destinatários únicos
- Tipos de notificação mais comuns

### Visualização
- Tab "📊 Histórico" em Configurações
- Log detalhado por envio
- Filtros por status, data, tipo

## 🚀 Próximas Melhorias

### Curto Prazo
- [ ] Agendamento de resumos semanais (cron/scheduler)
- [ ] Templates customizáveis de email
- [ ] Anexos em notificações (PDFs, docs)
- [ ] Confirmação de leitura

### Médio Prazo
- [ ] Histórico persistente (banco de dados)
- [ ] Dashboard de estatísticas de envio
- [ ] Integração com Microsoft Teams
- [ ] Notificações push (mobile)

### Longo Prazo
- [ ] Sistema de filas (Celery/RQ)
- [ ] Retry automático em falhas
- [ ] Templates com editor visual
- [ ] Multi-idioma (PT/EN)

## 💡 Exemplos de Uso

### 1. Configurar Email ao Iniciar Sistema
```python
# Usuário acessa: Configurações > Notificações Email
# Define: fiscal@tjsp.jus.br como email principal
# Ativa: Alertas Críticos Automáticos
# Salva configurações
```

### 2. Receber Alerta Automático
```python
# Sistema detecta: Contrato vence em 3 dias (crítico)
# Verifica: Config ativa + Email configurado
# Envia: Email com template de alerta crítico
# Marca: Alerta como notificado (evita duplicação)
```

### 3. Enviar Alertas Manualmente
```python
# Usuário acessa: Alertas > 📤 Enviar Alertas
# Sistema: Envia todos os alertas críticos
# Feedback: "✅ 5 emails enviados com sucesso!"
```

### 4. Testar Configuração
```python
# Usuário acessa: Configurações > Testar Email
# Escolhe: "Alerta Crítico (Simulado)"
# Resultado: Email simulado registrado no histórico
```

## 📚 Referências

- [Python smtplib](https://docs.python.org/3/library/smtplib.html)
- [Email MIME](https://docs.python.org/3/library/email.mime.html)
- [Streamlit Session State](https://docs.streamlit.io/library/api-reference/session-state)

## 🆘 Troubleshooting

### Erro: "Connection refused"
- Verifique `SMTP_SERVER` e `SMTP_PORT`
- Confirme firewall/ACL permite conexão

### Erro: "Authentication failed"
- Valide `SMTP_USER` e `SMTP_PASSWORD`
- Confirme conta de serviço ativa

### Emails não chegam
- Verifique `EMAIL_MODO_PILOTO=false`
- Confira spam/lixeira do destinatário
- Valide SPF/DKIM do domínio

### Duplicação de alertas
- Sistema usa `st.session_state.alertas_notificados`
- Limpa ao reiniciar navegador
- Implementar persistência para produção

---

**Desenvolvido para TJSP - Tribunal de Justiça de São Paulo**  
**Projeto SAAB-Tech / Synapse.IA**  
**Versão 1.0.1 - Dezembro 2025**
