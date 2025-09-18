import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database.db_manager import DatabaseManager

def check_database():
    db = DatabaseManager()
    
    print('=== TRAINS IN DATABASE ===')
    trains = db.execute_query('SELECT * FROM Train ORDER BY priority, train_no')
    for train in trains:
        print(f"Train {train['train_no']} ({train['train_type']}) - Status: {train['current_status']}, Delay: {train['delay_minutes']}min")
        print(f"  Crew: {train['crew_status']}, Loco: {train['loco_health']}")
    
    print('\n=== STATIONS IN DATABASE ===')
    stations = db.execute_query('SELECT * FROM Station')
    for station in stations:
        print(f"Station {station['station_id']}: {station['current_occupancy']}/{station['yard_capacity']} occupied")
        print(f"  Facilities: {station['special_facility']}")
    
    print('\n=== SECTIONS IN DATABASE ===')
    sections = db.execute_query('SELECT * FROM Section')
    for section in sections:
        print(f"Section {section['section_id']} ({section['name']})")
        print(f"  Track: {section['track_type']}, Block: {section['block_status']}")
        print(f"  Power: {section['power_status']}, Signals: {section['signal_status']}")
    
    print('\n=== CHECKING AI CLAIMS ===')
    # Check if Train 14005 exists and its status
    train_14005 = db.execute_query("SELECT * FROM Train WHERE train_no = '14005'")
    if train_14005:
        t = train_14005[0]
        print(f"Train 14005: Status={t['current_status']}, Delay={t['delay_minutes']}min, Crew={t['crew_status']}, Loco={t['loco_health']}")
    else:
        print("Train 14005: NOT FOUND in database")
    
    # Check Station 101 and 102 facilities
    station_101 = db.execute_query("SELECT * FROM Station WHERE station_id = 101")
    station_102 = db.execute_query("SELECT * FROM Station WHERE station_id = 102")
    
    if station_101:
        print(f"Station 101: Facilities = {station_101[0]['special_facility']}")
    else:
        print("Station 101: NOT FOUND")
        
    if station_102:
        print(f"Station 102: Facilities = {station_102[0]['special_facility']}")
    else:
        print("Station 102: NOT FOUND")

if __name__ == "__main__":
    check_database()
