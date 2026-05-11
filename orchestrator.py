"""
Governo AI — Orquestrador
=========================

Executa uma simulação quinzenal de governação onde agentes representam
os partidos com assento parlamentar e o moderador conduz o debate até
produzir três cenários de desfecho.

Uso básico:
    python orchestrator.py --briefing 2026-05-08-reforma-laboral

Uso com seleção de partidos:
    python orchestrator.py --briefing 2026-05-08-reforma-laboral --parties psd ps chega

Estrutura de pastas esperada:
    agents/                          # prompts base dos agentes (.md)
    briefings/<sessao>/_context.md   # contexto factual da sessão
    briefings/<sessao>/<partido>.md  # atualização específica por partido (opcional)
    simulations/<data-slug>/         # output gerado (criado automaticamente)
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parent
# .env primeiro; .env.txt como fallback (Notepad no Windows adiciona .txt ao nome).
load_dotenv(_ROOT / ".env")
load_dotenv(_ROOT / ".env.txt")

import anthropic

# =========================================================================
# CONFIGURAÇÃO
# =========================================================================

MODEL = "claude-opus-4-7"
MAX_TOKENS_AGENT = 600
MAX_TOKENS_MODERATOR = 4000
MAX_TOKENS_REPORT = 5000

ALL_PARTIES = ["psd", "chega", "ps", "il", "livre", "pcp", "pan", "be"]

DEPUTIES = {
    "psd": 91, "chega": 60, "ps": 58, "il": 9,
    "livre": 6, "pcp": 3, "pan": 1, "be": 1,
}

PARTY_NAMES = {
    "psd": "PSD", "chega": "Chega", "ps": "PS", "il": "IL",
    "livre": "Livre", "pcp": "PCP", "pan": "PAN", "be": "BE",
}

# =========================================================================
# CLIENTE ANTHROPIC
# =========================================================================

client = anthropic.Anthropic()  # usa ANTHROPIC_API_KEY do ambiente

# =========================================================================
# CARREGAMENTO DE PROMPTS E BRIEFINGS
# =========================================================================

def load_agent_prompt(party: str, briefing_dir: Path = None) -> str:
    """
    Carrega o prompt base do agente e injeta atualização da sessão se existir.
    """
    base_path = Path("agents") / f"{party}.md"
    if not base_path.exists():
        raise FileNotFoundError(f"Prompt do agente não encontrado: {base_path}")
    
    prompt = base_path.read_text(encoding="utf-8")
    
    if briefing_dir:
        update_path = briefing_dir / f"{party}.md"
        if update_path.exists():
            prompt += "\n\n## Atualização desta sessão\n\n" + update_path.read_text(encoding="utf-8")
    
    return prompt


def load_moderator_prompt() -> str:
    path = Path("agents") / "moderador.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt do moderador não encontrado: {path}")
    return path.read_text(encoding="utf-8")


def load_session_context(briefing_dir: Path) -> str:
    """Carrega o contexto factual da sessão."""
    path = briefing_dir / "_context.md"
    if not path.exists():
        raise FileNotFoundError(f"Contexto da sessão não encontrado: {path}")
    return path.read_text(encoding="utf-8")


# =========================================================================
# FORMATAÇÃO DA TRANSCRIÇÃO
# =========================================================================

def format_transcript(transcript: list, last_n: int = None) -> str:
    """
    Formata a transcrição como texto coeso para passar aos agentes.
    Se last_n for fornecido, devolve apenas as últimas N intervenções.
    """
    items = transcript[-last_n:] if last_n else transcript
    blocks = []
    for entry in items:
        role = entry["role"]
        label = "MODERADOR" if role == "moderador" else PARTY_NAMES.get(role, role.upper())
        blocks.append(f"**{label}:**\n{entry['content']}")
    return "\n\n---\n\n".join(blocks)


# =========================================================================
# CHAMADAS À API
# =========================================================================

def call_agent(party: str, context: str, transcript: list, briefing_dir: Path) -> str:
    """Uma intervenção de um agente partidário."""
    system = load_agent_prompt(party, briefing_dir)
    system += f"\n\n## Contexto desta sessão\n\n{context}"
    
    history_text = format_transcript(transcript) if transcript else "(início da sessão)"
    
    user_message = (
        f"## Debate até agora\n\n{history_text}\n\n"
        f"---\n\n"
        f"É a tua vez de intervir como representante do {PARTY_NAMES[party]}. "
        f"Apresenta a tua posição ou reage às intervenções anteriores. "
        f"Sê concreto e específico. Máximo 200 palavras."
    )
    
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS_AGENT,
        system=system,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text.strip()


def call_moderator(context: str, transcript: list, action: str, parties: list) -> str:
    """Intervenção do moderador num dos cinco modos."""
    system = load_moderator_prompt()
    system += f"\n\n## Contexto desta sessão\n\n{context}"
    system += f"\n\n## Partidos presentes nesta sessão\n\n"
    for p in parties:
        system += f"- {PARTY_NAMES[p]}: {DEPUTIES[p]} deputados\n"
    
    action_prompts = {
        "open": (
            "Modo OPEN. Apresenta o tema da sessão em 2-3 parágrafos: contexto factual, "
            "tensões políticas centrais, e convite à primeira ronda dirigido ao partido "
            "que faz mais sentido começar (tipicamente o partido do Governo ou o que tem "
            "posição pública mais nítida sobre o tema)."
        ),
        "probe": (
            "Modo PROBE. Após ouvires todos os partidos, intervém para forçar progresso. "
            "Mapeia as posições agrupando-as. Nomeia a tensão central estrutural. "
            "Faz 2-3 perguntas concretas a partidos específicos — perguntas que exijam "
            "resposta sim/não ou número, não perguntas abertas."
        ),
        "force_agreement": (
            "Modo FORCE_AGREEMENT. Procura agora o acordo viável — a geometria de pelo "
            "menos 116 deputados mais provável dado o que foi dito. Mapeia posições finais. "
            "Apresenta proposta de acordo com aritmética EXPLÍCITA (ex: AD 91 + PS 58 = 149). "
            "Identifica o pivô decisivo e dirige-lhe a pergunta final. Se não houver acordo "
            "possível, regista impasse honestamente — não inventes consensos."
        ),
        "force_unanimity": (
            "Modo FORCE_UNANIMITY (cenário de consenso). Missão: acordo concreto onde "
            "TODOS os partidos presentes assinam; construtivo, não descritivo; expandes "
            "o perímetro a outros dossiês se preciso.\n\n"
            "ORDEM OBRIGATÓRIA: (1) Mapa partido-a-partido PRIMEIRO — para CADA um dos "
            "8 partidos, três linhas concisas: Cede | Ganha no tema | Ganha fora do tema "
            "(moeda de troca). Cobre todos antes de avançar; se faltar espaço, comprime "
            "o passo 2, nunca o mapa. (2) Pacote integrado: 5-8 cláusulas concretas. "
            "(3) O que torna possível: 1-2 frases sobre contexto político.\n\n"
            "Começa SEMPRE com: 'Em cenário hipotético de consenso, o acordo seria o seguinte:'\n"
            "PROIBIDO concluir com 'impossível', 'intransponível', 'inviável' ou "
            "'linha vermelha intransponível' — identifica moeda de troca ou contexto que resolva."
        ),
        "report": (
            "Modo REPORT. Produz agora o relatório final desta sessão, em português, "
            "com 600-800 palavras. Estrutura OBRIGATÓRIA com cabeçalhos markdown:\n\n"
            "# [Título da sessão]\n\n"
            "## Contexto\n2 frases factuais.\n\n"
            "## Posições iniciais\nTabela markdown com colunas: Partido | Deputados | Posição (1 frase).\n\n"
            "## Momento de viragem\n1 parágrafo.\n\n"
            "## Cenário 1 — Acordo provável\nGeometria, descrição (3-5 pontos), cedências, custo político.\n\n"
            "## Cenário 2 — Consenso (todos assinam)\nReproduz a postura construtiva "
            "do FORCE_UNANIMITY. Para cada partido: o que cede, o que ganha (dentro e "
            "fora do tema). NÃO termines com 'impossível' ou 'linhas vermelhas inviabilizam'. "
            "Se há barreira, identifica o que teria de mudar no contexto político. "
            "Este é o cenário mais distintivo da simulação — não o comprimas para caber.\n\n"
            "## Cenário 3 — Impasse\nDescrição, quem ganha politicamente, quem perde.\n\n"
            "## Leitura política\n2-3 frases sobre quem sai mais forte narrativamente.\n\n"
            "## Comparação com o real\nNota fixa de aviso sobre simulação."
        ),
    }
    
    if action not in action_prompts:
        raise ValueError(f"Modo de moderação inválido: {action}")
    
    history_text = format_transcript(transcript) if transcript else "(início da sessão)"
    user_message = f"## Debate até agora\n\n{history_text}\n\n---\n\n{action_prompts[action]}"
    
    max_tokens = MAX_TOKENS_REPORT if action == "report" else MAX_TOKENS_MODERATOR
    
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text.strip()


# =========================================================================
# EXECUÇÃO DA SESSÃO
# =========================================================================

def run_session(briefing_slug: str, parties: list = None, debate_rounds: int = 2) -> dict:
    """
    Executa uma sessão completa e devolve dicionário com transcript e relatório.
    """
    briefing_dir = Path("briefings") / briefing_slug
    if not briefing_dir.exists():
        raise FileNotFoundError(f"Pasta de briefing não encontrada: {briefing_dir}")
    
    context = load_session_context(briefing_dir)
    
    if parties is None:
        parties = ["psd", "chega", "ps", "il", "livre", "pcp", "pan", "be"]  # default com BE
    
    # Validação
    for p in parties:
        if p not in ALL_PARTIES:
            raise ValueError(f"Partido desconhecido: {p}. Válidos: {ALL_PARTIES}")
    
    transcript = []
    
    print(f"\n{'='*60}")
    print(f"  GOVERNO AI — Simulação")
    print(f"  Briefing: {briefing_slug}")
    print(f"  Partidos: {', '.join(PARTY_NAMES[p] for p in parties)}")
    print(f"{'='*60}\n")
    
    # FASE 1: Abertura do moderador
    print("→ Fase 1: Abertura pelo moderador...")
    opening = call_moderator(context, [], "open", parties)
    transcript.append({"role": "moderador", "content": opening, "phase": "open"})
    
    # FASE 2: Posições iniciais (cada partido fala uma vez)
    print("→ Fase 2: Posições iniciais...")
    for party in parties:
        position = call_agent(party, context, transcript, briefing_dir)
        transcript.append({"role": party, "content": position, "phase": "opening_statement"})
        print(f"   ✓ {PARTY_NAMES[party]}")
    
    # FASE 3: Rondas de debate
    for round_num in range(1, debate_rounds + 1):
        print(f"→ Fase 3.{round_num}: Ronda de debate {round_num}...")
        probe = call_moderator(context, transcript, "probe", parties)
        transcript.append({"role": "moderador", "content": probe, "phase": f"probe_{round_num}"})
        
        for party in parties:
            reaction = call_agent(party, context, transcript, briefing_dir)
            transcript.append({"role": party, "content": reaction, "phase": f"debate_{round_num}"})
            print(f"   ✓ {PARTY_NAMES[party]}")
    
    # FASE 4: Tentativa de acordo viável
    print("→ Fase 4: Tentativa de acordo (force_agreement)...")
    agreement = call_moderator(context, transcript, "force_agreement", parties)
    transcript.append({"role": "moderador", "content": agreement, "phase": "force_agreement"})
    
    # FASE 5: Reação final dos partidos ao acordo proposto
    print("→ Fase 5: Reação final ao acordo proposto...")
    for party in parties:
        final = call_agent(party, context, transcript, briefing_dir)
        transcript.append({"role": party, "content": final, "phase": "final_reaction"})
        print(f"   ✓ {PARTY_NAMES[party]}")
    
    # FASE 6: Cenário de consenso (unanimidade construtiva)
    print("→ Fase 6: Cenário de consenso (force_unanimity)...")
    unanimity = call_moderator(context, transcript, "force_unanimity", parties)
    transcript.append({"role": "moderador", "content": unanimity, "phase": "force_unanimity"})
    
    # FASE 7: Relatório final
    print("→ Fase 7: Relatório final...")
    report = call_moderator(context, transcript, "report", parties)
    
    print("\n✓ Sessão concluída.\n")
    
    return {
        "briefing_slug": briefing_slug,
        "parties": parties,
        "context": context,
        "transcript": transcript,
        "report": report,
        "metadata": {
            "model": MODEL,
            "generated_at": datetime.now().isoformat(),
            "deputies_present": sum(DEPUTIES[p] for p in parties),
            "majority_threshold": 116,
        },
    }


# =========================================================================
# PERSISTÊNCIA
# =========================================================================

def save_session(result: dict) -> Path:
    """Guarda transcript.json e report.md na pasta da sessão."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    folder_name = f"{date_str}-{result['briefing_slug'].split('-', 3)[-1] if '-' in result['briefing_slug'] else result['briefing_slug']}"
    
    # Se o briefing_slug já tem data, usa-a
    if result["briefing_slug"][:10].count("-") == 2:
        folder_name = result["briefing_slug"]
    
    folder = Path("simulations") / folder_name
    folder.mkdir(parents=True, exist_ok=True)
    
    # transcript.json (transcrição completa, alimenta o site)
    transcript_path = folder / "transcript.json"
    transcript_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    
    # report.md (relatório publicável)
    report_path = folder / "report.md"
    report_path.write_text(result["report"], encoding="utf-8")
    
    print(f"✓ Transcrição: {transcript_path}")
    print(f"✓ Relatório:   {report_path}")
    
    return folder


# =========================================================================
# CLI
# =========================================================================

def _configure_stdio_utf8() -> None:
    """Evita UnicodeEncodeError na consola Windows (cp1252)."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass


def main():
    _configure_stdio_utf8()
    parser = argparse.ArgumentParser(
        description="Executa uma sessão do Governo AI."
    )
    parser.add_argument(
        "--briefing",
        required=True,
        help="Slug da pasta em briefings/ (ex: 2026-05-08-reforma-laboral)"
    )
    parser.add_argument(
        "--parties",
        nargs="+",
        default=None,
        help=f"Partidos a incluir. Default: todos com assento. Válidos: {', '.join(ALL_PARTIES)}"
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=2,
        help="Número de rondas de debate após posições iniciais (default: 2)"
    )
    
    args = parser.parse_args()
    
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERRO: variável de ambiente ANTHROPIC_API_KEY não definida.")
        print("Define-a com: export ANTHROPIC_API_KEY='sk-ant-...'")
        return 1
    
    try:
        result = run_session(
            briefing_slug=args.briefing,
            parties=args.parties,
            debate_rounds=args.rounds,
        )
        save_session(result)
        print("\n" + "="*60)
        print("  Sessão pronta. Próximos passos:")
        print("  1. Lê o report.md e edita se necessário")
        print("  2. Publica no site: atualiza src/content/sessoes/<slug>.md a partir do report.md (ou python publish.py <slug>)")
        print("  3. git add . && git commit -m 'Sessão #N' && git push")
        print("="*60 + "\n")
        return 0
    except FileNotFoundError as e:
        print(f"\nERRO: {e}")
        return 1
    except anthropic.APIError as e:
        print(f"\nERRO API Anthropic: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
