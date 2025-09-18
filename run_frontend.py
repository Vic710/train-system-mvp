"""
Simple startup script for the Railway Section Controller Frontend
"""
import sys
import os
import subprocess

# Add the main project directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    print("🚂 Starting Railway Section Controller Web Interface...")
    print("="*60)
    
    # Check if required modules are available
    try:
        from frontend.app import app
        print("✅ All modules loaded successfully")
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        print("pip install -r frontend_requirements.txt")
        sys.exit(1)
    
    print("🌐 Starting Flask development server...")
    print("📍 Server will be available at: http://localhost:5000")
    print("📊 Railway Dashboard will load automatically")
    print("="*60)
    
    try:
        # Run the Flask app
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)
