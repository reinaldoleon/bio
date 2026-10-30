"""Generate localized social previews for the coding-agent traceability article.

Requires Pillow to regenerate assets; the static website has no runtime dependency.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from tools.build_agent_social import font


OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "writing"


def build() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    content = {
        "en": (["Your agent writes code.", "Can it explain", "how it got there?"], "From generated code to traceable delivery."),
        "es": (["Tu agente escribe código.", "¿Puede demostrar", "cómo llegó hasta él?"], "Del código generado a la entrega trazable."),
    }
    for lang, (lines, subline) in content.items():
        image = Image.new("RGB", (1200, 630), "#122031")
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((38, 38, 1162, 592), radius=28, outline="#466b80", width=2)
        draw.text((88, 81), "REINALDO LEÓN  /  WRITING", font=font(23), fill="#a9c4d5")
        for index, line in enumerate(lines):
            draw.text((88, 166 + index * 82), line, font=font(58), fill="#f3f4f6")
        draw.text((88, 465), subline, font=font(27), fill="#a9c4d5")
        draw.line((88, 535, 1110, 535), fill="#466b80", width=2)
        image.save(OUTPUT / f"ai-agent-code-traceability-{lang}.png", optimize=True)
    print("Built 2 bilingual social previews")


if __name__ == "__main__":
    build()
