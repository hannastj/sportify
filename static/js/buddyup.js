document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll('.buddy-card');

    cards.forEach(card => {
        // On mouseover: scale the card and fetch extra data
        card.addEventListener('mouseover', function() {
            card.style.transform = 'scale(1.05)';
            const buddyId = card.dataset.buddyId; // get the buddy id from the data attribute
            if (buddyId) {
                fetch(`/social/ajax/buddy-details/${buddyId}/`)
                    .then(response => response.json())
                    .then(data => {
                        console.log("Buddy data:", data);
                        const infoEl = card.querySelector('.buddy-info');
                        infoEl.textContent = data.username + ", " + (data.age !== null ? data.age : "Age not available");})
                    .catch(error => console.error("Error fetching buddy details:", error));
            }
        });

        card.addEventListener('mouseout', function() {
            card.style.transform = 'scale(1)';
        });
    });
});
