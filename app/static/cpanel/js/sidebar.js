let sideBar = document.querySelector(".sidebar");
let menuOpenBtn = document.querySelector(".app-header .bx-menu");
let menuCloseBtn = document.querySelector(".sidebar .bx-x");
let appContent = document.querySelector(".app-content");
let menuCollapseBtn = document.querySelector(".collapse");
let minProfile = document.querySelector(".minProfileContainer");
let theMinProfile = document.querySelector(".minProfile");
let minProfileMenu = document.querySelector(".minProfileMenu");

// open & close sidebar on mobile
menuOpenBtn.onclick = function () {
    sideBar.style.left = "0";
}
menuCloseBtn.onclick = function () {
    sideBar.style.left = "-100%";
}

// collapse & expand sidebar on desktop sidebar-list-item
const sidebarState = localStorage.getItem("sidebarState");

if (sidebarState == "expanded" || sidebarState === null) {
    sideBar.classList.add("sidebar-expanded");
    appContent.classList.add("sidebar-expanded");
} else if (sidebarState == "collapsed") {
    sideBar.classList.add("sidebar-collapsed");
    appContent.classList.add("sidebar-collapsed");
}

menuCollapseBtn.onclick = function () {
    state = 'expanded'
    if (sideBar.classList.contains("sidebar-collapsed")) {
        sideBar.classList.remove("sidebar-collapsed");
        appContent.classList.remove("sidebar-collapsed");
        sideBar.classList.toggle("sidebar-expanded");
        appContent.classList.toggle("sidebar-expanded");
    } else if (sideBar.classList.contains("sidebar-expanded")) {
        state = 'collapsed'
        sideBar.classList.remove("sidebar-expanded");
        appContent.classList.remove("sidebar-expanded");
        sideBar.classList.toggle("sidebar-collapsed");
        appContent.classList.toggle("sidebar-collapsed");
    }
    localStorage.setItem("sidebarState", state);
}

// open & close min profile info
minProfile.onclick = function () {
    minProfileMenu.style.opacity = '0';
    minProfileMenu.classList.toggle("opened");
    theMinProfile.classList.toggle("opened");
    setTimeout(() => minProfileMenu.style.opacity = '1', 100);
}