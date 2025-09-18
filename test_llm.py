import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Simple test to verify LLM works
def test_llm():
    try:
        from src.rag.llm_manager import LLMManager
        from src.rag.retriever import RAGRetriever
        print("Testing LLM connection...")
        
        llm = LLMManager()
        retriever = RAGRetriever()
        print("LLM Manager initialized successfully!")
        
        # Get real context from database
        context = retriever.get_current_section_snapshot(1)
        historical = retriever.search_decisions_by_keywords(['power', 'delay'], limit=2)
        
        print("Context retrieved, testing LLM...")
        suggestion = llm.generate_decision_suggestion(
            context,
            historical,
            "Power failure affecting the section"
        )
        
        print("LLM Response received:")
        print(suggestion[:300] + "...")
        return True
        
    except Exception as e:
        print(f"LLM Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_llm()
