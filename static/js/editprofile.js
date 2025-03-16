// editprofile.js

document.addEventListener('DOMContentLoaded', () => {
    // Toggle functionality for the "See more" link in the clubs list
    window.toggleItems = function(link, hiddenClass) {
      // Find the parent <ul> element that contains the clubs
      const ul = link.closest('ul');
      if (!ul) return;
  
      // Select all items with the given hiddenClass
      const hiddenItems = ul.querySelectorAll('.' + hiddenClass);
      if (!hiddenItems.length) return;
  
      // Check if items are currently hidden
      const currentlyHidden = hiddenItems[0].style.display === 'none';
  
      // Toggle visibility: change to list-item when showing, or hide when collapsing
      hiddenItems.forEach(item => {
        item.style.display = currentlyHidden ? 'list-item' : 'none';
      });
  
      // Update the link text accordingly
      link.textContent = currentlyHidden ? 'See less' : 'See more';
    }
  });
  