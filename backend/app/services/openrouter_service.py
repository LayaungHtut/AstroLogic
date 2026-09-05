import httpx
import logging
import base64
import re
from app.config import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_BASE_URL, MODELS

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a thoughtful tarot and astrology interpreter for the AstroLogic application.
Your role is to provide symbolic, reflective interpretations based on tarot cards and zodiac information.

IMPORTANT RULES:
- NEVER claim that astrology or tarot scientifically predicts the future
- NEVER diagnose mental health conditions or medical issues
- NEVER tell users that an event will definitely happen
- NEVER ask the user follow-up questions - always provide direct, complete answers
- ALWAYS frame readings as reflective entertainment and personal insight
- Use phrases like "You may find this useful to reflect on..." or "This could suggest..."
- Focus on symbolic meaning, personal growth, and self-reflection
- Be warm, supportive, and thoughtful in your tone
- Connect card meanings to the user's question when relevant
- Use the Prolog-derived themes and facts provided to you
- Keep responses concise but meaningful (2-4 paragraphs max)
- If you don't know something, say so directly rather than deflecting"""


def _clean_horoscope_section(value: str) -> str:
    """Keep the structured horoscope fields free of Markdown delimiters."""
    value = re.sub(r"\\([*_`])", r"\1", value)
    return re.sub(r"[*_`]+", "", value).strip()

TAROT_SCANNER_PROMPT = """You are a tarot card identification expert. The user will send an image of a tarot card.
Your job is to:
1. Identify the tarot card in the image
2. Tell me the card name
3. Tell me if it appears upright or reversed
4. List the card's key meanings
5. Provide a brief interpretation

Respond in this exact JSON format:
{
  "card_name": "The card name (e.g., 'The Hermit')",
  "card_id": "the_hermit (snake_case identifier)",
  "orientation": "upright or reversed",
  "confidence": "high, medium, or low",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "upright_meaning": "Brief upright meaning",
  "reversed_meaning": "Brief reversed meaning",
  "brief_interpretation": "A 2-3 sentence interpretation of this card as it appears in the image"
}

If you cannot identify the card, return:
{"error": "Could not identify the tarot card in this image", "confidence": "none"}

Do not make up card names. Only identify cards from the standard 78-card Rider-Waite-Smith tarot deck."""


async def call_openrouter(
    messages: list[dict],
    system_prompt: str = SYSTEM_PROMPT,
    model: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 800,
) -> str | None:
    if not OPENROUTER_API_KEY:
        logger.warning("OpenRouter API key not configured")
        return None

    use_model = model or MODELS.get("default", OPENROUTER_MODEL)

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OPENROUTER_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:5173",
                    "X-Title": "AstroLogic",
                },
                json={
                    "model": use_model,
                    "messages": [
                        {"role": "system", "content": system_prompt}
                    ]
                    + messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
            )

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(
                    f"OpenRouter API error ({use_model}): {response.status_code} - {response.text}"
                )
                return None

    except httpx.TimeoutException:
        logger.error(f"OpenRouter API timeout ({use_model})")
        return None
    except httpx.HTTPError as e:
        logger.error(f"OpenRouter HTTP error: {e}")
        return None
    except Exception as e:
        logger.error(f"OpenRouter unexpected error: {e}")
        return None


async def call_openrouter_with_image(
    image_base64: str,
    mime_type: str = "image/jpeg",
    system_prompt: str = TAROT_SCANNER_PROMPT,
    model: str | None = None,
) -> str | None:
    """Call OpenRouter with an image for vision models."""
    if not OPENROUTER_API_KEY:
        logger.warning("OpenRouter API key not configured")
        return None

    use_model = model or MODELS.get("vision", OPENROUTER_MODEL)

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OPENROUTER_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:5173",
                    "X-Title": "AstroLogic",
                },
                json={
                    "model": use_model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{mime_type};base64,{image_base64}"
                                    },
                                },
                                {
                                    "type": "text",
                                    "text": "Identify the tarot card in this image. Respond in the exact JSON format specified.",
                                },
                            ],
                        },
                    ],
                    "temperature": 0.3,
                    "max_tokens": 600,
                },
            )

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(
                    f"OpenRouter vision API error: {response.status_code} - {response.text}"
                )
                return None

    except httpx.TimeoutException:
        logger.error("OpenRouter vision API timeout")
        return None
    except Exception as e:
        logger.error(f"OpenRouter vision error: {e}")
        return None


async def scan_tarot_image(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict | None:
    """Scan a tarot card image and identify it."""
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    result = await call_openrouter_with_image(
        image_b64, mime_type, TAROT_SCANNER_PROMPT
    )

    if not result:
        return None

    # Try to parse JSON from the response
    import json
    try:
        # Find JSON in the response (might be wrapped in markdown)
        start = result.find("{")
        end = result.rfind("}") + 1
        if start >= 0 and end > start:
            json_str = result[start:end]
            return json.loads(json_str)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse vision model response as JSON: {result}")
        return None

    return None


async def generate_tarot_interpretation(
    question: str,
    zodiac_sign: str,
    element: str,
    spread_name: str,
    cards: list[dict],
    themes: list[str],
    category: str,
    topic: str = "general",
) -> str | None:
    cards_text = "\n".join(
        [
            f"- {c['name']} ({c['position']}) {'[Reversed]' if c['is_reversed'] else '[Upright]'}: {', '.join(c['keywords'])}"
            for c in cards
        ]
    )

    user_msg = f"""Please interpret this tarot reading:

Question: {question}
Zodiac: {zodiac_sign} ({element} element)
Topic: {topic}
Spread: {spread_name}
Category: {category}

Cards drawn:
{cards_text}

Prolog-derived themes: {', '.join(themes)}

Please provide a thoughtful, reflective interpretation that connects these cards to the user's question.
Focus on the {topic} dimension of this reading.
Use the themes and card meanings to guide your interpretation.
Remember this is for entertainment and self-reflection only.
Provide your answer directly - do not ask follow-up questions."""

    messages = [{"role": "user", "content": user_msg}]
    result = await call_openrouter(messages, model=MODELS.get("creative"))
    return result


async def generate_horoscope(
    zodiac_sign: str,
    element: str,
    modality: str,
    theme: str,
    mood: str,
    mood_theme: str,
    focus: str,
) -> dict | None:
    user_msg = f"""Generate a personalized horoscope for {zodiac_sign} ({element} element, {modality} modality).

Today's theme: {theme}
Current mood: {mood}
Mood-based theme: {mood_theme}
Focus area: {focus}

Return exactly five plain-text lines using these labels: Theme:, Guidance:, Reflection:, Opportunity:, and Caution:.
Do not use Markdown, bullets, asterisks, or headings. Keep each section on one line.
Guidance should be 2-3 sentences; the other sections should be concise.

Remember: This is for entertainment and self-reflection. Do not make deterministic predictions. Provide your answer directly."""

    messages = [{"role": "user", "content": user_msg}]
    result = await call_openrouter(messages, max_tokens=500, model=MODELS.get("creative"))
    if result:
        lines = result.strip().split("\n")
        sections = {
            "theme": "",
            "guidance": "",
            "reflection": "",
            "opportunity": "",
            "caution": "",
        }
        current = None
        for line in lines:
            lower = line.lower().strip()
            if "theme" in lower and ":" in line:
                current = "theme"
                sections["theme"] = _clean_horoscope_section(line.split(":", 1)[-1])
            elif "guidance" in lower and ":" in line:
                current = "guidance"
                sections["guidance"] = _clean_horoscope_section(line.split(":", 1)[-1])
            elif "reflection" in lower and ":" in line:
                current = "reflection"
                sections["reflection"] = _clean_horoscope_section(line.split(":", 1)[-1])
            elif "opportunity" in lower and ":" in line:
                current = "opportunity"
                sections["opportunity"] = _clean_horoscope_section(line.split(":", 1)[-1])
            elif "caution" in lower and ":" in line:
                current = "caution"
                sections["caution"] = _clean_horoscope_section(line.split(":", 1)[-1])
            elif current and line.strip():
                sections[current] += " " + _clean_horoscope_section(line)
        return sections
    return None


async def chat_with_assistant(
    message: str,
    zodiac_sign: str | None = None,
    current_reading: dict | None = None,
    chat_history: list[dict] | None = None,
) -> str | None:
    context_parts = []
    if zodiac_sign:
        context_parts.append(f"User's zodiac sign: {zodiac_sign}")
    if current_reading:
        cards = current_reading.get("cards", [])
        if cards:
            card_names = [c.get("name", c.get("card", "")) for c in cards]
            context_parts.append(
                f"Current reading cards: {', '.join(card_names)}"
            )
        if current_reading.get("themes"):
            context_parts.append(
                f"Reading themes: {', '.join(current_reading['themes'])}"
            )

    system = SYSTEM_PROMPT + "\n\nAdditional context:\n" + "\n".join(
        context_parts
    )

    messages = []
    if chat_history:
        for msg in chat_history[-10:]:
            messages.append(
                {"role": msg["role"], "content": msg["content"]}
            )
    messages.append({"role": "user", "content": message})

    # Try creative model first, fall back to default
    result = await call_openrouter(messages, system_prompt=system, model=MODELS.get("creative"))
    if not result:
        result = await call_openrouter(messages, system_prompt=system)
    return result


async def explain_tarot_card(card_name: str, orientation: str = "upright") -> str | None:
    """Get a detailed explanation of a specific tarot card."""
    user_msg = f"""Provide a detailed explanation of the tarot card "{card_name}" in the {orientation} position.

Include:
1. Card meaning and symbolism
2. Key themes and keywords
3. What it means in a reading
4. How it relates to daily life
5. Any cautionary notes

Provide your answer directly as a knowledgeable tarot interpreter. Do not ask follow-up questions."""

    messages = [{"role": "user", "content": user_msg}]
    result = await call_openrouter(messages, model=MODELS.get("creative"), max_tokens=600)
    return result
