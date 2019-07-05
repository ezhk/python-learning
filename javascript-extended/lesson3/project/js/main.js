const API = `https://raw.githubusercontent.com/GeekBrainsTutorial/online-store-api/master/responses`;

const APITest = 'https://raw.githubusercontent.com/GeekBrainsTutorial/online-store-api/master/responses/addToBasket.json';
let getRequestXML = (url, cb) => {
  let xhr = new XMLHttpRequest();
  // window.ActiveXObject -> xhr = new ActiveXObject()
  xhr.open('GET', url, true);
  xhr.send();
  xhr.onreadystatechange = () => {
    if (xhr.readyState === 4) {
      if (xhr.status !== 200) {
        console.log('error XML')
      } else {
        cb(xhr.responseText)
      }
    }
  }
};

let getRequestFetch = (url, cb) => {
  fetch(url)
    .then(response => {
      if (response.status !== 200) {
        throw Error("error fetch")
      }
      return response.text()
    })
    .then(response => cb(response))
    .catch(() => console.log('error fetch catch'))
};

let getRequestPromise = (url, cb) => {
  return new Promise((resolve, reject) => {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.send();
    xhr.onreadystatechange = () => {
      if (xhr.readyState === 4) {
        if (xhr.status !== 200) {
          reject(xhr.status);
          // console.log('error XML')
        } else {
          // cb(xhr.responseText)
          resolve(xhr.responseText);
        }
      }
    }
  });
};

function out(value) {
  console.log('out: ' + value);
}

getRequestXML(APITest, out);
getRequestFetch(APITest, out);
getRequestPromise(APITest, out)
  .then((result) => out('promise: ' + result))
  .catch(() => console.log('error Promise'));

class Products {
  constructor(container = '.products') {
    this.container = container;
    this.data = [];
    this.allProducts = [];
    this._fetchGoods()
      .then(() => this._render())
  }

  _fetchGoods() {
    return fetch(`${API}/catalogData.json`)
      .then(result => result.json())
      .then(data => {
        this.data = [...data];
      })
      .catch(error => console.log(error));
  }

  calcSum() {
    // let result = 0;
    // for (let prod of this.allProducts) {
    //     result += prod.price;
    // }
    return this.allProducts.reduce((accum, el) => accum + el.price, 0)
  }

  _render() {
    const block = document.querySelector(this.container);
    for (let el of this.data) {
      const product = new ProductItem(el);
      this.allProducts.push(product);
      block.insertAdjacentHTML('beforeend', product.render());
    }
  }
}

class ProductItem {
  constructor(product, img = "https://placehold.it/200x150") {
    this.price = product.price;
    this.product_name = product.product_name;
    this.id_product = product.id_product;
    this.img = img
  }

  render() {
    return `<div class="product-item">
                 <img src="${this.img}" alt="${this.product_name}">
                 <div class="desc">
                     <h3>${this.product_name}</h3>
                     <p>${this.price}</p>
                     <button class="buy-btn">Купить</button>
                 </div>
             </div>`
  }
}

const products = new Products();
console.log(products.calcSum());


class Cart {
  constructor() {
    // products presented as {productId: {title: X, price: Y, quantity: Z}, ...}
    this.products = {};
  }

  /**
   * Add product from Cart
   * @param product: object {id: 1, title: 'Notebook', price: 2000}
   */
  add(product) {
    let {id, title, price} = product;
    if (!this.products.hasOwnProperty(id)) {
      this.products[id] = {title, price, quantity: 0};
    }
    this.products[id].quantity++;
  }

  /**
   * Remove product from Cart
   * @param product: object {id: 1, title: 'Notebook', price: 2000}
   */
  del(product) {
    if (this.products.hasOwnProperty(product.id)) {
      this.products[product.id].quantity--;

      if (this.products[product.id].quantity < 1) {
        delete this.products[product.id];
      }
    }
  }

  /**
   * Clear all items in Cart
   */
  clear() {
    this.products = {};
  }

  /**
   * Return object with all products in cart
   * @return {Object}: {ID: {title: X, price: Y, quantity: Z}, ...}
   */
  show() {
    return this.products;
  }

  /**
   * Get product by ID.
   * @param el: product ID
   * @return {Object} or null: {title: X, price: Y, quantity: Z}
   */
  product(el) {
    if (this.products.hasOwnProperty(el)) {
      return this.products[el];
    }
    return null;
  }

  /**
   * Calculate products count in Cart
   * @return number: counts
   */
  quantity() {
    let quantity = 0;
    for (let productId in this.products) {
      quantity += this.products[productId].quantity;
    }
    return quantity;
  }

  /**
   * Calculate summary cost of all products in Cart
   * @return number: summary price
   */
  price() {
    let price = 0;
    for (let productId in this.products) {
      price += this.products[productId].quantity * this.products[productId].price;
    }
    return price;
  }

  _render() {
    for (let product of this.products) {
      `<li class="product"><li>`
    }
  }
}

//
// const renderProduct = (title, price, img="https://placehold.it/200x150") => {
//     return `<div class="product-item">
//                  <img src="${img}" alt="${title}">
//                  <div class="desc">
//                      <h3>${title}</h3>
//                      <p>${price}</p>
//                      <button class="buy-btn">Купить</button>
//                  </div>
//              </div>`
// };
//
// const renderPage = list => {
//     const productList = list.map(item => renderProduct(item.title, item.price));
//     // document.querySelector(`.products`).innerHTML = list.map(item => renderProduct(item.title, item.price)).join('');
//     for(let el of productList){
//         document.querySelector(`.products`).insertAdjacentHTML('', el);
//     }
// };
//
// renderPage(products);

