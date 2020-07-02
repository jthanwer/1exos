<template>
<div>
  <div class="container">
    <div class="columns is-centered">
      <div class="column is-10">
        <section class="is-bold">
          <h1 class="title is-1 has-text-centered">
            Bienvenue sur 1Exo !
          </h1>
          <h2 class="mt-8 mb-15 subtitle">
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
            enim ad minim veniam, quis nostrud exercitation ullamco laboris
            nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
            reprehenderit in voluptate velit esse cillum dolore eu fugiat
            nulla pariatur. Excepteur sint occaecat cupidatat non proident,
            sunt in culpa qui officia deserunt mollit anim id est laborum.
          </h2>

          <div class="columns my-3">
            <div class="column is-6">
              <b-button v-if="!isAuthenticated"
                        tag="router-link"
                        type="is-warning"
                        expanded
                        class=" big-button"
                        size="is-large"
                        icon-left="account"
                        :to="{ name: 'login' }">Se connecter</b-button>
            </div>
            <div class="column is-6">
              <b-button v-if="!isAuthenticated"
                        tag="router-link"
                        type="is-warning"
                        expanded
                        class="big-button"
                        size="is-large"
                        icon-left="account-plus"
                        :to="{ name: 'register' }">Créer un compte</b-button>
            </div>
          </div>

          <div class="columns is-centered is-multiline my-3">
            <div class="column is-6">
              <b-button tag="router-link"
                        type="is-success"
                        class="big-button"
                        expanded
                        size="is-large"
                        icon-left="magnify"
                        :to="{ name: 'search' }">
                Rechercher un exo
              </b-button>
            </div>
          </div>
          <div class="columns is-centered is-multiline my-3">
            <div class="column is-6">
              <b-button tag="router-link"
                        type="is-primary"
                        expanded
                        class="big-button"
                        size="is-large"
                        icon-left="hand"
                        :to="{ name: 'post-exo' }">
                <span>Demander la </span>
                <span>correction d'un exo</span> </b-button>
            </div>
            <div class="column is-6">
              <b-button tag="router-link"
                        type="is-primary"
                        expanded
                        class="big-button"
                        size="is-large"
                        icon-left="upload"
                        :to="{ name: 'post-exo-with-correc' }">
                Poster un exo et sa correction
              </b-button>
            </div>
            <div class="column is-6">
              <b-button tag="router-link"
                        type="is-primary"
                        expanded
                        class="big-button"
                        size="is-large"
                        icon-left="pencil"
                        :to="{ name: 'search' , params: {id:2, is_corrected: false}}">
                Corriger un exo
              </b-button>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "home",
  data() {
    return {};
  },
  computed: {
    ...mapGetters("authentication", ["isAuthenticated", ""])
  }
};
</script>

<style>
</style>
