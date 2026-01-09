from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'benco-secret-key-change-in-production'

# Game data structures
ROLES = ['Junior Developer', 'Senior Developer', 'System Administrator', 'Support Specialist']

SUPPORT_TICKETS = [
    {'id': 1, 'title': 'Server not responding', 'priority': 'High', 'description': 'Customer reports server downtime on EU-West-3'},
    {'id': 2, 'title': 'Slow website loading', 'priority': 'Medium', 'description': 'Website loading takes more than 5 seconds'},
    {'id': 3, 'title': 'Email configuration issue', 'priority': 'Low', 'description': 'Customer cannot configure email on cPanel'},
    {'id': 4, 'title': 'Database connection error', 'priority': 'High', 'description': 'MySQL database refusing connections'},
    {'id': 5, 'title': 'SSL certificate expired', 'priority': 'Critical', 'description': 'Domain SSL certificate needs renewal'},
    {'id': 6, 'title': 'Bandwidth limit reached', 'priority': 'Medium', 'description': 'Customer exceeded monthly bandwidth limit'},
    {'id': 7, 'title': 'FTP access denied', 'priority': 'Low', 'description': 'Unable to connect via FTP credentials'},
]

WORK_TASKS = [
    {'id': 1, 'task': 'Review 5 support tickets', 'points': 10, 'type': 'support'},
    {'id': 2, 'task': 'Monitor server uptime for 2 hours', 'points': 15, 'type': 'monitoring'},
    {'id': 3, 'task': 'Deploy security patches', 'points': 20, 'type': 'maintenance'},
    {'id': 4, 'task': 'Optimize database queries', 'points': 25, 'type': 'development'},
    {'id': 5, 'task': 'Update documentation', 'points': 8, 'type': 'documentation'},
]

RANDOM_EVENTS = [
    {'type': 'error', 'message': 'CRITICAL: Server US-East-1 is experiencing high CPU usage!', 'impact': -10},
    {'type': 'warning', 'message': 'Warning: Backup system is running slowly', 'impact': -5},
    {'type': 'success', 'message': 'Great news! Customer satisfaction rating increased!', 'impact': 15},
    {'type': 'info', 'message': 'Management: Team meeting scheduled for 3 PM', 'impact': 0},
    {'type': 'error', 'message': 'ALERT: DDoS attack detected on EU-West-2!', 'impact': -15},
    {'type': 'success', 'message': 'Bonus: Successfully resolved major incident!', 'impact': 20},
]

SERVER_LOCATIONS = ['US-East-1', 'US-West-2', 'EU-West-1', 'EU-West-3', 'Asia-Pacific-1']

def initialize_session():
    """Initialize session data for new game"""
    if 'initialized' not in session:
        session['initialized'] = True
        session['employee_name'] = 'Player'
        session['role'] = random.choice(ROLES)
        session['score'] = 0
        session['tickets_resolved'] = 0
        session['tasks_completed'] = 0
        session['current_day'] = 1
        session['active_tickets'] = random.sample(SUPPORT_TICKETS, 3)
        session['daily_tasks'] = random.sample(WORK_TASKS, 2)
        session['last_event_time'] = datetime.now().isoformat()

@app.route('/')
def index():
    """Landing page with game start"""
    return render_template('index.html')

@app.route('/start-game', methods=['POST'])
def start_game():
    """Start a new game session"""
    session.clear()
    employee_name = request.form.get('employee_name', 'Player')
    session['employee_name'] = employee_name
    initialize_session()
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    """Main staff dashboard"""
    initialize_session()
    
    # Calculate performance metrics
    total_actions = session['tickets_resolved'] + session['tasks_completed']
    performance_rating = min(100, (session['score'] / max(1, total_actions)) * 5) if total_actions > 0 else 50
    
    return render_template('dashboard.html',
                         employee_name=session['employee_name'],
                         role=session['role'],
                         score=session['score'],
                         tickets_resolved=session['tickets_resolved'],
                         tasks_completed=session['tasks_completed'],
                         current_day=session['current_day'],
                         performance_rating=round(performance_rating, 1))

@app.route('/tickets')
def tickets():
    """Support tickets page"""
    initialize_session()
    return render_template('tickets.html',
                         tickets=session['active_tickets'],
                         employee_name=session['employee_name'])

@app.route('/resolve-ticket/<int:ticket_id>', methods=['POST'])
def resolve_ticket(ticket_id):
    """Resolve a support ticket"""
    initialize_session()
    
    response_quality = request.form.get('response', 'standard')
    
    # Remove ticket from active tickets
    session['active_tickets'] = [t for t in session['active_tickets'] if t['id'] != ticket_id]
    session['tickets_resolved'] += 1
    
    # Award points based on response quality
    points = {'quick': 5, 'standard': 10, 'detailed': 15}.get(response_quality, 10)
    session['score'] += points
    
    # Add new ticket if needed
    remaining_tickets = [t for t in SUPPORT_TICKETS if t not in session['active_tickets']]
    if remaining_tickets and len(session['active_tickets']) < 3:
        session['active_tickets'].append(random.choice(remaining_tickets))
    
    session.modified = True
    return redirect(url_for('tickets'))

@app.route('/servers')
def servers():
    """Server monitoring panel"""
    initialize_session()
    
    # Generate random server stats
    server_stats = []
    for location in SERVER_LOCATIONS:
        uptime = round(random.uniform(95.0, 99.99), 2)
        cpu_usage = round(random.uniform(10, 90), 1)
        memory_usage = round(random.uniform(20, 85), 1)
        disk_usage = round(random.uniform(30, 75), 1)
        status = 'Operational' if cpu_usage < 80 else 'Warning' if cpu_usage < 95 else 'Critical'
        
        server_stats.append({
            'location': location,
            'uptime': uptime,
            'cpu': cpu_usage,
            'memory': memory_usage,
            'disk': disk_usage,
            'status': status
        })
    
    return render_template('servers.html',
                         servers=server_stats,
                         employee_name=session['employee_name'])

@app.route('/tasks')
def tasks():
    """Work assignments page"""
    initialize_session()
    return render_template('tasks.html',
                         tasks=session['daily_tasks'],
                         employee_name=session['employee_name'],
                         current_day=session['current_day'])

@app.route('/complete-task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    """Complete a work task"""
    initialize_session()
    
    # Find and remove the task
    task = None
    for t in session['daily_tasks']:
        if t['id'] == task_id:
            task = t
            break
    
    if task:
        session['daily_tasks'] = [t for t in session['daily_tasks'] if t['id'] != task_id]
        session['tasks_completed'] += 1
        session['score'] += task['points']
        
        # Add new task if needed
        remaining_tasks = [t for t in WORK_TASKS if t not in session['daily_tasks']]
        if remaining_tasks and len(session['daily_tasks']) < 2:
            session['daily_tasks'].append(random.choice(remaining_tasks))
    
    session.modified = True
    return redirect(url_for('tasks'))

@app.route('/scoreboard')
def scoreboard():
    """Performance scoreboard"""
    initialize_session()
    
    # Calculate various metrics
    total_actions = session['tickets_resolved'] + session['tasks_completed']
    efficiency = round((session['score'] / max(1, total_actions)) * 10, 1) if total_actions > 0 else 5.0
    rank = 'Intern' if session['score'] < 50 else 'Junior' if session['score'] < 150 else 'Senior' if session['score'] < 300 else 'Lead' if session['score'] < 500 else 'Manager'
    
    return render_template('scoreboard.html',
                         employee_name=session['employee_name'],
                         role=session['role'],
                         score=session['score'],
                         tickets_resolved=session['tickets_resolved'],
                         tasks_completed=session['tasks_completed'],
                         current_day=session['current_day'],
                         efficiency=efficiency,
                         rank=rank)

@app.route('/api/random-event')
def random_event():
    """API endpoint for random events"""
    initialize_session()
    
    # Check if enough time has passed since last event (at least 30 seconds for demo)
    last_event = datetime.fromisoformat(session['last_event_time'])
    if datetime.now() - last_event < timedelta(seconds=30):
        return jsonify({'event': None})
    
    # 30% chance of event occurring
    if random.random() < 0.3:
        event = random.choice(RANDOM_EVENTS)
        session['score'] += event['impact']
        session['last_event_time'] = datetime.now().isoformat()
        session.modified = True
        return jsonify({'event': event})
    
    return jsonify({'event': None})

@app.route('/next-day')
def next_day():
    """Advance to next work day"""
    initialize_session()
    session['current_day'] += 1
    
    # Reset daily tasks
    session['daily_tasks'] = random.sample(WORK_TASKS, 2)
    
    # Refresh tickets
    session['active_tickets'] = random.sample(SUPPORT_TICKETS, 3)
    
    session.modified = True
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
