/*!  Author: Zeddy Emmanuel

    --> Java script for the Header
    --> Copyright (c) 2021 - Zeddy Emmanuel
    
    --> File: header.js
*/

// Cache frequently accessed DOM elements
const header = document.querySelector(".default");
const searchBar = document.querySelector(".search-bar"); // search bar/Search Field
const triggerSearch = document.querySelector(".trigger-search"); // search icon
const wrapper = document.querySelector(".wrapper"); // body
const navLinks = document.querySelector(".nav-links");
const menuOpenBtn = document.querySelector(".navbar .bx-menu");
const menuCloseBtn = document.querySelector(".nav-links .bx-x");
const arrow = document.querySelectorAll(".arrow");

/*  ---------------------SCRIPT CODE FOR THE SEARCH BOX--------------------- */
// SLIDE UP FUNCTION
let slideUp = (target, duration = 500) => {
    target.style.transitionProperty = 'height, margin, padding';
    target.style.transitionDuration = duration + 'ms';
    target.style.height = target.offsetHeight + 'px';
    target.offsetHeight;
    target.style.overflow = 'hidden';
    target.style.height = 0;
    window.setTimeout(() => {
        target.style.display = 'none';
        target.style.removeProperty('height');
        target.style.removeProperty('overflow');
        target.style.removeProperty('transition-duration');
        target.style.removeProperty('transition-property');
        //alert("!");
    }, duration);
};
// SLIDE DOWN FUNCTION
const slideDown = (target, duration = 500) => {
    target.style.removeProperty('display');
    let display = window.getComputedStyle(target).display;
    if (display === 'none') display = 'block';
    target.style.display = display;
    const height = target.offsetHeight;
    target.style.overflow = 'hidden';
    target.style.height = 0;

    target.offsetHeight;
    target.style.transitionProperty = "height, margin, padding";
    target.style.transitionDuration = duration + 'ms';
    target.style.height = height + 'px';
    window.setTimeout(() => {
        target.style.removeProperty('height');
        target.style.removeProperty('overflow');
        target.style.removeProperty('transition-duration');
        target.style.removeProperty('transition-property');
    }, duration);
};

const toggleSearchBox = () => {
    triggerSearch.classList.toggle("active"); // toggle active class to to search icon
    searchBar.classList.toggle("expanded");
    header.classList.toggle("expand-1x"); // toggle class to expand/reduce header
    wrapper.classList.toggle("expand-wrapper"); // toggle class to expand/reduce wrapper
};
// If the search icon is clicked
triggerSearch.addEventListener("click", () => {
    toggleSearchBox();
    if (triggerSearch.classList.contains("active")) {
        slideDown(searchBar, 600); //now searchBox will be slide down with the 600ms speed.
        //after sliding search box, the input will immediately focus
        setTimeout(() => searchBar.querySelector("input").focus(), 300);
    } else {
        slideUp(searchBar, 300); //slide up the search box
    }
});
/*  -------------------------------END---------------------------------- */


/*  --------------------SCRIPT FOR THE NAVIGATION--------------------- */
// open & close sidebar
/*menuOpenBtn.addEventListener("click", () => (navLinks.style.right = "0"));
menuCloseBtn.addEventListener("click", () => (navLinks.style.right = "-100%"));

// open & close sidebar submenu
document.addEventListener("click", function (event) {
    if (event.target.matches('.arrow')) {
        const dropdownContent = event.target.nextElementSibling;
        event.target.classList.toggle("active");
        dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
    }
});*/

// When the user scrolls down, hide the navbar. When the user scrolls up, show the navbar
let lastScrollPos = 0;
const SCROLL_THRESHOLD = 35;
let isScrolling = false;

window.addEventListener("scroll", function () {
    const currentScrollPos = window.pageYOffset || document.documentElement.scrollTop;
    const headerHeight = header.getBoundingClientRect().height;

    // Check if the user has scrolled far enough
    if (Math.abs(lastScrollPos - currentScrollPos) <= SCROLL_THRESHOLD) {
        return;
    }

    // Throttle the scroll event
    if (!isScrolling) {
        window.requestAnimationFrame(function () {
            header.classList[(currentScrollPos > lastScrollPos) && (lastScrollPos > 0) ? 'add' : 'remove']('hide');
            // header.style.background = currentScrollPos > headerHeight ? "var(--header-bg-color)" : "transparent";
            
            // Store the current scroll position
            lastScrollPos = currentScrollPos;
            isScrolling = false;
        });
    }
    isScrolling = true;
});
/*  -------------------------------END---------------------------------- */
