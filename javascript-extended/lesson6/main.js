const app = new Vue({
  el: '#app',
  data: {
    currentTab: 'one',
    tabs: ['one', 'two', 'three']
  },
  computed: {
    compCurrentTab() {
      return `comp-${this.currentTab}`;
    }
  }
});

// const app = new Vue({
//     data: {
//         text: 'Some string',
//         counter: 0,
//     },
//     components: {
//        el: el
//     },
//     methods: {
//         increase(some){
//           console.log(some);
//           console.log(this);
//         },
//         some(){
//             console.log('global');
//         }
//     },
//     el: '#app'
// })