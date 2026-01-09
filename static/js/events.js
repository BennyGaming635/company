// Random Events System for Benco Company Simulation

// Check for random events periodically
function checkRandomEvents() {
    fetch('/api/random-event')
        .then(response => response.json())
        .then(data => {
            if (data.event) {
                showEventNotification(data.event);
            }
        })
        .catch(error => {
            console.error('Error checking for random events:', error);
        });
}

// Display event notification
function showEventNotification(event) {
    const notification = document.getElementById('event-notification');
    
    if (!notification) return;
    
    // Set notification content and type
    notification.textContent = event.message;
    notification.className = `event-notification ${event.type}`;
    
    // Show notification
    notification.classList.remove('hidden');
    
    // Hide after 5 seconds
    setTimeout(() => {
        notification.classList.add('hidden');
    }, 5000);
}

// Start checking for events when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Check for events every 45 seconds
    checkRandomEvents();
    setInterval(checkRandomEvents, 45000);
});
