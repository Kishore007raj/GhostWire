#this is for creating models using sqllite for storing agent data

#this table is for storing network connection data
CONNECTION_TABLE = """
CREATE TABLE connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL,
    pid INTEGER,
    process_name TEXT,
    exe TEXT,
    username TEXT,
    create_time REAL,
    local_ip TEXT,
    local_port INTEGER,
    remote_ip TEXT,
    remote_port INTEGER,
    protocol TEXT,
    status TEXT,
    bytes_sent INTEGER,
    bytes_recv INTEGER
);
"""
#this table is for storing bandwidth summary data
BANDWIDTH_TABLE =  """
CREATE TABLE bandwidth_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL,
    pid INTEGER,
    process_name TEXT,
    exe TEXT,
    bytes_sent INTEGER,
    bytes_recv INTEGER,
    interval REAL
);
"""