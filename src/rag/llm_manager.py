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
            model="gemini-2.5-pro",
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
        
        # Prepare the system prompt
        system_prompt = """You are an expert Railway Section Controller AI assistant. Your role is to suggest optimal decisions for managing train operations in a railway section.

Consider the following factors when making decisions:
1. Train Priority: Superfast (1) > Express (2) > Passenger (3) > Freight (4)
2. Safety: Always prioritize safety over speed
3. Efficiency: Minimize delays and maximize track utilization
4. Resource constraints: Track capacity, crew availability, locomotive health
5. External factors: Weather, strikes, festivals, emergencies

Provide specific, actionable recommendations with clear reasoning."""

        # Prepare current context
        context_text = self._format_current_context(current_context)
        
        # Prepare historical decisions
        historical_text = self._format_historical_decisions(historical_decisions)
        
        # Create the human message
        human_prompt = f"""
CURRENT SITUATION:
{context_text}

ISSUE TO RESOLVE:
{issue_description}

RELEVANT HISTORICAL DECISIONS:
{historical_text}

Based on the current situation and similar past decisions, please provide:
1. Recommended action
2. Reasoning behind the decision
3. Potential risks or considerations
4. Expected outcome

Keep your response concise but comprehensive."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        # Generate response
        response = self.llm.invoke(messages)
        return response.content
    
    def _format_current_context(self, context: Dict[str, Any]) -> str:
        """Format current context for LLM"""
        formatted = []
        
        if 'section' in context:
            section = context['section']
            formatted.append(f"SECTION: {section['name']}")
            formatted.append(f"- Track Type: {section['track_type']}")
            formatted.append(f"- Congestion: {section['congestion_level']}")
            formatted.append(f"- Block Status: {section['block_status']}")
            formatted.append(f"- Power Status: {section['power_status']}")
            formatted.append(f"- Signal Status: {section['signal_status']}")
            formatted.append(f"- Weather: {section['weather_condition']}")
        
        if 'trains' in context:
            formatted.append("\nTRAINS IN SECTION:")
            for train in context['trains']:
                status_info = f"Train {train['train_no']} ({train['train_type']}, Priority: {train['priority']})"
                status_info += f" - Status: {train['current_status']}"
                if train['delay_minutes'] > 0:
                    status_info += f", Delayed by {train['delay_minutes']} minutes"
                status_info += f", Crew: {train['crew_status']}, Loco: {train['loco_health']}"
                formatted.append(f"- {status_info}")
        
        if 'stations' in context:
            formatted.append("\nSTATIONS:")
            for station in context['stations']:
                occupancy_pct = (station['current_occupancy'] / station['yard_capacity']) * 100
                station_info = f"Station {station['station_id']}: {station['current_occupancy']}/{station['yard_capacity']} occupied ({occupancy_pct:.1f}%)"
                if station['special_facility']:
                    station_info += f", Facilities: {station['special_facility']}"
                formatted.append(f"- {station_info}")
        
        if 'external_factors' in context:
            formatted.append("\nEXTERNAL FACTORS:")
            for factor in context['external_factors']:
                formatted.append(f"- {factor['type']} ({factor['severity']} severity): {factor['remarks']}")
        
        if 'recent_incidents' in context:
            formatted.append("\nRECENT INCIDENTS:")
            for incident in context['recent_incidents']:
                incident_info = f"- {incident['type']}"
                if incident['train_id']:
                    incident_info += f" involving Train {incident['train_id']}"
                incident_info += f": {incident['resolution'] or 'Under investigation'}"
                formatted.append(incident_info)
        
        return "\n".join(formatted)
    
    def _format_historical_decisions(self, decisions: List[Dict[str, Any]]) -> str:
        """Format historical decisions for LLM"""
        if not decisions:
            return "No similar historical decisions found."
        
        formatted = []
        for i, decision in enumerate(decisions, 1):
            formatted.append(f"{i}. Action: {decision['controller_action']}")
            formatted.append(f"   Outcome: {decision['outcome']}")
            formatted.append(f"   Timestamp: {decision['timestamp']}")
            formatted.append("")
        
        return "\n".join(formatted)
