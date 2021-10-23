window.onload = () => {
  const App = {
    data() {
      return {
        title: 'My Frolick App',
        content: '',
      }
    },
    delimiters: ['[[', ']]'],
    computed: {
      compiledMarkdown () {
        return marked(this.input, { sanitize: true })
      }
    },
    mounted () {
      axios.get('/title', {})
      .then(response => {
        this.title = response.data.title
      })
      axios.get('/content', {})
      .then(response => {
        this.content = response.data.content
      })
    },
    methods: {
      update: _.debounce(function(e) {
        this.input = e.target.value;
      }, 300),
      ping () {
        axios.get('/ping', {})
        .then(response => {
          console.log(response.data)
        })
      },
      getContent () {
        axios.get('/content', {})
        .then(response => {
          this.input = response.data.content
        })
      }
    }
  }
  Vue.createApp(App).mount('#app')
}