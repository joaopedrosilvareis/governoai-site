# Patch do Orquestrador — Renomear para "Consenso"

Alterações ao projeto `governoai-starter` para que as próximas sessões
saiam do orquestrador já com a nomenclatura "Consenso" em vez de
"Máxima ambição".

## Ficheiro 1: agents/moderador.md

### Procura:

```markdown
### Modo FORCE_UNANIMITY (cenário de máxima ambição)
```

### Substitui por:

```markdown
### Modo FORCE_UNANIMITY (cenário de consenso)
```

### Procura também:

```markdown
Este é exercício de máxima ambição negocial — NÃO é previsão.
Sinaliza-o no início da intervenção: "Em cenário hipotético de
unanimidade, seria preciso que..."
```

### Substitui por:

```markdown
Este é exercício de consenso construtivo — NÃO é previsão.
Sinaliza-o no início da intervenção: "Em cenário hipotético de
consenso, o acordo seria o seguinte..."
```

### Procura no modo REPORT (a secção "## Cenário 2 — Máxima ambição..."):

```markdown
## Cenário 2 — Máxima ambição (todos assinam)
```

### Substitui por:

```markdown
## Cenário 2 — Consenso (todos assinam)
```

E onde aparecer "cenário de máxima ambição" no texto explicativo do
modo REPORT, substituir por "cenário de consenso".

## Ficheiro 2: orchestrator.py

### Procura no dicionário action_prompts (dentro de call_moderator):

```python
"force_unanimity": (
    "Modo FORCE_UNANIMITY. Independentemente da geometria parlamentar, descreve "
    "agora um cenário HIPOTÉTICO onde TODOS os partidos presentes assinam. Para "
    "cada partido, identifica: (a) cedência mais profunda face à posição inicial, "
    "(b) o que receberia em troca, (c) condição-fronteira intransponível. Se algum "
    "partido tem linha vermelha verdadeiramente intransponível, nomeia-o. "
    "Sinaliza desde o início: 'Em cenário hipotético de unanimidade, seria preciso que...'"
),
```

### Substitui por (versão expandida que reforça o construtivismo):

```python
"force_unanimity": (
    "Modo FORCE_UNANIMITY (cenário de consenso). A tua missão é construir "
    "um acordo concreto onde TODOS os partidos presentes assinam. Não é descritivo, "
    "é construtivo — não desistes. Se as posições do tema central não chegam, "
    "expandes o perímetro para outros dossiês.\\n\\n"
    "Para CADA partido, três linhas obrigatórias:\\n"
    "- O que cede no tema central\\n"
    "- O que GANHA dentro do tema central (cedência simétrica do outro lado)\\n"
    "- O que GANHA fora do tema central (moeda de troca de outro dossier, "
    "calendarização vinculativa, símbolo legislativo)\\n\\n"
    "A terceira linha é crítica — os acordos políticos reais raramente "
    "fecham com cedências apenas no tema em discussão. Pensa: pacotes "
    "legislativos paralelos, presidências de comissões, prioridade em "
    "orçamentos setoriais, comissões de inquérito, alterações ao Regimento.\\n\\n"
    "Sinaliza no início: 'Em cenário hipotético de consenso, o acordo seria...'\\n\\n"
    "NUNCA digas 'impossível' ou 'linhas vermelhas tornam isto inviável'. "
    "Se há barreira, encontras a moeda de troca que a contorna. No final, "
    "podes explicar em 1-2 frases o que teria de mudar no contexto político "
    "(crise externa, diretiva europeia, momento eleitoral) para o consenso "
    "se materializar."
),
```

### Procura também a secção do "report":

```python
"## Cenário 2 — Máxima ambição (todos assinam)\\nMarcar como hipotético. "
"O que cada partido teria de ceder e receber. Linha vermelha intransponível se houver.\\n\\n"
```

### Substitui por:

```python
"## Cenário 2 — Consenso (todos assinam)\\nReproduz a postura construtiva "
"do FORCE_UNANIMITY. Para cada partido: o que cede, o que ganha (dentro e "
"fora do tema). NÃO termines com 'impossível' ou 'linhas vermelhas inviabilizam'. "
"Se há barreira, identifica o que teria de mudar no contexto político. "
"Este é o cenário mais distintivo da simulação — não o comprimas para caber.\\n\\n"
```

## Ficheiro 3 (opcional): agents/moderador.md — limite de tokens

Garante que tens estes valores no topo de `orchestrator.py`:

```python
MAX_TOKENS_AGENT = 600
MAX_TOKENS_MODERATOR = 4000
MAX_TOKENS_REPORT = 5000
```

Se já fizeste o ajuste anterior (2000 → 4000 para o moderador), o
`MAX_TOKENS_REPORT` pode também precisar de subir para 5000 com a
nova estrutura mais densa do cenário 2.

## Validar

Corre uma nova sessão:

```bash
python orchestrator.py --briefing 2026-05-08-reforma-laboral
```

No relatório gerado, o cenário 2 deve:

1. Chamar-se "Consenso" (não "Máxima ambição")
2. Para cada partido, ter cedência + 2 ganhos (dentro e fora do tema)
3. NÃO terminar com "impossível" ou "intransponível"
4. Terminar com 1-2 frases sobre o contexto político que tornaria
   o consenso possível
