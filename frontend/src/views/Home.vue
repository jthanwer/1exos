<template>
  <div>
    <div class="container">
      <div class="columns is-centered is-vcentered">
        <div class="column is-10">
          <section class="is-bold">
            <h1 class="title is-2 has-text-centered has-text-danger">
              Ce site n'est pas encore utilisable !
            </h1>

            <h1 class="title is-4 has-text-centered has-text-danger">
              La date de mise en fonctionnement est prévue pour le lundi
              14/09/2020. <br />
              Aucun exercice posté jusque là ne sera corrigé et les exercices
              postés seront supprimés.
            </h1>

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

            <h2 class="is-size-4 mt-8 has-text-centered">
              <p>
                Ce site te permet d’avoir accès à la correction de tes exos de
                maths.
              </p>
              <p>Chaque correction coûte un certain nombre de points.</p>
              <p>
                Tu peux gagner des points soit en mettant de l’argent sur ton
                compte soit en corrigeant des exos.
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
