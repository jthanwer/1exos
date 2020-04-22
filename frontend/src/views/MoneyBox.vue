<template>
<div class="container is-fluid">
  <div class="columns is-centered">
    <div class="column is-6">
      <div class="card">
        <div class="card-content">
          <div class="media">
            <div class="media-left">
            </div>
            <div class="media-content">
              <p class="title is-2">Ma tirelire</p>
            </div>
          </div>
          <div class="level">
            <div class="level-left">
            </div>
            <div class="level-right">
              <p class="title is-1 has-text-info">{{user.moneybox}} €</p>
            </div>
          </div>
        </div>
      </div>

      <b-button tag="router-link"
                type="is-info"
                expanded
                size="is-large"
                :to="{name: 'recharge'}">Recharger ma tirelire</b-button>
    </div>
  </div>

</div>
</template>

<script>
import { mapState } from 'vuex';
export default {
  name: "MoneyBox",
  data() {
    return {}
  },
  computed: {
    ...mapState('authentication', ['user'])
  },
  methods: {

  },
  watch: {},
  created() {}
}
</script>

<style scoped>
</style>
