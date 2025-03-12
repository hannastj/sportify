$(document).ready(function() {
    const $carousel = $("#carousel-container");
    const images = [
      $carousel.data("img1"),
      $carousel.data("img2"),
      $carousel.data("img3")
    ];
    let currentIndex = 0;
  
    // HS Function to update the background image with a fade effect
    function updateBackground() {
      $carousel.fadeOut(600, function() {
        $carousel.css("background-image", `url(${images[currentIndex]})`).fadeIn(600);
      });
    }
  
    // HS: Initialise with the first image
    updateBackground();
  
    // HS: Click event for left arrow: show previous image
    $(".left-arrow").click(function() {
      currentIndex = (currentIndex - 1 + images.length) % images.length;
      updateBackground();
    });
  
    // HS: Click event for right arrow: show next image
    $(".right-arrow").click(function() {
      currentIndex = (currentIndex + 1) % images.length;
      updateBackground();
    });
  });
  