class Products {
  constructor(container = '.products') {
    this.container = container;
    this.data = [];
    this.allProducts = [];
    this.init()
  }

  init() {
    this._fetchGoods();
    this._render();
  }

  _fetchGoods() {
    this.data = [
      {id: 1, title: 'Notebook', price: 2000},
      {id: 2, title: 'Keyboard', price: 70},
      {id: 3, title: 'Mouse', price: 46},
      {id: 4, title: 'Gamepad', price: 68},
      {id: 5, title: 'Chair', price: 168},
    ];
  }

  _render() {
    const block = document.querySelector(this.container);
    for (let el of this.data) {
      const product = new ProductItem(el);
      this.allProducts.push(product);
      block.insertAdjacentHTML('beforeend', product.render());
    }
  }

  /**
   * Method, that calculate summary price of fetched Goods
   * @return number: summary price
   */
  price() {
    let price = 0;
    for (let product of this.data) {
      price += product.price;
    }

    return price;
  }
}

class ProductItem {
  constructor(product, img = "https://placehold.it/200x150") {
    this.price = product.price;
    this.title = product.title;
    this.id = product.id;
    this.img = img
  }

  render() {
    return `<div class="product-item">
                 <img src="${this.img}" alt="${this.title}">
                 <div class="desc">
                     <h3>${this.title}</h3>
                     <p>${this.price}</p>
                     <button class="buy-btn">Купить</button>
                 </div>
             </div>`
  }
}

const products = new Products();


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
}

/**
 * Class describes base presentation on food-product.
 * Prepare description of all products at init stage.
 */
class Foods {
  constructor() {
    this.description = {};
    this.init();
  }

  init() {
    this._fetchDescription();
  }

  /**
   * Update description attr.
   */
  _fetchDescription() {
    this.description = {
      'burger': {
        'size': {
          'small': {
            'price': 50,
            'calories': 20,
          },
          'big': {
            'price': 100,
            'calories': 40,
          },
        },
        'type': {
          'cheese': {
            'price': 10,
            'calories': 20,
          },
          'salad': {
            'price': 20,
            'calories': 5,
          },
          'potato': {
            'price': 15,
            'calories': 10,
          },
        },
        'additional': {
          'seasoning': {
            'price': 15,
            'calories': 0,
          },
          'mayonnaise': {
            'price': 20,
            'calories': 5,
          },
        },
      },
    };
  }

  /**
   * Return fetched presentation of products.
   * @return {Object}
   */
  description() {
    return this.description;
  }
}

/**
 * Class for work with one food object.
 * Include methods: price, calories and calculate.
 */
class OneFood extends Foods {
  // new OneFood('burger', 'big', 'potato', ['seasoning'])
  constructor(name, size, type, additional = []) {
    super();

    this.name = name;
    this.size = size;
    this.type = type;
    this.additional = additional;

    // this.description = super.description();
  }

  /**
   * Calculate price with selected options.
   * @return number: price
   */
  price() {
    let price = 0;
    price += this.description[this.name]['size'][this.size].price;
    price += this.description[this.name]['type'][this.type].price;
    for (let item of this.additional) {
      price += this.description[this.name]['additional'][item].price;
    }

    return price;
  }

  /**
   * Calculate summary calories.
   * @return number: calories
   */
  calories() {
    let calories = 0;
    calories += this.description[this.name]['size'][this.size].calories;
    calories += this.description[this.name]['type'][this.type].calories;
    for (let item of this.additional) {
      calories += this.description[this.name]['additional'][item].calories;
    }

    return calories;
  }

  /**
   * Return price and calories — see previous methods.
   * @return {Object}: {price: number, calories: number}
   */
  calculate() {
    return {
      'price': this.price(),
      'calories': this.calories(),
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
