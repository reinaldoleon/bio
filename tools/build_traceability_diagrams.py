"""Generate localized SVG diagrams for the coding-agent traceability article."""

from __future__ import annotations

from pathlib import Path

from tools.build_agent_diagrams import arrow, base, box, chips, text


OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "flows"
KINDS = ("short-path", "lifecycle", "harness", "profiles", "evidence", "premise", "friction", "synthesis")


def render(kind: str, lang: str) -> str:
    es = lang == "es"
    if kind == "short-path":
        parts = base("El camino corto" if es else "The short path", "Generar no equivale a entregar" if es else "Generation is not delivery")
        parts += [box(105, "Intención de negocio" if es else "Business intent", height=74), arrow(179, 205), box(207, "Coding agent", height=74), arrow(281, 307), box(309, "Código" if es else "Code", height=74), arrow(383, 409), box(411, "Despliegue" if es else "Deploy", height=74), arrow(485, 523), box(525, "¿Qué falta?" if es else "What is missing?", "El camino no explica el porqué" if es else "The path does not explain why", accent="#e2b977", height=95), chips(648, ["Requisitos" if es else "Requirements", "Decisiones" if es else "Decisions", "Evidencia" if es else "Evidence", "Aprobaciones" if es else "Approvals"], height=51)]
    elif kind == "lifecycle":
        parts = base("Un lifecycle explícito" if es else "An explicit lifecycle", "Del objetivo a la operación" if es else "From intent to operation")
        parts += [box(108, "Intención → requisitos" if es else "Intent → requirements", height=79), arrow(187, 217), box(219, "Diseño → decisiones" if es else "Design → decisions", height=79), arrow(298, 328), box(330, "Implementación" if es else "Implementation", height=79), arrow(409, 439), box(441, "Validación → evidencia" if es else "Validation → evidence", accent="#8bbca7", height=91), arrow(532, 562), box(564, "Aprobación humana" if es else "Human approval", accent="#e2b977", height=79), arrow(643, 673), box(675, "Operación" if es else "Operation", height=79)]
    elif kind == "harness":
        parts = base("Método y harness" if es else "Method & harness", "Capas que pueden evolucionar" if es else "Layers that can evolve")
        parts += [box(117, "Metodología de ingeniería" if es else "Engineering methodology", "Contratos · etapas · gates" if es else "Contracts · stages · gates", accent="#8bbca7", height=104), arrow(221, 271), chips(273, ["Claude Code", "Codex", "Cursor", "Kiro", "opencode", "Copilot"], height=77), arrow(535, 570), box(572, "Modelos / herramientas" if es else "Models / tools", "El proceso permanece estable" if es else "The process remains stable", height=120), text(240, 754, "Harness ≠ metodología" if es else "Harness ≠ methodology", 18, color="#e2b977")]
    elif kind == "profiles":
        parts = base("Perfiles adaptativos" if es else "Adaptive profiles", "Una ruta para cada tipo de trabajo" if es else "A route for each kind of work")
        parts += [box(111, "Petición de trabajo" if es else "Work request", height=84), arrow(195, 231), box(233, "Elegir perfil" if es else "Select profile", "Según alcance, efecto y riesgo" if es else "By scope, effect and risk", accent="#8bbca7", height=102), arrow(335, 365), chips(367, ["PoC · ligero" if es else "PoC · light", "Bugfix · focal" if es else "Bugfix · focused", "Feature · medio" if es else "Feature · medium", "Infra · fuerte" if es else "Infra · strong", "Security · fuerte" if es else "Security · strong", "Enterprise · alto" if es else "Enterprise · high"], height=70), arrow(597, 630), box(632, "Etapas y controles" if es else "Stages and controls", "Proporcionales al cambio" if es else "Proportional to the change", height=105)]
    elif kind == "evidence":
        parts = base("Cadena de evidencia" if es else "Evidence chain", "Una aprobación que se puede revisar" if es else "An approval you can review")
        labels = ["Requisito" if es else "Requirement", "Decisión" if es else "Decision", "Implementación" if es else "Implementation", "Validación" if es else "Validation", "Evidencia" if es else "Evidence", "Aprobación" if es else "Approval"]
        for i, label in enumerate(labels):
            y = 103 + i * 111
            parts.append(box(y, label, height=75, accent="#e2b977" if i == 5 else ("#8bbca7" if i == 4 else "#80aeca")))
            if i < len(labels) - 1:
                parts.append(arrow(y + 75, y + 110))
    elif kind == "premise":
        parts = base("Estructura ≠ rigor" if es else "Structure ≠ rigor", "Una premisa mala también puede escalar" if es else "A bad premise can scale too")
        labels = ["Suposición errónea" if es else "Wrong assumption", "Requisito estructurado" if es else "Structured requirement", "Diseño estructurado" if es else "Structured design", "Código estructurado" if es else "Structured code", "Tests estructurados" if es else "Structured tests"]
        for i, label in enumerate(labels):
            y = 110 + i * 126
            parts.append(box(y, label, height=82, accent="#df8e84" if i == 0 else "#80aeca"))
            if i < len(labels) - 1:
                parts.append(arrow(y + 82, y + 125))
        parts.append(text(240, 758, "Revisar la premisa temprano" if es else "Challenge the premise early", 18, color="#e2b977"))
    elif kind == "friction":
        parts = base("Presupuesto de fricción" if es else "Friction budget", "Control proporcional al riesgo" if es else "Control proportional to risk")
        parts += [chips(118, ["PoC · ligero" if es else "PoC · light", "Feature · medio" if es else "Feature · medium", "Infra · fuerte" if es else "Infra · strong", "Security · fuerte" if es else "Security · strong"], height=83), arrow(283, 325), box(327, "Riesgo y reversibilidad" if es else "Risk and reversibility", "Determinan gates y profundidad" if es else "Set gates and review depth", accent="#8bbca7", height=113), arrow(440, 478), box(480, "Coste del workflow" if es else "Workflow cost", "Preguntas · modelos · latencia" if es else "Questions · models · latency", height=113), arrow(593, 632), box(634, "Entrega con confianza" if es else "Delivery with confidence", "Sin ceremonia innecesaria" if es else "Without unnecessary ceremony", accent="#e2b977", height=108)]
    elif kind == "synthesis":
        parts = base("Sistema de ingeniería" if es else "Engineering system", "Del asistente al delivery gobernado" if es else "From assistant to governed delivery")
        parts += [box(103, "Intención" if es else "Intent", height=69), arrow(172, 197), box(199, "Workflow adaptable" if es else "Adaptive workflow", "Perfil · etapas · agentes" if es else "Profile · stages · agents", height=94), arrow(293, 319), box(321, "Requisitos → decisiones" if es else "Requirements → decisions", height=69), arrow(390, 416), box(418, "Código → tests" if es else "Code → tests", height=69), arrow(487, 513), box(515, "Evidencia → gates humanos" if es else "Evidence → human gates", accent="#8bbca7", height=94), arrow(609, 635), box(637, "Entrega → operación" if es else "Delivery → operation", "Explicable · revisable · gobernable" if es else "Explainable · reviewable · governable", accent="#e2b977", height=104)]
    else:
        raise ValueError(kind)
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def build() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for kind in KINDS:
        for lang in ("en", "es"):
            (OUTPUT / f"coding-agent-traceability-{kind}-{lang}.svg").write_text(render(kind, lang), encoding="utf-8")
    print(f"Built {len(KINDS) * 2} bilingual traceability diagrams")


if __name__ == "__main__":
    build()
