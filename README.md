# Ghostwire

Ghostwire is a **host-based outbound network monitoring tool** that shows which applications on your system are communicating with the internet, where they are sending data, and whether that behavior looks normal or suspicious.

It focuses on **visibility, attribution, and clarity** — not blocking traffic, not deep packet inspection, and not antivirus behavior.

---

## Problem Statement

Many applications initiate background network communication without user awareness.

Most users do not know:
- which application is sending data
- where the data is going
- whether that activity is expected or dangerous

Existing tools are either:
- too technical
- noisy and raw
- blocking-focused without explanation
- designed for enterprises, not individuals

There is no simple, local tool that clearly maps **application → destination → behavior**.

Ghostwire exists to fill that gap.

---

## Objective

Build a **local-first, privacy-friendly watchdog** that:

- Monitors outbound network activity
- Maps traffic to the exact application responsible
- Flags unexpected or suspicious behavior
- Presents the information in a clear, human-readable way

All analysis happens **on the user’s machine**.  
No cloud. No telemetry. No data exfiltration.

---

## What Ghostwire Does (In Scope)

### Core Capabilities

- Monitor **outbound** network connections
- Map network sockets to running processes
- Track data usage per application
- Detect suspicious or unexpected behavior
- Generate local alerts
- Provide a real-time visual summary

### Key Features

- **Process-to-Network Mapping**
  - Identify the exact app responsible for traffic
- **Top Talkers**
  - Apps consuming the most bandwidth
- **Anomaly Detection**
  - Rule-based detection of unusual behavior
- **Local Dashboard**
  - Real-time view of app activity
- **Structured Logs**
  - CSV and JSON exports for analysis

---

## What Ghostwire Does NOT Do (Out of Scope)

- ❌ Block connections (not a firewall)
- ❌ Inspect packet payloads (no DPI)
- ❌ Scan files for malware
- ❌ Act as an antivirus or IDS
- ❌ Monitor inbound traffic

Ghostwire is **visibility-first**, not prevention-first.

---

## Target Users

- Privacy-conscious individuals
- Security-focused users
- Remote workers / home office users
- Software developers testing network behavior
- IT administrators in small-to-medium environments

---

## System Architecture

Ghostwire follows a **lightweight, host-centric architecture**.

### Components

- OS-level outbound traffic monitoring
- Process-to-socket correlation
- Rule-based anomaly detection
- Local severity scoring
- Optional local web dashboard

All components run locally.

---

## Tech Stack

### Core

- **Language:** Python 3.10+
- **Process Mapping:** `psutil`
- **Packet / Connection Data:** OS-native APIs, Scapy / PyShark (optional)

### Backend

- **API:** FastAPI
- **Real-Time:** WebSockets
- **Storage:** SQLite (local, WAL mode)

### Frontend

- **Framework:** React / Next.js
- **Charts:** Chart.js / Recharts

### Output & Alerts

- OS notifications
- CSV exports
- JSON logs

---

## Detection Coverage

Ghostwire can detect:

- Apps sending data without user interaction
- Unknown or suspicious executables communicating externally
- Very high background data usage
- Repeated short-lived connections (tracking-like behavior)
- Inactive apps suddenly transmitting data
- New destinations contacted by existing apps

---

## Security & Privacy Design

- Runs only on the local system
- No cloud connection
- No payload inspection
- No external APIs required
- All data stored locally
- Minimal permissions beyond OS requirements

---

## Setup & Usage

1. Install Ghostwire as a local agent
2. Start monitoring via CLI or service mode
3. Network activity is tracked in real time
4. Alerts are generated using defined rules
5. Dashboard shows live application activity

No account. No login. No cloud dependency.

---

## Project Structure

ghostwire/
├── agent/
│ ├── capture/ # network capture
│ ├── process/ # PID ↔ socket mapping
│ ├── detect/ # anomaly rules
│ ├── store/ # SQLite storage
│ ├── models/ # data models
│ └── main.py # agent loop
├── backend/
│ ├── api.py # FastAPI endpoints
│ ├── ws.py # WebSocket streaming
│ └── db.py # DB access
├── frontend/ # React dashboard
├── data/ # local data
├── docs/ # design notes
└── README.md

---

## Expected Outcomes (MVP)

- Reliable process-to-network correlation
- High-signal suspicious traffic alerts
- Clear, readable activity summaries
- Minimal false positives
- Stable long-running local agent

---

## Key Challenges & Constraints

- No traffic blocking
- No file scanning
- No payload inspection
- No ML in MVP
- Approximate bandwidth attribution is acceptable

Correctness and clarity matter more than completeness.

---

## Future Scope

- Adaptive baseline learning
- Policy-based allowlists
- Lightweight ML-assisted scoring
- Cross-host aggregation for SMEs
- SIEM integration
- Windows and macOS support

---

## References (Study, Not Copy)

- VolkanSah / Monitoring-outgoing-connections
- WhoYouCalling
- BPFView
- netproc
- network-security-monitor
- psutil documentation
- FastAPI WebSocket guides

---

## Philosophy

Ghostwire is not trying to see *everything*.  
It is trying to show **the right things**.

Visibility over noise.  
Local over cloud.  
Understanding over blind blocking.
