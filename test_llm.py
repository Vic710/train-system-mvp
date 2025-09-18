import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Simple test to verify LLM works
def test_llm():
    try:
        from src.rag.llm_manager import LLMManager
        print("Testing LLM connection...")
        
        llm = LLMManager()
        print("LLM Manager initialized successfully!")
        
        # Test with simple context
        simple_context = {
            'section': {
                'name': 'Test Section',
                'track_type': 'Double Line',
                'congestion_level': 'High',
                'block_status': 'Occupied',
                'power_status': 'Power Block',
                'signal_status': 'Normal',
                'weather_condition': 'Clear'
            },
            'trains': [],
            'stations': [],
            'external_factors': [],
            'recent_incidents': []
        }
        
        suggestion = llm.generate_decision_suggestion(
            simple_context,
            [],
            "Power failure affecting the section"
        )
        
        print("LLM Response received:")
        print(suggestion[:300] + "...")
        return True
        
    except Exception as e:
        print(f"LLM Error: {e}")
        return False

if __name__ == "__main__":
    test_llm()
