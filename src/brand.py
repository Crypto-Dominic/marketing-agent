"""Brand configuration loader."""

from pathlib import Path

import yaml


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "brand_config.yaml"


def load_brand_config(path: Path | None = None) -> dict:
    """Load and return the brand configuration dictionary."""
    config_path = path or DEFAULT_CONFIG_PATH
    if not config_path.exists():
        raise FileNotFoundError(f"Brand config not found at {config_path}")
    with open(config_path) as f:
        return yaml.safe_load(f)


def brand_context_block(config: dict) -> str:
    """Convert brand config into a structured context block for the agent prompt."""
    brand = config.get("brand", {})
    voice = config.get("voice", {})
    audience = config.get("audience", {})
    products = config.get("products", [])
    differentiators = config.get("differentiators", [])
    competitors = config.get("competitors", [])

    sections = []

    # Brand overview
    sections.append(
        f"BRAND: {brand.get('name', 'N/A')}\n"
        f"Tagline: {brand.get('tagline', 'N/A')}\n"
        f"Mission: {brand.get('mission', 'N/A')}\n"
        f"Vision: {brand.get('vision', 'N/A')}\n"
        f"Website: {brand.get('website', 'N/A')}"
    )

    # Voice
    tone = ", ".join(voice.get("tone", []))
    traits = ", ".join(voice.get("personality_traits", []))
    dos = "\n  - ".join(voice.get("dos", []))
    donts = "\n  - ".join(voice.get("donts", []))
    sections.append(
        f"BRAND VOICE\n"
        f"Tone: {tone}\n"
        f"Personality: {traits}\n"
        f"Style: {voice.get('writing_style', 'N/A')}\n"
        f"Do:\n  - {dos}\n"
        f"Don't:\n  - {donts}"
    )

    # Audience
    for segment_key in ("primary", "secondary"):
        seg = audience.get(segment_key, {})
        if seg:
            channels = ", ".join(seg.get("channels", []))
            pains = "\n  - ".join(seg.get("pain_points", []))
            sections.append(
                f"AUDIENCE ({segment_key.upper()})\n"
                f"Description: {seg.get('description', 'N/A')}\n"
                f"Age range: {seg.get('age_range', 'N/A')}\n"
                f"Channels: {channels}\n"
                f"Pain points:\n  - {pains}"
            )

    # Products
    if products:
        product_lines = []
        for p in products:
            benefits = ", ".join(p.get("key_benefits", []))
            product_lines.append(f"- {p['name']}: {p.get('description', '')} (Benefits: {benefits})")
        sections.append("PRODUCTS\n" + "\n".join(product_lines))

    # Differentiators
    if differentiators:
        diff_lines = "\n  - ".join(differentiators)
        sections.append(f"KEY DIFFERENTIATORS\n  - {diff_lines}")

    # Competitors
    if competitors:
        comp_lines = []
        for c in competitors:
            comp_lines.append(f"- {c['name']}: {c.get('positioning', '')}")
        sections.append("COMPETITIVE LANDSCAPE\n" + "\n".join(comp_lines))

    return "\n\n".join(sections)
