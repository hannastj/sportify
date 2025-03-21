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
    //SEARCH BUDDY CARD LOGIC
    const buddySearchForm = document.getElementById('buddySearchForm');
    const searchInput = document.getElementById('searchQuery');
    const buddyGrid = document.getElementById('buddyGrid');

    buddySearchForm.addEventListener('submit', function (e) {
        e.preventDefault();

        //CALL SEARCH
        const query = searchInput.value.trim();
        fetch(`/social/ajax/buddy-search/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {

                //CLEAR EXISTING BUDDY GRID
                buddyGrid.innerHTML = '';

                //RE-BUILD NEW BUDDY CARD VIA JSON
                data.users.forEach(user => {
                    const cardDiv = document.createElement('div');
                    cardDiv.classList.add('buddy-card');
                    cardDiv.dataset.buddyId = user.id;

                    //RE-SET BUDDY CARD INFO TO ONLY SHOW USERNAME
                    cardDiv.innerHTML = `
                    <img src="/media/profile_pictures/avatar.jpg" alt="${user.username}">
                    <p class="buddy-info">${user.username}</p>
                    <button class="buddy-request-btn">Request</button>`;

                    //RE-SET SCALE UPON HOVER
                    cardDiv.addEventListener('mouseover', function () {
                        cardDiv.style.transform = 'scale(1.3)';
                        cardDiv.style.zIndex = "9999";

                        //RE-FETCH BUDDY DETAILS UPON HOVER & SELECT RANDOM COLOUR AGAIN
                        fetch(`/social/ajax/buddy-details/${user.id}/`)
                            .then(r => r.json())
                            .then(d => {
                                const infoEl = cardDiv.querySelector('.buddy-info');
                                infoEl.textContent = d.username;
                                infoEl.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                                infoEl.style.transform = 'scale(1.3)';
                            })
                            .catch(err => console.error("Error fetching details:", err));
                    });

                    cardDiv.addEventListener('mouseout', function () {
                        cardDiv.style.transform = 'scale(1)';
                        cardDiv.style.zIndex = '0';
                    });
                    buddyGrid.appendChild(cardDiv);
                });
            });

        //-------------------------------------------------------------------------------
        //HELPER FUNCTION FOR CSRF
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