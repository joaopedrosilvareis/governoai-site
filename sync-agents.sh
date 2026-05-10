#!/bin/bash
# sync-agents.sh
# Sincroniza os prompts dos agentes do projeto Python para o site Astro.
# Corre antes de cada build se mexeste em algum prompt.
#
# Uso (na raiz do repositório Governo AI):
#   ./sync-agents.sh
#   ./sync-agents.sh /caminho/para/pasta-com-agents

set -e

ORIGEM="${1:-.}/agents"
DESTINO="src/content/agentes"

if [ ! -d "$ORIGEM" ]; then
  echo "❌ Não encontrei $ORIGEM"
  echo "   Uso: ./sync-agents.sh (corre na raiz do repo, com pasta agents/)"
  exit 1
fi

mkdir -p "$DESTINO"

echo "→ A sincronizar prompts de $ORIGEM"
for ficheiro in "$ORIGEM"/*.md; do
  nome=$(basename "$ficheiro")
  cp "$ficheiro" "$DESTINO/$nome"
  echo "  ✓ $nome"
done

echo ""
echo "✓ Sincronizados $(ls $DESTINO/*.md | wc -l | tr -d ' ') prompts."
echo ""
echo "Próximo passo: npm run dev (ou git commit + push)"
