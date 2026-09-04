from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.config import CORS_ORIGIN_REGEX, CORS_ORIGINS
from app.database import init_db
from app.api.horoscope import router as zodiac_router
from app.api.tarot import router as tarot_router
from app.api.reasoning import router as reading_router
from app.api.horoscope_api import router as horoscope_router
from app.api.compatibility import router as compatibility_router
from app.api.chat import router as chat_router
from app.api.analytics import router as history_router
from app.api.analytics_api import router as analytics_router
from app.api.tarot_scan import router as tarot_scan_router
from app.api.topics import router as topics_router
from app.api.birth_chart import router as birth_chart_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="AstroLogic API",
    description="AI Zodiac & Tarot Reasoning System",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )

app.include_router(zodiac_router)
app.include_router(tarot_router)
app.include_router(reading_router)
app.include_router(horoscope_router)
app.include_router(compatibility_router)
app.include_router(chat_router)
app.include_router(history_router)
app.include_router(analytics_router)
app.include_router(tarot_scan_router)
app.include_router(topics_router)
app.include_router(birth_chart_router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "AstroLogic API"}
