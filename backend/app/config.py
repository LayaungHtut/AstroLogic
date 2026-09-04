import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
PROLOG_DIR = BASE_DIR.parent / "prolog"
DATABASE_DIR = BASE_DIR.parent / "database"
DATABASE_PATH = DATABASE_DIR / "astrologic.db"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Multiple model support
MODELS = {
    "default": os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo"),
    "vision": os.getenv("OPENROUTER_VISION_MODEL", "openai/gpt-4o"),
    "creative": os.getenv("OPENROUTER_CREATIVE_MODEL", "anthropic/claude-3.5-sonnet"),
    "fast": os.getenv("OPENROUTER_FAST_MODEL", "openai/gpt-4o-mini"),
}

# Vite selects the next available port when 5173 is already in use. Permit
# requests from local development servers on either localhost address so a
# normal port change does not make browser preflight requests fail with 400.
CORS_ORIGINS = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]
CORS_ORIGIN_REGEX = r"^https?://(localhost|127\.0\.0\.1)(?::\d+)?$"

MAX_INPUT_LENGTH = 500
MAX_CHAT_MESSAGES = 50
