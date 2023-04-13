const cartWrapper = document.querySelector('.cartWrapper');
const cartCount = document.querySelector('.cart-count');

cartWrapper.addEventListener('click', (event) => {
    const target = event.target;

    if (target.classList.contains('quantityBtn')) {
        const inputBox = target.parentNode.querySelector('.quantityInput');
        const currentValue = parseInt(inputBox.value);
        if (target.classList.contains('minus')) {
            inputBox.value = Math.max(currentValue - 1, 1);
        } else {
            inputBox.value = currentValue + 1;
        }
    } else if (target.classList.contains('delBtn')) {
        const cartItem = target.closest('.cartItem');
        const productId = target.dataset.product_id;
        const productSize = target.dataset.size;
        const productColor = target.dataset.color;
        const url = '/delete-from-cart';

        cartItem.classList.toggle('faded');

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
                const success = jsonResponse['success'];

                if (success === true) {
                    const msg = 'Product deleted from cart successfully';
                    const status = 'success';
                    cartCount.textContent = jsonResponse['cart_count'];
                    toggleAlert(msg, status)
                    removeItem(cartItem)
                } else {
                    const msg = 'Error Deleting product from cart. Please try again';
                    const status = 'error';
                    toggleAlert(msg, status)
                    return
                }
            })
            .catch((error) => {
                const msg = 'Error deleting product from cart. Please try again. <br> if error persist, please contact the site owner';
                const status = 'error';
                toggleAlert(msg, status)
                throw error;
            })
            .finally(() => {
                cartItem.classList.toggle('faded');
            });
    }
});

const removeItem = (itemToRemove) => {
    requestAnimationFrame(() => {
        itemToRemove.style.transform = 'translateX(-100vw)'

        itemToRemove.addEventListener('transitionend', () => {
            itemToRemove.style.height = '0px'
            itemToRemove.style.margin = '0px'
            itemToRemove.style.padding = '0px'
            setTimeout(() => {
                itemToRemove.remove();

                // Check if all items have been removed
                const cartItems = document.querySelectorAll('.cartItem');
                if (cartItems.length === 0) {
                    const cartEmptyMessage = `
                        <section class="noCart flexCenter">
                            <div class="card noCartCard flexCenter">
                                <img src="/static/frontend/img/cart.svg" alt="no cart">
                                <h2 title=""> Your cart is empty. </h2>
                                <p> Use the button below to start shopping </p>
                                <a href="/" class="btn start-shopping"> Start Shopping </a>
                            </div>
                        </section>
                    `;
                    cartWrapper.innerHTML = cartEmptyMessage;
                }
            }, 150);
        }, { once: true })
    });
}