#!/bin/bash

# =============================================================================
# Script de Setup - Módulo COPILOTO com IA
# =============================================================================
# Instala dependências e valida configuração
# =============================================================================

echo "🚀 Iniciando setup do Módulo COPILOTO com IA..."
echo ""

# -----------------------------------------------------------------------------
# 1. Instalar dependências
# -----------------------------------------------------------------------------
echo "📦 Instalando dependências..."
pip install openai>=1.12.0

if [ $? -eq 0 ]; then
    echo "✅ Biblioteca openai instalada com sucesso"
else
    echo "❌ Erro ao instalar biblioteca openai"
    exit 1
fi

echo ""

# -----------------------------------------------------------------------------
# 2. Verificar estrutura de diretórios
# -----------------------------------------------------------------------------
echo "📁 Verificando estrutura de diretórios..."

if [ ! -d ".streamlit" ]; then
    echo "📁 Criando diretório .streamlit/..."
    mkdir -p .streamlit
fi

if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "⚠️  Arquivo .streamlit/secrets.toml não encontrado"
    echo "💡 Crie o arquivo com base em .streamlit/secrets.toml.example"
    echo ""
    echo "   cp .streamlit/secrets.toml.example .streamlit/secrets.toml"
    echo "   # Depois edite e adicione sua chave OpenAI"
    echo ""
else
    echo "✅ Arquivo .streamlit/secrets.toml encontrado"
fi

echo ""

# -----------------------------------------------------------------------------
# 3. Verificar .gitignore
# -----------------------------------------------------------------------------
echo "🔒 Verificando .gitignore..."

if grep -q ".streamlit/secrets.toml" .gitignore; then
    echo "✅ .streamlit/secrets.toml está no .gitignore"
else
    echo "⚠️  Adicionando .streamlit/secrets.toml ao .gitignore..."
    echo ".streamlit/secrets.toml" >> .gitignore
    echo "✅ Adicionado ao .gitignore"
fi

echo ""

# -----------------------------------------------------------------------------
# 4. Validar arquivos criados
# -----------------------------------------------------------------------------
echo "✅ Validando arquivos implementados..."

arquivos=(
    "services/copiloto_ai_service.py"
    "docs/COPILOTO_IA_IMPLEMENTACAO.md"
    "docs/CONFIGURACAO_CHAVES_API.md"
    "docs/RESUMO_EXECUTIVO_IA.md"
    "services/README_COPILOTO_AI.md"
    ".streamlit/secrets.toml.example"
)

for arquivo in "${arquivos[@]}"; do
    if [ -f "$arquivo" ]; then
        echo "  ✅ $arquivo"
    else
        echo "  ❌ $arquivo (não encontrado)"
    fi
done

echo ""

# -----------------------------------------------------------------------------
# 5. Resumo
# -----------------------------------------------------------------------------
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup concluído!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Próximos passos:"
echo ""
echo "1. Configure sua chave OpenAI:"
echo "   • Copie: cp .streamlit/secrets.toml.example .streamlit/secrets.toml"
echo "   • Edite .streamlit/secrets.toml e adicione sua chave"
echo ""
echo "2. Execute o app:"
echo "   streamlit run Home.py"
echo ""
echo "3. Teste o COPILOTO:"
echo "   • Acesse a página 💬 Copiloto"
echo "   • Selecione um contrato"
echo "   • Faça uma pergunta"
echo ""
echo "📚 Documentação:"
echo "   • Implementação: docs/COPILOTO_IA_IMPLEMENTACAO.md"
echo "   • Configuração: docs/CONFIGURACAO_CHAVES_API.md"
echo "   • Resumo: docs/RESUMO_EXECUTIVO_IA.md"
echo ""
echo "💡 Sem chave configurada? O sistema funcionará em modo padrão!"
echo ""
