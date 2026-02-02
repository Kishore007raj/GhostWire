# Ghostwire

Ghostwire is a **local, host-based outbound network visibility tool**.  
It shows **which application is talking to the internet**, **where it is talking**, and **whether that behavior makes sense**.

Ghostwire does not block traffic, inspect packet contents, or act like an antivirus.  
It exists to expose background network behavior that usually stays invisible.

---

## Problem

Modern applications routinely send data in the background.

Users usually have no idea:

- which app is sending data
- which server or country it is talking to
- whether the traffic is normal, excessive, or suspicious

Existing tools fail because they:

- dump raw network data with no attribution
- block traffic without explaining why
- require enterprise-level knowledge
- prioritize control over understanding

There is no simple local tool that answers:
**“Which app is doing this, and should I care?”**

Ghostwire answers exactly that.

---

## Goal

Build a **local-first network watchdog** that:

- Monitors outbound connections only
- Accurately maps traffic to the responsible process
- Detects unexpected or suspicious behavior
- Explains findings clearly to the user

All analysis happens **on the machine itself**.  
No cloud. No telemetry. No external data sharing.

---

## What Ghostwire Does

### Core Functions

- Monitor outbound network connections
- Correlate sockets to running processes
- Track per-application data usage
- Detect anomalous background behavior
- Generate local alerts
- Present activity in a clean dashboard

### Key Capabilities

- **Process ↔ Network Attribution**  
  Every connection is tied to a specific executable

- **Top Talkers**  
  Identify apps consuming the most bandwidth

- **Rule-Based Anomaly Detection**  
  Detect behavior that deviates from normal usage

- **Live Visibility**  
  Real-time view of active and background traffic

- **Structured Output**  
  CSV and JSON exports for auditing or debugging

---

## What Ghostwire Does NOT Do

Ghostwire is intentionally narrow in scope.

It does **not**:

- Block or filter traffic
- Inspect packet payloads
- Scan files for malware
- Act as a firewall, IDS, or antivirus
- Monitor inbound connections

Ghostwire prioritizes **visibility and attribution**, not enforcement.

---

## Intended Users

- Privacy-focused individuals
- Security-conscious users
- Remote and home-office workers
- Developers debugging network behavior
- Small-to-medium IT teams needing local visibility

---

## Architecture Overview

Ghostwire uses a **lightweight, host-centric design**.

### Main Components

- OS-level outbound connection monitoring
- Process-to-socket correlation
- Rule-based anomaly engine
- Local severity scoring
- Optional local web dashboard

Everything runs locally.  
Nothing is shipped off-device.

---

## Technical Stack

### Core

- **Language:** Python 3.10+
- **Process Mapping:** `psutil`
- **Connection Data:** OS-native APIs  
  (Scapy / PyShark optional for metadata)

### Backend

- **API:** FastAPI
- **Real-Time Streaming:** WebSockets
- **Storage:** SQLite (local, WAL mode)

### Frontend

- **Framework:** React / Next.js
- **Visualization:** Chart.js / Recharts

### Alerts & Output

- OS-level notifications
- CSV exports
- JSON logs

---

## Detection Coverage

Ghostwire can identify:

- Applications sending data without user interaction
- Unknown or unsigned executables making outbound connections
- Excessive background bandwidth usage
- Repeated short-lived connections (tracking-like behavior)
- Inactive apps suddenly transmitting data
- New or rare destinations contacted by known apps

Detection is **explainable and rule-driven**, not opaque.

---

## Security & Privacy Design

- Runs only on the local machine
- No cloud services
- No payload inspection
- No external threat feeds required
- All data stored locally
- Uses only necessary OS permissions

Ghostwire cannot spy on the user — by design.

---

## Setup & Usage

1. Install Ghostwire as a local agent
2. Start it via CLI or service mode
3. Outbound traffic is monitored continuously
4. Alerts trigger when rules are violated
5. Dashboard shows live application activity

No accounts.  
No logins.  
No internet dependency.

---

## Project Structure

```text
ghostwire/
├── agent/
│   ├── capture/     # outbound connection tracking
│   ├── process/     # PID ↔ socket correlation
│   ├── detect/      # anomaly rules
│   ├── store/       # SQLite persistence
│   ├── models/      # shared data models
│   └── main.py      # agent loop
├── backend/
│   ├── api.py       # FastAPI endpoints
│   ├── ws.py        # WebSocket streams
│   └── db.py        # database access
├── frontend/        # React dashboard
├── data/            # local runtime data
├── docs/            # design notes
└── README.md
```

---

## MVP Outcomes

- Correct and stable process-to-network mapping
- High-signal alerts with clear explanations
- Readable summaries of network behavior
- Minimal false positives
- Reliable long-running local agent

---

## Constraints

- No traffic blocking
- No file scanning
- No payload inspection
- No ML in MVP
- Approximate bandwidth attribution is acceptable

Correct attribution matters more than perfect precision.

---

## Future Work

- Adaptive behavioral baselines
- User-defined allowlists
- Lightweight ML-assisted scoring
- Cross-host aggregation for SMEs
- SIEM integration
- Expanded OS support (Windows / macOS)

---

## References (For Study)

- [Monitoring-outgoing-connections](https://github.com/VolkanSah/Monitoring-outgoing-connections)
- [WhoYouCalling](https://github.com/H4NM/WhoYouCalling)
- [BPFView](https://github.com/jnesss/bpfview)
- [netproc](https://github.com/berghetti/netproc)
- [network-security-monitor](https://github.com/rafi03/network-security-monitor)
- [psutil documentation](https://psutil.readthedocs.io/en/latest/)
- [FastAPI WebSocket guides](https://testdriven.io/blog/fastapi-postgres-websockets/)


---

## Design Philosophy

Ghostwire does not try to see everything.  
It tries to show **the right things**.

Visibility over noise.  
Local over cloud.  
Understanding over blind blocking.
