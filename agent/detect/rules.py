import time

# ============================================================================
# STEP-1-TRUSTED EXECUTABLE LOCATIONS
# ============================================================================
# These paths represent legitimate system executables locations on Windows.
# Any executable originating from outside these paths is considered suspicious.
# This helps identify potentially malicious or untrusted binaries running on
# the system, which is a critical indicator of compromise or exploitation.
SYSTEM_PATH_PREFIXES = (
    "C:\\Windows\\",
    "C:\\Program Files\\",
    "C:\\Program Files (x86)\\",
)

# ============================================================================
# STATEFUL TRACKERS
# ============================================================================
# These global dictionaries maintain state across rule evaluations to enable
# detection of anomalous patterns based on historical behavior.

# Tracks which remote destinations each process has connected to.
# Used to detect when a process connects to a new, previously unseen IP address.
# Structure: (process_name, exe) -> set(remote_ip)
_seen_destinations = {}

# Tracks the most recent network activity timestamp for each process ID.
# Used to identify processes that suddenly become active after long idle periods,
# which could indicate malware activation or backdoor command execution.
# Structure: pid -> last_timestamp
_last_activity = {}

# Tracks timestamps of connection attempts for each process.
# Used to identify rapid connection patterns that may indicate scanning,
# flooding attacks, or botnet command & control communication.
# Structure: pid -> list[timestamps]
_connection_counts = {}


# ============================================================================
# RULE 1: UNKNOWN EXECUTABLE DETECTION
# ============================================================================
def rule_unknown_executable(record):
    """
    Detect executables running from untrusted/non-standard locations.
    
    PURPOSE:
    Identifies processes that are not installed in standard system directories.
    This is critical for detecting:
    - Malware disguised as legitimate processes
    - Unauthorized installations
    - Exploits that drop payloads to temporary/unusual locations
    
    WHY NEEDED:
    Malware often avoids standard installation paths. Most legitimate applications
    install to Program Files or system directories. Any deviation is highly suspicious.
    
    SEVERITY: HIGH
    This is a direct indicator of potential malicious activity and should be
    investigated immediately.
    """
    exe = record.get("exe")
    if not exe:
        return None

    if not exe.startswith(SYSTEM_PATH_PREFIXES):
        return {
            "rule": "unknown_executable",
            "severity": "high",
            "reason": f"Executable outside trusted paths: {exe}"
        }

    return None


# ============================================================================
# RULE 2: NEW DESTINATION DETECTION
# ============================================================================
def rule_new_destination(record):
    """
    Detect when a process connects to a new, previously unseen remote IP.
    
    PURPOSE:
    Identifies when established processes suddenly connect to new destinations.
    This can indicate:
    - Compromised process making malicious connections
    - Lateral movement in a network breach
    - Command & control (C2) communication
    
    WHY NEEDED:
    Legitimate applications typically connect to a consistent set of servers.
    New connections from known processes are unusual and warrant investigation.
    This rule establishes a baseline of expected behavior per process.
    
    SEVERITY: MEDIUM
    New connections aren't inherently malicious but represent deviation from
    established patterns that requires investigation.
    """
    key = (record["process_name"], record["exe"])
    dest = record["remote_ip"]

    seen = _seen_destinations.setdefault(key, set())

    if dest not in seen and seen:
        seen.add(dest)
        return {
            "rule": "new_destination",
            "severity": "medium",
            "reason": f"Process connected to a new destination: {dest}"
        }

    seen.add(dest)
    return None


# ============================================================================
# RULE 3: HIGH BANDWIDTH USAGE DETECTION
# ============================================================================
def rule_high_bandwidth(record, threshold_bytes=5_000_000):
    """
    Detect unusually high data transfer volumes in a single network interval.
    
    PURPOSE:
    Identifies processes consuming abnormal amounts of bandwidth, which may indicate:
    - Data exfiltration/theft
    - Tunneling of internal network traffic
    - Cryptomining or distributed computing malware
    - DDoS attack origination
    
    WHY NEEDED:
    Normal applications have predictable bandwidth patterns. Sudden spikes warrant
    investigation. The threshold (5MB) is configurable to match your organization's
    baseline expectations. Fine-tune based on your environment's normal patterns.
    
    SEVERITY: MEDIUM
    High bandwidth usage could have legitimate explanations but is worth monitoring
    as it can indicate data exfiltration or other malicious activity.
    
    PARAMETERS:
    - threshold_bytes: The bandwidth threshold in bytes. Default is 5MB per interval.
    """
    if record["bytes_sent"] > threshold_bytes or record["bytes_recv"] > threshold_bytes:
        return {
            "rule": "high_bandwidth",
            "severity": "medium",
            "reason": "Unusually high bandwidth usage in a short interval"
        }

    return None


# ============================================================================
# RULE 4: IDLE PROCESS REACTIVATION DETECTION
# ============================================================================
def rule_idle_process_activity(record, idle_seconds=300):
    """
    Detect when a process sends network traffic after a prolonged idle period.
    
    PURPOSE:
    Identifies dormant processes that suddenly become active, which may indicate:
    - Malware activation triggered by external commands
    - Backdoor listening for remote commands (C2 beacon)
    - Scheduled malicious activity (based on timers/triggers)
    - Process hijacking - legitimate app repurposed by attacker
    
    WHY NEEDED:
    Many legitimate services and background processes send traffic on predictable
    schedules. A process that's been silent for 5+ minutes suddenly sending traffic
    is anomalous and suggests external triggering or compromise.
    
    SEVERITY: MEDIUM
    Idle reactivation is particularly suspicious for processes that should be
    continuously active (like services) or never active (like installers).
    
    PARAMETERS:
    - idle_seconds: The idle threshold in seconds. Default is 300 seconds (5 minutes).
    """
    pid = record["pid"]
    now = record["timestamp"]

    last = _last_activity.get(pid)
    _last_activity[pid] = now

    if last and (now - last) > idle_seconds:
        return {
            "rule": "idle_activity",
            "severity": "medium",
            "reason": "Process sent network data after a long idle period"
        }

    return None


# ============================================================================
# RULE 5: REPEATED CONNECTION ATTEMPTS DETECTION
# ============================================================================
def rule_repeated_connections(record, window_seconds=60, threshold=10):
    """
    Detect when a process makes multiple rapid connection attempts.
    
    PURPOSE:
    Identifies processes making numerous connection attempts in a short timeframe,
    which can indicate:
    - Port/network scanning
    - Botnet spreading (trying multiple targets)
    - Brute force attacks against internal services
    - Mass spreading of exploits or malware
    
    WHY NEEDED:
    Normal applications connect to a small set of known servers. Rapid firing of
    connections is abnormal and suggests automated attack behavior. This is
    particularly effective at detecting lateral movement and self-propagating malware.
    
    SEVERITY: LOW
    While rapid connections are suspicious, they're less immediately dangerous than
    unknown executables. However, when combined with other rules, this indicates
    active attack behavior (worm/botnet spreading).
    
    PARAMETERS:
    - window_seconds: The time window to analyze. Default is 60 seconds.
    - threshold: The connection count threshold. Default is 10 connections per window.
    """
    pid = record["pid"]
    now = record["timestamp"]

    timestamps = _connection_counts.setdefault(pid, [])
    timestamps.append(now)

    # Keep only recent timestamps within the time window
    _connection_counts[pid] = [t for t in timestamps if now - t <= window_seconds]

    if len(_connection_counts[pid]) > threshold:
        # Reset timestamps to avoid repeated spam from the same ongoing burst.
        _connection_counts[pid] = []
        return {
            "rule": "repeated_connections",
            "severity": "low",
            "reason": "Frequent repeated outbound connections in a short time window"
        }

    return None