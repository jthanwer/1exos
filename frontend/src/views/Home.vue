<template>
<div>
  <div class="container">
    <div class="columns is-centered">
      <div class="column is-10">
        <section class="is-bold">
          <h1 class="title is-1 has-text-centered">
            Bienvenue sur 1Exo !
          </h1>

          <h2 class="subtitle is-size-4 mt-8 mb-8 has-text-centered">
            <p>Ce site te permet d’avoir accès à la correction de tes exos de maths.</p>
            <p>Chaque correction coûte un certain nombre de points.</p>
            <p>Tu peux gagner des points en mettant de l’argent sur ton compte ou en corrigeant des exos.</p>
          </h2>

          <div class="columns">
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

          <div class="columns is-centered is-multiline">
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

          <b-collapse class="card mt-8"
                      animation="slide"
                      aria-id="contentId">
            <div slot="trigger"
                 slot-scope="props"
                 class="card-header has-background-primary"
                 role="button"
                 aria-controls="contentId">
              <p class="card-header-title has-text-white">
                Comment ça marche ?
              </p>
              <a class="card-header-icon">
                <b-icon type="is-white"
                        :icon="props.open ? 'menu-down' : 'menu-up'">
                </b-icon>
              </a>
            </div>
            <div class="card-content">
              <div class="content">
                <ol class="is-size-6"
                    style="line-height: 1.5em;">
                  <li>Inscris-toi sur le site (tu as 4 points de bienvenue).</li>
                  <li>Connecte-toi.</li>
                  <li>Cherche ton exo sur le site :
                    <ul>
                      <li>Si tu le trouves, tu peux accéder à sa correction.</li>
                      <li>Si tu ne le trouves pas, demande sa correction.</li>
                      <p class="mb-3">Dans les 2 cas, cela te coûte un certain nombre de points</p>
                    </ul>
                  </li>
                  <li>Si tu n’as pas assez de points, recharge ta tirelire :
                    <ul>
                      <li>Avec de l’argent réel (1 € = 4 points).</li>
                      <li>En corrigeant des exos.</li>
                    </ul>
                  </li>
                </ol>
                <p class="mt-5 is-size-4 has-text-centered">Amuse-toi bien !</p>
              </div>
            </div>
          </b-collapse>

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
    ...mapGetters("authentication", ["isAuthenticated"])
  }
};
</script>

<style>
</style>
