# governoai-site

Site público do projeto Governo AI (governoai.pt). Construído com Astro
e alojado no Netlify. As sessões são ficheiros markdown em
`src/content/sessoes/` que o Astro renderiza automaticamente.

## Pré-requisitos

- Node.js 20 ou superior — descarrega em https://nodejs.org

Para confirmar que tens:

```bash
node --version
```

## Setup local (5 minutos)

```bash
# 1. Entra na pasta
cd governoai-site

# 2. Instala dependências
npm install

# 3. Corre o servidor de desenvolvimento
npm run dev
```

Abre http://localhost:4321 no browser. Vês o site com a sessão de
exemplo já lá.

Sempre que mexeres em ficheiros, o site recarrega sozinho. Para parar,
Ctrl+C no terminal.

## Estrutura

```
governoai-site/
├── src/
│   ├── content/sessoes/        # ← cada sessão é um .md aqui
│   ├── pages/                  # rotas do site
│   │   ├── index.astro         # homepage
│   │   ├── sobre.astro
│   │   ├── agentes.astro
│   │   ├── arquivo.astro
│   │   └── sessoes/[...slug].astro  # template de sessão
│   ├── layouts/Base.astro      # layout comum
│   ├── components/             # componentes reutilizáveis
│   └── styles/global.css       # CSS global
├── public/                     # ficheiros estáticos
├── netlify.toml                # configuração do Netlify
├── astro.config.mjs
└── package.json
```

## Publicar uma nova sessão

1. Corre o orquestrador no projeto Python:
   ```bash
   python orchestrator.py --briefing 2026-05-22-novo-tema
   ```

2. Lê o `report.md` gerado em `simulations/.../`

3. Cria um ficheiro novo em
   `governoai-site/src/content/sessoes/2026-05-22-novo-tema.md`

4. Copia a estrutura do exemplo `2026-05-08-reforma-laboral.md`,
   adaptando frontmatter e conteúdo

5. Localmente, confirma que aparece bem em http://localhost:4321

6. Commit e push:
   ```bash
   git add .
   git commit -m "Sessão #02: novo tema"
   git push
   ```

7. Netlify rebuild automático em ~1 minuto

## Anatomia de uma sessão

Cada `.md` em `src/content/sessoes/` tem duas partes:

### Frontmatter (entre `---`)

Define os dados estruturados que aparecem no cartão de destaque
da homepage e no topo da página de sessão. Campos obrigatórios:
`titulo`, `data`, `numero`, `tema`, `sumario`, `partidos`.

Campos opcionais que enriquecem o cartão de leitura rápida:
`quick_facts`, `posicoes`, `cenarios`, `takeaway`.

### Corpo (markdown depois do `---`)

O relatório completo da sessão. Aparece na página de sessão.
Usa markdown standard: `##`, tabelas, listas, **negrito**, *itálico*.

## Deploy no Netlify

### Primeira vez

1. Cria conta em https://netlify.com (login com GitHub)
2. "Add new site" → "Import an existing project" → escolhe o
   repositório `governoai-site`
3. Aceita as configurações (já estão no `netlify.toml`)
4. Deploy automático

### Domínio personalizado (governoai.pt)

1. No painel Netlify: Site settings → Domain management
2. "Add custom domain" → governoai.pt
3. Configura DNS no teu registar:
   - Registo A: 75.2.60.5 (apex)
   - Registo CNAME: www → o-teu-site.netlify.app

Netlify trata do certificado SSL gratuito automaticamente.

## Comandos úteis

| Comando | Descrição |
|---------|-----------|
| `npm install` | Instala dependências |
| `npm run dev` | Servidor local em http://localhost:4321 |
| `npm run build` | Compila o site para `dist/` |
| `npm run preview` | Pré-visualiza a build local |

## Resolução de problemas

**Erro "command not found: npm"** — instala Node.js em nodejs.org

**Site não atualiza ao guardar** — verifica que estás a guardar em
`src/`, não em `dist/`. Se persistir, Ctrl+C e `npm run dev` outra vez.

**Frontmatter inválido** — campos com texto que tenham `:` ou `"`
precisam de ficar entre aspas. Por exemplo:
`titulo: "Reforma laboral: o pacote chega ao Parlamento"`

**Build falha no Netlify** — tipicamente erro no markdown da sessão
mais recente. Vê os logs do Netlify e corrige o frontmatter.
