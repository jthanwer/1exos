<template>
<div class="container is-fluid">
  <b-button tag="router-link"
            :to="{name: 'recharge'}">Recharger ma tirelire</b-button>
</div>
</template>

<script>
export default {
  name: "MoneyBox",
  data() {
    return {}
  },
  methods: {

  },
  watch: {},
  created() {}
}
</script>

<style scoped>
</style>
