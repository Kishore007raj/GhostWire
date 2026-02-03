#this file is created for database related operations

import sqlite3
import os
from pathlib import Path
from agent.store.models import CONNECTION_TABLE, BANDWIDTH_TABLE

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
        cursor.execute("DROP TABLE IF EXISTS connections;")
        cursor.execute(CONNECTION_TABLE)
        cursor.execute("DROP TABLE IF EXISTS bandwidth_summary;")
        cursor.execute(BANDWIDTH_TABLE)
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
    
    #commit the current transaction
    def commit(self):
        self.conn.commit()
        