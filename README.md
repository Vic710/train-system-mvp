# Section Controller Decision Engine MVP

This is an MVP implementation of a Railway Section Controller Decision Engine using RAG (Retrieval-Augmented Generation) with Google Gemini LLM.

## Features

- Database schema for train operations management
- RAG-based decision retrieval system
- LLM-powered decision suggestions
- Feedback loop for continuous learning

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the demo:
```bash
python main.py
```

## Project Structure

- `src/database/` - Database schema and operations
- `src/models/` - Data models and structures
- `src/rag/` - RAG retrieval system
- `src/decision_engine/` - Core decision engine logic
- `main.py` - Demo interface
