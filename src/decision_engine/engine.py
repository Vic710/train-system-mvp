import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag.retriever import RAGRetriever
from src.rag.llm_manager import LLMManager
from src.database.db_manager import DatabaseManager
from datetime import datetime
from typing import Dict, Any, Optional

class DecisionEngine:
    def __init__(self):
        self.retriever = RAGRetriever()
        try:
            self.llm_manager = LLMManager()
            self.llm_available = True
        except Exception as e:
            print(f"Warning: LLM not available - {e}")
            self.llm_available = False
        
        self.db = DatabaseManager()
    
    def make_decision(self, 
                     section_id: int, 
                     issue_description: str, 
                     issue_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Main decision-making process
        """
        print(f"\n=== Processing Decision Request ===")
        print(f"Section: {section_id}")
        print(f"Issue: {issue_description}")
        
        # Step 1: Gather current context
        print("\n1. Gathering current context...")
        current_context = self.retriever.get_current_section_snapshot(section_id)
        
        # Step 2: Retrieve similar historical decisions
        print("2. Retrieving similar historical decisions...")
        keywords = self._extract_keywords(issue_description)
        historical_decisions = self.retriever.search_decisions_by_keywords(keywords, limit=5)
        
        # Step 3: Generate LLM suggestion (if available)
        llm_suggestion = None
        if self.llm_available:
            print("3. Generating LLM suggestion...")
            try:
                llm_suggestion = self.llm_manager.generate_decision_suggestion(
                    current_context, historical_decisions, issue_description
                )
            except Exception as e:
                print(f"Error generating LLM suggestion: {e}")
                llm_suggestion = "LLM suggestion unavailable due to error"
        else:
            print("3. LLM unavailable, using rule-based fallback...")
            llm_suggestion = self._generate_rule_based_suggestion(current_context, issue_description)
        
        # Step 4: Prepare decision package
        decision_package = {
            'section_id': section_id,
            'issue_description': issue_description,
            'current_context': current_context,
            'historical_decisions': historical_decisions,
            'llm_suggestion': llm_suggestion,
            'timestamp': datetime.now(),
            'keywords_used': keywords
        }
        
        print("4. Decision analysis complete!")
        return decision_package
    
    def store_controller_decision(self, 
                                decision_package: Dict[str, Any], 
                                controller_action: str, 
                                outcome: str = "Resolved") -> int:
        """
        Store the final controller decision in the database
        """
        query = """
            INSERT INTO Decisions (section_id, controller_action, timestamp, outcome)
            VALUES (?, ?, ?, ?)
        """
        
        decision_id = self.db.execute_insert(
            query, 
            (decision_package['section_id'], 
             controller_action, 
             decision_package['timestamp'], 
             outcome)
        )
        
        print(f"Stored decision with ID: {decision_id}")
        return decision_id
    
    def _extract_keywords(self, issue_description: str) -> list:
        """
        Extract keywords from issue description for similarity search
        """
        # Simple keyword extraction - in production, this could be more sophisticated
        keywords = []
        
        # Common railway operation keywords
        railway_keywords = {
            'delay': ['delay', 'late', 'behind'],
            'priority': ['priority', 'urgent', 'superfast', 'express'],
            'signal': ['signal', 'failure', 'fault'],
            'power': ['power', 'electric', 'traction'],
            'crew': ['crew', 'staff', 'driver'],
            'freight': ['freight', 'goods', 'cargo'],
            'passenger': ['passenger', 'people'],
            'emergency': ['emergency', 'accident', 'incident'],
            'maintenance': ['maintenance', 'repair', 'work'],
            'weather': ['weather', 'fog', 'rain', 'storm']
        }
        
        issue_lower = issue_description.lower()
        
        for category, terms in railway_keywords.items():
            if any(term in issue_lower for term in terms):
                keywords.append(category)
        
        # Also add direct words from the description
        words = issue_description.split()
        important_words = [word.strip('.,!?') for word in words if len(word) > 3]
        keywords.extend(important_words[:3])  # Take first 3 meaningful words
        
        return list(set(keywords))  # Remove duplicates
    
    def _generate_rule_based_suggestion(self, context: Dict[str, Any], issue_description: str) -> str:
        """
        Generate a basic rule-based suggestion when LLM is unavailable
        """
        suggestions = []
        
        # Analyze current context
        if 'section' in context:
            section = context['section']
            
            # Signal-related issues
            if 'signal' in issue_description.lower() and section['signal_status'] != 'Normal':
                suggestions.append("Implement manual working procedures for signal failure")
                suggestions.append("Coordinate with signal maintainer for immediate repair")
            
            # Power-related issues
            if 'power' in issue_description.lower() and section['power_status'] != 'Normal':
                suggestions.append("Coordinate with traction power controller")
                suggestions.append("Arrange diesel locomotives if electric traction unavailable")
            
            # Congestion issues
            if section['congestion_level'] == 'High':
                suggestions.append("Priority to high-priority trains (Superfast/Express)")
                suggestions.append("Hold freight trains at stations to clear mainline")
            
        # Train-specific suggestions
        if 'trains' in context:
            delayed_trains = [t for t in context['trains'] if t['current_status'] == 'Delayed']
            if delayed_trains:
                suggestions.append(f"Address {len(delayed_trains)} delayed trains - prioritize by train type")
        
        # Weather-related
        if 'weather' in issue_description.lower():
            suggestions.append("Implement speed restrictions if necessary")
            suggestions.append("Increase vigilance for track safety")
        
        if not suggestions:
            suggestions.append("Assess situation and coordinate with adjacent sections")
            suggestions.append("Monitor train movements and update as situation develops")
        
        return "RULE-BASED SUGGESTIONS:\n" + "\n".join(f"• {s}" for s in suggestions)
    
    def display_decision_analysis(self, decision_package: Dict[str, Any]):
        """
        Display a formatted analysis of the decision
        """
        print("\n" + "="*60)
        print("DECISION ANALYSIS REPORT")
        print("="*60)
        
        print(f"\nISSUE: {decision_package['issue_description']}")
        print(f"SECTION: {decision_package['section_id']}")
        print(f"TIMESTAMP: {decision_package['timestamp']}")
        
        # Current context summary
        context = decision_package['current_context']
        if 'section' in context:
            section = context['section']
            print(f"\nSECTION STATUS:")
            print(f"  Name: {section['name']}")
            print(f"  Track: {section['track_type']}")
            print(f"  Congestion: {section['congestion_level']}")
            print(f"  Block: {section['block_status']}")
            print(f"  Power: {section['power_status']}")
            print(f"  Signals: {section['signal_status']}")
            print(f"  Weather: {section['weather_condition']}")
        
        if 'trains' in context and context['trains']:
            print(f"\nTRAINS IN SECTION: {len(context['trains'])}")
            for train in context['trains'][:5]:  # Show first 5
                status = f"  {train['train_no']} ({train['train_type']}) - {train['current_status']}"
                if train['delay_minutes'] > 0:
                    status += f" (+{train['delay_minutes']}min)"
                print(status)
        
        # Historical decisions
        if decision_package['historical_decisions']:
            print(f"\nSIMILAR PAST DECISIONS: {len(decision_package['historical_decisions'])}")
            for i, decision in enumerate(decision_package['historical_decisions'][:3], 1):
                print(f"  {i}. {decision['controller_action'][:80]}...")
                print(f"     Outcome: {decision['outcome']}")
        
        # LLM Suggestion
        print(f"\nAI SUGGESTION:")
        print(decision_package['llm_suggestion'])
        
        print("="*60)
