/*!  Author: Zeddy Emmanuel

    --> Global Java script for pages that display products
    --> Copyright (c) 2021 - Zeddy Emmanuel
    
    --> File: index.js
*/

/** increase or reduce quantity of product */
wrapper.addEventListener('click', (event) => { // 'wrapper' is already been declared (at header.js:1:1)
    const target = event.target;

    if (target.classList.contains('quantityBtn')) {
        const inputBox = target.parentNode.querySelector('.quantityInput');
        const currentValue = parseInt(inputBox.value);
        if (target.classList.contains('minus')) {
            inputBox.value = Math.max(currentValue - 1, 1);
        } else {
            inputBox.value = currentValue + 1;
        }
    }
});