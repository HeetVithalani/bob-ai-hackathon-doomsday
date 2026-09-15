## What We Built

A single-command, zero-dependency local web dashboard (`python src/app.py`) that generates synthetic supply-chain telemetry, runs four detection engines over it, and presents all results in an auto-refreshing browser UI. No cloud, no database, no npm.

## How It Works

1. **Data layer (`src/data.py`):** Generates a deterministic set of 15 shipments and 12 fleet vehicles using Python's `random` module with a fixed seed. Each shipment has an origin, destination, carrier, status (on_time / delayed / blocked), ETA, and current location. Each fleet vehicle has a type (truck / reefer / van), status (active / idle / maintenance), idle hours, and — for reefer units — a current temperature and an allowed band.

2. **Engine layer (`src/engine.py`):** Four pure functions apply rules to the raw data:
   - `detect_disruptions()` — filters shipments by status
   - `recommend_reroutes()` — looks up a pre-built alternate-route table keyed on (origin, destination)
   - `detect_idle_fleet()` — filters vehicles by status and idle hours threshold
   - `detect_cold_chain_alerts()` — flags reefer vehicles outside their temperature band

3. **Server layer (`src/app.py`):** A Python `http.server.HTTPServer` subclass that serves the dashboard HTML at `GET /` and a fresh JSON snapshot at `GET /api/status` on every request.

4. **UI layer (`src/dashboard.html`):** A single self-contained HTML file with inline CSS and vanilla JS. Polls `/api/status` every 10 seconds, populates KPI cards and five data tables, and applies colour-coded badges for status and alert severity.

## Architecture Diagram

```
Browser
  │
  ├── GET /          ──▶  app.py  ──▶  dashboard.html (served as static file)
  │
  └── GET /api/status ──▶ app.py
                              │
                        data.py (generate_shipments, generate_fleet)
                              │
                        engine.py (run_all)
                              │
                         JSON response
                              │
                    dashboard.html (fetch + DOM update)
```

## Key Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Language | Python 3 stdlib only | No install step; runs anywhere Python is present |
| UI | Single HTML file, vanilla JS | No build step, no CDN, fully offline |
| Data | In-memory, fixed seed | Reproducible demos; no file I/O or DB required |
| Rerouting | Lookup table | Deterministic, auditable, zero ML dependency |
| Refresh | 10-second client poll | Simple; no WebSocket or SSE infrastructure needed |

## IBM Technologies Used

IBM Bob was used as an AI pair-programming assistant throughout development — helping plan module boundaries, review logic, and draft documentation.
