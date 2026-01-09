from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import random
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

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
    {'id': 8, 'title': 'Website hacked', 'priority': 'Critical', 'description': 'Customer website showing malicious content'},
    {'id': 9, 'title': 'Backup restore request', 'priority': 'High', 'description': 'Customer needs backup from 2 days ago restored'},
    {'id': 10, 'title': 'DNS not propagating', 'priority': 'Medium', 'description': 'Domain DNS changes not taking effect'},
    {'id': 11, 'title': 'WordPress white screen', 'priority': 'High', 'description': 'Customer WordPress site showing blank page'},
    {'id': 12, 'title': 'Disk space full', 'priority': 'High', 'description': 'Account reached 100% disk usage'},
    {'id': 13, 'title': 'PHP version upgrade', 'priority': 'Low', 'description': 'Customer wants to upgrade from PHP 7.4 to 8.1'},
    {'id': 14, 'title': 'Email not sending', 'priority': 'Medium', 'description': 'SMTP server rejecting outgoing emails'},
    {'id': 15, 'title': '404 errors on website', 'priority': 'Medium', 'description': 'Multiple pages returning 404 errors'},
    {'id': 16, 'title': 'Database too large', 'priority': 'Low', 'description': 'MySQL database exceeding allocated space'},
    {'id': 17, 'title': 'Cron job not running', 'priority': 'Low', 'description': 'Scheduled task failed to execute'},
    {'id': 18, 'title': 'File permissions error', 'priority': 'Medium', 'description': 'Cannot upload files due to permission issues'},
    {'id': 19, 'title': 'Suspended account inquiry', 'priority': 'High', 'description': 'Customer asking why account was suspended'},
    {'id': 20, 'title': 'Migration assistance', 'priority': 'Medium', 'description': 'Help needed migrating from another host'},
    {'id': 21, 'title': 'Memory limit exceeded', 'priority': 'High', 'description': 'PHP scripts hitting memory limit'},
    {'id': 22, 'title': 'Malware scan request', 'priority': 'Medium', 'description': 'Customer suspects malware on their site'},
    {'id': 23, 'title': 'Subdomain not working', 'priority': 'Low', 'description': 'Newly created subdomain shows error'},
    {'id': 24, 'title': 'Payment failed', 'priority': 'High', 'description': 'Auto-renewal payment declined'},
]

WORK_TASKS = [
    {'id': 1, 'task': 'Review 5 support tickets', 'points': 10, 'type': 'support'},
    {'id': 2, 'task': 'Monitor server uptime for 2 hours', 'points': 15, 'type': 'monitoring'},
    {'id': 3, 'task': 'Deploy security patches', 'points': 20, 'type': 'maintenance'},
    {'id': 4, 'task': 'Optimize database queries', 'points': 25, 'type': 'development'},
    {'id': 5, 'task': 'Update documentation', 'points': 8, 'type': 'documentation'},
    {'id': 6, 'task': 'Perform security audit', 'points': 30, 'type': 'maintenance'},
    {'id': 7, 'task': 'Set up automated backups', 'points': 20, 'type': 'maintenance'},
    {'id': 8, 'task': 'Migrate customer to new server', 'points': 35, 'type': 'development'},
    {'id': 9, 'task': 'Create knowledge base article', 'points': 12, 'type': 'documentation'},
    {'id': 10, 'task': 'Investigate slow queries', 'points': 18, 'type': 'monitoring'},
    {'id': 11, 'task': 'Update control panel', 'points': 22, 'type': 'maintenance'},
    {'id': 12, 'task': 'Train new support staff', 'points': 15, 'type': 'support'},
    {'id': 13, 'task': 'Fix broken API endpoints', 'points': 28, 'type': 'development'},
    {'id': 14, 'task': 'Analyze server logs', 'points': 16, 'type': 'monitoring'},
    {'id': 15, 'task': 'Configure firewall rules', 'points': 24, 'type': 'maintenance'},
    {'id': 16, 'task': 'Implement caching system', 'points': 32, 'type': 'development'},
    {'id': 17, 'task': 'Respond to customer surveys', 'points': 10, 'type': 'support'},
    {'id': 18, 'task': 'Load test new infrastructure', 'points': 26, 'type': 'monitoring'},
]

RANDOM_EVENTS = [
    {'type': 'error', 'message': 'CRITICAL: Server US-East-1 is experiencing high CPU usage!', 'impact': -10},
    {'type': 'warning', 'message': 'Warning: Backup system is running slowly', 'impact': -5},
    {'type': 'success', 'message': 'Great news! Customer satisfaction rating increased!', 'impact': 15},
    {'type': 'info', 'message': 'Management: Team meeting scheduled for 3 PM', 'impact': 0},
    {'type': 'error', 'message': 'ALERT: DDoS attack detected on EU-West-2!', 'impact': -15},
    {'type': 'success', 'message': 'Bonus: Successfully resolved major incident!', 'impact': 20},
    {'type': 'error', 'message': 'URGENT: Database server crashed in Asia-Pacific region!', 'impact': -20},
    {'type': 'warning', 'message': 'Network latency spike detected across multiple regions', 'impact': -8},
    {'type': 'success', 'message': 'Excellent work! Received positive feedback from VIP client', 'impact': 25},
    {'type': 'info', 'message': 'Reminder: Security training session tomorrow', 'impact': 0},
    {'type': 'error', 'message': 'Storage array failure on backup system!', 'impact': -12},
    {'type': 'success', 'message': 'Achievement unlocked: 100% uptime for 30 days!', 'impact': 30},
    {'type': 'warning', 'message': 'SSL certificates expiring in 7 days for 5 domains', 'impact': -3},
    {'type': 'info', 'message': 'New company policy: All changes require approval', 'impact': 0},
    {'type': 'error', 'message': 'Power outage in US-West datacenter!', 'impact': -18},
    {'type': 'success', 'message': 'Record low response time achieved!', 'impact': 18},
    {'type': 'warning', 'message': 'Unusual traffic pattern detected', 'impact': -6},
    {'type': 'success', 'message': 'Customer upgraded to enterprise plan!', 'impact': 22},
    {'type': 'error', 'message': 'RAID array degraded on storage server', 'impact': -14},
    {'type': 'info', 'message': 'Maintenance window scheduled for tonight', 'impact': 0},
    {'type': 'success', 'message': 'Performance optimization saved company $10K!', 'impact': 35},
    {'type': 'warning', 'message': 'Bandwidth usage at 85% capacity', 'impact': -4},
    {'type': 'error', 'message': 'Email server blacklisted! Immediate action required', 'impact': -16},
    {'type': 'success', 'message': 'Zero security incidents this month!', 'impact': 28},
]

SERVER_LOCATIONS = ['US-East-1', 'US-West-2', 'US-Central-1', 'EU-West-1', 'EU-West-3', 'EU-North-1', 'Asia-Pacific-1', 'Asia-Pacific-2', 'South-America-1']

ACHIEVEMENTS = [
    {'id': 1, 'name': 'First Step', 'description': 'Resolve your first ticket', 'requirement': 'tickets_resolved', 'threshold': 1, 'points': 10},
    {'id': 2, 'name': 'Support Hero', 'description': 'Resolve 10 support tickets', 'requirement': 'tickets_resolved', 'threshold': 10, 'points': 50},
    {'id': 3, 'name': 'Task Master', 'description': 'Complete 10 work tasks', 'requirement': 'tasks_completed', 'threshold': 10, 'points': 50},
    {'id': 4, 'name': 'High Achiever', 'description': 'Reach 500 points', 'requirement': 'score', 'threshold': 500, 'points': 100},
    {'id': 5, 'name': 'Veteran', 'description': 'Work for 7 days', 'requirement': 'current_day', 'threshold': 7, 'points': 75},
    {'id': 6, 'name': 'Speed Demon', 'description': 'Resolve 25 tickets', 'requirement': 'tickets_resolved', 'threshold': 25, 'points': 100},
    {'id': 7, 'name': 'Elite Status', 'description': 'Reach 1000 points', 'requirement': 'score', 'threshold': 1000, 'points': 200},
]

BONUS_CHALLENGES = [
    {'id': 1, 'title': 'Rush Hour', 'description': 'Resolve 3 tickets in a row', 'points': 50, 'type': 'streak'},
    {'id': 2, 'title': 'Perfect Day', 'description': 'Complete all daily tasks', 'points': 40, 'type': 'daily'},
    {'id': 3, 'title': 'Critical Response', 'description': 'Resolve 2 critical tickets', 'points': 60, 'type': 'priority'},
    {'id': 4, 'title': 'Efficiency Expert', 'description': 'Use detailed responses for 5 tickets', 'points': 45, 'type': 'quality'},
]

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
        session['achievements_unlocked'] = []
        session['ticket_streak'] = 0
        session['detailed_responses'] = 0
        session['critical_tickets_resolved'] = 0
        session['active_bonus'] = random.choice(BONUS_CHALLENGES)

def check_achievements():
    """Check and unlock achievements"""
    newly_unlocked = []
    for achievement in ACHIEVEMENTS:
        if achievement['id'] not in session.get('achievements_unlocked', []):
            current_value = session.get(achievement['requirement'], 0)
            if current_value >= achievement['threshold']:
                session['achievements_unlocked'].append(achievement['id'])
                session['score'] += achievement['points']
                newly_unlocked.append(achievement)
    return newly_unlocked

def check_bonus_challenge():
    """Check if active bonus challenge is completed"""
    bonus = session.get('active_bonus', {})
    if not bonus:
        return None
    
    challenge_type = bonus.get('type')
    completed = False
    
    if challenge_type == 'streak' and session.get('ticket_streak', 0) >= 3:
        completed = True
    elif challenge_type == 'daily' and len(session.get('daily_tasks', [])) == 0:
        completed = True
    elif challenge_type == 'priority' and session.get('critical_tickets_resolved', 0) >= 2:
        completed = True
    elif challenge_type == 'quality' and session.get('detailed_responses', 0) >= 5:
        completed = True
    
    if completed:
        session['score'] += bonus['points']
        completed_bonus = bonus.copy()
        session['active_bonus'] = random.choice(BONUS_CHALLENGES)
        return completed_bonus
    return None


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
                         performance_rating=round(performance_rating, 1),
                         active_bonus=session.get('active_bonus', {}),
                         achievements_count=len(session.get('achievements_unlocked', [])))

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
    
    # Find the ticket to check priority
    resolved_ticket = None
    for t in session['active_tickets']:
        if t['id'] == ticket_id:
            resolved_ticket = t
            break
    
    # Remove ticket from active tickets
    session['active_tickets'] = [t for t in session['active_tickets'] if t['id'] != ticket_id]
    session['tickets_resolved'] += 1
    
    # Track bonus challenge progress
    session['ticket_streak'] = session.get('ticket_streak', 0) + 1
    if response_quality == 'detailed':
        session['detailed_responses'] = session.get('detailed_responses', 0) + 1
    if resolved_ticket and resolved_ticket.get('priority') == 'Critical':
        session['critical_tickets_resolved'] = session.get('critical_tickets_resolved', 0) + 1
    
    # Award points based on response quality
    points = {'quick': 5, 'standard': 10, 'detailed': 15}.get(response_quality, 10)
    session['score'] += points
    
    # Check for achievements and bonus challenges
    check_achievements()
    check_bonus_challenge()
    
    # Add new ticket if needed
    active_ticket_ids = {t['id'] for t in session['active_tickets']}
    remaining_tickets = [t for t in SUPPORT_TICKETS if t['id'] not in active_ticket_ids]
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
        
        # Check for achievements and bonus challenges
        check_achievements()
        check_bonus_challenge()
        
        # Add new task if needed
        active_task_ids = {t['id'] for t in session['daily_tasks']}
        remaining_tasks = [t for t in WORK_TASKS if t['id'] not in active_task_ids]
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
                         rank=rank,
                         achievements=ACHIEVEMENTS,
                         unlocked_ids=session.get('achievements_unlocked', []))

@app.route('/achievements')
def achievements():
    """View achievements page"""
    initialize_session()
    
    unlocked_achievements = []
    locked_achievements = []
    
    for achievement in ACHIEVEMENTS:
        current_value = session.get(achievement['requirement'], 0)
        progress = min(100, int((current_value / achievement['threshold']) * 100))
        achievement_data = achievement.copy()
        achievement_data['progress'] = progress
        
        if achievement['id'] in session.get('achievements_unlocked', []):
            unlocked_achievements.append(achievement_data)
        else:
            locked_achievements.append(achievement_data)
    
    return render_template('achievements.html',
                         employee_name=session['employee_name'],
                         unlocked=unlocked_achievements,
                         locked=locked_achievements,
                         total_achievements=len(ACHIEVEMENTS),
                         unlocked_count=len(unlocked_achievements))


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
    # Get configuration from environment variables
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', '5000'))
    
    app.run(debug=debug_mode, host=host, port=port)
