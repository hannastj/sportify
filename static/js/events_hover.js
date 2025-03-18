// Hover effect for events on Events page
$(document).ready(function(){
    $('.list-group-item').hover(
        function() { // mouse enters
            $(this).css({
                'transform': 'scale(1.05)',
                'transition': 'transform 0.3s'
            });
        },
        function() { // mouse leaves
            $(this).css('transform', 'scale(1)');
        }
    );
});