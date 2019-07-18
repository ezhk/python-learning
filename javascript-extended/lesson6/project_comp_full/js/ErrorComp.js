Vue.component('error', {
  data() {
    return {
      error: '',
    }
  },
  template: `<div class="error" v-show="showError">
                 ERROR {{error}}
             </div>`,
  computed: {
    showError() {
      return this.error.length > 0;
    }
  },
});