const theTabItems = document.querySelectorAll('.theTabs-item');
const loadingDiv = document.getElementById("loading");
let list = document.getElementById("allProductsWrapper");
let pagination = document.getElementById("pagination");


for (let i = 0; i < theTabItems.length; i++) {
    const tabItem = theTabItems[i];
    tabItem.onclick = function (e) {
        e.preventDefault();
        console.log('Tab Item Clicked', e);
        const tabId = e.target.id;
        const tabName = e.target.innerText;
        const tabSlug = e.target.dataset.slug;

        loadingDiv.classList.toggle("flexCenter");

        for (const theTabItem of theTabItems) {
            theTabItem.classList.remove(
                'active'
            );
        }
        tabItem.classList.toggle("active");

        fetch('/products-json/' + tabId, {
            method: 'GET',
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonResponse) {
            const item = e.target.parentElement;
            products = jsonResponse['products'];
            prodLen = products.length
            iter_pages = jsonResponse['iter_pages'];
            currentPage = jsonResponse['currentPage'];
            prev_num = jsonResponse['prev_num'];
            next_num = jsonResponse['next_num'];
            has_prev = jsonResponse['has_prev'];
            has_next = jsonResponse['has_next'];
            
            console.log('Parent?', e.target);
            console.log(item);
            console.log(jsonResponse);
            console.log(products);
            console.log(prodLen);
            
            while (list.hasChildNodes()) {
                list.removeChild(list.firstChild);
                pagination.textContent = '';
            }
            if (products == 0) {
                const content = `
                <article class="the-products card no-products">
                    <p> Oops! There are no Products in this category </p>
                </article>
                `
                list.innerHTML += content;
                loadingDiv.classList.remove('flexCenter');
            } else {
                products.forEach(function (product) {
                    console.log(product);
                    const liItem = document.createElement('article');
                    liItem.classList = 'the-products card';
                    console.log(product.id);
                    // Construct card content
                    const content = `
                    <article class="the-products card 3">
                        <a href="/product/${product.slug}">
                                <div class="card-img product-img">
                                <img src="${product.product_img}" alt="">
                            </div>
                        </a>
                        <div class="card-text">
                            <a href="/product/${product.slug}">
                                <h2 class="product-title">${product.name}</h2>
                            </a>
                            <span class="product-price">${product.sellingPrice}</span>
                        </div>
                    </article>
                    `
                    loadingDiv.classList.remove('flexCenter');
                    // Append newly created card element to the container
                    list.innerHTML += content;
                });
                
                let paginationLinks = "";
                for (let index = 0; index < iter_pages.length; index++) {
                    let page = iter_pages[index];
                    let urlRoute = `/category/${tabSlug}?page=${page}`;
                    paginationLinks += `<a href="${urlRoute}" class="page-numbers ${page === currentPage ? 'current' : ''}">${page}</a>`;
                }
                // Construct Pagination Content
                const thePagination = `
                    <a href="/category/${tabSlug}?page=${prev_num}" class="page-numbers ${has_prev ? '' : 'disabled'}"> &laquo; </a>
                    ${paginationLinks}
                    <a href="/category/${tabSlug}?page=${next_num}" class="page-numbers ${has_next ? '' : 'disabled'}"> &raquo; </a>
                    `

                // Append newly created pagination element to the Pagination container
                pagination.innerHTML += thePagination;
            }
        })
        .catch(function (e) {
            console.error(e);
        });
    };
}
