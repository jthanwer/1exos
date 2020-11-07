<template>
  <div>
    <NavbarComponent />
    <div class="app-container">
      <transition name="fade" mode="out-in">
        <keep-alive include="PostExo,Search">
          <router-view
            :key="
              $route.path +
                ($route.params.id ? $route.params.id : '').toString()
            "
          />
        </keep-alive>
      </transition>
    </div>
    <FooterComponent />
  </div>
</template>

<script>
require('@/assets/css/animate.css')
import { mapState, mapGetters } from 'vuex'
import NavbarComponent from '@/components/layout/Navbar.vue'
import FooterComponent from '@/components/layout/Footer.vue'

export default {
  name: 'App',
  components: {
    NavbarComponent,
    FooterComponent
  },
  computed: {
    ...mapState('authentication', ['notifications']),
    ...mapGetters('authentication', ['isAuthenticated'])
  },
  beforeCreate() {
    this.$store.dispatch('general/updateConstants').then(() => {
      if (this.isAuthenticated) {
        this.$store.dispatch('authentication/getProfileUser')
        this.$store.dispatch('authentication/getNotifications')
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
  z-index: 1;
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
