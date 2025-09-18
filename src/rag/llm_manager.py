import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

class LLMManager:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=self.api_key,
            temperature=0.3,
            convert_system_message_to_human=True
        )
    
    def generate_decision_suggestion(self, 
                                   current_context: Dict[str, Any], 
                                   historical_decisions: List[Dict[str, Any]], 
                                   issue_description: str) -> str:
        """
        Generate decision suggestion based on current context and historical decisions
        """
        
        # Prepare the system prompt - enhanced for detailed section-wide analysis
        system_prompt = """You are an expert Railway Section Controller Supporter AI. Provide detailed, actionable railway operation decisions considering the ENTIRE section.

Priority Rules: Superfast (1) > Express (2) > Passenger (3) > Freight (4)
Focus: Safety first, then section-wide efficiency.

CRITICAL: Consider the impact on ALL trains in the section, not just the problem train.

Response Format:
1. DETAILED ACTIONS (step-by-step with specific trains, stations, and timing)
2. SECTION-WIDE COORDINATION (how other trains will be managed during the operation)
3. RESOURCE DEPLOYMENT (specific stations, facilities, and personnel)
4. EXPECTED TIMELINE (estimated duration and sequence)

Be specific about:
- Which trains to halt and where
- Station-by-station coordination 
- Crew and locomotive movements
- Impact on approaching trains
- Traffic flow restoration sequence"""

        # Prepare current context
        context_text = self._format_current_context(current_context)
        
        # Prepare historical decisions
        historical_text = self._format_historical_decisions(historical_decisions)
        
        # Create the human message - enhanced for comprehensive analysis
        human_prompt = f"""
INCIDENT: {issue_description}

COMPLETE SECTION STATUS:
{context_text}

HISTORICAL CONTEXT:
{historical_text}

INSTRUCTIONS:
Analyze the ENTIRE section situation. Consider:
1. ALL trains currently in section and their positions
2. Approaching trains that may need to be halted
3. Station capacities and available resources
4. Ripple effects of your actions on other trains
5. Optimal sequence to restore normal operations

Provide a comprehensive section controller decision with detailed coordination plan."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        # Generate response
        response = self.llm.invoke(messages)
        return response.content
    
    def _format_current_context(self, context: Dict[str, Any]) -> str:
        """Format current context for LLM - enhanced for comprehensive analysis"""
        formatted = []
        
        if 'section' in context:
            section = context['section']
            formatted.append(f"Section: {section['name']} ({section['track_type']})")
            formatted.append(f"Infrastructure: Block={section['block_status']}, Power={section['power_status']}, Signals={section['signal_status']}")
            formatted.append(f"Conditions: Weather={section['weather_condition']}, Congestion={section['congestion_level']}")
        
        if 'trains' in context and context['trains']:
            # Show ALL trains with detailed status for comprehensive planning
            formatted.append("\nALL TRAINS IN SECTION:")
            
            # Group by priority for better organization
            trains_by_priority = {}
            for train in context['trains']:
                priority = train['priority']
                if priority not in trains_by_priority:
                    trains_by_priority[priority] = []
                trains_by_priority[priority].append(train)
            
            # Display by priority groups
            for priority in sorted(trains_by_priority.keys()):
                trains = trains_by_priority[priority]
                priority_name = {1: "SUPERFAST", 2: "EXPRESS", 3: "PASSENGER", 4: "FREIGHT"}[priority]
                formatted.append(f"\n{priority_name} TRAINS (Priority {priority}):")
                
                for train in trains:
                    status = f"  • {train['train_no']} - {train['current_status']}"
                    if train['delay_minutes'] > 0:
                        status += f" (Delayed +{train['delay_minutes']}min)"
                    
                    # Add crew and loco details for operational planning
                    details = []
                    if train['crew_status'] and train['crew_status'] != 'Fresh Crew':
                        details.append(f"Crew: {train['crew_status']}")
                    if train['loco_health'] and train['loco_health'] in ['Poor', 'Fair']:
                        details.append(f"Loco: {train['loco_health']}")
                    
                    if details:
                        status += f" [{', '.join(details)}]"
                    
                    formatted.append(status)
        
        if 'stations' in context and context['stations']:
            formatted.append("\nSTATION RESOURCES & CAPACITY:")
            for station in context['stations']:
                occupancy_pct = (station['current_occupancy'] / station['yard_capacity']) * 100
                capacity_status = "FULL" if occupancy_pct >= 100 else "HIGH" if occupancy_pct >= 75 else "AVAILABLE"
                
                station_info = f"  • Station {station['station_id']}: {station['current_occupancy']}/{station['yard_capacity']} occupied ({capacity_status})"
                if station.get('special_facility'):
                    station_info += f" - {station['special_facility']}"
                formatted.append(station_info)
        
        # Add external factors for comprehensive planning
        if 'external_factors' in context and context['external_factors']:
            formatted.append("\nEXTERNAL FACTORS:")
            for factor in context['external_factors']:
                formatted.append(f"  • {factor['type']} ({factor['severity']} severity): {factor['remarks']}")
        
        # Add recent incidents for context
        if 'recent_incidents' in context and context['recent_incidents']:
            formatted.append("\nRECENT INCIDENTS:")
            for incident in context['recent_incidents']:
                incident_info = f"  • {incident['type']}"
                if incident.get('train_id'):
                    incident_info += f" (Train {incident['train_id']})"
                incident_info += f": {incident.get('resolution', 'Under investigation')}"
                formatted.append(incident_info)
        
        return "\n".join(formatted)
    
    def _format_historical_decisions(self, decisions: List[Dict[str, Any]]) -> str:
        """Format historical decisions for LLM - optimized for speed"""
        if not decisions:
            return "No similar cases found."
        
        # Only show most relevant decisions (max 3)
        formatted = []
        for i, decision in enumerate(decisions[:3], 1):
            formatted.append(f"{i}. {decision['controller_action'][:80]}... → {decision['outcome']}")
        
        return "\n".join(formatted)
