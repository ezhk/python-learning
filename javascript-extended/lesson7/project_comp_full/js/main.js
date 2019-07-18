const API = `https://raw.githubusercontent.com/GeekBrainsTutorial/online-store-api/master/responses`;


const app = new Vue({
  el: '#app',
  methods: {
    getJson(url) {
      return fetch(url)
        .then(result => result.json())
        .catch(error => this.$refs.error.setText(error));
    }
  }
});

// let getRequest = (url) => {
//     return new Promise((resolve, reject) => {
//         let xhr = new XMLHttpRequest();
//         // window.ActiveXObject -> xhr = new ActiveXObject()
//         xhr.open('GET', url, true);
//         xhr.onreadystatechange = () => {
//             if(xhr.readyState === 4) {
//                 if (xhr.status !== 200){
//                     reject('error')
//                 } else {
//                     resolve(xhr.responseText)
//                 }
//             }
//         };
//         xhr.send()
//     })
// };
// getRequest(url).then(data => console.log(data));

// class List {
//     constructor(url, container) {
//         this.container = container;
//         this.url = url;
//         this.data = [];
//         this.allProducts = [];
//         this.filtered = [];
//         this._init();
//     }
//     _init(){
//         return false
//     }
//     getJson(url){
//         return fetch(url ? url : `${API + this.url}`)
//             .then(result => result.json())
//             .catch(error => console.log(error));
//     }
//     handleData(data){
//         this.data = [...data];
//         this._render();
//     }
//     calcSum(){
//         return this.allProducts.reduce((accum, el) => accum + el.price, 0)
//     }
//     _render(){
//         const block = document.querySelector(this.container);
//         for (let el of this.data) {
//             const product = new lists[this.constructor.name](el);
//             this.allProducts.push(product);
//             block.insertAdjacentHTML('beforeend', product.render());
//         }
//     }
//     getItem(id){
//         return this.allProducts.find(el => el.id_product === id);
//     }
//     filter(value){
//         const regexp = new RegExp(value, 'i');
//         this.filtered = this.allProducts.filter(el => regexp.test(el.product_name));
//         this.allProducts.forEach(el => {
//             const block = document.querySelector(`.product-item[data-id="${el.id_product}"]`);
//             if(!this.filtered.includes(el)){
//                 block.classList.add('invisible');
//             } else {
//                 block.classList.remove('invisible');
//             }
//         })
//     }
// }
//
// class Item {
//     constructor(product, img="https://placehold.it/200x150") {
//         this.price = product.price;
//         this.product_name = product.product_name;
//         this.id_product = product.id_product;
//         this.img = img
//     }
//     render(){
//         return `<div class="product-item" data-id="${this.id_product}">
//                  <img src="${this.img}" alt="${this.product_name}">
//                  <div class="desc">
//                      <h3>${this.product_name}</h3>
//                      <p>${this.price}</p>
//                      <button class="buy-btn" data-id="${this.id_product}">Купить</button>
//                  </div>
//              </div>`
//     }
// }
//
// class Products extends List{
//     constructor(cart, url='/catalogData.json', container='.products') {
//         super(url, container);
//         this.cart = cart;
//         this.getJson()
//             .then(data => this.handleData(data))
//     }
//     _init(){
//         document.querySelector(this.container).addEventListener('click', e => {
//             if(e.target.classList.contains('buy-btn')){
//                 const id = +e.target.dataset['id'];
//                 cart.addProduct(this.getItem(id))
//             }
//         });
//         document.querySelector(`.search-form`).addEventListener('submit', e => {
//             e.preventDefault();
//             this.filter(document.querySelector(`.search-field`).value);
//         })
//     }
// }
//
// class ProductItem extends Item{}
// class Cart extends List {
//     constructor(url='/getBasket.json', container='.cart-block'){
//         super(url, container);
//         this.getJson()
//             .then(data => this.handleData(data.contents))
//     }
//     addProduct(product){
//         this.getJson(`${API}/addToBasket.json`)
//             .then(data => {
//                 if(data.result){
//                     let find = this.getItem(product.id_product);
//                     if(find){
//                         find.quantity++;
//                         this._updateCart(find);
//                     } else {
//                         let prod = Object.assign({quantity: 1}, product);
//                         this.data = [prod];
//                         this._render()
//                     }
//                 } else {
//                     console.log('Error!');
//                 }
//             })
//     }
//     removeProduct(element){
//         this.getJson(`${API}/deleteFromBasket.json`)
//             .then(data => {
//                 if(data.result){
//                     const id = +element.dataset['id'];
//                     let find = this.getItem(id);
//                     if(find.quantity > 1){
//                         find.quantity--;
//                         this._updateCart(find);
//                     } else {
//                         this.allProducts.splice(this.allProducts.indexOf(find), 1);
//                         document.querySelector(`.cart-item[data-id="${id}"]`).remove();
//                     }
//                 } else {
//                     console.log('Error!');
//                 }
//             })
//     }
//     _updateCart(product){
//         let block = document.querySelector(`.cart-item[data-id="${product.id_product}"]`);
//         block.querySelector(`.product-quantity`).textContent = `Quantity: ${product.quantity}`;
//         block.querySelector(`.product-price`).textContent = `$${product.quantity*product.price}`;
//     }
//     _init(){
//         document.querySelector(this.container).addEventListener('click', e => {
//             if(e.target.classList.contains('del-btn')){
//                 this.removeProduct(e.target)
//             }
//         });
//         document.querySelector(`.btn-cart`).addEventListener('click', () => {
//             document.querySelector(this.container).classList.toggle('invisible');
//         })
//     }
//
// }
// class CartItem extends Item {
//     constructor(el, img="https://placehold.it/50x100"){
//         super(el, img);
//         this.quantity = el.quantity;
//     }
//     render() {
//         return `<div class="cart-item" data-id="${this.id_product}">
//             <div class="product-bio">
//             <img src="${this.img}" alt="Some image">
//             <div class="product-desc">
//             <p class="product-title">${this.product_name}</p>
//             <p class="product-quantity">Quantity: ${this.quantity}</p>
//         <p class="product-single-price">$${this.price} each</p>
//         </div>
//         </div>
//         <div class="right-block">
//             <p class="product-price">$${this.quantity*this.price}</p>
//         <button class="del-btn" data-id="${this.id_product}">&times;</button>
//         </div>
//         </div>`
//     }
// }
//
// const lists = {
//     Cart: CartItem,
//     Products: ProductItem
// };
//
// const cart = new Cart();
// const products = new Products(cart);
//
// products.getJson(`getProducts.json`).then(data => products.handleData(data));

//
// class Cart {
//     constructor(){
//         // this.some здесь будет что-то
//     }
//     // some(){} - делает что-то
// }

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

