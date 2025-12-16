# 🚀 Guia Rápido - Desenvolvedor

## Início Rápido

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar aplicativo
streamlit run app.py

# 3. Executar testes
python -m unittest discover tests -v
```

## Estrutura do Código

### Adicionar Nova Página
```python
# pages/05_📊_Nova_Pagina.py
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from ui.styles import apply_tjsp_styles
from services.session_manager import initialize_session_state

def main():
    st.set_page_config(page_title="TJSP - Nova Página", page_icon="📊")
    apply_tjsp_styles()
    initialize_session_state()
    
    st.title("Nova Página")
    # Seu código aqui

if __name__ == "__main__":
    main()
```

### Adicionar Novo Agente
```python
# agents/novo_agent.py
from typing import Dict

def processar_acao(dados: Dict) -> str:
    """
    Descrição da ação do agente.
    
    Args:
        dados: Dados de entrada
        
    Returns:
        Resultado processado
    """
    # Implementação
    return resultado
```

### Adicionar Novo Serviço
```python
# services/novo_service.py
def funcao_servico(parametro: str) -> Dict:
    """
    Descrição do serviço.
    
    Args:
        parametro: Descrição do parâmetro
        
    Returns:
        Dados processados
    """
    # Implementação
    return resultado
```

## Padrões de Código

### Nomenclatura
- **Arquivos:** `snake_case.py`
- **Classes:** `PascalCase`
- **Funções/Variáveis:** `snake_case`
- **Constantes:** `UPPER_SNAKE_CASE`

### Session State
```python
# Dados estruturados para IA
st.session_state.nome_campos_ai = {}

# Cache/buffer temporário
st.session_state.nome_buffer = ""

# Dados gerais
st.session_state.variavel_normal = valor
```

### CSS Institucional
Sempre usar cores oficiais TJSP:
```python
--tjsp-azul-primario: #003366
--tjsp-azul-secundario: #0066CC
--tjsp-azul-claro: #E6F2FF
--tjsp-dourado: #B8860B
```

## Comandos Úteis

### Git
```bash
# Status
git status

# Commit
git add .
git commit -m "feat: descrição da feature"

# Push
git push origin main
```

### Streamlit
```bash
# Rodar com auto-reload
streamlit run app.py

# Limpar cache
streamlit cache clear

# Ver versão
streamlit --version
```

### Testes
```bash
# Todos os testes
python -m unittest discover tests -v

# Teste específico
python -m unittest tests.test_agents -v

# Um teste específico
python -m unittest tests.test_agents.TestCopilotAgent.test_processar_pergunta_sobre_valor
```

## Debug

### Streamlit Debug
```python
# Exibir dados de session state
st.write("Debug:", st.session_state)

# Exibir variável
st.write(variavel)

# Info, warning, error
st.info("Informação")
st.warning("Aviso")
st.error("Erro")
```

### Python Debug
```python
# Print debug
print(f"Debug: {variavel}")

# Breakpoint
import pdb; pdb.set_trace()
```

## Integração Futura com LLM

### Exemplo OpenAI
```python
# Adicionar em requirements.txt
# openai==1.10.0

import openai

def processar_com_llm(prompt: str, contexto: str) -> str:
    """Processa prompt usando LLM"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": contexto},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
```

## Boas Práticas

### ✅ Fazer
- Comentar código complexo
- Usar type hints
- Documentar funções (docstrings)
- Testar novas funcionalidades
- Seguir padrões institucionais
- Aplicar CSS TJSP em todas as páginas

### ❌ Evitar
- Hardcode de valores
- Código duplicado
- Funções muito longas (>50 linhas)
- Variáveis de um caractere (exceto loops)
- Commits sem mensagem descritiva
- Ignorar testes falhando

## Recursos

### Documentação
- [Streamlit Docs](https://docs.streamlit.io)
- [Python Docs](https://docs.python.org/3/)
- Padrões TJSP: `synapse-next-homologacao`

### Suporte
- Issues: GitHub Issues
- Email: equipe-saab-tech@tjsp.jus.br (fictício)
- Slack: #contrato-regional-ia (fictício)

## Troubleshooting

### Erro: Module not found
```bash
pip install -r requirements.txt
```

### Erro: Port already in use
```bash
streamlit run app.py --server.port 8502
```

### Cache não atualiza
```bash
streamlit cache clear
```

### Importação não funciona
Verificar se `__init__.py` existe nos pacotes.

---

**Mantenha este guia atualizado conforme o projeto evolui!**
