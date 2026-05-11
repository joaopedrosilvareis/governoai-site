# Patch v3 — Hero refinado + renomeação "Consenso"

Este patch faz três alterações ao site:

1. **Hero refinado** na homepage: novo título, sub-explicação em três
   parágrafos, sem tag, sem frase em bold.
2. **Logo maior** no navbar (1.4rem → 1.65rem).
3. **Renomeação do cenário 2** de "Máxima ambição" para "Consenso"
   em todos os ficheiros.

## Como aplicar (5 min)

Abre o site no Cursor, copia este zip para a raiz do projeto, e pede
ao agente:

> "Aplica o patch descrito em PATCH-V3-README.md"

Em alternativa, manualmente:

### Substituir 5 ficheiros

| Patch | Substituir |
|---|---|
| `index.astro` | `src/pages/index.astro` |
| `Base.astro` | `src/layouts/Base.astro` |
| `config.ts` | `src/content/config.ts` |
| `SessaoDestaque.astro` | `src/components/SessaoDestaque.astro` |
| `2026-05-08-reforma-laboral.md` | `src/content/sessoes/2026-05-08-reforma-laboral.md` |

### Testar localmente

```bash
npm run dev
```

Confirma:

- Homepage: novo hero com 3 parágrafos
- Logo "Governo AI" no navbar visivelmente maior
- Cartão da sessão: cenário 2 chama-se "Consenso" (não "Máxima ambição")
- Página de sessão: secção "Cenário 2 — Consenso (todos assinam)"

### Push

```bash
git add .
git commit -m "v3: hero refinado, cenário 2 renomeado para consenso"
git push
```

Em 1-2 min está online.

## Importante: sessões futuras

Para as **próximas sessões** saírem do orquestrador já com a nomenclatura
"consenso", há alterações que tens de fazer ao projeto Python
(`governoai-starter`). Ver ficheiro separado `ORQUESTRADOR-PATCH.md`.

Se não aplicares essas alterações, o orquestrador continuará a usar
"máxima ambição" no relatório gerado, e terás de substituir manualmente
ao publicar cada sessão. Não é fim do mundo, mas vale a pena fazer
uma vez.
