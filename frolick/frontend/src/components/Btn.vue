<template>
  <button class="bg-gray-700 text-white px-4 py-2 shadow rounded mx-2 first:ml-0 last:mr-0" @click="click">
      {{ label }}
  </button>
</template>

<script>
import axios from "axios"
export default {
  name: 'Btn',
  props: {
    label: String,
    callback: String,
  },
  emits: {
    'update': null,
  },
  data () {},
  components: {},
  mounted () {},
  methods: {
    click () {
      axios.get(`/${this.callback}`, {})
      .then(response => {
        this.$emit('update', response.data)
      })    
    }
  }
}
</script>

<style scoped>
</style>
