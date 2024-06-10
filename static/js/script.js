document.addEventListener("DOMContentLoaded", function() {
    let stickyNavbar = document.querySelector('.sticky-navbar');
    let logo = document.querySelector('.logo');
    let navbarButton = document.querySelector('.navbar-button');
    let navbarButtonIcon = document.querySelector('.navbar-button i.fa-bars');

    if (!stickyNavbar) {
        console.error("Sticky navbar element not found");
        return;
    }

    if (!logo) { 
        console.error("Logo element not found");
        return;
    }

    if (!navbarButton) { 
        console.error("Navbar button element not found");
        return;
    }

    if (!navbarButtonIcon) {
        console.error("Navbar button icon element not found");
        return;
    }

    console.log("Sticky navbar script loaded");

    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            stickyNavbar.style.backgroundColor = 'rgba(25, 21, 33, 1)';
            logo.style.color = 'white';
            navbarButton.style.color = 'white';
            navbarButtonIcon.style.color = 'white'; 
        } else {
            stickyNavbar.style.backgroundColor = 'rgba(25, 21, 33, 0.1)';
            logo.style.color = '#191521';
            navbarButton.style.color = '#191521';
            navbarButtonIcon.style.color = '#191521';  
        }
    });
});