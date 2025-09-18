import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db_manager import DatabaseManager
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

class RAGRetriever:
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_current_section_snapshot(self, section_id: int) -> Dict[str, Any]:
        """
        Get complete current snapshot of a section including all relevant data
        """
        print(f"\n🔍 RAG RETRIEVAL - Section Snapshot for ID: {section_id}")
        print("=" * 60)
        
        snapshot = {}
        
        # Get section details
        section_query = "SELECT * FROM Section WHERE section_id = ?"
        section_data = self.db.execute_query(section_query, (section_id,))
        if section_data:
            snapshot['section'] = section_data[0]
            print(f"📍 Section: {section_data[0].get('name', 'Unknown')} (Track: {section_data[0].get('track_type', 'N/A')}, Congestion: {section_data[0].get('congestion_level', 'N/A')})")
        else:
            print("❌ Section not found!")
        
        # Get all trains in the section (simulated by getting trains of matching priority/type)
        trains_query = """
            SELECT * FROM Train 
            ORDER BY priority ASC, delay_minutes DESC
            LIMIT 10
        """
        snapshot['trains'] = self.db.execute_query(trains_query)
        print(f"🚂 Retrieved {len(snapshot['trains'])} trains (ordered by priority)")
        
        # Get stations in the section
        stations_query = "SELECT * FROM Station WHERE section_id = ?"
        snapshot['stations'] = self.db.execute_query(stations_query, (section_id,))
        print(f"🚉 Retrieved {len(snapshot['stations'])} stations in section")
        
        # Get external factors affecting the section
        external_factors_query = "SELECT * FROM ExternalFactors WHERE section_id = ?"
        snapshot['external_factors'] = self.db.execute_query(external_factors_query, (section_id,))
        print(f"🌍 Retrieved {len(snapshot['external_factors'])} external factors")
        
        # Get recent incidents in the section (last 24 hours)
        yesterday = datetime.now() - timedelta(days=1)
        incidents_query = """
            SELECT * FROM Incidents 
            WHERE section_id = ? AND timestamp > ?
            ORDER BY timestamp DESC
        """
        snapshot['recent_incidents'] = self.db.execute_query(incidents_query, (section_id, yesterday))
        print(f"⚠️  Retrieved {len(snapshot['recent_incidents'])} recent incidents (last 24h)")
        
        print(f"✅ RAG snapshot complete - Total data points: {len(snapshot)}")
        return snapshot
    
    def get_similar_historical_decisions(self, 
                                       issue_type: str, 
                                       section_id: Optional[int] = None,
                                       limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve similar historical decisions based on issue type and section
        """
        # Base query for historical decisions
        query = """
            SELECT d.*, s.name as section_name, s.track_type, s.congestion_level
            FROM Decisions d
            JOIN Section s ON d.section_id = s.section_id
            WHERE d.controller_action LIKE ?
        """
        params = [f"%{issue_type}%"]
        
        # If specific section provided, prioritize decisions from same section
        if section_id:
            query += " ORDER BY CASE WHEN d.section_id = ? THEN 0 ELSE 1 END, d.timestamp DESC"
            params.append(section_id)
        else:
            query += " ORDER BY d.timestamp DESC"
        
        query += f" LIMIT {limit}"
        
        return self.db.execute_query(query, tuple(params))
    
    def get_section_performance_metrics(self, section_id: int, days: int = 7) -> Dict[str, Any]:
        """
        Get performance metrics for a section over the last N days
        """
        start_date = datetime.now() - timedelta(days=days)
        
        metrics = {}
        
        # Get decision outcomes distribution
        outcomes_query = """
            SELECT outcome, COUNT(*) as count
            FROM Decisions
            WHERE section_id = ? AND timestamp > ?
            GROUP BY outcome
        """
        outcomes = self.db.execute_query(outcomes_query, (section_id, start_date))
        metrics['decision_outcomes'] = {outcome['outcome']: outcome['count'] for outcome in outcomes}
        
        # Get incident frequency
        incidents_query = """
            SELECT COUNT(*) as incident_count
            FROM Incidents
            WHERE section_id = ? AND timestamp > ?
        """
        incident_count = self.db.execute_query(incidents_query, (section_id, start_date))
        metrics['recent_incidents'] = incident_count[0]['incident_count'] if incident_count else 0
        
        # Get average delay information (simulated)
        # In real scenario, this would be calculated from actual train data
        metrics['avg_delay_minutes'] = 25.5  # Placeholder
        metrics['on_time_percentage'] = 73.2  # Placeholder
        
        return metrics
    
    def search_decisions_by_keywords(self, keywords: List[str], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search historical decisions by keywords in controller actions
        """
        print(f"\n🔍 RAG HISTORICAL SEARCH")
        print("=" * 40)
        print(f"🔑 Keywords: {', '.join(keywords)}")
        
        # Create LIKE conditions for each keyword
        conditions = " OR ".join(["controller_action LIKE ?" for _ in keywords])
        params = [f"%{keyword}%" for keyword in keywords]
        
        query = f"""
            SELECT d.*, s.name as section_name
            FROM Decisions d
            JOIN Section s ON d.section_id = s.section_id
            WHERE {conditions}
            ORDER BY d.timestamp DESC
            LIMIT {limit}
        """
        
        results = self.db.execute_query(query, tuple(params))
        print(f"📊 Found {len(results)} historical decisions")
        
        for i, decision in enumerate(results[:3], 1):  # Log first 3 decisions
            print(f"   {i}. Section: {decision.get('section_name', 'Unknown')} - Action: {decision.get('controller_action', 'N/A')[:50]}...")
        
        if len(results) > 3:
            print(f"   ... and {len(results) - 3} more decisions")
        
        print("✅ Historical search complete")
        return results
    
    def get_train_details(self, train_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Get detailed information about specific trains
        """
        if not train_ids:
            return []
        
        placeholders = ",".join(["?" for _ in train_ids])
        query = f"""
            SELECT * FROM Train
            WHERE train_id IN ({placeholders})
            ORDER BY priority ASC, delay_minutes DESC
        """
        
        return self.db.execute_query(query, tuple(train_ids))
    
    def get_context_for_decision(self, section_id: int, issue_description: str) -> Dict[str, Any]:
        """
        Get comprehensive context for making a decision
        """
        context = {
            'current_snapshot': self.get_current_section_snapshot(section_id),
            'performance_metrics': self.get_section_performance_metrics(section_id),
            'similar_decisions': self.get_similar_historical_decisions(issue_description, section_id),
            'timestamp': datetime.now().isoformat()
        }
        
        return context
