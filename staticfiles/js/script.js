document.addEventListener("DOMContentLoaded", function() {
    var stickyNavbar = document.querySelector('.sticky-navbar');

    if (!stickyNavbar) {
        console.error("Sticky navbar element not found");
        return;
    }

    console.log("Sticky navbar script loaded");

    window.addEventListener('scroll', function() {
        console.log("Scroll event detected");
        if (window.scrollY > 100) {
            stickyNavbar.style.backgroundColor = 'rgba(25, 21, 33, 1)';
            console.log("Navbar set to fully opaque");
        } else {
            stickyNavbar.style.backgroundColor = 'rgba(25, 21, 33, 0.5)';
            console.log("Navbar set to more opaque");
        }
    });
});