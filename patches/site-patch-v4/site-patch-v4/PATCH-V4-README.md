# Patch v4 — Hero comprimido + downloads na página de sessão

Este patch faz duas alterações ao site e melhora o script de publicação:

1. **Hero da homepage comprimido**: título em uma linha (com ellipsis se
   exceder), terceiro parágrafo eliminado, espaçamentos reduzidos. O
   cartão da sessão fica visível na primeira vista de ecrã em telas
   comuns.

2. **Downloads na página de sessão**: secção discreta no fim da página
   com `report.md` e `transcript.json` para descarregar.

3. **`publish.py` melhorado**: copia os ficheiros raw para
   `public/sessoes/<slug>/` automaticamente.

## Como aplicar (5 min)

### Passo 1: Substituir ficheiros no site

| Patch | Substituir |
|---|---|
| `index.astro` | `src/pages/index.astro` |
| `[...slug].astro` | `src/pages/sessoes/[...slug].astro` |

### Passo 2: Copiar publish.py melhorado

Há dois caminhos válidos para o `publish.py`. Decide qual prefires:

**Opção A** (recomendada): substitui o que está em `governoai-site/publish.py`
pelo novo. Corres a partir da pasta do projeto Python apontando para
o site.

**Opção B**: copia para `governoai-starter/publish.py` se quiseres ter
o script junto ao orquestrador. Adapta o argumento default `--site` para
apontar para o site.

### Passo 3: Para a sessão #01 que já está publicada

A sessão da reforma laboral já está no site mas os ficheiros raw não
foram copiados para `public/sessoes/`. Para que os botões de download
funcionem nessa primeira sessão, corre:

```bash
# Estás em governoai-starter
mkdir -p ../governoai-site/public/sessoes/2026-05-08-reforma-laboral
cp simulations/2026-05-08-reforma-laboral/report.md \\
   ../governoai-site/public/sessoes/2026-05-08-reforma-laboral/

cp simulations/2026-05-08-reforma-laboral/transcript.json \\
   ../governoai-site/public/sessoes/2026-05-08-reforma-laboral/
```

(Em Windows, substitui `cp` por `copy` e ajusta as barras.)

### Passo 4: Testar localmente

```bash
cd governoai-site
npm run dev
```

Confirma:

- Homepage: hero ocupa menos espaço, cartão da sessão aparece logo abaixo
  sem scroll em laptop de 13"
- Página da sessão: no fim, antes do disclaimer, há secção "Material da
  sessão" com dois botões clicáveis (report.md e transcript.json)
- Clicar nos botões descarrega os ficheiros

### Passo 5: Push

```bash
git add .
git commit -m "v4: hero comprimido + downloads na página de sessão"
git push
```

## Workflow para sessões futuras

A partir de agora, publicar nova sessão é:

```bash
# Em governoai-starter
python orchestrator.py --briefing 2026-05-22-novo-tema

# Copiar tudo para o site automaticamente
python publish.py 2026-05-22-novo-tema \\
    --site ../governoai-site \\
    --titulo "Título da sessão" \\
    --numero 2 \\
    --tema "Habitação"

# Preencher frontmatter no ficheiro criado (5-10 min de leitura editorial)

# Push
cd ../governoai-site
git add . && git commit -m "Sessão #02" && git push
```

## Decisão sobre tamanho do repositório

Cada sessão adiciona ~70 KB ao repositório do site (report.md + transcript.json).
Em 26 sessões anuais isto soma ~2 MB. Não há problema. Quando o repositório
ultrapassar 100 MB (cerca de 7 anos), aí podemos pensar em estratégias
alternativas. Não te preocupes com isso agora.

## Monorepo (raiz `Governo AI`)

Neste layout, o site e o orquestrador estão na mesma pasta: o default de
`--site` no `publish.py` incluído no patch é `.` (directório actual).

```bash
python publish.py 2026-05-22-novo-tema --titulo "…" --numero 2 --tema "…"
```

Os ficheiros em `patches/site-patch-v4/site-patch-v4/` estão alinhados com
o site monorepo: `getCollection('sessoes')` com `id` no frontmatter, rotas
`/partidos` (redirect de `/agentes`), e hero comprimido v4.

## O que NÃO faz este patch

- Não cria página `/sessoes/<slug>/debate` com transcrição renderizada
  (decisão diferida — se vires que pessoas descarregam o JSON com
   frequência, vale a pena fazer essa página)
- Não muda o registo de quaisquer outros ficheiros
- Não toca em ficheiros de agentes
