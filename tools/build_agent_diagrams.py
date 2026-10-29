"""Build the localized, mobile-readable diagrams for the agent adoption article."""

from __future__ import annotations

from html import escape
from pathlib import Path


OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "flows"


def text(x: int, y: int, value: str, size: int = 21, *, color: str = "#f3f4f6", weight: int = 600, anchor: str = "middle") -> str:
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}">{escape(value)}</text>'


def box(y: int, title: str, detail: str = "", *, accent: str = "#80aeca", height: int = 92) -> str:
    middle = y + height // 2
    parts = [f'<rect x="34" y="{y}" width="412" height="{height}" rx="16" fill="#1d3041" stroke="{accent}" stroke-width="2"/>']
    parts.append(text(240, middle - (4 if detail else -8), title, 22))
    if detail:
        parts.append(text(240, middle + 26, detail, 17, color="#c6d5de", weight=400))
    return "".join(parts)


def arrow(y1: int, y2: int) -> str:
    return f'<path d="M240 {y1} V{y2 - 8} M232 {y2 - 16} L240 {y2 - 7} L248 {y2 - 16}" fill="none" stroke="#80aeca" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'


def chips(y: int, labels: list[str], *, columns: int = 2, height: int = 58) -> str:
    gap = 10
    width = (412 - gap * (columns - 1)) // columns
    parts = []
    for i, label in enumerate(labels):
        row, col = divmod(i, columns)
        x = 34 + col * (width + gap)
        yy = y + row * (height + gap)
        parts.append(f'<rect x="{x}" y="{yy}" width="{width}" height="{height}" rx="12" fill="#22394c" stroke="#466b80"/>')
        parts.append(text(x + width // 2, yy + height // 2 + 7, label, 18))
    return "".join(parts)


def base(title: str, subtitle: str) -> list[str]:
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 800" width="480" height="800" role="img" aria-labelledby="diagram-title diagram-desc">',
        f'<title id="diagram-title">{escape(title)}</title>',
        f'<desc id="diagram-desc">{escape(subtitle)}</desc>',
        '<rect width="480" height="800" rx="24" fill="#122031"/>',
        '<rect x="1" y="1" width="478" height="798" rx="23" fill="none" stroke="#304a5c" stroke-width="2"/>',
        text(240, 48, title, 26),
        text(240, 79, subtitle, 17, color="#a9c4d5", weight=400),
    ]


def render(kind: str, lang: str) -> str:
    es = lang == "es"
    if kind == "adoption":
        parts = base("Adopción distribuida" if es else "Distributed adoption", "Señales locales → problema de escala" if es else "Local gains → scaling problem")
        parts += [chips(112, ["Equipo A · Copilot" if es else "Team A · Copilot", "Equipo B · Claude" if es else "Team B · Claude", "Equipo C · agentes" if es else "Team C · agents", "Producto · análisis" if es else "Product · analysis", "Dev · código" if es else "Dev · code", "Plataforma · auto." if es else "Platform · auto."]), arrow(306, 332), box(334, "Productividad local" if es else "Local productivity"), arrow(426, 456), box(458, "ESCALA" if es else "SCALE", accent="#e2b977", height=72), arrow(530, 558), chips(560, ["Contexto" if es else "Context", "Gobernanza" if es else "Governance", "Trazabilidad" if es else "Traceability"], columns=1, height=50), arrow(754, 775)]
        parts.append(text(240, 783, "Problema de ingeniería" if es else "Engineering problem", 18, color="#e2b977"))
    elif kind == "context":
        parts = base("Contexto para el agente" if es else "Context for the agent", "Seleccionar, no volcarlo todo" if es else "Select, do not dump everything")
        parts += [chips(112, ["Estándares" if es else "Standards", "Instrucciones" if es else "Instructions", "Especificación" if es else "Specification", "Conocimiento" if es else "Knowledge", "Procedimientos" if es else "Procedures", "Capacidades" if es else "Capabilities"]), arrow(306, 338), box(340, "Resolver aplicabilidad" if es else "Resolve applicability", "Repositorio · tarea · fase" if es else "Repository · task · phase"), arrow(432, 470), box(472, "Contexto relevante" if es else "Relevant context", "Mínimo · versionado · trazable" if es else "Minimal · versioned · traceable", accent="#8bbca7", height=102), arrow(574, 612), box(614, "Agente" if es else "Agent", "Conoce el origen de cada instrucción" if es else "Knows each instruction's source"), text(240, 770, "Todo disponible ≠ todo aplicable" if es else "Everything available ≠ applicable", 17, color="#e2b977")]
    elif kind == "lifecycle":
        parts = base("Ciclo y metodología" if es else "Lifecycle & method", "Conectados mediante contratos" if es else "Connected by contracts")
        parts += [box(112, "Idea → Inception → Definición" if es else "Idea → Inception → Definition", height=82), arrow(194, 226), box(228, "Contrato de entrada" if es else "Input contract", "Objetivo · alcance · restricciones" if es else "Objective · scope · constraints", accent="#8bbca7"), arrow(320, 352), box(354, "Construcción / SDD" if es else "Construction / SDD", "Especificar → planificar → verificar" if es else "Specify → plan → verify", height=116), arrow(470, 504), box(506, "Contrato de salida" if es else "Output contract", "Evidencia · aprobación" if es else "Evidence · approval", accent="#8bbca7"), arrow(598, 630), box(632, "Validación → Revisión" if es else "Validation → Review", "Entrega → Producción → Feedback" if es else "Delivery → Production → Feedback", height=104)]
    elif kind == "delivery":
        parts = base("Entrega de contexto" if es else "Context delivery", "Una capacidad de Plataforma" if es else "A Platform capability")
        parts += [chips(110, ["Repositorio" if es else "Repository", "Tipo de tarea" if es else "Task type", "Fase" if es else "Phase", "Tecnología" if es else "Technology", "Dominio" if es else "Domain", "Responsable" if es else "Owner"]), arrow(306, 338), box(340, "Resolver aplicabilidad" if es else "Resolve applicability", "Entorno · permisos · dominio" if es else "Environment · permissions · domain"), arrow(432, 464), box(466, "Paquete de contexto" if es else "Context package", "Estándares · conocimiento · skills" if es else "Standards · knowledge · skills", accent="#8bbca7", height=112), arrow(578, 610), box(612, "Capacidades → agente" if es else "Capabilities → agent", height=78), text(240, 754, "Fuente + versión + aplicabilidad" if es else "Source + version + applicability", 18, color="#e2b977")]
    elif kind == "repository":
        parts = base("Repositorio preparado" if es else "Agent-ready repository", "Tres mecanismos distintos" if es else "Three separate mechanisms")
        parts += [box(114, "STANDARD", "¿Qué debe cumplirse?" if es else "What must be true?", height=112), arrow(226, 270), box(272, "BOOTSTRAP", "¿Cómo llegar a ese estado?" if es else "How do we get there?", height=112), arrow(384, 428), box(430, "VALIDATION", "¿Se cumple de verdad?" if es else "Is it actually true?", accent="#8bbca7", height=112), arrow(542, 582), box(584, "Resultado accionable" if es else "Actionable result", "Cumple · falta · corregible" if es else "Compliant · missing · fixable", height=108), text(240, 744, "Revisión humana · no aplica" if es else "Human review · not applicable", 18, color="#e2b977")]
    elif kind == "deterministic":
        parts = base("Determinista primero" if es else "Deterministic first", "Elegir el mecanismo adecuado" if es else "Choose the right mechanism")
        parts += [box(118, "Pregunta de ingeniería" if es else "Engineering question", height=100), arrow(218, 266), chips(268, ["Verificable" if es else "Verifiable", "Ambigua" if es else "Ambiguous"], height=74), chips(365, ["Código / políticas" if es else "Code / policy", "Razonamiento IA" if es else "AI reasoning"], height=96), arrow(567, 608), box(610, "Evidencia examinable" if es else "Inspectable evidence", "Resultado · fuente · explicación" if es else "Result · source · explanation", accent="#8bbca7", height=112)]
    elif kind == "tracks":
        parts = base("Dos responsabilidades" if es else "Two responsibilities", "Relacionadas, pero distintas" if es else "Related, but different")
        parts += [box(112, "AI ENGINEERING", "IA para construir software" if es else "AI to build software", height=102), arrow(214, 248), box(250, "Plan → construir → validar" if es else "Plan → build → validate", "Revisar → entregar → operar" if es else "Review → deliver → operate", height=102), text(240, 407, "AI Runtime solo si el producto usa IA" if es else "AI Runtime only if product uses AI", 18, color="#e2b977"), box(444, "AI RUNTIME", "IA dentro de la aplicación" if es else "AI inside the application", accent="#8bbca7", height=102), arrow(546, 580), box(582, "Modelos · identidad · seguridad" if es else "Models · identity · security", "Evaluación · observabilidad · coste" if es else "Evaluation · observability · cost", accent="#8bbca7", height=126)]
    elif kind == "architecture":
        parts = base("Arquitectura completa" if es else "Complete architecture", "Una plataforma, dos tracks" if es else "One platform, two tracks")
        parts += [box(104, "Intención de producto" if es else "Product intent", height=74), arrow(178, 206), box(208, "Ciclo de ingeniería" if es else "Engineering lifecycle", "Idea → Construcción → Entrega" if es else "Idea → Construction → Delivery", height=98), arrow(306, 334), box(336, "Context Delivery", "Estándares · conocimiento · skills" if es else "Standards · knowledge · skills", accent="#8bbca7", height=98), arrow(434, 462), box(464, "Agentes + contratos" if es else "Agents + contracts", "Evidencia · revisión · autoridad" if es else "Evidence · review · authority", height=98), arrow(562, 594), box(596, "Producto usa IA en producción?" if es else "Product uses AI in production?", height=76), arrow(672, 700), box(702, "AI Runtime, si aplica" if es else "AI Runtime, if needed", "Modelos · evaluación · gobierno" if es else "Models · evaluation · governance", accent="#e2b977", height=76)]
    else:
        raise ValueError(kind)
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def build() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for kind in ("adoption", "context", "lifecycle", "delivery", "repository", "deterministic", "tracks", "architecture"):
        for lang in ("en", "es"):
            (OUTPUT / f"ai-agent-adoption-{kind}-{lang}.svg").write_text(render(kind, lang), encoding="utf-8")
    print("Built 16 localized agent-adoption diagrams")


if __name__ == "__main__":
    build()
