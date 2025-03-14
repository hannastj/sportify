// JS for the hover effect for log out button

$(document).ready(function() {

    $(".logout-btn").hover(
      function() {

        $(this).addClass("logout-hover");
      },
      function() {

        $(this).removeClass("logout-hover");
      }
    );
  });
  