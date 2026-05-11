"""
publish.py — Helper para publicar uma sessão no site

Cria um esqueleto de ficheiro markdown a partir do report.md gerado
pelo orquestrador. Tens depois de preencher os campos do frontmatter
manualmente (não dá para automatizar tudo — algumas decisões editoriais
são tuas).

Uso (na raiz do repositório, site e orquestrador na mesma pasta):
    python publish.py 2026-05-22-novo-tema --site .

Ou com path absoluto:
    python publish.py 2026-05-22-novo-tema --site /Users/joao/Governo AI
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
partidos: [psd, ps, chega]  # ajustar conforme a sessão
quinzenal_link: ""

# Cartão de leitura rápida na homepage (opcional mas recomendado)
quick_facts:
  - label: "Em jogo"
    value: "TODO"
  - label: "Custo"
    value: "TODO"
  - label: "Maioria necessária"
    value: "116 de 230 deputados"
  - label: "Quinzenal"
    value: "TODO"

posicoes:
  - partido: PSD
    deputados: 89
    frase: "TODO: posição do PSD em uma frase"
  - partido: PS
    deputados: 58
    frase: "TODO: posição do PS em uma frase"

cenarios:
  provavel:
    titulo: "TODO: título curto"
    geometria: "PSD + PS = 147 dep."
    sumario: "TODO: 1-2 frases"
    chave: "TODO: pivô da decisão"
  consenso:
    titulo: "Todos assinam"
    geometria: "230 dep. (hipotético)"
    sumario: "TODO: o que seria preciso"
    chave: "TODO: moeda decisiva / troca entre dossiês"
  impasse:
    titulo: "TODO: título curto"
    geometria: "< 116 dep."
    sumario: "TODO: o que acontece"
    chave: "TODO: quem ganha"

takeaway: "TODO: parágrafo de síntese política. Usa <strong>negrito</strong> nas palavras-chave."
---

{conteudo}
"""


def main():
    parser = argparse.ArgumentParser(
        description="Converte um report.md em sessão pronta para o site Astro"
    )
    parser.add_argument(
        "slug",
        help="Slug da sessão (ex: 2026-05-22-tema)"
    )
    parser.add_argument(
        "--site",
        default=".",
        help="Caminho para a raiz do site Astro (default: . , mesmo repositório)"
    )
    parser.add_argument(
        "--titulo",
        default="TODO: título da sessão",
        help="Título da sessão (preencher depois se omitido)"
    )
    parser.add_argument(
        "--numero",
        type=int,
        default=1,
        help="Número da sessão (default: 1)"
    )
    parser.add_argument(
        "--tema",
        default="TODO",
        help="Tema da sessão (Trabalho, Saúde, etc.)"
    )
    
    args = parser.parse_args()
    
    # Lê o report do orquestrador
    report_path = Path("simulations") / args.slug / "report.md"
    if not report_path.exists():
        print(f"❌ Não encontrei {report_path}")
        print("   Correste o orchestrator.py para este briefing?")
        return 1
    
    conteudo = report_path.read_text(encoding="utf-8")
    
    # Extrai a data do slug (formato: YYYY-MM-DD-tema)
    try:
        data_str = args.slug[:10]
        datetime.strptime(data_str, "%Y-%m-%d")
    except ValueError:
        print(f"⚠️  Slug não começa com YYYY-MM-DD. A usar data de hoje.")
        data_str = datetime.now().strftime("%Y-%m-%d")
    
    # Gera o ficheiro de saída
    output_md = TEMPLATE.format(
        titulo=args.titulo,
        data=data_str,
        numero=args.numero,
        tema=args.tema,
        conteudo=conteudo,
    )
    
    # Escreve no site
    site_path = Path(args.site).expanduser().resolve()
    if not site_path.exists():
        print(f"❌ Site não encontrado em {site_path}")
        return 1
    
    output_path = site_path / "src" / "content" / "sessoes" / f"{args.slug}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output_md, encoding="utf-8")
    
    print(f"✓ Sessão criada em: {output_path}")
    print()
    print("Próximos passos:")
    print("  1. Abre o ficheiro e preenche os campos TODO no frontmatter")
    print("  2. Revê o conteúdo do relatório")
    print(f"  3. cd {site_path} && npm run dev (para pré-visualizar)")
    print("  4. git add, commit, push para publicar")
    return 0


if __name__ == "__main__":
    exit(main())
