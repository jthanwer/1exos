<template>
  <div>
    <NavbarComponent />
    <div class="app-container">
      <transition name="fade" mode="out-in">
        <keep-alive include="Search">
          <router-view
            :key="
              $route.path +
                ($route.params.id ? $route.params.id : '').toString()
            "
          />
        </keep-alive>
      </transition>
    </div>
    <footer class="footer has-background-primary" style="margin-top:50px;">
      <div class="columns is-centered">
        <div class="column is-3">
          <h1 class="title is-3 has-text-white-ter">À propos de nous</h1>
          <router-link class="has-text-white" :to="{ name: 'home' }">
            <h2>Qui sommes-nous ?</h2>
          </router-link>
          <router-link class="has-text-white" :to="{ name: 'home' }">
            <h2>FAQ</h2>
          </router-link>
          <router-link class="has-text-white" :to="{ name: 'home' }">
            <h2>Nous contacter</h2>
          </router-link>
        </div>
        <div class="column is-3">
          <h1 class="title is-3 has-text-white-ter">Nous contacter</h1>
          <router-link class="has-text-white" :to="{ name: 'home' }">
            <h2>profinou@gmail.com</h2>
          </router-link>
        </div>
        <div class="column is-3">
          <h1 class="title is-3 has-text-white-ter">Mentions légales</h1>
          <router-link
            class="has-text-white"
            :to="{ name: 'conditions-generales' }"
          >
            <h2>Conditions générales</h2>
          </router-link>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
require('@/assets/css/animate.css')
import { mapGetters } from 'vuex'
import NavbarComponent from '@/components/layout/Navbar.vue'

export default {
  name: 'App',
  components: {
    NavbarComponent
  },
  computed: {
    ...mapGetters('authentication', ['isAuthenticated'])
  },
  created() {
    this.$store.dispatch('general/updateConstants').then(() => {
      if (this.isAuthenticated) {
        this.$store.dispatch('authentication/getProfileUser')
        this.$store.dispatch('exercices/loadPostedExercices')
        this.$store.dispatch('exercices/loadLikedExercices')
        this.$store.dispatch('corrections/loadPostedCorrections')
        this.$store.dispatch('corrections/loadUnlockedCorrections')
      }
    })
  }
}
</script>

<style lang="scss">
@import '@/assets/scss/core.scss';
</style>

<style lang="css">
.app-container {
  position: relative;
  width: 100%;
  min-height: 1000px;
  margin-top: 0px;
  padding-top: 50px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
