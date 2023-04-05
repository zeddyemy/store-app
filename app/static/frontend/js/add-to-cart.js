// get the necessary elements
const productWrapper = document.querySelector('.allProductsWrapper')
const plusCartBtns = document.querySelectorAll('.plusCart');
const bottomSheet = document.getElementById('bottomSheet');
const bottomSheetTitle = bottomSheet.querySelector('h3.title');
const sizeOptionsLabel = document.querySelector('.sizeTitle');
const colorOptionsLabel = document.querySelector('.colorTitle');
const theSizeOptions = document.querySelector('.sizeRadios');
const theColorOptions = document.querySelector('.colorRadios');
const quantityInput = document.querySelector('.quantityInput');

const validateMsg = document.getElementById('validateMsg');
const addToCartBtn = document.querySelector('.addToCart');
const btnTxt = document.getElementById('btnTxt');
const loadIco = document.getElementById('loadIco');
const theIco = loadIco.querySelector('.bx')

const toggleLoading = () => {
    addToCartBtn.disabled = !addToCartBtn.disabled; // disable button to prevent multiple clicks
    btnTxt.classList.toggle('hidden');
    loadIco.classList.toggle('hidden');
    theIco.classList.toggle('bx-spin')
};

const toggleSheet = () => {
    bottomSheet.classList.toggle('visible')
}

window.addEventListener('click', event => {
    let closeSheet = bottomSheet.querySelector('.closeSheet');
    if (event.target == bottomSheet || event.target == closeSheet) {
        toggleSheet();
    }
});

// function to populate the size options
function populateSizeOptions(sizes) {
    // add each size option as a radio button
    sizes.split(',').forEach((size) => {
        const sizeOption = document.createElement('label');
        sizeOption.innerHTML = `
            <input type="radio" name="size" value="${size}">
            <span>${size}</span>
        `;
        theSizeOptions.appendChild(sizeOption);
    });
}

// function to populate the color options
function populateColorOptions(colors) {
    // add each color option as a radio button
    colors.split(',').forEach((color) => {
        const colorOption = document.createElement('label');
        colorOption.innerHTML = `
            <input type="radio" name="color" value="${color}">
            <span style="background-color: ${color}"></span>
        `;
        theColorOptions.appendChild(colorOption);
    });
}

// Listen for clicks on the add to cart button
productWrapper.addEventListener('click', function (e) {
    // Check if the clicked element has the class 'plusCart'
    if (e.target.classList.contains('plusCart')) {
        // Get the product ID and other data from the data attributes
        const productId = e.target.dataset.product_id;
        const productSizes = e.target.dataset.sizes;
        const productColors = e.target.dataset.colors;

        console.log('PLUS BTN LOG\n', 'productId =>', productId, '\nproductSizes =>', productSizes, '\nproductColors =>', productColors);
        showBottomSheet(productId, productSizes, productColors);
    }
});

function showBottomSheet(productId, productSizes, productColors) {
    // Clear any existing options
    bottomSheetTitle.innerHTML = 'Please select a variation';
    sizeOptionsLabel.innerHTML = '';
    colorOptionsLabel.innerHTML = '';
    theSizeOptions.innerHTML = '';
    theColorOptions.innerHTML = '';

    if (!productSizes && !productColors) {
        bottomSheetTitle.innerHTML = 'Please select the quantity of your choice'
    }

    if (productSizes !== '') {
        sizeOptionsLabel.innerHTML = 'Size';
        populateSizeOptions(productSizes)
    }
    if (productColors !== '') {
        colorOptionsLabel.innerHTML = 'Color';
        populateColorOptions(productColors)
    }

    // Update the add to cart button with the selected product ID
    addToCartBtn.dataset.productId = productId;
    addToCartBtn.dataset.productSizes = productSizes;
    addToCartBtn.dataset.productColors = productColors;

    toggleSheet();
};

// Listen for clicks on the add to cart button
addToCartBtn.addEventListener('click', () => {
    const productId = addToCartBtn.dataset.productId;
    const productSizes = addToCartBtn.dataset.productSizes;
    const productColors = addToCartBtn.dataset.productColors;
    const selectedSize = document.querySelector('input[name="size"]:checked');
    const selectedColor = document.querySelector('input[name="color"]:checked');
    const selectedSizeVal = selectedSize ? selectedSize.value : '';
    const selectedColorVal = selectedColor ? selectedColor.value : '';
    const quantity = quantityInput.value;
    const url = '/add-to-cart/' + productId;
    let msg;
    let status;

    const resetOptions = () => {
        quantityInput.value = 1;
        if (selectedSize) {
            selectedSize.checked = false;
        }
        if (selectedColor) {
            selectedColor.checked = false;
        }
    };

    console.log('<-----ADD TO CART LOG----->\n', 'productId =>', productId, '\nproductSizes =>', productSizes, '\nproductColors =>', productColors, '\nselectedSize =>', selectedSize, '\nselectedColor =>', selectedColor, '\nquantity =>', quantity);

    // validate that options have been selected
    console.log('productSizes => ', productSizes);
    console.log('productColors => ', productColors);
    console.log('\n----------------------------\n');
    console.log('!selectedSize => ', !selectedSize);
    console.log('!selectedColor => ', !selectedColor);
    if ((productSizes.length && !selectedSize) || (productColors.length && !selectedColor)) {
        validateMsg.style.color = 'red';
        validateMsg.textContent = 'Please make sure you select the necessary variation';
        return;
    }

    // disable the add to cart button and show the loading spinner
    toggleLoading();

    // make the ajax request to add the item to the cart
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            productId: productId,
            size: selectedSizeVal,
            color: selectedColorVal,
            quantity: quantity
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
                console.log('Product added to cart');
                msg = 'Product added to cart successfully';
                status = 'success';
                cartCount.textContent = jsonResponse['cart_count'];

                // reset the form and close the bottom sheet
                resetOptions();
                toggleAlert(msg, status)
                toggleSheet();
            } else {
                msg = 'Error adding product to cart. Please try again';
                status = 'error';
                toggleAlert(msg, status)
                return
            }
        })
        .catch((error) => {
            msg = 'Error adding product to cart. Please try again. <br> if error persist, please contact the site owner';
            status = 'error';
            toggleAlert(msg, status)
            throw error;
        })
        .finally(() => {
            // re-enable the add to cart button and hide the loading spinner
            toggleLoading();
        });
});