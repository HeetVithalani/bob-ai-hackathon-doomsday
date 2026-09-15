# Setup Guide

## Prerequisites

- [ ] **Python 3.7 or higher** — `python --version` or `python3 --version`
- [ ] **A modern web browser** — Chrome, Firefox, Edge, or Safari
- [ ] **Git** (to clone the repo)

No other tools, packages, or services are required.

## Environment Variables

None required. The app runs with zero configuration out of the box.

Optional override:

| Variable | Default | Description |
|---|---|---|
| `APP_PORT` | `8000` | Port the server listens on |

Example: `APP_PORT=9000 python src/app.py`

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/heetvitalani/bob-ai-hackathon-doomsday.git
cd bob-ai-hackathon-doomsday

# 2. No pip install needed — Python stdlib only
```

## Running the Application

```bash
python src/app.py
```

Expected output:
```
Supply Chain MVP running at http://localhost:8000
  Dashboard : http://localhost:8000/
  API       : http://localhost:8000/api/status
Press Ctrl-C to stop.
```

Then open **http://localhost:8000** in your browser.

## Verifying the API

```bash
# Verify the JSON endpoint (PowerShell)
Invoke-WebRequest -Uri http://localhost:8000/api/status | Select-Object -ExpandProperty Content

# Or with curl (if available)
curl http://localhost:8000/api/status
```

Expected: a JSON object with keys `summary`, `shipments`, `fleet`, `disruptions`, `reroutes`, `idle_vehicles`, `cold_chain_alerts`.

## Running Tests

No test runner is required. To smoke-test the modules directly:

```bash
# From the repo root
python -c "import sys; sys.path.insert(0,'src'); import data, engine; print(engine.run_all(data.generate_shipments(), data.generate_fleet())['summary'])"
```

Expected output (approximate):
```
{'total_shipments': 15, 'disruptions': 5, 'reroutes': 5, 'idle_vehicles': 3, 'cold_chain_alerts': 2, 'total_fleet': 12}
```

## Stopping the Server

Press **Ctrl-C** in the terminal where `app.py` is running.

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| `Address already in use` | Port 8000 is taken | `APP_PORT=8001 python src/app.py` |
| `ModuleNotFoundError: No module named 'data'` | Running from wrong directory | Run `python src/app.py` from the repo root |
| Browser shows blank page | JS fetch failed | Check terminal for errors; ensure server is running |
| `python` not found | Python not on PATH | Try `python3 src/app.py` |
