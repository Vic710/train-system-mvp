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
        
        # Prepare the system prompt - optimized for speed
        system_prompt = """You are an expert Railway Section Controller AI. Provide CONCISE, actionable railway operation decisions.

Priority Rules: Superfast (1) > Express (2) > Passenger (3) > Freight (4)
Focus: Safety first, then efficiency.

Response Format:
1. IMMEDIATE ACTION (1-2 bullet points)
2. REASONING (2-3 lines max)
3. EXPECTED OUTCOME (1-2 lines)

Be specific about train numbers, stations, and resources. Keep responses under 200 words."""

        # Prepare current context
        context_text = self._format_current_context(current_context)
        
        # Prepare historical decisions
        historical_text = self._format_historical_decisions(historical_decisions)
        
        # Create the human message - streamlined for speed
        human_prompt = f"""
SITUATION: {issue_description}

SECTION STATUS:
{context_text}

PAST SOLUTIONS:
{historical_text}

Provide immediate railway controller decision following the format above."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        # Generate response
        response = self.llm.invoke(messages)
        return response.content
    
    def _format_current_context(self, context: Dict[str, Any]) -> str:
        """Format current context for LLM - optimized for speed"""
        formatted = []
        
        if 'section' in context:
            section = context['section']
            formatted.append(f"Section: {section['name']} ({section['track_type']})")
            formatted.append(f"Status: Block={section['block_status']}, Power={section['power_status']}, Signals={section['signal_status']}")
        
        if 'trains' in context and context['trains']:
            # Only show problem trains and high priority trains
            problem_trains = [t for t in context['trains'] if t['current_status'] != 'On Time' or t['priority'] <= 2][:5]
            if problem_trains:
                formatted.append("\nKey Trains:")
                for train in problem_trains:
                    status = f"- {train['train_no']} ({train['train_type']}, P{train['priority']}): {train['current_status']}"
                    if train['delay_minutes'] > 0:
                        status += f" +{train['delay_minutes']}min"
                    if train['crew_status'] != 'Fresh Crew' or train['loco_health'] in ['Poor', 'Fair']:
                        status += f", Crew: {train['crew_status']}, Loco: {train['loco_health']}"
                    formatted.append(status)
        
        if 'stations' in context and context['stations']:
            # Only show stations with special facilities
            facilities = [s for s in context['stations'] if s.get('special_facility')]
            if facilities:
                formatted.append("\nResources:")
                for station in facilities:
                    formatted.append(f"- Station {station['station_id']}: {station['special_facility']} ({station['current_occupancy']}/{station['yard_capacity']})")
        
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
