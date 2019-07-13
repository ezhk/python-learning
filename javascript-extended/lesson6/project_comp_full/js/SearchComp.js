Vue.component('search', {
  data() {
    return {
      userSearch: '',
      filtered: [],
    }
  },
  template: `<form action="#" method="post" class="search-form" @submit.prevent="filter">
                 <input type="text" class="search-field" v-model="userSearch">
                 <button class="btn-search" type="submit">
                     <i class="fas fa-search"></i>
                 </button>
             </form>`,

  methods: {
    filter() {
      let regexp = new RegExp(this.userSearch, 'i');
      this.filtered = this.$root.$refs.products.products.filter(el => regexp.test(el.product_name));
    }
  },

  mounted() {
    this.filtered = this.$root.$refs.products.products;
  },
});