document.addEventListener("DOMContentLoaded", function () {
    
    let categorySlider = document.getElementById('theCategories') 
    let NavButtons = categorySlider.querySelectorAll(".flickity-button");

    // my custom-nav
    let customCatNav = document.getElementById('cat-custom-control')

    customCatNav.appendChild(NavButtons[0])
    customCatNav.appendChild(NavButtons[1])

});