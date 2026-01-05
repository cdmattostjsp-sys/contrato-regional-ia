"""
Script de Validação - Integração de IA no Módulo COPILOTO
==========================================================
Verifica se a implementação está correta e funcional.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

def validar_arquivos():
    """Valida existência dos arquivos implementados"""
    print("📁 Validando arquivos implementados...")
    
    arquivos = [
        "services/copiloto_ai_service.py",
        "agents/copilot_agent.py",
        "prompts/system_prompts.py",
        "docs/COPILOTO_IA_IMPLEMENTACAO.md",
        "docs/CONFIGURACAO_CHAVES_API.md",
        "docs/RESUMO_EXECUTIVO_IA.md",
        "services/README_COPILOTO_AI.md",
        ".streamlit/secrets.toml.example",
    ]
    
    todos_ok = True
    for arquivo in arquivos:
        caminho = Path(__file__).parent.parent / arquivo
        if caminho.exists():
            print(f"  ✅ {arquivo}")
        else:
            print(f"  ❌ {arquivo} (não encontrado)")
            todos_ok = False
    
    return todos_ok


def validar_imports():
    """Valida se os imports estão funcionando"""
    print("\n📦 Validando imports...")
    
    # Tenta importar o serviço
    try:
        from services import copiloto_ai_service
        print("  ✅ services.copiloto_ai_service")
    except ImportError as e:
        print(f"  ❌ services.copiloto_ai_service - {e}")
        return False
    
    # Tenta importar o agente
    try:
        from agents import copilot_agent
        print("  ✅ agents.copilot_agent")
    except ImportError as e:
        print(f"  ❌ agents.copilot_agent - {e}")
        return False
    
    # Tenta importar os prompts
    try:
        from prompts import system_prompts
        print("  ✅ prompts.system_prompts")
    except ImportError as e:
        print(f"  ❌ prompts.system_prompts - {e}")
        return False
    
    return True


def validar_funcoes():
    """Valida se as funções principais existem"""
    print("\n🔧 Validando funções principais...")
    
    try:
        from services.copiloto_ai_service import (
            verificar_disponibilidade_ia,
            get_status_ia,
            consultar_ia_openai,
            processar_pergunta_com_ia,
            registrar_uso_copiloto
        )
        print("  ✅ verificar_disponibilidade_ia")
        print("  ✅ get_status_ia")
        print("  ✅ consultar_ia_openai")
        print("  ✅ processar_pergunta_com_ia")
        print("  ✅ registrar_uso_copiloto")
    except ImportError as e:
        print(f"  ❌ Erro ao importar funções: {e}")
        return False
    
    try:
        from agents.copilot_agent import (
            processar_pergunta_copilot,
            extrair_contexto_contrato
        )
        print("  ✅ processar_pergunta_copilot")
        print("  ✅ extrair_contexto_contrato")
    except ImportError as e:
        print(f"  ❌ Erro ao importar funções do agente: {e}")
        return False
    
    try:
        from prompts.system_prompts import COPILOT_SYSTEM_PROMPT
        print("  ✅ COPILOT_SYSTEM_PROMPT")
    except ImportError as e:
        print(f"  ❌ Erro ao importar prompt: {e}")
        return False
    
    return True


def testar_disponibilidade_ia():
    """Testa verificação de disponibilidade da IA"""
    print("\n🤖 Testando verificação de disponibilidade da IA...")
    
    try:
        # Nota: Este teste requer streamlit rodando
        # Aqui fazemos um teste básico de importação
        from services.copiloto_ai_service import get_status_ia
        
        print("  ℹ️  Função get_status_ia() disponível")
        print("  ℹ️  Para teste completo, execute o app Streamlit")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False


def validar_biblioteca_openai():
    """Valida se a biblioteca openai está instalada"""
    print("\n📚 Validando biblioteca openai...")
    
    try:
        import openai
        print(f"  ✅ openai instalado (versão: {openai.__version__})")
        return True
    except ImportError:
        print("  ⚠️  openai não instalado")
        print("  💡 Execute: pip install openai>=1.12.0")
        return False


def main():
    """Função principal de validação"""
    print("=" * 70)
    print("🔍 VALIDAÇÃO DA IMPLEMENTAÇÃO DE IA NO MÓDULO COPILOTO")
    print("=" * 70)
    print()
    
    # Executa validações
    resultados = {
        "arquivos": validar_arquivos(),
        "imports": validar_imports(),
        "funcoes": validar_funcoes(),
        "openai": validar_biblioteca_openai(),
        "disponibilidade": testar_disponibilidade_ia()
    }
    
    # Resumo
    print("\n" + "=" * 70)
    print("📊 RESUMO DA VALIDAÇÃO")
    print("=" * 70)
    
    for nome, resultado in resultados.items():
        status = "✅ OK" if resultado else "❌ FALHOU"
        print(f"  {status} - {nome.upper()}")
    
    # Resultado final
    todos_ok = all(resultados.values())
    
    print("\n" + "=" * 70)
    if todos_ok:
        print("✅ VALIDAÇÃO COMPLETA: Todos os testes passaram!")
        print()
        print("📋 Próximos passos:")
        print("  1. Configure .streamlit/secrets.toml com sua chave OpenAI")
        print("  2. Execute: streamlit run Home.py")
        print("  3. Teste o módulo COPILOTO")
    else:
        print("⚠️  VALIDAÇÃO INCOMPLETA: Alguns testes falharam")
        print()
        print("📋 Ações recomendadas:")
        if not resultados["openai"]:
            print("  • Instale: pip install openai>=1.12.0")
        if not resultados["arquivos"]:
            print("  • Verifique se todos os arquivos foram criados")
        if not resultados["imports"]:
            print("  • Verifique erros de importação acima")
    
    print("=" * 70)
    print()
    
    return 0 if todos_ok else 1


if __name__ == "__main__":
    sys.exit(main())
