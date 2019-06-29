const products = [
    {id: 1, title: 'Notebook', price: 2000},
    {id: 2, title: 'Keyboard', price: 70},
    {id: 3, title: 'Mouse', price: 46},
    {id: 4, title: 'Gamepad', price: 68},
    {id: 5, title: 'Chair', price: 168},
    {id:6},
];

const renderProduct = (title="Empty product", price=0) => {
    return `<div class="product-item">
                <img src="" alt="Product image" class="product-image"/>
                <h5>${title}</h5>
                <p>${price}</p>
                <button class="btn btn-default">Купить</button>
            </div>`
};

const renderPage = (list=[]) => {
    const productList = list.map(item => renderProduct(item.title, item.price));
    document.querySelector(`.products`).innerHTML = productList.join('\n');
};

/* Как бы сделал я без innerHTML */
/*
const renderProduct = (title="Empty product", price=0) => {
    let itemBlock = document.createElement('div');
    itemBlock.classList.add('product-item');

    let itemImage = new Image();
    // itemImage.src = null;
    itemImage.classList.add('product-image');
    itemImage.alt = "Product image";

    let itemTitle = document.createElement('h5');
    itemTitle.textContent = title;

    let itemPrice = document.createElement('p');
    itemPrice.textContent = price;

    let itemButton = document.createElement('button');
    itemButton.classList.add('btn');
    itemButton.classList.add('btn-default');
    itemButton.textContent = 'Добавить';

    itemBlock.appendChild(itemImage);
    itemBlock.appendChild(itemTitle);
    itemBlock.appendChild(itemPrice);
    itemBlock.appendChild(itemButton);

    return itemBlock;
};

const renderPage = (list=[]) => {
    let qsProducts = document.querySelector(`.products`);
    list.forEach(item => {
        qsProducts.appendChild(renderProduct(item.title, item.price));
    });
};
*/

renderPage(products);
