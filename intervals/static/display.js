
$(window).scroll(function () {
    if ($(this).scrollTop() > 0) {
        $('.amazon-button').fadeOut();
    } else {
        $('.amazon-button').fadeIn();
    }
});

$(window).scroll(function () {
    if ($(this).scrollTop() >= 0) {
        $('#btn-for-mobile1').fadeOut();
    } else {
        $('#btn-for-mobile1').fadeIn();
    }
});

window.addEventListener('scroll', function () {
    document.body.classList[
        window.scrollY > 20 ? 'add' : 'remove'
    ]('scrolled');
});
