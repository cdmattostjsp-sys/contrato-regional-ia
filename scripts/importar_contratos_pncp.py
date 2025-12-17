"""
Script de Importação de Contratos do PNCP
==========================================
Importa contratos do Excel exportado do BI do PNCP para o sistema.

Uso:
    python scripts/importar_contratos_pncp.py
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime


def limpar_valor(valor):
    """Converte valor para float, tratando None e NaN"""
    if pd.isna(valor) or valor is None:
        return 0.0
    return float(valor)


def extrair_comarca_objeto(objeto):
    """Tenta extrair comarca do objeto do contrato"""
    # Padrões comuns: "RAJ X", "comarca de X", etc
    import re
    
    # Procura por RAJ
    raj_match = re.search(r'RAJ\s*(\d+)', objeto, re.IGNORECASE)
    if raj_match:
        return f"RAJ {raj_match.group(1)}"
    
    # Procura por nome de comarca
    comarca_match = re.search(r'comarca[s]?\s+(?:de\s+)?([A-ZÀ-Ú][a-zà-ú\s]+)', objeto, re.IGNORECASE)
    if comarca_match:
        return comarca_match.group(1).strip()
    
    return "Não especificada"


def importar_contratos_pncp():
    """
    Importa contratos do Excel do PNCP para o sistema
    """
    print("=" * 70)
    print("IMPORTAÇÃO DE CONTRATOS DO PNCP")
    print("=" * 70)
    
    # Caminhos
    excel_path = Path("data/importacao/contratos_pncp.xlsx")
    json_path = Path("data/contratos_cadastrados.json")
    
    # Lê Excel (pula 2 primeiras linhas de cabeçalho)
    print(f"\n📂 Lendo arquivo: {excel_path}")
    df = pd.read_excel(excel_path, skiprows=2)
    print(f"✅ {len(df)} registros encontrados")
    
    # Filtra apenas contratos vigentes (não revogados/anulados)
    print("\n🔍 Filtrando contratos vigentes...")
    df_vigentes = df[df['Situação'] == 'Divulgada no PNCP'].copy()
    print(f"✅ {len(df_vigentes)} contratos vigentes")
    print(f"❌ {len(df) - len(df_vigentes)} contratos excluídos (revogados/anulados)")
    
    # Carrega contratos já cadastrados (se existirem)
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            contratos_existentes = json.load(f)
        print(f"\n📋 {len(contratos_existentes)} contratos já cadastrados no sistema")
    else:
        contratos_existentes = []
        print("\n📋 Nenhum contrato cadastrado anteriormente")
    
    # Converte para lista de contratos
    print("\n🔄 Convertendo dados do PNCP para formato do sistema...")
    contratos_importados = []
    
    for idx, row in df_vigentes.iterrows():
        # Gera ID único
        controle_pncp = str(row.get('Controle PNCP', '')).replace('/', '_')
        contrato_id = f"PNCP_{controle_pncp}"
        
        # Extrai data de publicação
        data_pub = row.get('Data Publicação PNCP')
        if pd.notna(data_pub):
            if isinstance(data_pub, str):
                data_inicio = datetime.fromisoformat(data_pub)
            else:
                data_inicio = data_pub
        else:
            data_inicio = datetime.now()
        
        # Estima data fim (1 ano após início - ajustar depois manualmente)
        data_fim = datetime(data_inicio.year + 1, data_inicio.month, data_inicio.day)
        
        # Valor (prioriza homologado, senão estimado)
        valor_homologado = limpar_valor(row.get('Soma de Valor Total Homologado'))
        valor_estimado = limpar_valor(row.get('Soma de Valor Total Estimado'))
        valor = valor_homologado if valor_homologado > 0 else valor_estimado
        
        # Extrai informações
        numero = row.get('Nº do Processo', controle_pncp)
        objeto = str(row.get('Objeto da Compra', 'Não especificado'))[:500]  # Limita
        modalidade = str(row.get('Modalidade', 'Não especificada'))
        
        # Tenta extrair comarca
        comarca = extrair_comarca_objeto(objeto)
        
        # Monta contrato
        contrato = {
            "id": contrato_id,
            "numero": f"{numero}",
            "tipo": "Serviços" if "serviço" in objeto.lower() else "Fornecimento",
            "fornecedor": "A definir",  # PNCP não tem fornecedor neste relatório
            "objeto": objeto,
            "vigencia": f"{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}",
            "valor": valor,
            "status": "ativo",
            "data_inicio": data_inicio.isoformat(),
            "data_fim": data_fim.isoformat(),
            "fiscal_titular": "A definir",
            "fiscal_substituto": "A definir",
            "ultima_atualizacao": datetime.now().isoformat(),
            
            # Metadados do PNCP
            "fonte": "PNCP",
            "controle_pncp": row.get('Controle PNCP', ''),
            "modalidade": modalidade,
            "amparo_legal": str(row.get('Amparo Legal', '')),
            "link_pncp": str(row.get('Link Sistema Origem', '')),
            "comarca_detectada": comarca,
            
            # Inicializa sem aditivos
            "aditivos": [],
            "total_aditivos": 0
        }
        
        contratos_importados.append(contrato)
    
    print(f"✅ {len(contratos_importados)} contratos convertidos")
    
    # Combina com contratos existentes (evita duplicação)
    print("\n🔗 Mesclando com contratos existentes...")
    ids_existentes = {c['id'] for c in contratos_existentes}
    novos = [c for c in contratos_importados if c['id'] not in ids_existentes]
    
    todos_contratos = contratos_existentes + novos
    
    print(f"✅ {len(novos)} contratos novos adicionados")
    print(f"⚠️  {len(contratos_importados) - len(novos)} contratos já existiam (não duplicados)")
    
    # Salva JSON
    print(f"\n💾 Salvando em: {json_path}")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(todos_contratos, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Arquivo salvo com {len(todos_contratos)} contratos")
    
    # Estatísticas
    print("\n" + "=" * 70)
    print("📊 ESTATÍSTICAS DA IMPORTAÇÃO")
    print("=" * 70)
    print(f"Total de contratos no sistema: {len(todos_contratos)}")
    print(f"Contratos do PNCP: {len([c for c in todos_contratos if c.get('fonte') == 'PNCP'])}")
    print(f"Contratos cadastrados manualmente: {len([c for c in todos_contratos if c.get('fonte') != 'PNCP'])}")
    
    # Top 5 por valor
    print("\n💰 TOP 5 CONTRATOS POR VALOR:")
    top5 = sorted(novos, key=lambda x: x['valor'], reverse=True)[:5]
    for i, c in enumerate(top5, 1):
        print(f"{i}. {c['numero']}: R$ {c['valor']:,.2f}")
        print(f"   {c['objeto'][:80]}...")
    
    print("\n✅ IMPORTAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)


if __name__ == "__main__":
    importar_contratos_pncp()
