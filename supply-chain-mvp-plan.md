# Supply Chain Disruption Assistant & Fleet Utilisation Optimizer — MVP Plan

## Team: Doomsday | Problem: L2

---

## Top-Level Overview

Build a **minimal, fully local, zero-dependency-beyond-stdlib** Python + HTML dashboard that demonstrates five supply-chain capabilities using synthetic in-memory data:

1. **Shipment Disruption Detection** — flag delayed/blocked shipments
2. **Rerouting Recommendations** — suggest alternate routes for disrupted shipments
3. **Idle Fleet Detection** — surface vehicles sitting beyond a threshold
4. **Cold-Chain Temperature Alerts** — alert when a reefer vehicle breaches temperature band
5. **Simple Dashboard** — a single HTML page served by Python's built-in `http.server`, auto-refreshing with JSON data

**Constraints honoured:**
- `src/` is the only code directory (validate.yml checks `find src/ -type f`)
- `validate.yml` is untouched
- No required template files are deleted or renamed
- No cloud, database, or external API calls
- All data is synthetic Python dicts generated at startup (no CSV/DB files needed)
- Only Python stdlib (`http.server`, `json`, `threading`, `random`, `datetime`) — no pip installs required
- The validator checks `src/` has ≥ 1 file (excluding README.md and .env.example) — we put all code there

**Technology choices:**
| Layer | Choice | Reason |
|---|---|---|
| Language | Python 3.x stdlib only | No install step, cross-platform |
| UI | Single-file HTML + vanilla JS | No build step, no npm |
| Server | `http.server.HTTPServer` | Built into Python, zero deps |
| Data | In-memory Python dicts | No files to commit or parse |

---

## File Layout After Implementation

```
bob-ai-hackathon-doomsday/
├── src/
│   ├── app.py                  # HTTP server + all business logic
│   ├── data.py                 # Synthetic data generator
│   ├── engine.py               # Detection/recommendation logic
│   └── dashboard.html          # Single-page dashboard UI
├── docs/
│   ├── problem-statement.md    # Filled in (was template)
│   ├── solution-overview.md    # Filled in
│   ├── architecture.md         # Filled in
│   └── setup-guide.md          # Filled in (run instructions)
├── README.md                   # Placeholders replaced
├── submission.yaml             # All required fields filled
└── demo/
    └── demo-video-link.txt     # Placeholder updated to localhost note
```

---

## Sub-Tasks

---

### Sub-Task 1 — Synthetic Data Generator (`src/data.py`)

**Intent**
Create a Python module that produces deterministic-but-realistic fake supply chain data in memory on every call. This is the single source of truth for the entire app — no files, no DB, no external calls.

**Expected Outcomes**
- `generate_shipments()` returns a list of shipment dicts with fields: `id`, `origin`, `destination`, `carrier`, `status` (on_time | delayed | blocked), `eta_hours`, `current_location`, `route`
- `generate_fleet()` returns a list of vehicle dicts with fields: `id`, `type` (truck | reefer | van), `status` (active | idle | maintenance), `idle_hours`, `last_location`, `temperature_celsius` (None for non-reefer), `temp_min`, `temp_max`
- Data is seeded so results are reproducible across server restarts
- At least 15 shipments and 10 fleet vehicles

**Todo List**
- [ ] Create `src/data.py`
- [ ] Implement `generate_shipments()` with realistic city names, carrier IDs, statuses
- [ ] Implement `generate_fleet()` with reefer trucks carrying temperature values
- [ ] Seed `random` with a fixed seed for reproducibility
- [ ] Return plain Python dicts (JSON-serialisable)

**Relevant Context**
- `src/` directory already exists with only `README.md` and `.env.example`
- Must produce ≥ 1 non-README, non-.env.example file to pass `validate.yml` step 4

---

### Sub-Task 2 — Detection & Recommendation Engine (`src/engine.py`)

**Intent**
Pure-logic module that takes the raw data from `data.py` and applies rules to produce: disruption alerts, rerouting recommendations, idle fleet flags, and cold-chain temperature alerts. No I/O — just functions that transform dicts to result dicts.

**Expected Outcomes**
- `detect_disruptions(shipments)` → list of shipments where `status == "delayed"` or `status == "blocked"`
- `recommend_reroutes(disrupted_shipments)` → for each disrupted shipment, adds a `recommended_route` and `reason` key
- `detect_idle_fleet(fleet, idle_threshold_hours=4)` → list of vehicles where `status == "idle"` and `idle_hours >= threshold`
- `detect_cold_chain_alerts(fleet)` → list of reefer vehicles where `temperature_celsius` is outside `[temp_min, temp_max]`
- `run_all(shipments, fleet)` → returns a single dict `{ disruptions, reroutes, idle_vehicles, cold_chain_alerts }` — this is what the API endpoint returns

**Todo List**
- [ ] Create `src/engine.py`
- [ ] Implement `detect_disruptions()`
- [ ] Implement `recommend_reroutes()` with a simple rule-based alternate route lookup dict
- [ ] Implement `detect_idle_fleet()`
- [ ] Implement `detect_cold_chain_alerts()`
- [ ] Implement `run_all()` as the single aggregator

**Relevant Context**
- All inputs/outputs are plain dicts — no class hierarchy needed
- Reroute recommendations can be a simple lookup: `{ ("CityA","CityB"): "via CityC" }` — no external graph library

---

### Sub-Task 3 — HTTP Server & API (`src/app.py`)

**Intent**
A minimal Python HTTP server (stdlib `http.server`) that:
- Serves `dashboard.html` at `GET /`
- Serves a JSON snapshot at `GET /api/status` (calls `engine.run_all()` each request for fresh data)
- Serves static assets if needed

This is the entire backend — no framework, no install.

**Expected Outcomes**
- `python src/app.py` starts a server on `http://localhost:8000`
- `GET /` returns the HTML dashboard
- `GET /api/status` returns JSON: `{ shipments, fleet, disruptions, reroutes, idle_vehicles, cold_chain_alerts, generated_at }`
- Server logs requests to stdout
- Graceful `Ctrl-C` shutdown

**Todo List**
- [ ] Create `src/app.py`
- [ ] Subclass `BaseHTTPRequestHandler` with `do_GET`
- [ ] Route `/` → read and serve `dashboard.html`
- [ ] Route `/api/status` → call `data.generate_*` + `engine.run_all()` → JSON response
- [ ] Add `Content-Type` headers correctly (text/html, application/json)
- [ ] Use `if __name__ == "__main__"` block with `HTTPServer(("", 8000), ...)`
- [ ] Import `data` and `engine` from same package using relative or `sys.path` insert

**Relevant Context**
- `http.server.BaseHTTPRequestHandler` and `http.server.HTTPServer` are stdlib
- Dashboard HTML is at `src/dashboard.html` — server resolves path relative to its own `__file__`

---

### Sub-Task 4 — Dashboard HTML (`src/dashboard.html`)

**Intent**
A single self-contained HTML file that polls `/api/status` every 10 seconds and renders all five feature panels: disrupted shipments table, rerouting recommendations, idle fleet list, cold-chain alerts, and a summary KPI row at the top.

No npm, no build, no CDN (optional: one small inline CSS reset). Vanilla JS `fetch` + DOM manipulation only.

**Expected Outcomes**
- Page loads at `http://localhost:8000`
- KPI summary bar shows counts: Disruptions | Reroutes | Idle Vehicles | Temp Alerts
- Table of disrupted shipments (id, origin → destination, carrier, status, ETA)
- Table of rerouting recommendations (shipment id, current route, recommended route, reason)
- Table of idle fleet (vehicle id, type, idle hours, last location)
- Cold-chain alerts table (vehicle id, current temp, allowed range, breach direction)
- Auto-refreshes every 10 seconds with a "Last updated" timestamp
- Works in any modern browser with no JS dependencies

**Todo List**
- [ ] Create `src/dashboard.html`
- [ ] Write HTML structure with 5 sections + KPI cards at top
- [ ] Write inline CSS for a clean, readable layout (dark header, card sections)
- [ ] Write `fetchData()` JS function that calls `/api/status` and populates all tables
- [ ] Add `setInterval(fetchData, 10000)` + immediate call on load
- [ ] Add "Last updated" timestamp display
- [ ] Colour-code status badges: red for blocked, orange for delayed, green for on-time
- [ ] Make temperature alerts visually prominent (red background on breach row)

**Relevant Context**
- Data shape comes from `engine.run_all()` — match field names exactly
- No external JS libraries; no CDN calls (keeps it fully offline)

---

### Sub-Task 5 — Fill Template Files

**Intent**
Satisfy the `validate.yml` checks that are unrelated to code: replace README placeholders, fill `submission.yaml`, update `demo-video-link.txt`, and populate the four `docs/` markdown files with real project content.

**Expected Outcomes**
- `README.md` contains no `[Your Project Title Here]` or `[Your Team Name]` strings
- `submission.yaml` has all REQUIRED fields filled: `team.name`, `team.track`, `team.lead.name`, `team.lead.email`, `submission.title`, `problem_statement`, `solution_summary`, `key_features` (≥ 1)
- `team.track` is exactly `AI` (valid enum value)
- `demo/demo-video-link.txt` first line does not contain `your-demo-video-link-here`
- `docs/problem-statement.md`, `solution-overview.md`, `architecture.md`, `setup-guide.md` — all filled with real content

**Todo List**
- [ ] Edit `README.md`: replace all `[...]` placeholders with project-specific content
- [ ] Edit `submission.yaml`: fill team.name="Doomsday", track="AI", lead info, title, problem_statement, solution_summary, key_features, tech_stack
- [ ] Edit `demo/demo-video-link.txt`: replace placeholder with `http://localhost:8000` and a note
- [ ] Edit `docs/problem-statement.md` with real problem framing
- [ ] Edit `docs/solution-overview.md` with architecture description
- [ ] Edit `docs/architecture.md` with component diagram (ASCII/Mermaid)
- [ ] Edit `docs/setup-guide.md` with exact `python src/app.py` run steps and prerequisites

**Relevant Context**
- `validate.yml` step 5 reads `head -1 demo/demo-video-link.txt` — the very first line must not contain `your-demo-video-link-here`
- `validate.yml` step 6 greps README.md for literal strings `[Your Project Title Here]` and `[Your Team Name]`
- `team.track` must match regex `^(AI|DevOps|Sustainability|Open)$` exactly

---

## Validation Checklist

Before calling implementation complete, verify:

| Check | How |
|---|---|
| `validate.yml` step 1 — required files exist | All 7 files present |
| `validate.yml` step 2 — submission.yaml parseable | Valid YAML, no syntax errors |
| `validate.yml` step 3 — required fields filled | All 7 fields + track enum + ≥1 feature |
| `validate.yml` step 4 — src/ has code | `src/app.py`, `src/data.py`, `src/engine.py`, `src/dashboard.html` |
| `validate.yml` step 5 — demo video link updated | First line of `demo-video-link.txt` changed |
| `validate.yml` step 6 — README placeholders gone | No `[Your Project Title Here]` or `[Your Team Name]` |
| App runs | `python src/app.py` starts without error |
| Dashboard loads | `http://localhost:8000` returns HTML |
| API works | `http://localhost:8000/api/status` returns valid JSON |

---

## Implementation Order

Sub-tasks must be done in this order (each depends on the previous):

```
Sub-Task 1 (data.py)
       ↓
Sub-Task 2 (engine.py)  ← depends on data shapes from Sub-Task 1
       ↓
Sub-Task 3 (app.py)     ← depends on engine.run_all() from Sub-Task 2
       ↓
Sub-Task 4 (dashboard.html) ← depends on API shape from Sub-Task 3
       ↓
Sub-Task 5 (template files) ← independent but last, to avoid distraction
```

---

## Status Tracking

| Sub-Task | Status |
|---|---|
| 1 — Synthetic Data Generator | [ ] pending |
| 2 — Detection & Recommendation Engine | [ ] pending |
| 3 — HTTP Server & API | [ ] pending |
| 4 — Dashboard HTML | [ ] pending |
| 5 — Fill Template Files | [ ] pending |
