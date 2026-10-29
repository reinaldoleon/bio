"""Generate editorial PNG social previews for the localized agent article.

Requires Pillow when an editor regenerates the static assets; the site build does not.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "writing"
FONT = next((path for path in (
    Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
) if path.exists()), None)


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    return ImageFont.truetype(str(FONT), size) if FONT else ImageFont.load_default()


def build() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    titles = {
        "en": ["Is AI agent adoption", "growing faster than", "your governance?"],
        "es": ["¿La adopción de agentes", "crece más rápido que", "tu gobernanza?"],
    }
    for lang, lines in titles.items():
        image = Image.new("RGB", (1200, 630), "#122031")
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((38, 38, 1162, 592), radius=28, outline="#466b80", width=2)
        draw.text((88, 81), "REINALDO LEÓN  /  WRITING", font=font(23), fill="#a9c4d5")
        for index, line in enumerate(lines):
            draw.text((88, 166 + index * 82), line, font=font(59), fill="#f3f4f6")
        subline = "De herramientas de IA a capacidad de ingeniería." if lang == "es" else "From AI tooling to an engineering capability."
        draw.text((88, 465), subline, font=font(26), fill="#a9c4d5")
        draw.line((88, 535, 1110, 535), fill="#466b80", width=2)
        labels = ("CONTEXTO", "CONTROL") if lang == "es" else ("CONTEXT", "CONTROL")
        for x, label in zip((930, 1030), labels):
            draw.rounded_rectangle((x, 80, x + 87, 114), radius=7, fill="#22394c")
            draw.text((x + 8, 88), label, font=font(12), fill="#c6d5de")
        image.save(OUTPUT / f"ai-agent-adoption-governance-{lang}.png", optimize=True)
    print("Built 2 localized social previews")


if __name__ == "__main__":
    build()
