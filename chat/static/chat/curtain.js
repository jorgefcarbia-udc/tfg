$(document).ready(function(){
    $(".chat-input form").on('submit', function(e) {
        $(".curtain, .dot-typing").css("display", "block");
    });
});