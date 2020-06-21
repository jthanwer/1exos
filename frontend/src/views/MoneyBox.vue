<template>
  <div class="container is-fluid">
    <div class="columns is-centered">
      <div class="column is-6">
        <div class="card has-background-white-ter">
          <div class="card-content has-text-centered">
            <p class="title is-3">Ma tirelire</p>
            <p class="title has-text-info" style="font-size: 5em;">
              {{ user.tirelire }} pts
            </p>
          </div>
        </div>
      </div>
    </div>

    <p class="title is-4 mt-10 has-text-centered">
      Recharger ma tirelire :
    </p>

    <div class="columns is-centered is-multiline">
      <div class="column is-3">
        <b-button
          tag="router-link"
          type="is-primary"
          class="mt-3"
          expanded
          size="is-large"
          :to="{ name: 'recharge' }"
        >
          En argent réel
        </b-button>
      </div>
      <div class="column is-3">
        <b-button
          tag="router-link"
          type="is-secondary"
          class="mt-3"
          expanded
          size="is-large"
          :to="{ name: 'search' }"
        >
          En corrigeant des exos
        </b-button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "MoneyBox",
  data() {
    return {};
  },
  computed: {
    ...mapState("authentication", ["user"])
  },
  methods: {},
  watch: {},
  created() {}
};
</script>

<style scoped></style>
