"""Build localized SVG flows for the deterministic AI Engineering article."""

from __future__ import annotations

from pathlib import Path

from tools.build_agent_diagrams import arrow, base, box, chips, text


OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "flows"
KINDS = ("decision", "propose-verify", "repository", "reviewer", "policy", "synthesis")


def render(kind: str, lang: str) -> str:
    es = lang == "es"
    if kind == "decision":
        parts = base("¿Otro LLM?" if es else "Another LLM?", "Primero, elegir el mecanismo" if es else "First, choose the mechanism")
        parts += [
            box(112, "Pregunta de ingeniería" if es else "Engineering question", height=88),
            arrow(200, 242),
            box(244, "¿Respuesta reproducible?" if es else "Reproducible answer?", accent="#e2b977", height=102),
            arrow(346, 386),
            chips(388, ["Sí · código / regla" if es else "Yes · code / rule", "No · LLM / juicio" if es else "No · LLM / judgment"], height=92),
            arrow(480, 570),
            box(572, "Evidencia" if es else "Evidence", "Resultado con límites claros" if es else "Result with clear limits", accent="#8bbca7", height=112),
            text(240, 749, "Sin modelo si el código responde" if es else "No model when code can answer", 18, color="#e2b977"),
        ]
    elif kind == "propose-verify":
        parts = base("Proponer y verificar" if es else "Propose and verify", "Responsabilidades distintas" if es else "Different responsibilities")
        parts += [
            box(112, "Problema ambiguo" if es else "Ambiguous problem", height=83),
            arrow(195, 225),
            box(227, "Razonamiento LLM" if es else "LLM reasoning", "Arquitectura · alternativas" if es else "Architecture · alternatives", height=98),
            arrow(325, 355),
            box(357, "Solución propuesta" if es else "Proposed solution", height=83),
            arrow(440, 467),
            chips(469, ["Formato" if es else "Format", "Validación" if es else "Validation", "Pruebas" if es else "Tests", "Políticas" if es else "Policies"], height=70),
            arrow(619, 658),
            box(660, "Evidencia examinable" if es else "Inspectable evidence", accent="#8bbca7", height=95),
        ]
    elif kind == "repository":
        parts = base("Repositorio preparado" if es else "Repository readiness", "Hechos y observaciones" if es else "Facts and observations")
        parts += [
            box(110, "Repositorio" if es else "Repository", height=82),
            arrow(192, 228),
            chips(230, ["Checks exactos" if es else "Exact checks", "Evaluación" if es else "Evaluation"], height=82),
            chips(335, ["CI · versiones" if es else "CI · versions", "Claridad · contexto" if es else "Clarity · context", "Tests · ficheros" if es else "Tests · files", "Contradicciones" if es else "Contradictions"], height=70),
            arrow(485, 525),
            box(527, "Hechos + observaciones" if es else "Facts + observations", "Con procedencia y límites" if es else "With provenance and limits", accent="#8bbca7", height=106),
            arrow(633, 675),
            box(677, "Recomendación revisable" if es else "Reviewable recommendation", accent="#e2b977", height=85),
        ]
    elif kind == "reviewer":
        parts = base("Revisión con evidencia" if es else "Evidence-led review", "Más que dos modelos de acuerdo" if es else "More than two agreeing models")
        parts += [
            box(110, "Creator → implementación" if es else "Creator → implementation", height=91),
            arrow(201, 239),
            chips(241, ["Tests", "Políticas" if es else "Policies", "Análisis estático" if es else "Static analysis", "Esquemas" if es else "Schemas"], height=74),
            arrow(399, 438),
            box(440, "Evidencia independiente" if es else "Independent evidence", accent="#8bbca7", height=96),
            arrow(536, 579),
            box(581, "Reviewer", "¿Qué prueba? ¿Qué falta?" if es else "What is proved? What is missing?", height=108),
            arrow(689, 723),
            text(240, 758, "Revisar el alcance de cada check" if es else "Examine each check's scope", 17, color="#e2b977"),
        ]
    elif kind == "policy":
        parts = base("Gobernanza verificable" if es else "Verifiable governance", "Reglas objetivas con límites claros" if es else "Objective rules with clear limits")
        parts += [
            box(111, "Regla explícita" if es else "Explicit rule", "Sin credenciales estáticas" if es else "No static credentials", height=110),
            arrow(221, 257),
            box(259, "Política ejecutable" if es else "Executable policy", "Configuración · identidad · CI" if es else "Config · identity · CI", accent="#8bbca7", height=111),
            arrow(370, 409),
            box(411, "Resultado + evidencia" if es else "Result + evidence", height=94),
            arrow(505, 542),
            box(544, "LLM: explicar / corregir" if es else "LLM: explain / correct", "Excepciones ambiguas a revisión" if es else "Review ambiguous exceptions", height=113),
            arrow(657, 694),
            text(240, 754, "La política decide la regla" if es else "Policy decides the rule", 19, color="#e2b977"),
        ]
    elif kind == "synthesis":
        parts = base("Sistema híbrido" if es else "Hybrid system", "Razonar donde aporta; verificar donde se puede" if es else "Reason where useful; verify where possible")
        parts += [
            box(105, "Intención" if es else "Intent", height=70),
            arrow(175, 201),
            box(203, "Razonamiento IA" if es else "AI reasoning", "Interpretar · proponer" if es else "Interpret · propose", height=89),
            arrow(292, 320),
            box(322, "Acción" if es else "Action", height=70),
            arrow(392, 418),
            box(420, "Checks deterministas" if es else "Deterministic checks", "Tests · políticas · schemas" if es else "Tests · policies · schemas", accent="#8bbca7", height=95),
            arrow(515, 542),
            box(544, "Evidencia → interpretación" if es else "Evidence → interpretation", height=76),
            arrow(620, 646),
            box(648, "Decidir o escalar" if es else "Decide or escalate", "Autoridad humana cuando importa" if es else "Human authority where it matters", accent="#e2b977", height=109),
        ]
    else:
        raise ValueError(kind)
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def build() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for kind in KINDS:
        for lang in ("en", "es"):
            (OUTPUT / f"deterministic-ai-engineering-{kind}-{lang}.svg").write_text(render(kind, lang), encoding="utf-8")
    print(f"Built {len(KINDS) * 2} bilingual deterministic AI Engineering diagrams")


if __name__ == "__main__":
    build()
