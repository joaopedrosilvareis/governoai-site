"""
publish.py — Helper para publicar uma sessão completa no site

Faz três coisas automaticamente:
1. Copia o report.md (formatado, para leitura) para src/content/sessoes/
2. Copia o report.md (cru) para public/sessoes/<slug>/ (download)
3. Copia o transcript.json para public/sessoes/<slug>/ (download)

O teu trabalho continua a ser preencher o frontmatter no ficheiro
criado em src/content/sessoes/. Isso requer leitura editorial do
relatório.

Uso (na raiz do monorepo, site e orquestrador na mesma pasta):
    python publish.py 2026-05-08-reforma-laboral --site .

Ou com path absoluto:
    python publish.py 2026-05-22-novo-tema --site "C:\\...\\Governo AI"
"""

import argparse
import shutil
from datetime import datetime
from pathlib import Path


TEMPLATE = """---
titulo: "{titulo}"
data: {data}
numero: {numero}
tema: "{tema}"
sumario: "TODO: escreve aqui um resumo de 2 frases para a homepage"
desfecho: acordo-provavel  # ou: impasse, consenso
partidos: [psd, chega, ps, il, livre, pcp, pan, be]
quinzenal_link: ""

quick_facts:
  - label: "Em jogo"
    value: "TODO"
  - label: "TODO"
    value: "TODO"
  - label: "Maioria necessária"
    value: "116 de 230 deputados"
  - label: "Quinzenal"
    value: "TODO data · AR"

posicoes:
  - partido: AD
    deputados: 91
    frase: "TODO: 1 frase"
  - partido: Chega
    deputados: 60
    frase: "TODO: 1 frase"
  - partido: PS
    deputados: 58
    frase: "TODO: 1 frase"
  - partido: IL
    deputados: 9
    frase: "TODO: 1 frase"
  - partido: Livre
    deputados: 6
    frase: "TODO: 1 frase"
  - partido: PCP
    deputados: 3
    frase: "TODO: 1 frase"
  - partido: PAN
    deputados: 1
    frase: "TODO: 1 frase"
  - partido: BE
    deputados: 1
    frase: "TODO: 1 frase"

cenarios:
  provavel:
    titulo: "TODO: título curto"
    geometria: "TODO: ex 'AD + PS = 149'"
    sumario: "TODO: 1-2 frases"
    chave: "TODO: pivô da decisão"
  consenso:
    titulo: "TODO: título curto"
    geometria: "230 dep. (hipotético)"
    sumario: "TODO: o que torna o consenso possível"
    chave: "TODO: moeda de troca decisiva"
  impasse:
    titulo: "TODO: título curto"
    geometria: "TODO: ex '< 116 dep.'"
    sumario: "TODO: o que acontece"
    chave: "TODO: quem ganha"

takeaway: "TODO: parágrafo de síntese. Usa <strong>negrito</strong> nas palavras-chave."
---

{conteudo}
"""


def main():
    parser = argparse.ArgumentParser(
        description="Publica uma sessão no site Astro a partir do output do orquestrador."
    )
    parser.add_argument(
        "slug",
        help="Slug da sessão (ex: 2026-05-08-reforma-laboral)",
    )
    parser.add_argument(
        "--site",
        default=".",
        help="Caminho para a raiz do site Astro (default: . , monorepo)",
    )
    parser.add_argument("--titulo", default="TODO: título da sessão")
    parser.add_argument("--numero", type=int, default=1)
    parser.add_argument("--tema", default="TODO")

    args = parser.parse_args()

    sim_dir = Path("simulations") / args.slug
    if not sim_dir.exists():
        print(f"❌ Não encontrei a pasta {sim_dir}")
        print(f"   Correste o orchestrator.py para o briefing '{args.slug}'?")
        return 1

    report_path = sim_dir / "report.md"
    transcript_path = sim_dir / "transcript.json"

    if not report_path.exists():
        print(f"❌ Não encontrei {report_path}")
        return 1

    site_path = Path(args.site).expanduser().resolve()
    if not site_path.exists():
        print(f"❌ Site não encontrado em {site_path}")
        return 1

    try:
        data_str = args.slug[:10]
        datetime.strptime(data_str, "%Y-%m-%d")
    except ValueError:
        data_str = datetime.now().strftime("%Y-%m-%d")
        print(f"⚠️  Slug não começa com YYYY-MM-DD. A usar data de hoje: {data_str}")

    conteudo_report = report_path.read_text(encoding="utf-8")
    output_md = TEMPLATE.format(
        titulo=args.titulo,
        data=data_str,
        numero=args.numero,
        tema=args.tema,
        conteudo=conteudo_report,
    )

    content_dir = site_path / "src" / "content" / "sessoes"
    content_dir.mkdir(parents=True, exist_ok=True)
    md_output = content_dir / f"{args.slug}.md"
    md_output.write_text(output_md, encoding="utf-8")
    print(f"✓ Markdown formatado: {md_output}")

    public_dir = site_path / "public" / "sessoes" / args.slug
    public_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(report_path, public_dir / "report.md")
    print(f"✓ Report para download: {public_dir / 'report.md'}")

    if transcript_path.exists():
        shutil.copy(transcript_path, public_dir / "transcript.json")
        print(f"✓ Transcript para download: {public_dir / 'transcript.json'}")
    else:
        print(f"⚠️  Transcript não encontrado em {transcript_path}, saltado.")

    print()
    print("Próximos passos:")
    print(f"  1. Abre {md_output}")
    print("     Preenche os campos TODO no frontmatter (5-10 min de leitura editorial)")
    print(f"  2. cd {site_path}")
    print("     npm run dev (pré-visualizar)")
    print("  3. git add . && git commit -m 'Sessão #X' && git push")
    return 0


if __name__ == "__main__":
    exit(main())
