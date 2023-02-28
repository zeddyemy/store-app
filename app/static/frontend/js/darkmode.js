const btn = document.querySelector(".btn-toggle");
const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");
const body = document.body;

const currentTheme = localStorage.getItem("theme");
if (currentTheme == "dark") {
    body.classList.add("dark-theme");
} else if (currentTheme == "light") {
    body.classList.add("light-theme");
}

btn.addEventListener("click", function () {
    let theme;
    if (prefersDarkScheme.matches) {
        body.classList.toggle("light-theme");
        theme = body.classList.contains("light-theme") ? "light" : "dark";
    } else {
        body.classList.toggle("dark-theme");
        theme = body.classList.contains("dark-theme") ? "dark" : "light";
    }
    localStorage.setItem("theme", theme);
});