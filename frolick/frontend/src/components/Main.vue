<template>
  <div class="max-w-prose mx-auto my-2 lg:my-8">
    <h1 class="font-bold text-5xl mx-auto mb-4 lg:mb-8">{{ title }}</h1>
    <Card v-for="c, i in content" :key="`content${i}`"
     :title="c.title" :content="c.content" />
    <Card v-for="v, i in show" :key="`var${i}`"
     :title="`${v}: ${$data.vars[v]}`" />
    <Btn v-for="b, i in buttons" :key="`btn${i}`"
     :label="b.label" :callback="b.callback" @update="update" />
  </div>
</template>

<script>
import axios from "axios"
import Btn from "./Btn.vue"
import Card from "./Card.vue"
export default {
  name: 'Main',
  data () {
    return {
        title: '',
        content: [],
        show: [],
        buttons: [],
        vars: {},
    }
  },
  components: {
    Btn,
    Card,
  },
  mounted () {
    axios.get('/vars', {})
    .then(response => {
      this.vars = response.data
    })
    axios.get('/title', {})
    .then(response => {
      this.title = response.data.title
    })
    axios.get('/content', {})
    .then(response => {
      this.content = response.data.content
    })
    axios.get('/show', {})
    .then(response => {
      this.show = response.data
    })
    axios.get('/buttons', {})
    .then(response => {
      this.buttons = response.data
    })
  },
  methods: {
    update (vars) {
      Object.entries(vars).forEach(v => {
        this.vars[v[0]] = v[1]
      })
    }
  }
}
</script>

<style scoped>
</style>
