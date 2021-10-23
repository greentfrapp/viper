<template>
  <div>
    {{ $data[varName] }}
    <button class="rounded bg-green-300" @click="add">Add</button>
  </div>
</template>

<script>
export default {
  name: 'Counter',
  props: {
    varName: String,
  },
  data () {
    return {}
  },
  components: {},
  mounted () {
    this.$data[this.varName] = 0
  },
  methods: {
    add () {
      this.$data[this.varName]++
    }
  }
}
</script>

<style scoped>
</style>
