// Helper function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// AJAX function for joining an event
function joinEvent(eventId) {
    fetch(`/events/${eventId}/join/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'joined') {
            // Update the button for this event
            const button = document.getElementById(`join-leave-btn-${eventId}`);
            button.innerText = 'Leave Event';
            button.setAttribute('data-action', 'leave');
            button.className = 'btn btn-warning mb-2';
        }
    })
    .catch(error => console.error('Error joining event:', error));
}

// AJAX function for leaving an event
function leaveEvent(eventId) {
    fetch(`/events/${eventId}/leave/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'left') {
            // Check if the event container exists
            const eventElement = document.getElementById(`event-item-${eventId}`);
            if (eventElement) {
                eventElement.remove();  // Remove the event from the DOM immediately
            } else {
                // Fallback: update the button if container not found
                const button = document.getElementById(`join-leave-btn-${eventId}`);
                button.innerText = 'Join Event';
                button.setAttribute('data-action', 'join');
                button.className = 'btn btn-primary mb-2';
            }
        }
    })
    .catch(error => console.error('Error leaving event:', error));
}

// Attach event listeners once the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Select all buttons whose id starts with "join-leave-btn-"
    const buttons = document.querySelectorAll('[id^="join-leave-btn-"]');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id');
            const action = this.getAttribute('data-action');
            if (action === 'join') {
                joinEvent(eventId);
            } else if (action === 'leave') {
                leaveEvent(eventId);
            }
        });
    });
});
