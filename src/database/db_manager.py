import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any

class DatabaseManager:
    def __init__(self, db_path: str = "railway_section.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database with all required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create Train table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Train (
                train_id INTEGER PRIMARY KEY,
                train_no VARCHAR(20) NOT NULL,
                train_type TEXT CHECK(train_type IN ('Superfast', 'Express', 'Passenger', 'Freight')) NOT NULL,
                priority INTEGER NOT NULL,
                current_status TEXT CHECK(current_status IN ('On Time', 'Delayed', 'Halted')) NOT NULL,
                delay_minutes INTEGER DEFAULT 0,
                crew_status VARCHAR(255),
                loco_health VARCHAR(255),
                linked_train_id INTEGER,
                FOREIGN KEY (linked_train_id) REFERENCES Train(train_id)
            )
        ''')
        
        # Create Section table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Section (
                section_id INTEGER PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                track_type TEXT CHECK(track_type IN ('Single Line', 'Double Line')) NOT NULL,
                congestion_level TEXT CHECK(congestion_level IN ('Low', 'Medium', 'High')) NOT NULL,
                block_status TEXT CHECK(block_status IN ('Free', 'Occupied', 'Under Maintenance')) NOT NULL,
                power_status TEXT CHECK(power_status IN ('Normal', 'Power Block', 'Tripped')) NOT NULL,
                signal_status TEXT CHECK(signal_status IN ('Normal', 'Failure', 'Manual Working')) NOT NULL,
                weather_condition TEXT CHECK(weather_condition IN ('Clear', 'Fog', 'Rain', 'Storm')) NOT NULL
            )
        ''')
        
        # Create Station table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Station (
                station_id INTEGER PRIMARY KEY,
                section_id INTEGER NOT NULL,
                num_platforms INTEGER NOT NULL,
                yard_capacity INTEGER NOT NULL,
                current_occupancy INTEGER DEFAULT 0,
                special_facility VARCHAR(255),
                FOREIGN KEY (section_id) REFERENCES Section(section_id)
            )
        ''')
        
        # Create ExternalFactors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ExternalFactors (
                factor_id INTEGER PRIMARY KEY,
                section_id INTEGER NOT NULL,
                type TEXT CHECK(type IN ('Festival', 'Strike', 'Exam Rush', 'Natural Disaster')) NOT NULL,
                severity TEXT CHECK(severity IN ('Low', 'Medium', 'High')) NOT NULL,
                remarks TEXT,
                FOREIGN KEY (section_id) REFERENCES Section(section_id)
            )
        ''')
        
        # Create Incidents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Incidents (
                incident_id INTEGER PRIMARY KEY,
                train_id INTEGER,
                section_id INTEGER NOT NULL,
                type TEXT CHECK(type IN ('Accident', 'Derailment', 'Level Crossing', 'Fire', 'Security', 'Technical Failure')) NOT NULL,
                timestamp DATETIME NOT NULL,
                resolution TEXT,
                FOREIGN KEY (train_id) REFERENCES Train(train_id),
                FOREIGN KEY (section_id) REFERENCES Section(section_id)
            )
        ''')
        
        # Create Decisions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Decisions (
                decision_id INTEGER PRIMARY KEY,
                issue_id INTEGER,
                section_id INTEGER NOT NULL,
                controller_action TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                outcome TEXT CHECK(outcome IN ('Resolved', 'Partially Resolved', 'Escalated')) NOT NULL,
                FOREIGN KEY (section_id) REFERENCES Section(section_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dictionaries"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT query and return the last row ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        last_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return last_id
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an UPDATE/DELETE query and return the number of affected rows"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        return affected_rows
