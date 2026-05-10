#!/bin/bash
# sync-agents.sh
# Sincroniza os prompts dos agentes do projeto Python para o site Astro.
# Corre antes de cada build se mexeste em algum prompt.
#
# Uso:
#   ./sync-agents.sh /caminho/para/governoai-starter

set -e

ORIGEM="${1:-../governoai-starter}/agents"
DESTINO="src/content/agentes"

if [ ! -d "$ORIGEM" ]; then
  echo "❌ Não encontrei $ORIGEM"
  echo "   Uso: ./sync-agents.sh /caminho/para/governoai-starter"
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
