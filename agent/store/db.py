#this file is created for database related operations

import sqlite3
import os
from pathlib import Path
from agent.store.models import CONNECTION_TABLE, BANDWIDTH_TABLE, ALERT_TABLE

# Make DB_PATH absolute to avoid working directory issues
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')
DB_PATH = os.path.join(project_root, 'data', 'db', 'ghostwire.db')

#this class is for handling database operations
class GhostwireDB:
    #initialize the database connection
    def __init__(self):
        Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.__init__tables()

    #initialize database tables
    def __init__tables(self):
        cursor = self.conn.cursor()
        # Create tables if they don't exist. Do NOT drop existing tables to avoid
        # data loss on agent restart.
        cursor.execute(CONNECTION_TABLE)
        cursor.execute(BANDWIDTH_TABLE)
        cursor.execute(ALERT_TABLE)
        self.conn.commit()
    
    #insert a network connection record into the database
    def insert_connection(self, data):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO connections (
                timestamp, pid, process_name, exe, username, create_time,
                local_ip, local_port, remote_ip, remote_port, protocol,
                status, bytes_sent, bytes_recv
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data['timestamp'], data['pid'], data['process_name'], data['exe'],
            data['username'], data['create_time'], data['local_ip'], data['local_port'],
            data['remote_ip'], data['remote_port'], data['protocol'], data['status'],
            data['bytes_sent'], data['bytes_recv']
        )
        )
        # Do not commit here; caller (main loop) batches commits for efficiency.
        
   #insert a bandwidth summary record into the database 
    def insert_bandwidth_summary(self, bw: dict):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO bandwidth_summary (
                timestamp, pid, process_name, exe,
                bytes_sent, bytes_recv, interval
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            bw['timestamp'], bw['pid'], bw['process_name'], bw['exe'],
            bw['bytes_sent'], bw['bytes_recv'], bw['interval']
        )
        )
        # insertion is staged until commit()

    #insert an alert record into the database
    def insert_alert(self, alert: dict):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO alerts (
                timestamp, pid, process_name, exe,
                rule, severity, reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            alert['timestamp'], alert['pid'], alert['process_name'], alert['exe'],
            alert['rule'], alert['severity'], alert['reason']
        )
        )
        # insertion is staged until commit()
    
    #commit the current transaction
    def commit(self):
        self.conn.commit()
        