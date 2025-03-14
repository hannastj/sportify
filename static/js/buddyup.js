document.addEventListener("DOMContentLoaded", function() {

    //HOVER OVER BUDDY CARD
    const cards = document.querySelectorAll('.buddy-card');
    const colors = ["#F4B942", "#6B9AC4", "#97D8C4", "#4059AD", "#242F40"];
    cards.forEach(card => {
        // On mouseover: scale the card and fetch extra data
        card.addEventListener('mouseover', function() {
            card.style.transform = 'scale(1.5)';
            card.style.zIndex = "9999";

            const buddyId = card.dataset.buddyId; // get the buddy id from the data attribute
            if (buddyId) {
                fetch(`/social/ajax/buddy-details/${buddyId}/`)
                    .then(response => response.json())
                    .then(data => {
                        console.log("Buddy data:", data);
                        const infoEl = card.querySelector('.buddy-info');
                        infoEl.textContent =
                        data.username + "\n" +
                        (data.age !== null ? data.age : "Age not available") + "\n" +
                        data.bio.replace(/\n/g, " ");

                        //Random background colour
                        infoEl.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                    })
                    .catch(error => console.error("Error fetching buddy details:", error));
            }
        });

        card.addEventListener('mouseout', function() {
            card.style.transform = 'scale(1)';
            card.style.zIndex = "0";
        });
        card.addEventListener('click', function() {
            const buddyId = card.dataset.buddyId;
            window.location.href = `/buddy/${buddyId}/`;
        });
    });
});
