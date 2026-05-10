# Patch v2 — Atualização do site

Este patch aplica três correções ao site `governoai-site`:

1. **Página de Agentes enriquecida** com prompts-base completos e
   colapsáveis, mais informação de eleitorado, e secção para
   partidos sem agente próprio (CDS, JPP)
2. **Aritmética parlamentar atualizada** em todas as páginas:
   AD com 91, BE com 1, JPP mencionado, sessão exemplo corrigida
3. **Link Instagram preparado** no footer (comentado, descomentar
   quando criares a conta)

## Como aplicar (5 minutos)

A forma mais rápida é abrir o site no Cursor, copiar este ficheiro
para a raiz do projeto, e pedir ao agente do Cursor:

> "Aplica o patch descrito em PATCH-V2.md ao site"

Em alternativa, manualmente:

### Passo 1: Criar pasta para os prompts dos agentes

```bash
cd governoai-site
mkdir -p src/content/agentes
```

### Passo 2: Sincronizar os prompts do projeto Python

Copia o ficheiro `sync-agents.sh` para a raiz do projeto site
e dá-lhe permissões de execução:

```bash
chmod +x sync-agents.sh
./sync-agents.sh ../governoai-starter
```

Isto copia os 9 ficheiros markdown de `governoai-starter/agents/`
para `governoai-site/src/content/agentes/`. Sempre que mexeres num
prompt no projeto Python, corres este script outra vez antes do
push para o site refletir.

### Passo 3: Substituir ficheiros

| Ficheiro do patch | Substituir |
|---|---|
| `agentes.astro` | `src/pages/agentes.astro` |
| `sobre.astro` | `src/pages/sobre.astro` |
| `Base.astro` | `src/layouts/Base.astro` |
| `2026-05-08-reforma-laboral.md` | `src/content/sessoes/2026-05-08-reforma-laboral.md` |

### Passo 4: Testar localmente

```bash
npm run dev
```

Abre http://localhost:4321/agentes — devias ver as 8 fichas
detalhadas com botão "Ver prompt-base completo" que abre o
ficheiro markdown.

Confirma também:
- Homepage mostra "AD (PSD+CDS)" com 91 deputados
- Página Sobre tem tabela de composição parlamentar atualizada
- Footer não tem link Instagram (está comentado)

### Passo 5: Commit e push

```bash
git add .
git commit -m "v2: aritmética atualizada, prompts públicos na página agentes"
git push
```

## Quando criares a conta de Instagram

Abre `src/layouts/Base.astro`, encontra este bloco:

```astro
{/* Descomentar quando a conta de Instagram estiver criada:
<li><a href="https://instagram.com/governoai" target="_blank" rel="noopener">Instagram</a></li>
*/}
```

Tira os `{/* */}` à volta. Push. Aparece no footer.

## Workflow para sessões futuras

Quando ajustares um prompt de agente no projeto Python:

```bash
# 1. Editas governoai-starter/agents/<partido>.md

# 2. No site, sincronizas os prompts atualizados
cd governoai-site
./sync-agents.sh ../governoai-starter

# 3. Push
git add .
git commit -m "Calibração do agente <partido>"
git push
```

A página de Agentes refletirá automaticamente a nova versão.

## Princípio que isto consagra

**Os prompts são código fonte público do projeto.** Qualquer pessoa
pode auditar como o "Chega" ou o "PCP" são representados. Esta
transparência é a tua melhor defesa contra acusações de manipulação
e o teu maior fator de credibilidade face a jornalistas e
investigadores.
