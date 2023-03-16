const theTabItems = document.querySelectorAll('.theTabs-item');
const loadingDiv = document.getElementById("loading");
const list = document.getElementById("all-products-wrapper");
const pagination = document.getElementById("pagination");

const activeTab = document.querySelector('.theTabs-item.active');
let activeTabSlug = activeTab ? activeTab.dataset.slug : '';

function setActiveTab(tabItem) {
    for (const theTabItem of theTabItems) {
        theTabItem.classList.remove('active');
    }
    tabItem.classList.add("active");
    activeTabSlug = tabItem.dataset.slug;
}

function renderProductCard(product) {
    const liItem = `
    <article class="the-products card ${product.category_id}">
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
            <span class="btn add-to-cart" id="" data-product_id="${product.id}">+</span>
        </div>
    </article>
    `;
    return liItem;
}

function generatePaginationLinks(iter_pages, currentPage, tabSlug) {
    let paginationLinks = "";
    for (let index = 0; index < iter_pages.length; index++) {
        let page = iter_pages[index];
        let urlRoute = `/category/${tabSlug}?page=${page}`;
        paginationLinks += `<a href="${urlRoute}" class="page-numbers ${page === currentPage ? 'current' : ''}">${page}</a>`;
    }
    return paginationLinks;
}

function renderProducts(jsonResponse) {
    const products = jsonResponse['products'];
    const prodLen = products.length;
    const iter_pages = jsonResponse['iter_pages'];
    const currentPage = jsonResponse['currentPage'];
    const prev_num = jsonResponse['prev_num'];
    const next_num = jsonResponse['next_num'];
    const has_prev = jsonResponse['has_prev'];
    const has_next = jsonResponse['has_next'];

    list.textContent = '';
    pagination.textContent = '';

    if (prodLen === 0) {
        const content = `
        <article class="the-products card no-products">
            <p> Oops! There are no Products in this category </p>
        </article>
        `;
        list.innerHTML += content;
        loadingDiv.classList.remove('flexCenter');
    } else {
        products.forEach((product) => {
            const liItem = renderProductCard(product);
            list.innerHTML += liItem;
        });

        const paginationLinks = generatePaginationLinks(iter_pages, currentPage, activeTabSlug);

        const thePagination = `
            <a href="/category/${activeTabSlug}?page=${prev_num}" class="page-numbers ${has_prev ? '' : 'disabled'}">Prev</a>
            ${paginationLinks}
            <a href="/category/${activeTabSlug}?page=${next_num}" class="page-numbers ${has_next ? '' : 'disabled'}">Next</a>
            `;
        pagination.innerHTML = thePagination;
        loadingDiv.classList.remove('flexCenter');
    }
}

for (let i = 0; i < theTabItems.length; i++) {
    const tabItem = theTabItems[i];
    tabItem.onclick = function (e) {
        e.preventDefault();
        console.log('Tab Item Clicked', e);
        const tabId = e.target.id;
        const tabName = e.target.innerText;
        const tabSlug = e.target.dataset.slug;

        loadingDiv.classList.toggle("flexCenter");

        setActiveTab(tabItem)

        fetch('/products-json/' + tabId, {
            method: 'GET',
        })
        .then(function (response) {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(function (jsonResponse) {
            renderProducts(jsonResponse)
        })
        .catch(function(error) {
            console.error('There was a problem with the fetch operation:', error);
            
            const content = `
            <article class="the-products card no-products">
                <p>Oops! There was an error loading products. Please try again later.</p>
            </article>
            `;
            list.innerHTML += content;
            loadingDiv.classList.remove('flexCenter');
        });
    }
}