# API Documentation

## Base URL

```
http://localhost:8000/api
```

## Endpoints

### Health Check

```
GET /api/health
```

Response:
```json
{"status": "ok", "service": "AstroLogic API"}
```

### Zodiac

```
GET /api/zodiac
GET /api/zodiac/{sign}
```

### Tarot

```
GET /api/tarot
POST /api/tarot/draw
```

Draw request:
```json
{"count": 3, "spread_type": "three_card"}
```

### Reading

```
POST /api/reading/analyze
POST /api/reading/generate
```

Analyze request:
```json
{
  "question": "I'm unsure about which direction to take",
  "zodiac_sign": "aries",
  "spread_type": "decision"
}
```

### Horoscope

```
POST /api/horoscope/generate
```

Request:
```json
{"zodiac_sign": "aries", "mood": "excited"}
```

### Compatibility

```
POST /api/compatibility/analyze
```

Request:
```json
{"sign1": "aries", "sign2": "leo"}
```

### Chat

```
POST /api/chat
```

Request:
```json
{
  "message": "What does The Hermit mean?",
  "zodiac_sign": "aries",
  "current_reading": null
}
```

### History

```
GET /api/history
GET /api/history/{id}
DELETE /api/history/{id}
```

### Analytics

```
GET /api/analytics
```
