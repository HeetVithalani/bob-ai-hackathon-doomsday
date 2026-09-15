# 🚚 Supply Chain Disruption Assistant & Fleet Utilisation Optimizer

> **Team Doomsday — IBM Bob AI Hackathon | Problem L2**

---

## 👥 Team

| Field | Value |
|---|---|
| **Team Name** | Doomsday |
| **Track** | AI |
| **Team Lead** | Fenil Thumbar - d24dce149@charusat.edu.in|
| **Members** | Fenil Thumbar - d24dce149@charusat.edu.in|
              | Heet Vithalani - d24dce144@charusat.edu.in|
              | Dhruvil Bhavinbhai Patel - d24dce149@charusat.edu.in|
              | Jikadra meet p - -jikadrameet44@gmail.com|

---

## 🎯 Problem Statement

Supply chain managers face daily disruptions — delayed shipments, blocked routes, idle trucks sitting at depots, and refrigerated cargo drifting out of temperature band — but lack a single consolidated view to act on all of them at once. The result is missed SLAs, spoiled goods, and underutilised fleet assets.

---

## 💡 Solution

We built a local, zero-dependency Python dashboard that ingests synthetic supply-chain telemetry, runs rule-based detection across four disruption categories, and surfaces actionable recommendations in a live auto-refreshing web UI. A logistics operator opens one browser tab and immediately sees every disrupted shipment, its recommended reroute, every idle vehicle, and every cold-chain temperature breach — no cloud, no database, no install step beyond `python src/app.py`.

---

## ✨ Key Features

- **Shipment Disruption Detection:** Automatically flags delayed and blocked shipments from the live telemetry feed.
- **Rerouting Recommendations:** For each disrupted shipment, suggests a specific alternate route with a plain-English reason.
- **Idle Fleet Detection:** Identifies vehicles idle beyond a configurable threshold and shows their last known location.
- **Cold-Chain Temperature Alerts:** Monitors reefer truck temperatures and raises directional alerts (too high / too low) on any breach.
- **Live Dashboard:** Single-page auto-refreshing UI with KPI summary cards and colour-coded status tables — no external JS dependencies.

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Languages** | Python 3.x |
| **Frameworks** | Python `http.server` (stdlib), Vanilla JS |
| **IBM Technologies** | IBM Bob (AI assistant used during development) |
| **Databases** | None — in-memory synthetic data |
| **Other** | HTML5, CSS3 |

---

## 📁 Repository Structure

```
├── src/
│   ├── app.py            # HTTP server (stdlib http.server)
│   ├── data.py           # Synthetic data generator
│   ├── engine.py         # Detection & recommendation logic
│   └── dashboard.html    # Single-page dashboard UI
├── docs/
│   ├── problem-statement.md
│   ├── solution-overview.md
│   ├── architecture.md
│   └── setup-guide.md
├── demo/
│   ├── screenshots/
│   └── demo-video-link.txt
├── presentation/
└── submission.yaml
```

---

## ⚡ How to Run

```bash
# 1. Clone the repo
git clone https://github.com/heetvitalani/bob-ai-hackathon-doomsday.git
cd bob-ai-hackathon-doomsday

# 2. No dependencies to install — Python stdlib only

# 3. Run the server
python src/app.py

# 4. Open the dashboard
#    http://localhost:8000
```

Requires **Python 3.7+** only. No `pip install` needed.

---

## 🖥️ Demo

| Artifact | Link |
|---|---|
| 📹 Demo Video | [See demo/demo-video-link.txt](demo/demo-video-link.txt) |
| 🌐 Live Demo | [See demo/live-demo-url.txt](demo/live-demo-url.txt) |
| 🖼️ Screenshots | [See demo/screenshots/](demo/screenshots/) |
| 📊 Presentation | [See presentation/](presentation/) |

---

## ⚠️ Known Limitations

- All data is synthetic and deterministic — not connected to real shipment systems.
- Reroute recommendations are rule-based (lookup table), not ML-driven.
- No authentication or multi-user support — single-user local tool only.
- Tested on Python 3.9–3.12 and Chrome/Firefox.

---

## 🏅 What We're Most Proud Of

The entire solution runs with `python src/app.py` — zero pip installs, zero config, zero cloud dependencies. Despite that constraint, it surfaces all five required capabilities (disruption detection, rerouting, idle fleet, cold-chain alerts, dashboard) in a clean, readable UI that auto-refreshes every 10 seconds. The separation between `data.py`, `engine.py`, and `app.py` also makes it straightforward to swap in real data sources later.
