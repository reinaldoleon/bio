"""Create bilingual social previews for the deterministic AI Engineering article."""

from pathlib import Path

from PIL import Image, ImageDraw

from tools.build_agent_social import font


OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "writing"


def build() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    content = {
        "en": (["Does AI Engineering", "need another LLM?"], "Reason where useful. Verify what you can."),
        "es": (["¿Necesita AI Engineering", "otro LLM?"], "Razonar donde aporta. Verificar donde se puede."),
    }
    for lang, (lines, subline) in content.items():
        image = Image.new("RGB", (1200, 630), "#122031")
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((38, 38, 1162, 592), radius=28, outline="#466b80", width=2)
        draw.text((88, 81), "REINALDO LEÓN  /  WRITING", font=font(23), fill="#a9c4d5")
        for index, line in enumerate(lines):
            draw.text((88, 187 + index * 84), line, font=font(59), fill="#f3f4f6")
        draw.text((88, 465), subline, font=font(27), fill="#a9c4d5")
        draw.line((88, 535, 1110, 535), fill="#466b80", width=2)
        image.save(OUTPUT / f"ai-engineering-without-another-llm-{lang}.png", optimize=True)
    print("Built 2 bilingual social previews")


if __name__ == "__main__":
    build()
