Vue.component('comp-one', {
  template: `<div>1. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusamus alias atque, blanditiis deserunt est ex laborum nam odio optio pariatur praesentium, quaerat, repellendus tempora vitae voluptate. Autem laudantium libero nesciunt.</div>`
});
Vue.component('comp-two', {
  template: `<div>2. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusamus alias atque, blanditiis deserunt est ex laborum nam odio optio pariatur praesentium, quaerat, repellendus tempora vitae voluptate. Autem laudantium libero nesciunt.</div>`
});
Vue.component('comp-three', {
  template: `<div>3. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusamus alias atque, blanditiis deserunt est ex laborum nam odio optio pariatur praesentium, quaerat, repellendus tempora vitae voluptate. Autem laudantium libero nesciunt.</div>`
});
// Глобальная регистрация
// Vue.component('el', {
//     props: ['title', 'counter'],
//     data(){
//         return {
//             prop: 123
//         }
//     },
//     methods: {
//       some(){
//           console.log('component')
//       }
//     },
//    template: `<div class="some">
//                 <h2>{{ counter }}</h2>
//                 <error></error>
//                 <button @click="$emit('increase', 123)">Button</button>
//             </div>`
// });
//
// Vue.component('error', {
//     template: `<p>Error</p>`
// });

// Локальная регистрация
// const error = {
//     template: `<p>Error</p>`
// };
// const el = {
//     props: ['title', 'counter'],
//     data(){
//         return {
//             prop: 123
//         }
//     },
//     components: {
//       error: error
//     },
//     methods: {
//         some(){
//             console.log('component')
//         }
//     },
//     template: `<div class="some">
//                 <h2>{{ counter }}</h2>
//                 <error></error>
//                 <button @click="$emit('increase', 123)">Button</button>
//             </div>`
// };

