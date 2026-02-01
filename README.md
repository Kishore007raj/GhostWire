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
- Presents the information in a clear, human-r
