// Hovering for event on Home page
$(document).ready(function() {
  $('.next-event-link').hover(
    function() { $(this).addClass('hovered'); },
    function() { $(this).removeClass('hovered'); }
  );
});