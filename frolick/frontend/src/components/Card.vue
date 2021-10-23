<template>
  <div class="bg-white shadow sm:rounded-lg my-4">
    <div class="px-4 py-5 sm:p-6">
      <h3 v-if="title" class="text-lg leading-6 font-medium text-gray-900">
        {{ title }}
      </h3>
      <div v-if="content" class="max-w-xl text-sm text-gray-500" :class="[title ? 'mt-2' : '']">
        <p>
          {{ content }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Card',
  props: {
    title: String,
    content: String,
  },
  data () {
    return {}
  },
  components: {},
  mounted () {},
  methods: {}
}
</script>

<style scoped>
</style>
