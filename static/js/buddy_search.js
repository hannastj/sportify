document.addEventListener("DOMContentLoaded", function() {
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchQuery');
    const buddyGrid = document.getElementById('buddyGrid');

    if (searchBtn && searchInput && buddyGrid) {
        searchBtn.addEventListener('click', function() {
            const query = searchInput.value.trim();
            if (!query) {
                alert("Please type a username to search.");
                return;
            }

            // Make AJAX call to search endpoint
            fetch(`/ajax/buddy-search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    // Clear existing cards
                    buddyGrid.innerHTML = '';

                    // data.results is an array of user objects
                    data.results.forEach(user => {
                        // Create a new card
                        const cardDiv = document.createElement('div');
                        cardDiv.classList.add('buddy-card');
                        cardDiv.dataset.buddyId = user.id;

                        cardDiv.innerHTML = `
              <p class="buddy-info">${user.username} - ${user.age || 'N/A'}</p>
            `;

                        // If you have hover logic, add it here
                        cardDiv.addEventListener('mouseover', () => {
                            cardDiv.style.transform = 'scale(1.5)';
                        });
                        cardDiv.addEventListener('mouseout', () => {
                            cardDiv.style.transform = 'scale(1)';
                        });

                        buddyGrid.appendChild(cardDiv);
                    });
                })
                .catch(error => console.error('Error fetching buddy search:', error));
        });
    }
});