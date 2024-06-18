// Sticky Navbar//
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

// Messages //
 document.addEventListener("DOMContentLoaded", function() {
            const messages = document.querySelectorAll('#messages .alert');
            messages.forEach(message => {
                setTimeout(() => {
                    message.style.opacity = 1;
                }, 100);
                setTimeout(() => {
                    message.style.opacity = 0;
                    setTimeout(() => {
                        message.remove();
                    }, 500); 
                }, 5000);
            });
        });

// Scroll to section with navbar//

document.addEventListener("DOMContentLoaded", function() {
    if (window.location.hash) {
      const element = document.querySelector(window.location.hash);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
      link.addEventListener('click', function(event) {
        event.preventDefault();
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          targetElement.scrollIntoView({ behavior: 'smooth' });
          history.pushState(null, null, targetId);
        }
      });
    });
  });

//Scroll to top button//

document.addEventListener('DOMContentLoaded', function() {
  const scrollToTopBtn = document.getElementById('scrollToTopBtn');

  window.addEventListener('scroll', function () {
    if (window.scrollY > 100) {
      scrollToTopBtn.style.display = 'block';
    } else {
      scrollToTopBtn.style.display = 'none';
    }
  });
  scrollToTopBtn.addEventListener('click', function () {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
});
