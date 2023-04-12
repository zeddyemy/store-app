var deductBtnArr = document.querySelectorAll('.quantityBtn.minus')
var addButtonArr = document.querySelectorAll('.quantityBtn.plus')

for (let deductBtn of deductBtnArr) {
    deductBtn.onclick = function () {
        console.log('minus clicked');
        let currentInputBox = deductBtn.nextElementSibling;
        currentInputBox.value = currentInputBox.value - 1;
        if (currentInputBox.value <= 0) {
            currentInputBox.value = 1
        }
    }
}

for (let addButton of addButtonArr) {
    addButton.onclick = () => {
        console.log('plus clicked');
        let currentInputBox = addButton.previousElementSibling;
        currentInputBox.value = parseInt(currentInputBox.value) + 1;
    }
}

const deleteButtons = document.querySelectorAll('.delBtn');
const cartList = document.querySelector('.cartList');

deleteButtons.forEach((delBtn) => {
    delBtn.addEventListener('click', (event) => {
        const cartItem = event.target.closest('.cartItem');
        const productId = delBtn.dataset.product_id;
        const productSize = delBtn.dataset.size;
        const productColor = delBtn.dataset.color;
        const url = '/delete-from-cart';
        let msg;
        let status;
        
        cartItem.classList.toggle('faded');
        
        const removeItem = (itemToRemove) => {
            requestAnimationFrame(() => {
                itemToRemove.style.transform = 'translateX(-100vw)'
                const itemHeight = itemToRemove.offsetHeight;
                const itemsBelow = Array.from(itemToRemove.nextElementSibling);

                itemsBelow.forEach(item => {
                    const newPosition = parseFloat(item.style.transform.replace(/translateY\((-?\d+)px\)/, '$1')) - itemHeight;

                    // Set the new position of the card
                    item.style.transform = `translateY(${newPosition}px)`;
                });
                
                cartItem.addEventListener('transitionend', () => {
                    cartItem.remove();
                }, { once: true })
            });
        }
    
        // Here you can send an AJAX request to delete the cart item
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                productId: productId,
                size: productSize,
                color: productColor
            })
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((jsonResponse) => {
                console.log(jsonResponse)
                const success = jsonResponse['success'];
                const cartCount = document.querySelector('.cart-count');

                if (success === true) {
                    console.log('Product deleted from cart');
                    msg = 'Product deleted from cart successfully';
                    status = 'success';
                    cartCount.textContent = jsonResponse['cart_count'];

                    toggleAlert(msg, status)
                    removeItem(cartItem)
                } else {
                    msg = 'Error Deleting product from cart. Please try again';
                    status = 'error';
                    toggleAlert(msg, status)
                    return
                }
            })
            .catch((error) => {
                msg = 'Error deleting product from cart. Please try again. <br> if error persist, please contact the site owner';
                status = 'error';
                toggleAlert(msg, status)
                throw error;
            })
            .finally(() => {
                // re-enable the add to cart button and hide the loading spinner
                cartItem.classList.toggle('faded');
            });
    });
});