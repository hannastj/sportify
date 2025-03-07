document.addEventListener("DOMContentLoaded", function() {
    // Select all buddy cards
    const buddyCards = document.querySelectorAll('.buddy-card');

    buddyCards.forEach((card) => {
        // On mouseover, enlarge the card
        card.addEventListener('mouseover', function() {
            // Smooth scale transform
            card.style.transition = 'transform 0.2s ease';
            card.style.transform = 'scale(1.2)';






            // OPTIONAL: If you want to do an AJAX call here, e.g. to fetch extra data
            const buddyId = card.dataset.buddyId;  // "1", "2", etc. if set in HTML
            if (buddyId) {
                fetch(`/ajax/buddy-details/${buddyId}/`)  // Example endpoint
                    .then(response => response.json())
                    .then(data => {
                        console.log("Buddy data:", data);
                        // e.g., update the card with more info
                        // card.querySelector('.buddy-info').textContent = data.username + ", " + data.age;
                    })
                    .catch(error => console.error("Error fetching buddy details:", error));
            }
        });

        // On mouseout, revert the card size
        card.addEventListener('mouseout', function() {
            card.style.transform = 'scale(1)';
        });
    });
});
