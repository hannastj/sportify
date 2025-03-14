// profile.js

// 1) Tab Switching
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

// 2) "See more"/"See less" toggling
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
