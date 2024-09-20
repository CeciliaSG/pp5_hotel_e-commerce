// Sticky Navbar

/**
 * JavaScript to handle the dynamic styling of a sticky navbar based on scroll position.
 *
 * - Once the DOM is fully loaded, the script selects elements for the sticky navbar, 
 *   logo, navbar button, and the button's icon.
 * - A scroll event listener is added to the window to monitor the vertical scroll position 
 *   (`scrollY`):
 *   - If the scroll position is greater than 100 pixels, the navbar background becomes opaque, 
 *     and the text colour of the logo, button, and icon changes to white.
 *   - If the scroll position is less than or equal to 100 pixels, the navbar becomes 
 *     semi-transparent, and the text colour reverts to the original colour (`#191521`).
 */
document.addEventListener("DOMContentLoaded", function() {
    let stickyNavbar = document.querySelector('.sticky-navbar');
    let logo = document.querySelector('.logo');
    let logoText = document.querySelector('.logo-text');
    let navbarButton = document.querySelector('.navbar-button');
    let navbarButtonIcon = document.querySelector('.navbar-button i.fa-bars');

    let originalNavbarHeight = stickyNavbar.offsetHeight;

    if (!stickyNavbar || !logo || !navbarButton || !navbarButtonIcon) {
        return;
    }

    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            stickyNavbar.style.backgroundColor = 'rgba(25, 21, 33, 1)';
            stickyNavbar.style.height = originalNavbarHeight * 0.7 + 'px';
            logo.style.color = 'white';
            logo.style.transform = 'scale(0.7)';
            logoText.style.display = 'none';
            navbarButton.style.color = 'white';
            navbarButtonIcon.style.color = 'white'; 
        } else {
            stickyNavbar.style.backgroundColor = 'rgba(25, 21, 33, 0.1)';
            stickyNavbar.style.height = originalNavbarHeight + 'px';
            logo.style.color = '#191521';
            logo.style.transform = 'scale(1)';
            logoText.style.display = 'block'; 
            navbarButton.style.color = '#191521';
            navbarButtonIcon.style.color = '#191521';  
        }
    });
});


// Messages
/**
 * JavaScript to handle fading out and removing alert messages after a delay.
 *
 * - Once the DOM is fully loaded, selects all alert messages within the `#messages` 
 *   container.
 * - For each alert message:
 *   - The message's opacity is initially set to 1 (fully visible) after a brief delay 
 *     of 100 milliseconds, ensuring any initial transition effects are applied.
 *   - After 5 seconds (5000 milliseconds), the message's opacity is gradually set to 0 
 *     (fade out effect).
 *   - Once the fade-out is complete (after 500 milliseconds), the message element is 
 *     removed from the DOM entirely.
 */
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

// Scroll to section with navbar
/**
 * JavaScript to handle smooth scrolling for anchor links and hash-based navigation.
 *
 * - Once the DOM is fully loaded, checks if the URL contains a hash (fragment identifier).
 *   - If a valid hash is found and corresponds to an existing element, the page scrolls 
 *     smoothly to that element.
 *   - The hash must match a valid CSS selector format (i.e., a hash followed by letters, 
 *     digits, underscores, or hyphens).
 *
 * - For all anchor links (`<a>`) that refer to an element with an ID (i.e., links 
 *   starting with `#`), adds a click event listener.
 *   - When clicked, prevents the default link behaviour and smoothly scrolls to the 
 *     target element if it exists.
 *   - The page's URL is updated to include the target element's ID without reloading 
 *     the page, using `history.pushState()`.
 */
document.addEventListener("DOMContentLoaded", function() {
    if (window.location.hash) {
        const hash = window.location.hash;
        if (/^#[\w-]+$/.test(hash)) {
            const element = document.querySelector(hash);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        }
    }

    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const targetId = this.getAttribute('href');
            if (/^#[\w-]+$/.test(targetId)) {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                    history.pushState(null, null, targetId);
                }
            }
        });
    });
});

// Scroll to top button
/**
 * JavaScript to handle scrolling and button visibility based on page sections.
 *
 * - Adds an event listener for 'DOMContentLoaded' to initialise event handling once 
 *   the DOM is fully loaded.
 * - The `isInViewport` function determines if an element is visible within the viewport,
 *   returning `true` if fully visible.
 * - Attaches a click event to the 'scrollToAboutBtn', which smoothly scrolls to the 
 *   "About" section's <h1> element when clicked.
 * - On page scroll, the visibility of the 'scrollToAboutBtn' is toggled:
 *   - The button is hidden when the "About" section is in view or if the "Home" section
 *     is no longer in view.
 *   - The button is displayed when the "Home" section is visible in the viewport.
 * - Uses a passive event listener for performance optimisation during the button click.
 */
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

// Scroll to about button
/**
 * JavaScript code to handle scrolling and button visibility behaviour on a webpage.
 *
 * - The `isInViewport` function checks if an HTML element is currently visible within
 *   the user's viewport. It returns `true` if the element is fully visible, otherwise `false`.
 * 
 * - On DOMContentLoaded, the script attaches functionality to a button (`scrollToAboutBtn`)
 *   that, when clicked, smoothly scrolls the page to the "About" section's `<h1>` element.
 *
 * - The button's visibility dynamically changes based on scroll position:
 *   - The button is hidden when the "About" section is in view or when the "Home" section 
 *     is no longer in view.
 *   - The button reappears when the "Home" section is back in view.
 *
 * - Uses a `passive` event listener for the button click to improve scrolling performance.
 */
document.addEventListener('DOMContentLoaded', function() {
    function isInViewport(element, threshold = 0) {
        const rect = element.getBoundingClientRect();
        const windowHeight = window.innerHeight || document.documentElement.clientHeight;
        const elementVisible = rect.top < windowHeight - threshold && rect.bottom > threshold;
        return elementVisible;
    }

    const scrollToAboutBtn = document.getElementById('scrollToAboutBtn');

    function checkButtonVisibility() {
        const homeSection = document.getElementById('home');
        const aboutSection = document.getElementById('about');

        if (aboutSection && homeSection) {
            const threshold = 150;
            
            const aboutInView = isInViewport(aboutSection, threshold);
            const homeInView = isInViewport(homeSection);

            console.log(`About Section in view: ${aboutInView}`);
            console.log(`Home Section in view: ${homeInView}`);

            if (aboutInView || !homeInView) {
                scrollToAboutBtn.style.display = 'none';
            } else {
                scrollToAboutBtn.style.display = 'block';
            }
        }
    }

    if (scrollToAboutBtn) {
        scrollToAboutBtn.addEventListener('click', function() {
            const aboutH1 = document.querySelector('#about h1');
            if (aboutH1) {
                const offsetTop = aboutH1.offsetTop;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth',
                });
            }
        }, { passive: true });

        window.addEventListener('scroll', checkButtonVisibility);
        window.addEventListener('resize', checkButtonVisibility);

        setTimeout(() => {
            console.log('Initial visibility check');
            checkButtonVisibility();
        }, 500);
    }
});




/**
 * JavaScript to handle the visibility of the "Book Now" button based on scroll position and screen width.
 *
 * - Once the DOM is fully loaded, the script selects the element with the class `.book-now-button`.
 * - If the screen width is less than 769 pixels, a scroll event listener is added to the window.
 * - The scroll event listener monitors the vertical scroll position (`scrollY`):
 *   - If the scroll position is greater than 200 pixels, the "Book Now" button is hidden by adding 
 *     the `hidden` class.
 *   - If the scroll position is less than or equal to 200 pixels, the "Book Now" button is shown by 
 *     removing the `hidden` class and re-enabling pointer events.
 *
 * This functionality is intended for smaller screens, ensuring that the "Book Now" button is not 
 * always visible when the user scrolls down, improving the user experience on mobile devices.
 */

document.addEventListener("DOMContentLoaded", function() {
  const bookingButton = document.querySelector(".book-now-button");

  if (window.innerWidth < 769) {
    window.addEventListener("scroll", function() {
      let scrollTop = window.scrollY || document.documentElement.scrollTop;

      if (scrollTop > 200) { 
        bookingButton.classList.add("hidden");
      } else { 
        bookingButton.classList.remove("hidden");
        bookingButton.style.pointerEvents = 'auto';
      }
    });
  }
});
