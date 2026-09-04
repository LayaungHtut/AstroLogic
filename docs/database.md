# Database

## Overview

AstroLogic uses SQLite for local persistence via aiosqlite (async Python SQLite). The database stores user profiles, readings, and chat history.

## Schema

### user_profile

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment ID |
| nickname | TEXT | User display name |
| birth_date | TEXT | Birth date |
| zodiac_sign | TEXT | Zodiac sign |
| preferred_style | TEXT | Reading style preference |
| created_at | TIMESTAMP | Creation time |

### reading

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment ID |
| profile_id | INTEGER FK | References user_profile |
| question | TEXT | User's question |
| category | TEXT | Classified category |
| zodiac_sign | TEXT | User's zodiac |
| spread_type | TEXT | Tarot spread used |
| cards_json | TEXT | JSON array of cards |
| orientations_json | TEXT | JSON array of reversed states |
| themes_json | TEXT | JSON array of themes |
| reasoning_json | TEXT | JSON array of reasoning steps |
| ai_interpretation | TEXT | AI-generated interpretation |
| created_at | TIMESTAMP | Creation time |

### reading_card

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment ID |
| reading_id | INTEGER FK | References reading |
| card_name | TEXT | Card identifier |
| position | TEXT | Spread position name |
| is_reversed | INTEGER | 0 or 1 |
| keywords_json | TEXT | JSON array of keywords |

### chat_message

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment ID |
| profile_id | INTEGER FK | References user_profile |
| role | TEXT | 'user' or 'assistant' |
| content | TEXT | Message content |
| created_at | TIMESTAMP | Creation time |

## Initialization

The database is automatically created on first backend startup via `init_db()` in `database.py`.

## Design Decisions

- Anonymous local profile (no authentication)
- JSON fields for flexible structured data
- Cascade delete for reading cards when reading is deleted
- Default profile created automatically
