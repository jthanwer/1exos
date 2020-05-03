<template>
<div>
  <div class="container">
    <div class="columns is-centered">
      <div class="column is-8">
        <section class="is-bold">
          <h1 class="title is-1 has-text-centered">
            Bienvenue sur 1Exo !
          </h1>
          <h2 class="mt-8 mb-15 subtitle">
            1Exo est une base de données communautaire d'énoncés et
            de corrections d'exercices de mathématiques accessibles par tous les élèves
            du secondaire de France.
          </h2>

          <div class="columns">
            <div class="column is-6">
              <b-button v-if="!isAuthenticated"
                        tag="router-link"
                        type="is-success"
                        expanded
                        class="m-3"
                        size="is-large"
                        icon-left="account"
                        :to="{name: 'login'}">Se connecter</b-button>
            </div>
            <div class="column is-6">
              <b-button v-if="!isAuthenticated"
                        tag="router-link"
                        type="is-warning"
                        expanded
                        class="m-3"
                        size="is-large"
                        icon-left="account-plus"
                        :to="{name: 'register'}">Créer un compte</b-button>
            </div>
          </div>

          <div class="columns is-centered">
            <div class="column is-6">
              <b-button tag="router-link"
                        type="is-primary"
                        class="m-3"
                        expanded
                        size="is-large"
                        icon-left="magnify"
                        :to="{name: 'search'}">Rechercher un exo</b-button>
            </div>
            <div class="column is-6">
              <b-button tag="router-link"
                        type="is-secondary"
                        expanded
                        class="m-3"
                        size="is-large"
                        icon-left="upload"
                        :to="{name: 'submit'}">Poster un exo</b-button>
            </div>
          </div>

        </section>
      </div>
    </div>
  </div>

</div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'home',
  data() {
    return {}
  },
  computed: {
    ...mapGetters('authentication', ['isAuthenticated', '']),
  },
}
</script>

<style>
.upload,
.upload-draggable {
  width: 100%;
}
</style>
