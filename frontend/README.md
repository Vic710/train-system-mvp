# Railway Section Controller - Web Frontend

A modern web interface for the Railway Section Controller Decision Engine MVP.

## Features

### 🚂 Real-time Section Dashboard
- Live section status monitoring
- Train counts and status indicators
- Power, signal, and block status visualization
- Weather condition tracking

### 🧠 AI-Powered Decision Analysis
- Interactive decision scenario analysis
- Google Gemini AI recommendations
- Predefined emergency scenarios
- Context-aware suggestions

### 📊 Decision Management
- Store controller decisions for AI training
- Historical decision tracking
- Outcome monitoring
- Feedback loop for system improvement

### 🎨 Modern UI/UX
- Responsive design for all devices
- Railway-themed professional interface
- Real-time updates and notifications
- Intuitive dashboard layout

## Quick Start

### 1. Install Dependencies
```bash
# Install main dependencies
pip install -r requirements.txt

# Install frontend dependencies
pip install -r frontend_requirements.txt
```

### 2. Configure Environment
Create `.env` file with your Google API key:
```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### 3. Initialize Database
```bash
python main.py
# Run once to create the database and sample data
# Exit after initialization
```

### 4. Start Web Server
```bash
python run_frontend.py
```

### 5. Access Dashboard
Open your browser and navigate to:
```
http://localhost:5000
```

## API Endpoints

The frontend communicates with these REST API endpoints:

- `GET /api/sections` - Get all section statuses
- `GET /api/trains` - Get train information
- `POST /api/decision/analyze` - Analyze decision scenario
- `POST /api/decision/store` - Store controller decision
- `GET /api/decisions/history` - Get decision history
- `GET /api/scenarios/predefined` - Get predefined scenarios

## File Structure

```
frontend/
├── app.py                 # Flask web application
├── templates/
│   └── index.html        # Main dashboard template
├── frontend_requirements.txt  # Frontend dependencies
└── static/               # Static assets (auto-created)
    ├── css/
    ├── js/
    └── images/
```

## Usage Guide

### Section Status Monitoring
- The left panel shows real-time status of all railway sections
- Color-coded indicators show normal/warning/danger states
- Train counts are updated automatically
- Auto-refreshes every 30 seconds

### Decision Analysis
- Select a section from the dropdown
- Describe the issue or situation
- Use "Load Scenarios" for predefined emergency situations
- Click "Analyze Decision" for AI recommendations
- Store your final decision for system learning

### Predefined Scenarios
Common scenarios are available for quick testing:
- Engine failures
- Signal malfunctions
- Crew fatigue issues
- Weather-related delays
- Platform overcrowding

### Decision History
- View recent controller decisions
- Track outcomes and effectiveness
- Provides context for future decisions
- Helps identify patterns and improvements

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **AI**: Google Gemini 1.5 Flash via LangChain
- **Database**: SQLite with custom railway schema
- **Styling**: Modern CSS with railway theme
- **Icons**: Font Awesome
- **Architecture**: RESTful API with responsive frontend

## Customization

### Themes
Modify the CSS variables in `templates/index.html` to customize:
- Color schemes
- Layout proportions
- Animation timings
- Typography

### API Integration
The frontend is designed to work with the existing decision engine.
No additional configuration needed if the main system is working.

### Responsive Design
The interface automatically adapts to:
- Desktop computers
- Tablets
- Mobile phones
- Different screen orientations

## Troubleshooting

### Common Issues

1. **Server won't start**
   - Check if all dependencies are installed
   - Verify Python path and module imports
   - Ensure port 5000 is available

2. **API calls failing**
   - Verify the main decision engine is working
   - Check database initialization
   - Confirm Google API key is set

3. **Empty sections/trains**
   - Run `main.py` once to populate sample data
   - Check database file creation
   - Verify data insertion scripts

4. **AI analysis not working**
   - Confirm Google API key is valid
   - Check internet connection
   - Verify Gemini model access

### Development Mode
Run with debug mode for development:
```bash
# Edit run_frontend.py to set debug=True
python run_frontend.py
```

This enables:
- Hot reloading on file changes
- Detailed error messages
- Development tools

## Production Deployment

For production use, consider:
- Using a production WSGI server (Gunicorn)
- Setting up reverse proxy (Nginx)
- Enabling HTTPS
- Database optimization
- Caching strategies
- Load balancing

Example production command:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 frontend.app:app
```

## Future Enhancements

Potential additions:
- WebSocket for real-time updates
- Advanced charting and analytics
- Mobile app integration
- Multi-language support
- Advanced user authentication
- Integration with real railway systems

## Support

This frontend is part of the Railway Section Controller MVP.
For technical support or feature requests, refer to the main project documentation.
