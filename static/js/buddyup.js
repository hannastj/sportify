document.addEventListener("DOMContentLoaded", function() {
    //BUDDY CARD LIST LOGIC
    const cards = document.querySelectorAll('.buddy-card');
    const colors = ["#F4B942", "#6B9AC4", "#97D8C4", "#4059AD", "#242F40"];

    //UPON HOVERING OVER BUDDY CARD
    cards.forEach(card => {
        card.addEventListener('mouseover', function () {
            card.style.transform = 'scale(1.3)';
            card.style.zIndex = "9999";

            //FETCH THE DATA
            const buddyId = card.dataset.buddyId;
            if (buddyId) {
                fetch(`/social/ajax/buddy-details/${buddyId}/`)
                    .then(response => response.json())
                    .then(data => {
                        const infoEl = card.querySelector('.buddy-info');
                        infoEl.textContent =
                            data.username

                        //SELECT RANDOM COLOUR UPON HOVER
                        infoEl.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                        infoEl.style.transform = 'scale(1.3)';
                        card.style.zIndex = "9998";
                    })
                    .catch(error => console.error("Error fetching buddy details:", error));
            }
        });

        //TRANSFORM BACK TO ORIGINAL CARD SIZE
        card.addEventListener('mouseout', function () {
            card.style.transform = 'scale(1)';
            card.style.zIndex = "0";
        });

        //REDIRECT TO BUDDY PROFILE ON CLICK
        card.addEventListener('click', function () {
            const buddyId = card.dataset.buddyId;
            window.location.href = `/buddy/${buddyId}/`;
        });
    });


    //-------------------------------------------------------------------------------
    //SEARCH BUDDY
    const buddySearchForm = document.getElementById('buddySearchForm');
    const searchInput = document.getElementById('searchQuery');
    const buddyGrid = document.getElementById('buddyGrid');

    buddySearchForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const query = searchInput.value.trim();
        // Call the search endpoint
        fetch(`/social/ajax/buddy-search/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                // data.users is an array of {id, username, age, bio}
                // Clear the existing .buddy-grid
                buddyGrid.innerHTML = '';

                // Build new cards from the JSON
                data.users.forEach(user => {
                    const cardDiv = document.createElement('div');
                    cardDiv.classList.add('buddy-card');
                    cardDiv.dataset.buddyId = user.id;
                    cardDiv.innerHTML = `<img src="/media/profile_pictures/avatar.jpg" alt="${user.username}"><p class="buddy-info">${user.username}, ${user.age || 'N/A'}, ${user.bio}</p>`;

                    // Re-attach the HOVER logic here:
                    cardDiv.addEventListener('mouseover', function () {
                        cardDiv.style.transform = 'scale(1.3)';
                        cardDiv.style.zIndex = "9998";

                        // buddy detail fetch
                        fetch(`/social/ajax/buddy-details/${user.id}/`)
                            .then(r => r.json())
                            .then(d => {
                                const infoEl = cardDiv.querySelector('.buddy-info');
                                infoEl.textContent = `${d.username}\n${d.age || 'Age not available'}\n${d.bio}`;
                                infoEl.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                            })
                            .catch(err => console.error("Error fetching details:", err));
                    });

                    cardDiv.addEventListener('mouseout', function () {
                        cardDiv.style.transform = 'scale(1)';
                        cardDiv.style.zIndex = '0';
                    });

                    cardDiv.addEventListener('click', function () {
                        window.location.href = `/buddy/${user.id}/`;
                    });
                    buddyGrid.appendChild(cardDiv);
                });
                // The request button
                const requestBtn = cardDiv.querySelector('.buddy-request-btn');
                if (requestBtn) {
                    requestBtn.addEventListener('click', function(e) {
                        e.stopPropagation(); // prevent card click from triggering
                        sendBuddyRequest(buddyId);
                    });
                }
            });

        function sendBuddyRequest(buddyId) {
            // We need the CSRF token if Django’s CSRF is enabled
            const csrftoken = getCookie('csrftoken');

            fetch('/social/ajax/send-buddy-request/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrftoken,
                },
                body: `buddy_id=${encodeURIComponent(buddyId)}`
            })
                .then(response => response.json())
                .then(data => {
                    console.log("Buddy request response:", data);
                    alert("Buddy request sent to user " + data.buddy_id);
                })
                .catch(error => console.error("Error sending buddy request:", error));
        }


        // Helper function for CSRF
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
    });
});
