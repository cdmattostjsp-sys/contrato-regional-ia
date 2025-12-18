"""
Serviço de Tags e Categorização
================================
Gerenciamento de tags personalizadas para contratos.

Instituição: TJSP
Projeto: SAAB-Tech / Synapse.IA
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


# Tags pré-definidas do sistema
TAGS_SISTEMA = [
    {"id": "urgente", "nome": "Urgente", "cor": "#DC3545", "icone": "🔴"},
    {"id": "revisao", "nome": "Revisão", "cor": "#FFC107", "icone": "⚠️"},
    {"id": "renovar", "nome": "Renovar", "cor": "#17A2B8", "icone": "🔄"},
    {"id": "atencao", "nome": "Atenção", "cor": "#FD7E14", "icone": "⚡"},
    {"id": "prioridade", "nome": "Prioridade", "cor": "#E83E8C", "icone": "⭐"},
    {"id": "aguardando", "nome": "Aguardando", "cor": "#6C757D", "icone": "⏳"},
    {"id": "aprovado", "nome": "Aprovado", "cor": "#28A745", "icone": "✅"},
    {"id": "pendente", "nome": "Pendente", "cor": "#FFC107", "icone": "📋"},
]


class TagService:
    """Serviço de gerenciamento de tags"""
    
    def __init__(self):
        self.tags_file = Path("data/tags.json")
        self.contract_tags_file = Path("data/contract_tags.json")
        
        # Garante que o diretório data existe
        self.tags_file.parent.mkdir(exist_ok=True)
        
        # Inicializa arquivos se não existirem
        self._inicializar_arquivos()
    
    def _inicializar_arquivos(self):
        """Inicializa arquivos de tags se não existirem"""
        if not self.tags_file.exists():
            self._salvar_tags(TAGS_SISTEMA)
        
        if not self.contract_tags_file.exists():
            self._salvar_contract_tags({})
    
    def _carregar_tags(self) -> List[Dict]:
        """Carrega lista de tags disponíveis"""
        try:
            with open(self.tags_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return TAGS_SISTEMA.copy()
    
    def _salvar_tags(self, tags: List[Dict]):
        """Salva lista de tags"""
        with open(self.tags_file, 'w', encoding='utf-8') as f:
            json.dump(tags, f, ensure_ascii=False, indent=2)
    
    def _carregar_contract_tags(self) -> Dict:
        """Carrega mapeamento contrato -> tags"""
        try:
            with open(self.contract_tags_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _salvar_contract_tags(self, contract_tags: Dict):
        """Salva mapeamento contrato -> tags"""
        with open(self.contract_tags_file, 'w', encoding='utf-8') as f:
            json.dump(contract_tags, f, ensure_ascii=False, indent=2)
    
    def obter_todas_tags(self) -> List[Dict]:
        """Retorna todas as tags disponíveis"""
        return self._carregar_tags()
    
    def obter_tag_por_id(self, tag_id: str) -> Optional[Dict]:
        """Retorna tag específica por ID"""
        tags = self._carregar_tags()
        return next((t for t in tags if t['id'] == tag_id), None)
    
    def criar_tag(self, nome: str, cor: str, icone: str = "🏷️") -> Dict:
        """
        Cria nova tag customizada
        
        Args:
            nome: Nome da tag
            cor: Cor em hexadecimal (ex: #FF5733)
            icone: Emoji ou ícone (opcional)
        
        Returns:
            Tag criada
        """
        tags = self._carregar_tags()
        
        # Gera ID único
        tag_id = nome.lower().replace(' ', '_')
        contador = 1
        tag_id_original = tag_id
        while any(t['id'] == tag_id for t in tags):
            tag_id = f"{tag_id_original}_{contador}"
            contador += 1
        
        nova_tag = {
            "id": tag_id,
            "nome": nome,
            "cor": cor,
            "icone": icone,
            "customizada": True,
            "criada_em": datetime.now().isoformat()
        }
        
        tags.append(nova_tag)
        self._salvar_tags(tags)
        
        return nova_tag
    
    def atualizar_tag(self, tag_id: str, nome: Optional[str] = None, 
                     cor: Optional[str] = None, icone: Optional[str] = None) -> bool:
        """
        Atualiza uma tag existente
        
        Args:
            tag_id: ID da tag
            nome: Novo nome (opcional)
            cor: Nova cor (opcional)
            icone: Novo ícone (opcional)
        
        Returns:
            True se atualizada, False se não encontrada
        """
        tags = self._carregar_tags()
        
        for tag in tags:
            if tag['id'] == tag_id:
                if nome:
                    tag['nome'] = nome
                if cor:
                    tag['cor'] = cor
                if icone:
                    tag['icone'] = icone
                
                tag['atualizada_em'] = datetime.now().isoformat()
                self._salvar_tags(tags)
                return True
        
        return False
    
    def excluir_tag(self, tag_id: str) -> bool:
        """
        Exclui uma tag customizada
        
        Args:
            tag_id: ID da tag
        
        Returns:
            True se excluída, False se não encontrada ou sistema
        """
        tags = self._carregar_tags()
        
        # Não permite excluir tags do sistema
        tag = next((t for t in tags if t['id'] == tag_id), None)
        if not tag or not tag.get('customizada', False):
            return False
        
        tags = [t for t in tags if t['id'] != tag_id]
        self._salvar_tags(tags)
        
        # Remove das associações com contratos
        contract_tags = self._carregar_contract_tags()
        for contrato_id in contract_tags:
            contract_tags[contrato_id] = [t for t in contract_tags[contrato_id] if t != tag_id]
        self._salvar_contract_tags(contract_tags)
        
        return True
    
    def obter_tags_do_contrato(self, contrato_id: str) -> List[Dict]:
        """
        Retorna tags associadas a um contrato
        
        Args:
            contrato_id: ID do contrato
        
        Returns:
            Lista de tags do contrato
        """
        contract_tags = self._carregar_contract_tags()
        tag_ids = contract_tags.get(contrato_id, [])
        
        todas_tags = self._carregar_tags()
        return [t for t in todas_tags if t['id'] in tag_ids]
    
    def adicionar_tag_ao_contrato(self, contrato_id: str, tag_id: str) -> bool:
        """
        Adiciona tag a um contrato
        
        Args:
            contrato_id: ID do contrato
            tag_id: ID da tag
        
        Returns:
            True se adicionada, False se já existia
        """
        contract_tags = self._carregar_contract_tags()
        
        if contrato_id not in contract_tags:
            contract_tags[contrato_id] = []
        
        if tag_id in contract_tags[contrato_id]:
            return False  # Já existe
        
        contract_tags[contrato_id].append(tag_id)
        self._salvar_contract_tags(contract_tags)
        
        return True
    
    def remover_tag_do_contrato(self, contrato_id: str, tag_id: str) -> bool:
        """
        Remove tag de um contrato
        
        Args:
            contrato_id: ID do contrato
            tag_id: ID da tag
        
        Returns:
            True se removida, False se não encontrada
        """
        contract_tags = self._carregar_contract_tags()
        
        if contrato_id not in contract_tags:
            return False
        
        if tag_id not in contract_tags[contrato_id]:
            return False
        
        contract_tags[contrato_id].remove(tag_id)
        self._salvar_contract_tags(contract_tags)
        
        return True
    
    def definir_tags_do_contrato(self, contrato_id: str, tag_ids: List[str]):
        """
        Define todas as tags de um contrato (substitui existentes)
        
        Args:
            contrato_id: ID do contrato
            tag_ids: Lista de IDs de tags
        """
        contract_tags = self._carregar_contract_tags()
        contract_tags[contrato_id] = tag_ids
        self._salvar_contract_tags(contract_tags)
    
    def obter_contratos_por_tag(self, tag_id: str) -> List[str]:
        """
        Retorna IDs dos contratos que possuem determinada tag
        
        Args:
            tag_id: ID da tag
        
        Returns:
            Lista de IDs de contratos
        """
        contract_tags = self._carregar_contract_tags()
        return [
            contrato_id 
            for contrato_id, tags in contract_tags.items() 
            if tag_id in tags
        ]
    
    def obter_estatisticas_tags(self) -> Dict:
        """
        Retorna estatísticas de uso de tags
        
        Returns:
            Dict com contagem de uso por tag
        """
        contract_tags = self._carregar_contract_tags()
        todas_tags = self._carregar_tags()
        
        estatisticas = {}
        for tag in todas_tags:
            tag_id = tag['id']
            count = sum(1 for tags in contract_tags.values() if tag_id in tags)
            estatisticas[tag_id] = {
                'nome': tag['nome'],
                'cor': tag['cor'],
                'icone': tag['icone'],
                'uso': count
            }
        
        return estatisticas


# Instância singleton
_tag_service = None

def get_tag_service() -> TagService:
    """Retorna instância singleton do serviço de tags"""
    global _tag_service
    if _tag_service is None:
        _tag_service = TagService()
    return _tag_service
