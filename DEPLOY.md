# Guia de Deploy — Governo AI

Passo a passo para passar do "site na minha máquina" para
"governoai.pt está online". Conta com 30-45 minutos na primeira vez,
5 minutos nas seguintes.

## Pré-requisitos

- [ ] Node.js 20+ instalado (https://nodejs.org)
- [ ] Conta GitHub
- [ ] Conta Netlify (cria com login GitHub: https://netlify.com)
- [ ] Domínio governoai.pt registado (já tens)

---

## PARTE 1 — Testar localmente (10 min)

```bash
# 1. Descompacta o zip se ainda não o fizeste
cd governoai-site

# 2. Instala dependências (demora ~1 min na primeira vez)
npm install

# 3. Corre o servidor local
npm run dev
```

Abre **http://localhost:4321** no browser. Devias ver o site com a
sessão de exemplo (reforma laboral). Navega entre páginas, testa em
mobile (Inspect → Toggle device toolbar no Chrome).

Se algo não funcionar, ver "Resolução de problemas" no fim deste guia.

---

## PARTE 2 — Subir para GitHub (10 min)

```bash
# 1. Inicializa repositório git
cd governoai-site
git init
git add .
git commit -m "Setup inicial do site Governo AI"

# 2. Cria repositório no GitHub
# Vai a github.com/new
# Nome: governoai-site
# Privado ou público (recomendo privado para já)
# NÃO inicializes com README, .gitignore ou license

# 3. Liga o repo local ao remoto (substitui USERNAME)
git remote add origin https://github.com/USERNAME/governoai-site.git
git branch -M main
git push -u origin main
```

Vai ao GitHub e confirma que os ficheiros estão lá.

---

## PARTE 3 — Deploy no Netlify (10 min)

1. Vai a https://app.netlify.com → **Add new site → Import an existing project**

2. Conecta com GitHub se ainda não está conectado

3. Escolhe o repositório **governoai-site**

4. Configurações de build (já estão certas pelo `netlify.toml`):
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Deixa tudo como está

5. Carrega em **Deploy site**

6. Espera 1-2 minutos. O Netlify dá-te um URL temporário tipo
   `random-name-12345.netlify.app`

7. Confirma que abre e está tudo bem

---

## PARTE 4 — Domínio personalizado (15 min)

### 4a. No Netlify

1. **Site settings → Domain management → Add custom domain**
2. Escreve `governoai.pt` → Verify → Yes, add domain
3. Repete para `www.governoai.pt`

O Netlify mostra-te os registos DNS que precisas de configurar.

### 4b. No registar do domínio (onde compraste o governoai.pt)

Login no painel do registar (provavelmente PT.SI, NameCheap, GoDaddy
ou similar). Procura **Gestão de DNS** ou **DNS Records**.

Adiciona estes registos:

| Tipo | Nome | Valor |
|------|------|-------|
| A | @ | 75.2.60.5 |
| CNAME | www | apex-loadbalancer.netlify.com |

(Os valores exatos podem variar — usa os que o Netlify te indicar.)

Guarda. **Aguarda 5 minutos a 24h** para propagação DNS (geralmente
30 minutos).

### 4c. Certificado SSL

No Netlify, depois do DNS propagar:
**Domain management → HTTPS → Provision certificate**

Funciona automaticamente. Espera 1-2 minutos.

---

## PARTE 5 — Validar (5 min)

- [ ] https://governoai.pt abre o site
- [ ] https://www.governoai.pt redireciona para governoai.pt
- [ ] Cadeado verde no browser (HTTPS)
- [ ] A sessão de exemplo abre clicando em "Ler sessão completa"
- [ ] Páginas Sobre, Partidos, Arquivo funcionam
- [ ] Em mobile, layout não está partido

---

## Workflow para sessões futuras

A partir daqui, publicar nova sessão é trivial:

```bash
# 1. No projeto Python, corres a sessão
cd governoai-starter
python orchestrator.py --briefing 2026-05-22-novo-tema

# 2. Usa o helper para criar o esqueleto no site
python publish.py 2026-05-22-novo-tema --site ../governoai-site

# 3. Edita o ficheiro novo
# Abre governoai-site/src/content/sessoes/2026-05-22-novo-tema.md
# Preenche os campos TODO no frontmatter

# 4. Pré-visualiza localmente (opcional mas recomendado)
cd ../governoai-site
npm run dev

# 5. Push para publicar
git add .
git commit -m "Sessão #02: novo tema"
git push
```

Em 30-60 segundos, o site está atualizado.

---

## Resolução de problemas

**`npm install` falha** — Atualiza Node.js para versão 20+.
Verifica com `node --version`.

**`npm run dev` não abre** — Outra app pode estar na porta 4321.
Tenta `npm run dev -- --port 4322`.

**Site no Netlify aparece em branco** — Vê os logs do build no
painel Netlify. Tipicamente erro de markdown numa sessão. Corrige o
frontmatter (campos com `:` ou `"` precisam de aspas).

**DNS não propaga** — Espera mais. Em casos raros, pode demorar 24h.
Testa com https://dnschecker.org/ a ver se já viu a tua mudança.

**Imagens do Open Graph não aparecem ao partilhar** — O Facebook/X
fazem cache agressivo. Usa as ferramentas de debug:
- Facebook: https://developers.facebook.com/tools/debug/
- X/Twitter: https://cards-dev.twitter.com/validator

---

## O que tens depois disto

- **governoai.pt** funcional, com SSL, gratuito
- Workflow de publicação em < 5 minutos
- Versionamento via Git (histórico de tudo)
- Zero custos mensais (Netlify Free é mais que suficiente)
- Capacidade de reverter qualquer alteração com 1 comando

Próximo passo natural depois de tudo isto: criar conta de Instagram
e começar a publicar a primeira sessão real.
