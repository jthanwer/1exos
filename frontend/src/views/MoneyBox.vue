<template>
  <div class="container is-fluid">
    <div class="columns is-centered">
      <div class="column is-6">
        <div class="card has-background-white-ter">
          <div class="card-content has-text-centered">
            <p class="title is-3">Ma tirelire</p>
            <p
              v-if="user"
              class="title has-text-primary"
              style="font-size: 5em;"
            >
              {{ user.tirelire }} {{ user.tirelire > 1 ? 'pts' : 'pt' }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <p class="title is-4 mt-10 has-text-centered">
      Recharger ma tirelire :
    </p>

    <div class="columns is-centered is-multiline">
      <div class="column is-4">
        <b-button
          tag="router-link"
          type="is-primary"
          icon-left="credit-card"
          class="mt-3 has-radius-border big-button"
          expanded
          size="is-large"
          :to="{ name: 'recharge' }"
        >
          En argent réel
        </b-button>
      </div>
      <div class="column is-4">
        <b-button
          tag="router-link"
          type="is-secondary"
          icon-left="pencil"
          class="mt-3 has-radius-border big-button"
          expanded
          size="is-large"
          :to="{ name: 'search', params: { id: 2, isCorrected: false } }"
        >
          En corrigeant un exo
        </b-button>
      </div>
    </div>
    <div class="columns is-centered is-multiline">
      <div class="column is-4">
        <b-button
          tag="router-link"
          type="is-tertiary"
          icon-left="pencil"
          class="mt-3 has-radius-border big-button"
          expanded
          size="is-large"
          :to="{ name: 'post-exo' }"
        >
          En postant un exo et sa correction
        </b-button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'MoneyBox',
  data() {
    return {}
  },
  computed: {
    ...mapState('authentication', ['user'])
  },
  watch: {},
  created() {},
  methods: {}
}
</script>

<style scoped></style>
