"""Generate accessible, bilingual SVG flow diagrams for Writing."""

from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "images" / "flows"
FLOWS = {
    "from-model-capability-to-operating-capability": {
        "en": [("Models", "& tools"), ("Policy", "& gates"), ("Evidence", "& review"), ("Operable", "capability")],
        "es": [("Modelos y", "herramientas"), ("Políticas y", "controles"), ("Evidencia y", "revisión"), ("Capacidad", "operable")],
    },
    "where-agent-autonomy-should-stop": {
        "en": [("Observe", "& propose"), ("Prepare", "reversible draft"), ("Authorize", "at the boundary"), ("Execute", "& reconcile")],
        "es": [("Observar y", "proponer"), ("Preparar", "borrador reversible"), ("Autorizar", "en el límite"), ("Ejecutar y", "reconciliar")],
    },
    "evaluate-the-workflow-not-just-the-model": {
        "en": [("Inputs", "& sources"), ("Models, tools", "& traces"), ("Quality gates", "& human review"), ("Published", "outcome")],
        "es": [("Entradas y", "fuentes"), ("Modelos,", "herramientas y trazas"), ("Controles y", "revisión humana"), ("Resultado", "publicado")],
    },
    "ai-finops-without-false-precision": {
        "en": [("Observed", "usage"), ("Estimated", "or projected"), ("Billed", "cost"), ("Reconcile", "& decide")],
        "es": [("Consumo", "observado"), ("Estimado o", "proyectado"), ("Coste", "facturado"), ("Reconciliar", "y decidir")],
    },
}


def render_flow(steps: list[tuple[str, str]]) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 680" width="480" height="680">',
        '<rect width="480" height="680" rx="24" fill="#122031"/>',
        '<rect x="1" y="1" width="478" height="678" rx="23" fill="none" stroke="#304a5c" stroke-width="2"/>',
    ]
    for number, (line_one, line_two) in enumerate(steps, 1):
        y = 36 + (number - 1) * 156
        parts += [
            f'<rect x="42" y="{y}" width="396" height="108" rx="16" fill="#1d3041" stroke="#466b80" stroke-width="2"/>',
            f'<circle cx="92" cy="{y + 54}" r="22" fill="#80aeca"/>',
            f'<text x="92" y="{y + 62}" text-anchor="middle" fill="#10202f" font-family="Arial, sans-serif" font-size="22" font-weight="700">{number}</text>',
            f'<text x="262" y="{y + 48}" text-anchor="middle" fill="#f3f4f6" font-family="Arial, sans-serif" font-size="23" font-weight="700">{escape(line_one)}</text>',
            f'<text x="262" y="{y + 79}" text-anchor="middle" fill="#c6d5de" font-family="Arial, sans-serif" font-size="21">{escape(line_two)}</text>',
        ]
        if number < len(steps):
            parts += [
                f'<path d="M240 {y + 108} V{y + 147}" stroke="#80aeca" stroke-width="3" stroke-linecap="round"/>',
                f'<path d="M232 {y + 139} L240 {y + 149} L248 {y + 139}" fill="none" stroke="#80aeca" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
            ]
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def build() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for slug, languages in FLOWS.items():
        for lang, steps in languages.items():
            (OUTPUT / f"{slug}-{lang}.svg").write_text(render_flow(steps), encoding="utf-8")
    print(f"Built {len(FLOWS) * 2} flow diagrams")


if __name__ == "__main__":
    build()
