import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db_manager import DatabaseManager
from datetime import datetime, timedelta
import random

class DataPopulator:
    def __init__(self):
        self.db = DatabaseManager()
    
    def populate_all_data(self):
        """Populate all tables with sample data"""
        print("Populating database with sample data...")
        
        # Clear existing data
        self.clear_all_data()
        
        # Populate in dependency order
        self.populate_sections()
        self.populate_stations()
        self.populate_trains()
        self.populate_external_factors()
        self.populate_incidents()
        self.populate_decisions()
        
        print("Sample data population completed!")
    
    def clear_all_data(self):
        """Clear all existing data"""
        tables = ['Decisions', 'Incidents', 'ExternalFactors', 'Station', 'Train', 'Section']
        for table in tables:
            self.db.execute_update(f"DELETE FROM {table}")
        print("Cleared existing data")
    
    def populate_sections(self):
        """Populate Section table"""
        sections_data = [
            (1, "SEC-A-Delhi-Ghaziabad", "Double Line", "Medium", "Occupied", "Normal", "Normal", "Clear"),
            (2, "SEC-B-Ghaziabad-Moradabad", "Single Line", "High", "Occupied", "Normal", "Failure", "Fog"),
            (3, "SEC-C-Moradabad-Bareilly", "Double Line", "Low", "Free", "Power Block", "Manual Working", "Rain")
        ]
        
        for data in sections_data:
            query = '''INSERT INTO Section 
                      (section_id, name, track_type, congestion_level, block_status, 
                       power_status, signal_status, weather_condition) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
            self.db.execute_insert(query, data)
        print(f"Populated {len(sections_data)} sections")
    
    def populate_stations(self):
        """Populate Station table"""
        stations_data = [
            (101, 1, 6, 12, 8, "Relief Loco Available"),
            (102, 1, 4, 8, 5, "Crew Base"),
            (201, 2, 3, 6, 6, "Limited Facilities"),
            (202, 2, 2, 4, 3, None),
            (301, 3, 5, 10, 2, "Maintenance Depot"),
            (302, 3, 3, 6, 1, None)
        ]
        
        for data in stations_data:
            query = '''INSERT INTO Station 
                      (station_id, section_id, num_platforms, yard_capacity, 
                       current_occupancy, special_facility) 
                      VALUES (?, ?, ?, ?, ?, ?)'''
            self.db.execute_insert(query, data)
        print(f"Populated {len(stations_data)} stations")
    
    def populate_trains(self):
        """Populate Train table with 15 trains"""
        trains_data = [
            # Superfast trains (Priority 1)
            (1001, "12951", "Superfast", 1, "On Time", 0, "Fresh Crew", "Good", None),
            (1002, "12952", "Superfast", 1, "Delayed", 25, "Tired Crew", "Fair", None),
            (1003, "12003", "Superfast", 1, "On Time", 0, "Fresh Crew", "Excellent", None),
            
            # Express trains (Priority 2)
            (2001, "15707", "Express", 2, "Delayed", 15, "Fresh Crew", "Good", None),
            (2002, "15708", "Express", 2, "On Time", 0, "Fresh Crew", "Good", None),
            (2003, "14005", "Express", 2, "Halted", 45, "Crew Change Required", "Poor", None),
            (2004, "14006", "Express", 2, "Delayed", 30, "Fresh Crew", "Fair", None),
            
            # Passenger trains (Priority 3)
            (3001, "54251", "Passenger", 3, "On Time", 0, "Local Crew", "Good", None),
            (3002, "54252", "Passenger", 3, "Delayed", 10, "Local Crew", "Fair", None),
            (3003, "54253", "Passenger", 3, "On Time", 0, "Local Crew", "Good", None),
            (3004, "54254", "Passenger", 3, "Delayed", 20, "Local Crew", "Good", None),
            
            # Freight trains (Priority 4)
            (4001, "FRT001", "Freight", 4, "Halted", 60, "Fresh Crew", "Good", None),
            (4002, "FRT002", "Freight", 4, "Delayed", 90, "Tired Crew", "Fair", 4003),
            (4003, "FRT003", "Freight", 4, "Delayed", 90, "Tired Crew", "Fair", 4002),
            (4004, "FRT004", "Freight", 4, "On Time", 0, "Fresh Crew", "Good", None)
        ]
        
        for data in trains_data:
            query = '''INSERT INTO Train 
                      (train_id, train_no, train_type, priority, current_status, 
                       delay_minutes, crew_status, loco_health, linked_train_id) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            self.db.execute_insert(query, data)
        print(f"Populated {len(trains_data)} trains")
    
    def populate_external_factors(self):
        """Populate ExternalFactors table"""
        factors_data = [
            (1, 1, "Festival", "High", "Diwali rush - expect 30% more passenger traffic"),
            (2, 2, "Strike", "Medium", "Local transport strike affecting crew availability"),
            (3, 3, "Natural Disaster", "Low", "Recent flooding cleared, track inspected and safe")
        ]
        
        for data in factors_data:
            query = '''INSERT INTO ExternalFactors 
                      (factor_id, section_id, type, severity, remarks) 
                      VALUES (?, ?, ?, ?, ?)'''
            self.db.execute_insert(query, data)
        print(f"Populated {len(factors_data)} external factors")
    
    def populate_incidents(self):
        """Populate Incidents table"""
        base_time = datetime.now() - timedelta(hours=2)
        incidents_data = [
            (1, 2003, 2, "Technical Failure", base_time, "Brake failure resolved, train cleared for movement"),
            (2, None, 2, "Level Crossing", base_time + timedelta(minutes=30), "Gate jam cleared, normal operations resumed"),
            (3, 4001, 1, "Security", base_time + timedelta(hours=1), "Security check completed, train released"),
            (4, None, 3, "Fire", base_time + timedelta(hours=1, minutes=30), "Track-side fire extinguished, line clear")
        ]
        
        for data in incidents_data:
            query = '''INSERT INTO Incidents 
                      (incident_id, train_id, section_id, type, timestamp, resolution) 
                      VALUES (?, ?, ?, ?, ?, ?)'''
            self.db.execute_insert(query, data)
        print(f"Populated {len(incidents_data)} incidents")
    
    def populate_decisions(self):
        """Populate Decisions table with historical decisions"""
        base_time = datetime.now() - timedelta(hours=3)
        decisions_data = [
            (1, 1, 1, "Priority given to Superfast 12951, held Freight FRT001 at station", 
             base_time, "Resolved"),
            (2, 2, 2, "Diverted Express 14005 to loop line due to signal failure, arranged crew change", 
             base_time + timedelta(minutes=45), "Partially Resolved"),
            (3, 3, 1, "Coordinated with adjacent section for power restoration, held all trains temporarily", 
             base_time + timedelta(hours=1), "Resolved"),
            (4, 4, 2, "Arranged alternate route for passenger trains due to gate jam at level crossing", 
             base_time + timedelta(hours=1, minutes=30), "Resolved"),
            (5, None, 3, "Implemented speed restriction due to track-side fire, all trains to proceed cautiously", 
             base_time + timedelta(hours=2), "Resolved")
        ]
        
        for data in decisions_data:
            query = '''INSERT INTO Decisions 
                      (decision_id, issue_id, section_id, controller_action, timestamp, outcome) 
                      VALUES (?, ?, ?, ?, ?, ?)'''
            self.db.execute_insert(query, data)
        print(f"Populated {len(decisions_data)} decisions")

if __name__ == "__main__":
    populator = DataPopulator()
    populator.populate_all_data()
