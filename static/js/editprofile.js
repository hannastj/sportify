document.addEventListener('DOMContentLoaded', () => {
  // Toggle functionality for the "See more" link in the clubs list
  window.toggleItems = function(link, hiddenClass) {
    const ul = link.closest('ul');
    if (!ul) return;
    const hiddenItems = ul.querySelectorAll('.' + hiddenClass);
    if (!hiddenItems.length) return;
    const currentlyHidden = hiddenItems[0].style.display === 'none';
    hiddenItems.forEach(item => {
      item.style.display = currentlyHidden ? 'list-item' : 'none';
    });
    link.textContent = currentlyHidden ? 'See less' : 'See more';
  };

  // Character counter for the bio field
  const bioField = document.getElementById('bio');
  const charCountDisplay = document.getElementById('char-count');
  const maxChars = 250;
  
  if (bioField && charCountDisplay) {
    // Set initial count
    charCountDisplay.textContent = maxChars - (bioField.value ? bioField.value.length : 0);
    
    // Update count on user input
    bioField.addEventListener('input', function() {
      const remaining = maxChars - this.value.length;
      charCountDisplay.textContent = remaining >= 0 ? remaining : 0;
    });
  }
});
