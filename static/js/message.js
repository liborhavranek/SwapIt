$(document).ready(function() {
    window.setTimeout(function() {
        $(".alert").fadeTo(1500, 0).slideUp(1500, function(){
            $(this).remove();
        });
    }, 2000);
});
