document.addEventListener("DOMContentLoaded", function() {
    let stickyNavbar = document.querySelector('.sticky-navbar');
    let logo = document.querySelector('.logo');

    if (!stickyNavbar) {
        console.error("Sticky navbar element not found");
        return;
    }

    console.log("Sticky navbar script loaded");

    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            stickyNavbar.style.backgroundColor = 'rgba(25, 21, 33, 1)';
            logo.style.color = 'white';
        } else {
            stickyNavbar.style.backgroundColor = 'rgba(25, 21, 33, 0.1)';
            logo.style.color = 'black';
        }
    });
});