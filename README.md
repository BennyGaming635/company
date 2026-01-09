# Benco Company Simulation Game 🏢

A fun, interactive web-based simulation game that simulates working for "Benco" (Biggest Server Hosting Platform). Experience the life of a staff member managing servers, handling support tickets, and completing daily tasks!

## Features

### 🎮 Core Gameplay
- **Staff Dashboard**: View your employee profile, role, and performance metrics
- **Support Tickets System**: Handle customer support requests with different response options
- **Server Monitoring Panel**: Monitor server statistics across multiple regions with real-time data
- **Work Assignments**: Complete daily tasks to earn performance points
- **Random Events System**: Experience random system events, alerts, and management directives
- **Performance Scoreboard**: Track your progress, score, and rank advancement

### 🎯 Game Mechanics
- Multiple employee roles (Junior Developer, Senior Developer, System Administrator, Support Specialist)
- Point-based scoring system with different reward tiers
- Rank progression from Intern to Manager
- Day-by-day advancement with refreshing tasks
- Performance rating based on efficiency

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/BennyGaming635/company.git
cd company
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Enter your name and click "Start Your Shift" to begin playing!

### Gameplay Instructions

1. **Dashboard**: Your central hub showing stats and quick actions
2. **Support Tickets**: Choose response quality (Quick +5pts, Standard +10pts, Detailed +15pts)
3. **Server Monitor**: View real-time server statistics and status
4. **Tasks**: Complete daily assignments for points
5. **Scoreboard**: Check your rank and overall performance
6. **Next Day**: Advance to get new tasks and tickets

## Project Structure

```
company/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css     # Styling for all pages
│   └── js/
│       └── events.js     # Random events system
├── templates/
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Landing/welcome page
│   ├── dashboard.html    # Main dashboard
│   ├── tickets.html      # Support tickets page
│   ├── servers.html      # Server monitoring panel
│   ├── tasks.html        # Daily tasks page
│   └── scoreboard.html   # Performance scoreboard
└── README.md
```

## Technical Details

### Backend (Flask)
- Session-based game state management
- RESTful API endpoints for game actions
- Random event generation system
- Dynamic content rendering with Jinja2 templates

### Frontend
- Responsive HTML5/CSS3 design
- JavaScript for interactive features
- Real-time event notifications
- Mobile-friendly interface

## Game Mechanics

### Scoring System
- Support Tickets: 5-15 points (based on response quality)
- Work Tasks: 8-25 points (based on task type)
- Random Events: -15 to +20 points (random impact)

### Rank Progression
- **Intern**: 0-49 points
- **Junior**: 50-149 points
- **Senior**: 150-299 points
- **Lead**: 300-499 points
- **Manager**: 500+ points

### Task Types
- **Support**: Customer assistance tasks
- **Monitoring**: System surveillance duties
- **Maintenance**: System upkeep and updates
- **Development**: Technical improvements
- **Documentation**: Record keeping and guides

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for educational and entertainment purposes.

## Credits

Created as a fun simulation game to experience working at a fictional server hosting company.