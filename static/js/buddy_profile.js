card.addEventListener('click', function() {
    const buddyId = card.dataset.buddyId;
    window.location.href = `/buddy/${buddyId}/`;
});