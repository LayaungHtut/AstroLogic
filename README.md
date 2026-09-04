# AstroLogic - AI Zodiac & Tarot Reasoning System

An AI-powered Zodiac, Tarot, and Horoscope application combining symbolic Prolog reasoning with modern web technologies.

## Technologies

- **SvelteKit 5** + TypeScript - Frontend framework
- **Tailwind CSS** - UI styling
- **Python FastAPI** - Backend API and AI orchestration
- **SWI-Prolog** - Symbolic reasoning and knowledge base
- **OpenRouter** - LLM functionality for natural language interpretation
- **SQLite** - Local persistence

## Architecture

```
User (SvelteKit 5) --> REST API (FastAPI) --> Prolog (Reasoning) + OpenRouter (AI) --> SQLite (Storage)
```

1. User asks a question in the SvelteKit frontend
2. Python FastAPI classifies the question
3. SWI-Prolog reasons symbolically (zodiac traits, spread selection, card interpretation)
4. Structured Prolog results are sent to OpenRouter for natural language interpretation
5. Combined results are displayed in the SvelteKit frontend

## Prolog Role

SWI-Prolog maintains a knowledge base of:
- 12 zodiac signs with elements, modalities, ruling planets, and traits
- 78 tarot cards with keywords, meanings, and themes
- Compatibility rules between elements and signs
- Spread recommendation rules based on question classification
- Card interpretation and thematic extraction rules
- Complete reasoning trace generation

## AI Role

OpenRouter (LLM) is used for:
- Generating natural language interpretations of tarot readings
- Creating personalized horoscope content
- Powering the AI chat assistant
- **Never** for core reasoning - Prolog handles all symbolic reasoning

## Setup

### Prerequisites

- Node.js 18+
- Python 3.10+
- SWI-Prolog 9.x
- OpenRouter API key (optional - app works without it using fallback interpretations)

### Install SWI-Prolog

**Windows:** Download from https://www.swi-prolog.org/Download.html

**macOS:**
```bash
brew install swi-prolog
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install swi-prolog
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env to add your OpenRouter API key (optional)
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173` and connects to the backend at `http://localhost:8000`.

### Environment Variables

Create `backend/.env`:

```
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=openai/gpt-3.5-turbo
```

Without an API key, the app uses fallback deterministic interpretations.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/zodiac` | All zodiac signs |
| GET | `/api/zodiac/{sign}` | Zodiac sign info |
| GET | `/api/tarot` | All tarot cards |
| POST | `/api/tarot/draw` | Draw random cards |
| POST | `/api/reading/analyze` | Full reading with Prolog + AI |
| POST | `/api/reading/generate` | Save reading to history |
| POST | `/api/horoscope/generate` | Generate horoscope |
| POST | `/api/compatibility/analyze` | Zodiac compatibility |
| POST | `/api/chat` | AI chat assistant |
| GET | `/api/history` | Reading history |
| GET | `/api/history/{id}` | Single reading |
| DELETE | `/api/history/{id}` | Delete reading |
| GET | `/api/analytics` | Reading analytics |

## Project Structure

```
astrologic/
├── frontend/          # SvelteKit 5 frontend
├── backend/           # Python FastAPI backend
├── prolog/            # SWI-Prolog knowledge base
├── database/          # SQLite schema
├── docs/              # Documentation
└── README.md
```

## Troubleshooting

**SWI-Prolog not found:**
Ensure `swipl` is in your system PATH. Run `swipl --version` to verify.

**Backend connection errors:**
Ensure the FastAPI server is running on port 8000: `python -m uvicorn app.main:app --port 8000`

**OpenRouter errors:**
The app works without an API key using fallback interpretations. Check your API key if you want AI-generated content.

**Frontend not connecting:**
Ensure the backend is running and CORS is configured for `http://localhost:5173`.

## License

Educational project - for school use.
