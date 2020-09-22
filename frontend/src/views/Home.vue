<template>
  <div>
    <div class="container">
      <div class="columns is-centered is-vcentered">
        <div class="column is-10">
          <section>
            <h1 class="title is-1 has-text-centered">
              Bienvenue sur 1Exo !
            </h1>

            <div class="columns mt-10 is-centered is-multiline">
              <div class="column is-6">
                <b-button
                  tag="router-link"
                  class="has-radius-border big-button"
                  type="is-primary"
                  expanded
                  size="is-large"
                  icon-left="magnify"
                  :to="{
                    name: 'search',
                    params: { id: 1, isCorrected: null }
                  }"
                >
                  Rechercher un exo
                </b-button>
              </div>
            </div>
            <div class="columns is-centered is-multiline">
              <div class="column is-half">
                <b-button
                  tag="router-link"
                  class="has-radius-border big-button"
                  icon-left="hand"
                  type="is-tertiary"
                  expanded
                  size="is-large"
                  :to="{ name: 'post-exo' }"
                >
                  Demander une correction
                </b-button>
              </div>
              <div v-if="isAuthenticated" class="column is-half">
                <b-button
                  tag="router-link"
                  class="has-radius-border big-button"
                  icon-left="plus-circle-multiple-outline"
                  type="is-secondary"
                  expanded
                  size="is-large"
                  :to="{ name: 'tirelire' }"
                >
                  Recharger ma tirelire
                </b-button>
              </div>
            </div>

            <h2 class="is-size-4 mt-8 has-text-centered">
              <p>
                Ce site te permet d’avoir accès à la correction de tes exos de
                maths.
              </p>
              <p>Chaque correction coûte un certain nombre de points.</p>
              <p>
                Tu peux gagner des points soit en mettant de l’argent sur ton
                compte soit en corrigeant des exercices.
              </p>
            </h2>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'Home',
  data() {
    return {}
  },
  computed: {
    ...mapGetters('authentication', ['isAuthenticated'])
  }
}
</script>

<style></style>
