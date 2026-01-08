# FASE 3 – Dual Write: Sincronização Automática V1/V2

## Objetivo
Garantir que toda operação de criação, atualização ou ação administrativa realizada no sistema de alertas V1 seja replicada automaticamente no modelo V2, mantendo integridade, rastreabilidade e permitindo auditoria.

---

## Fluxo Técnico

1. **Interceptação de Operações V1**
   - Toda criação/atualização de alerta V1 dispara sincronização para V2
   - Toda ação administrativa registrada no V1 é replicada no V2

2. **Serviço Dual Write**
   - Novo arquivo: `services/dual_write_service.py`
   - Funções principais:
     - `criar_alerta_dual(v1_alert_data)`
     - `atualizar_alerta_dual(v1_alert_id, changes)`
     - `sincronizar_acao_dual(v1_action_data)`
   - Log dedicado: `logs/dual_write.log`

3. **Mapeamento de Campos**
   - Correspondência direta dos campos essenciais
   - Transformação de campos quando necessário
   - Referência cruzada entre IDs V1 e V2

4. **Auditoria e Rollback**
   - Registro detalhado de todas operações dual write
   - Possibilidade de reverter sincronizações em caso de erro

5. **Testes Automatizados**
   - Garantir que cada operação V1 resulta em operação V2 equivalente
   - Testar cenários de falha e rollback

---

## Exemplo de Uso

```python
from services.dual_write_service import criar_alerta_dual

novo_alerta = {
    'contrato_id': '123/2026',
    'titulo': 'Alerta de renovação',
    'descricao': 'Prazo para renovação próximo',
    'prazo': 30,
    'responsavel': 'gestor.silva',
}
criar_alerta_dual(novo_alerta)
```

---

## Pontos de Atenção

- Erros na sincronização V2 não devem bloquear o fluxo V1 (apenas logar)
- Auditoria completa para cada operação
- Rollback manual disponível
- Testes unitários obrigatórios

---

## Glossário

| Termo         | Definição |
|---------------|-----------|
| Dual Write    | Escrita simultânea em dois sistemas |
| Rollback      | Reversão de operação |
| Auditoria     | Registro detalhado de ações |
| Mapeamento    | Correspondência de campos entre modelos |

---

**Status:** Estrutura inicial criada. Pronto para integração e testes.
**Data:** 08/01/2026
