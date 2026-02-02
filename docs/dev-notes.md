## `psutil.net_connections(kind='inet')` — topic-1

This function shows **all open network sockets on the system**.

It returns a **list of connection records**. Each record describes **one socket**.

### What each connection contains

* **fd**
  File descriptor for the socket.

  * Only useful for the *current process*.
  * On Windows and SunOS it’s always `-1`.

* **family**
  Address family:

  * `AF_INET` → IPv4
  * `AF_INET6` → IPv6
  * `AF_UNIX` → Unix domain socket

* **type**
  Socket type:

  * `SOCK_STREAM` → TCP
  * `SOCK_DGRAM` → UDP
  * `SOCK_SEQPACKET` → less common, Unix sockets

* **laddr (local address)**
  Where *your machine* is bound.

  * IP + port for internet sockets
  * File path for Unix sockets

* **raddr (remote address)**
  The peer on the other end.

  * IP + port if connected
  * Empty if not connected
  * For Unix sockets, often empty due to OS limits

* **status**
  TCP state like `ESTABLISHED`, `LISTEN`, `SYN_SENT`.

  * Always `CONN_NONE` for UDP and Unix sockets.

* **pid**
  Process ID that owns the socket.

  * Often `None` unless you run as root/admin.

---

### `kind` filter (what sockets you want)

| kind    | returns             |
| ------- | ------------------- |
| `inet`  | IPv4 + IPv6         |
| `inet4` | IPv4 only           |
| `inet6` | IPv6 only           |
| `tcp`   | all TCP             |
| `tcp4`  | TCP over IPv4       |
| `tcp6`  | TCP over IPv6       |
| `udp`   | all UDP             |
| `udp4`  | UDP over IPv4       |
| `udp6`  | UDP over IPv6       |
| `unix`  | Unix domain sockets |
| `all`   | everything          |

---

### Permissions and OS gotchas (important)

* **Linux**

  * Without root: some connections are silently skipped.
  * Result list may be incomplete.

* **macOS / AIX**

  * Requires root.
  * Otherwise `AccessDenied` is raised.

* **Solaris**

  * Unix sockets not supported.

* **Linux / BSD**

  * `raddr` for Unix sockets is always empty.

---

### Practical takeaway

* Use this to **inspect system-wide network activity**.
* Expect **missing data** unless running with elevated privileges.
* If you only care about *your process*, use `Process.net_connections()` instead.

---

That’s all you need in `dev-notes.md`.

Ghostwire is a local tool that shows which apps on your computer are secretly using the internet in the background.
It maps every outgoing network connection to the exact app that made it, flags unusual or suspicious behavior, and shows it in a simple dashboard.
It doesn’t block traffic, read data, or scan files. It just exposes what’s happening so you can decide.


# How Ghostwire Actually Works

Ghostwire is a **host-based outbound network visibility tool**.  
It runs locally on a user’s machine and continuously answers one question:

**“Which application is sending data to the internet right now, and should I care?”**

This section explains the full working of the project end-to-end, without shortcuts.

---

## 1. Core Idea

Every time an application sends data to the internet, the operating system creates:

- a **process** (the app)
- a **socket** (the network connection)
- an **outbound flow** (data leaving the machine)

Ghostwire **observes these three things and links them together**.

No guessing. No packet content inspection. No blocking.

---

## 2. High-Level Flow

