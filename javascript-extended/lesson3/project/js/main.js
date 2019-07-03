const API = `https://raw.githubusercontent.com/GeekBrainsTutorial/online-store-api/master/responses`;
// let getRequest = (url, cb) => {
//     let xhr = new XMLHttpRequest();
//     // window.ActiveXObject -> xhr = new ActiveXObject()
//     xhr.open('GET', url, true);
//     xhr.onreadystatechange = () => {
//         if(xhr.readyState === 4) {
//             if (xhr.status !== 200){
//                 console.log('error')
//             } else {
//                 cb(xhr.responseText)
//             }
//         }
//     }
// }


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
    // this.some здесь будет что-то
  }

  // some(){} - делает что-то
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

