import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime

from src.decision_engine.engine import DecisionEngine
from src.rag.retriever import RAGRetriever
from src.database.populate_data import DataPopulator

app = Flask(__name__)
CORS(app)

# Initialize the decision engine
engine = DecisionEngine()
retriever = RAGRetriever()

# Ensure database is populated
try:
    populator = DataPopulator()
    populator.populate_all_data()
    print("Database initialized and populated successfully!")
except Exception as e:
    print(f"Database initialization warning: {e}")

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/sections')
def get_sections():
    """Get all sections with their current status"""
    try:
        sections = []
        for section_id in [1, 2, 3]:
            snapshot = retriever.get_current_section_snapshot(section_id)
            
            if 'section' in snapshot:
                section_data = snapshot['section']
                
                # Count trains by status
                trains = snapshot.get('trains', [])
                delayed_trains = len([t for t in trains if t['current_status'] == 'Delayed'])
                halted_trains = len([t for t in trains if t['current_status'] == 'Halted'])
                on_time_trains = len([t for t in trains if t['current_status'] == 'On Time'])
                
                sections.append({
                    'id': section_id,
                    'name': section_data['name'],
                    'track_type': section_data['track_type'],
                    'congestion_level': section_data['congestion_level'],
                    'block_status': section_data['block_status'],
                    'power_status': section_data['power_status'],
                    'signal_status': section_data['signal_status'],
                    'weather_condition': section_data['weather_condition'],
                    'train_counts': {
                        'delayed': delayed_trains,
                        'halted': halted_trains,
                        'on_time': on_time_trains,
                        'total': len(trains)
                    }
                })
        
        return jsonify(sections)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/section/<int:section_id>')
def get_section_details(section_id):
    """Get detailed information about a specific section"""
    try:
        snapshot = retriever.get_current_section_snapshot(section_id)
        return jsonify(snapshot)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trains')
def get_all_trains():
    """Get all trains across all sections"""
    try:
        trains = retriever.db.execute_query("""
            SELECT * FROM Train 
            ORDER BY priority ASC, delay_minutes DESC
        """)
        return jsonify(trains)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decisions/history')
def get_decision_history():
    """Get historical decisions"""
    try:
        decisions = retriever.db.execute_query("""
            SELECT d.*, s.name as section_name
            FROM Decisions d
            JOIN Section s ON d.section_id = s.section_id
            ORDER BY d.timestamp DESC
            LIMIT 20
        """)
        return jsonify(decisions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decision/analyze', methods=['POST'])
def analyze_decision():
    """Analyze a decision scenario"""
    try:
        data = request.json
        section_id = data.get('section_id')
        issue_description = data.get('issue_description')
        
        if not section_id or not issue_description:
            return jsonify({'error': 'Missing section_id or issue_description'}), 400
        
        # Process the decision
        decision_package = engine.make_decision(section_id, issue_description)
        
        return jsonify({
            'success': True,
            'analysis': {
                'section_id': decision_package['section_id'],
                'issue_description': decision_package['issue_description'],
                'timestamp': decision_package['timestamp'].isoformat(),
                'current_context': decision_package['current_context'],
                'historical_decisions': decision_package['historical_decisions'],
                'ai_suggestion': decision_package['llm_suggestion'],
                'keywords_used': decision_package['keywords_used']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decision/store', methods=['POST'])
def store_decision():
    """Store a controller's final decision"""
    try:
        data = request.json
        section_id = data.get('section_id')
        controller_action = data.get('controller_action')
        outcome = data.get('outcome', 'Resolved')
        
        if not section_id or not controller_action:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create a minimal decision package for storage
        decision_package = {
            'section_id': section_id,
            'timestamp': datetime.now()
        }
        
        decision_id = engine.store_controller_decision(
            decision_package, 
            controller_action, 
            outcome
        )
        
        return jsonify({
            'success': True,
            'decision_id': decision_id,
            'message': 'Decision stored successfully for future training'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scenarios/predefined')
def get_predefined_scenarios():
    """Get predefined test scenarios"""
    scenarios = [
        {
            'id': 1,
            'name': 'Signal System Failure',
            'section_id': 1,
            'description': 'Signal failure at main line, two superfast trains approaching',
            'category': 'Infrastructure'
        },
        {
            'id': 2,
            'name': 'Weather & Crew Management',
            'section_id': 2,
            'description': 'Heavy fog conditions, multiple delayed trains, crew fatigue reported',
            'category': 'Weather'
        },
        {
            'id': 3,
            'name': 'Power Failure & Track Blocking',
            'section_id': 3,
            'description': 'Power block due to tripped overhead line, freight train blocking main line',
            'category': 'Power'
        },
        {
            'id': 4,
            'name': 'High Traffic Management',
            'section_id': 1,
            'description': 'Festival rush with 40% extra passenger load, platform congestion at major station',
            'category': 'Traffic'
        }
    ]
    return jsonify(scenarios)

if __name__ == '__main__':
    print("🚂 Railway Section Controller Web Interface")
    print("=" * 50)
    print("Starting server at http://localhost:5000")
    print("Database populated with sample data")
    print("AI Decision Engine ready!")
    app.run(debug=True, host='0.0.0.0', port=5000)
