# Plano de Correção: [Título do Bug]

**Gerado:** [data auto-gerada]
**Spec:** `[caminho para spec.yaml]`
**Tipo de Ticket:** Bug
**Severidade:** [critical/high/medium/low]

---

## Resumo do Bug

[Descrição breve do bug e seu impacto]

**Comportamento Atual:** [O que está errado]
**Comportamento Esperado:** [O que deveria acontecer]

---

## Análise da Causa Raiz

### Causa Identificada
[Explicação detalhada do que está causando o bug]

### Localização no Código
- **Arquivo:** `[caminho/para/arquivo.py]`
- **Função/Classe:** `[nome]`
- **Linhas:** [números de linha]

### Por Que Isto Aconteceu
[Explicação de como o bug foi introduzido]

---

## Estratégia de Correção

### Abordagem
[Como o bug será corrigido]

### Mudanças Necessárias

1. **Mudança 1:** [Descrição]
   - Arquivo: `[caminho]`
   - Impacto: [O que esta mudança afeta]

2. **Mudança 2:** [Descrição]
   - Arquivo: `[caminho]`
   - Impacto: [O que esta mudança afeta]

---

## Passos de Implementação

### Passo 1: [Descrição]
**Resultado:** [O que estará corrigido após este passo]

**Detalhes:**
1. [Sub-tarefa 1]
2. [Sub-tarefa 2]

**Validação:**
- [Como verificar que a correção funciona]

---

### Passo 2: [Descrição]
**Resultado:** [O que estará completo]

**Detalhes:**
1. [Sub-tarefa 1]
2. [Sub-tarefa 2]

**Validação:**
- [Como verificar]

---

## Testes de Regressão

### Teste para Reproduzir Bug Original
```python
def test_bug_reproducao():
    """Deve falhar antes da correção, passar depois."""
    # [Passos de reprodução como teste]
    pass
```

### Testes para Casos Relacionados
```python
def test_caso_relacionado_1():
    """Garantir que a correção não quebrou isto."""
    pass
```

---

## Definição de Pronto

- ✅ Bug não pode mais ser reproduzido
- ✅ Testes de regressão passando
- ✅ Sem novos bugs introduzidos
- ✅ Código revisado
- ✅ Testes adicionados para prevenir regressão futura

---

*Gerado pelo comando /plan do Framework CDD*
