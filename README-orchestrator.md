# Governo AI

Simulação quinzenal de governação onde agentes de IA representam os 
partidos com assento parlamentar e debatem o tema da quinzenal seguinte.

## Estrutura do projeto

```
governo-ai/
├── orchestrator.py              # script principal
├── agents/                      # prompts base dos agentes
│   ├── moderador.md
│   ├── psd.md
│   ├── chega.md
│   ├── ps.md
│   ├── il.md
│   ├── livre.md
│   ├── pcp.md
│   ├── pan.md
│   └── be.md
├── briefings/                   # contexto por sessão
│   └── 2026-05-08-reforma-laboral/
│       ├── _context.md          # contexto factual (obrigatório)
│       ├── psd.md               # atualização PSD (opcional)
│       ├── chega.md             # atualização Chega (opcional)
│       └── ...
└── simulations/                 # output gerado (criado automaticamente)
    └── 2026-05-08-reforma-laboral/
        ├── transcript.json
        └── report.md
```

## Instalação

```bash
# 1. Cria o ambiente
python3 -m venv venv
source venv/bin/activate

# 2. Instala dependências
pip install anthropic

# 3. Define a API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

A API key obtém-se em https://console.anthropic.com.

## Workflow quinzenal

### Quinta ou sexta-feira (preparação, ~1h)

1. Decide o tema com base na agenda da quinzenal seguinte 
   (consulta agenda em https://www.parlamento.pt)
2. Cria a pasta de briefing:
   ```bash
   mkdir -p briefings/2026-MM-DD-tema-slug
   ```
3. Escreve `_context.md` com o contexto factual (15-30 min)
4. Para cada partido com posição pública relevante, escreve um 
   ficheiro de atualização (5 min cada). Não precisas de fazer 
   para todos — só para os que têm declarações ou eventos novos.

### Sexta ou sábado (execução, ~10 min)

```bash
# Sessão completa com todos os partidos parlamentares
python orchestrator.py --briefing 2026-05-08-reforma-laboral

# Só com os principais (mais rápido, mais foco)
python orchestrator.py --briefing 2026-05-08-reforma-laboral \
    --parties psd ps chega

# Mais rondas de debate
python orchestrator.py --briefing 2026-05-08-reforma-laboral --rounds 3
```

A sessão demora 5-10 minutos a executar e usa ~30-50 mil tokens 
(custo aproximado: $0.50-1.00 por sessão com Claude Opus 4.7).

### Sábado/domingo (publicação, ~30 min)

1. Lê `simulations/.../report.md` e edita se necessário
2. Copia para o site:
   ```bash
   cp simulations/.../report.md governoai-site/src/content/sessoes/
   ```
3. Adiciona frontmatter ao topo do ficheiro
4. Commit e push — Vercel/Netlify rebuild automático
5. Gera os 5 posts de Instagram a partir do template

## Argumentos do orchestrator

| Argumento | Default | Descrição |
|-----------|---------|-----------|
| `--briefing` | obrigatório | Slug da pasta em `briefings/` |
| `--parties` | todos com assento | Partidos a incluir |
| `--rounds` | 2 | Rondas de debate após posições iniciais |

Partidos válidos: `psd`, `chega`, `ps`, `il`, `livre`, `pcp`, `pan`, `be`.

Nota: por defeito a simulação inclui todos estes partidos (incluindo BE,
com 1 deputada na XVII Legislatura). O `psd` na aritmética representa a
AD (91 lugares PSD+CDS). O JPP (1 deputado) não tem agente próprio.

## Estrutura das fases

Cada sessão executa 7 fases sequenciais:

1. **Open** — moderador apresenta tema
2. **Posições iniciais** — cada partido fala uma vez (ordem da lista)
3. **Probe ×N** — moderador faz perguntas concretas, cada partido responde
4. **Force agreement** — moderador propõe acordo viável (≥116 deputados)
5. **Reação final** — partidos respondem à proposta de acordo
6. **Force unanimity** — moderador desenha cenário hipotético de unanimidade
7. **Report** — moderador produz relatório final com 3 cenários

## Custos estimados

Com Claude Opus 4.7 e configuração default (8 partidos, 2 rondas):
- ~25 chamadas à API por sessão
- ~40k tokens de input, ~10k de output
- Custo: ~$0.75-1.00 por sessão
- 26 sessões/ano (quinzenal): ~$25/ano

## Resolução de problemas

**"Prompt do agente não encontrado"** — verifica que tens todos os 
ficheiros em `agents/` (`moderador.md`, `psd.md`, `chega.md`, etc.)

**"Pasta de briefing não encontrada"** — o slug passado em `--briefing` 
deve corresponder ao nome exato da pasta em `briefings/`

**API rate limits** — se acontecer, aumenta o delay entre chamadas 
adicionando `time.sleep(1)` no orquestrador entre fases

**Output muito longo ou curto** — ajusta `MAX_TOKENS_AGENT`, 
`MAX_TOKENS_MODERATOR` e `MAX_TOKENS_REPORT` no topo do orchestrator.py
