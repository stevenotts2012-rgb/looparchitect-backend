# LoopArchitect Backend

LoopArchitect is a music production platform backend. It provides an API to accept loop/stem inputs, apply style-driven arrangement logic, and (in the full vision) render complete structured songs.

This repository currently contains an initial FastAPI scaffold with generation defaults and health checks, plus project dependency/runtime files.

## What it does today

- Runs a FastAPI server (`main.py`)
- Exposes health endpoints (`/`, `/health`)
- Exposes a simple generation endpoint (`/generate`) that merges user-provided values with sensible defaults

## Product vision (target architecture)

The intended backend architecture is a pipeline-based arranger/producer engine:

1. **Ingestion & Analysis**: detect BPM/key, classify stems, extract metadata, optionally separate stems.
2. **Arrangement Planning**: build section plans (intro/verse/hook/bridge), energy curves, and transitions.
3. **Producer Logic**: apply deterministic rules + optional AI co-producer guidance.
4. **Rendering**: render/mix/master arranged stems to output audio.
5. **Storage & Export**: store outputs locally or in object storage and export stems/MIDI.

## Tech stack

- **Python**: 3.11+
- **Web API**: FastAPI
- **ASGI server**: Uvicorn / Gunicorn
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Queue**: Redis + RQ
- **Audio**: pydub, librosa, soundfile, ffmpeg
- **Storage**: local disk or S3-compatible storage
- **Optional AI layer**: OpenAI API

## Current API

### `GET /`
Returns basic service status.

Example response:

```json
{"status": "ok"}
```

### `GET /health`
Returns health state for probes and uptime checks.

Example response:

```json
{"ok": true}
```

### `POST /generate`
Accepts style and music intent parameters and returns merged output with defaults.

Request body fields (all optional):

- `bpm` (int)
- `key` (str)
- `scale` (str)
- `mood` (str)
- `energy` (str)
- `genre` (str)
- `loop_length_bars` (int)

Example request:

```json
{
  "bpm": 128,
  "key": "A minor",
  "genre": "House"
}
```

Example response:

```json
{
  "bpm": 128,
  "key": "A minor",
  "scale": "Natural Minor",
  "mood": "Dark",
  "energy": "High",
  "genre": "House",
  "loop_length_bars": 8
}
```

## Local development

### 1) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the app

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4) Verify

```bash
curl http://localhost:8000/health
```

## Environment

- `PORT` (optional): server port used by `main.py` (defaults to `8000`).

## Next steps toward full LoopArchitect backend

- Add modular `app/` package structure (routes/services/models/config).
- Introduce SQLAlchemy models (`Loop`, `Arrangement`, `Job`) and Alembic migrations.
- Add asynchronous render job processing with Redis + RQ.
- Add storage abstraction layer (local + S3).
- Add arranger/producer pipeline and feature flags.

