// Hover effect for events on Events page
$(document).ready(function(){
    $('.list-group-item').hover(
        function() { 
            $(this).css({
                'transform': 'scale(1.05)',
                'transition': 'transform 0.3s'
            });
        },
        function() { 
            $(this).css('transform', 'scale(1)');
        }
    );
});