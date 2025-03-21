// profile.js

// Tab Switching
document.addEventListener('DOMContentLoaded', () => {
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');
  tabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
          tabButtons.forEach(b => b.classList.remove('active'));
          tabContents.forEach(tc => tc.classList.remove('active'));
          btn.classList.add('active');
          const targetId = btn.getAttribute('data-tab');
          document.getElementById(targetId).classList.add('active');
      });
  });
});

// "See more"/"See less" toggling
function toggleItems(link, hiddenClass) {
// Find all items in this <ul> with the given hiddenClass
const ul = link.closest('ul');
const hiddenItems = ul.querySelectorAll('.' + hiddenClass);
if (!hiddenItems.length) return;

// Determine if they're currently hidden or visible
const currentlyHidden = hiddenItems[0].style.display === 'none';

// Toggle visibility
hiddenItems.forEach(item => {
  item.style.display = currentlyHidden ? 'flex' : 'none';
});

// Change the link text
link.textContent = currentlyHidden ? 'See less' : 'See more';
}

// Make toggleItems globally available
window.toggleItems = toggleItems;


document.addEventListener("DOMContentLoaded", function() {
    // Select all forms that respond to buddy requests
    const respondForms = document.querySelectorAll('.respond-buddy-form');

    respondForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Stop normal form submission

            const requestId = form.dataset.requestId;
            // Which button was clicked? accept or reject
            const clickedButton = document.activeElement;
            const actionValue = clickedButton.value; // "accept" or "reject"

            // Build POST data
            const formData = new FormData(form);
            formData.set('action', actionValue); // ensure correct action

            // Make an AJAX (fetch) call
            fetch(`/social/buddy-requests/respond/${requestId}/`, {
                method: 'POST',
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    console.log("Buddy request response:", data);
                    // data => { message: "...", request_id: ... }

                    // Show success/failure in the message div
                    const msgDiv = document.getElementById(`buddy-message-${requestId}`);
                    if (msgDiv) {
                        msgDiv.textContent = data.message;
                        msgDiv.style.color = (actionValue === 'accept') ? 'green' : 'red';
                    }

                    // Remove or hide the form so user can't re-click
                    form.style.display = 'none';
                })
                .catch(error => console.error("Error responding to buddy request:", error));
        });
    });
});
