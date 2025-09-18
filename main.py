import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database.populate_data import DataPopulator
from src.decision_engine.engine import DecisionEngine
from src.rag.retriever import RAGRetriever
import time

class DecisionEngineDemo:
    def __init__(self):
        self.engine = DecisionEngine()
        self.retriever = RAGRetriever()
        self.setup_data()
    
    def setup_data(self):
        """Initialize database with sample data"""
        print("Setting up sample data...")
        populator = DataPopulator()
        populator.populate_all_data()
        print("Data setup complete!\n")
    
    def run_demo(self):
        """Run the interactive demo"""
        print("🚂 Railway Section Controller Decision Engine Demo")
        print("=" * 60)
        
        while True:
            print("\nSelect an option:")
            print("1. View section status")
            print("2. Simulate decision scenario")
            print("3. View historical decisions")
            print("4. Run predefined scenarios")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                self.view_section_status()
            elif choice == '2':
                self.simulate_custom_scenario()
            elif choice == '3':
                self.view_historical_decisions()
            elif choice == '4':
                self.run_predefined_scenarios()
            elif choice == '5':
                print("Thank you for using the Decision Engine Demo!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def view_section_status(self):
        """Display current status of all sections"""
        print("\n📊 CURRENT SECTION STATUS")
        print("-" * 40)
        
        for section_id in [1, 2, 3]:
            snapshot = self.retriever.get_current_section_snapshot(section_id)
            
            if 'section' in snapshot:
                section = snapshot['section']
                print(f"\nSection {section_id}: {section['name']}")
                print(f"  Track: {section['track_type']}")
                print(f"  Congestion: {section['congestion_level']}")
                print(f"  Block: {section['block_status']}")
                print(f"  Power: {section['power_status']}")
                print(f"  Signals: {section['signal_status']}")
                print(f"  Weather: {section['weather_condition']}")
                
                if 'trains' in snapshot:
                    active_trains = len([t for t in snapshot['trains'] if t['current_status'] != 'On Time'])
                    print(f"  Active Issues: {active_trains} trains with delays/problems")
    
    def simulate_custom_scenario(self):
        """Allow user to input custom scenario"""
        print("\n🎯 CUSTOM SCENARIO SIMULATION")
        print("-" * 40)
        
        # Select section
        print("Available sections:")
        print("1. SEC-A-Delhi-Ghaziabad (Double Line)")
        print("2. SEC-B-Ghaziabad-Moradabad (Single Line)")
        print("3. SEC-C-Moradabad-Bareilly (Double Line)")
        
        try:
            section_choice = int(input("Select section (1-3): "))
            if section_choice not in [1, 2, 3]:
                print("Invalid section choice.")
                return
        except ValueError:
            print("Invalid input.")
            return
        
        # Get issue description
        issue = input("Describe the issue/situation: ").strip()
        if not issue:
            print("Please provide an issue description.")
            return
        
        # Process decision
        print("\n🤖 Processing decision...")
        decision_package = self.engine.make_decision(section_choice, issue)
        
        # Display analysis
        self.engine.display_decision_analysis(decision_package)
        
        # Get controller feedback
        print("\nWhat action would you take as the controller?")
        controller_action = input("Your decision: ").strip()
        
        if controller_action:
            # Store the decision
            decision_id = self.engine.store_controller_decision(
                decision_package, controller_action
            )
            print(f"\n✅ Decision stored (ID: {decision_id})")
            print("This decision will be used for future training!")
    
    def view_historical_decisions(self):
        """View past decisions"""
        print("\n📜 HISTORICAL DECISIONS")
        print("-" * 40)
        
        decisions = self.retriever.db.execute_query("""
            SELECT d.*, s.name as section_name
            FROM Decisions d
            JOIN Section s ON d.section_id = s.section_id
            ORDER BY d.timestamp DESC
            LIMIT 10
        """)
        
        for i, decision in enumerate(decisions, 1):
            print(f"\n{i}. Section: {decision['section_name']}")
            print(f"   Action: {decision['controller_action']}")
            print(f"   Outcome: {decision['outcome']}")
            print(f"   Time: {decision['timestamp']}")
    
    def run_predefined_scenarios(self):
        """Run predefined test scenarios"""
        print("\n🧪 PREDEFINED SCENARIOS")
        print("-" * 40)
        
        scenarios = [
            {
                'section_id': 1,
                'issue': 'Signal failure at main line, two superfast trains approaching',
                'description': 'Signal System Failure Scenario'
            },
            {
                'section_id': 2,
                'issue': 'Heavy fog conditions, multiple delayed trains, crew fatigue reported',
                'description': 'Weather & Crew Management Scenario'
            },
            {
                'section_id': 3,
                'issue': 'Power block due to tripped overhead line, freight train blocking main line',
                'description': 'Power Failure & Track Blocking Scenario'
            },
            {
                'section_id': 1,
                'issue': 'Festival rush with 40% extra passenger load, platform congestion at major station',
                'description': 'High Traffic Management Scenario'
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"{i}. {scenario['description']}")
        
        try:
            choice = int(input("\nSelect scenario (1-4): "))
            if choice < 1 or choice > len(scenarios):
                print("Invalid choice.")
                return
            
            scenario = scenarios[choice - 1]
            print(f"\n🎬 Running scenario: {scenario['description']}")
            print(f"Issue: {scenario['issue']}")
            
            # Process the scenario
            print("\n🤖 AI analyzing situation...")
            time.sleep(1)  # Simulate processing time
            
            decision_package = self.engine.make_decision(
                scenario['section_id'], 
                scenario['issue']
            )
            
            # Display analysis
            self.engine.display_decision_analysis(decision_package)
            
            print("\n✅ Scenario analysis complete!")
            
        except ValueError:
            print("Invalid input.")

def main():
    """Main function to run the demo"""
    try:
        demo = DecisionEngineDemo()
        demo.run_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nError running demo: {e}")
        print("Please check your environment setup and try again.")

if __name__ == "__main__":
    main()
