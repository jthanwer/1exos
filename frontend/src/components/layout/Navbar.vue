<template>
<b-navbar id="main-navbar"
          shadow>
  <template slot="brand">
    <b-navbar-item class="is-size-4"
                   tag="router-link"
                   :to="{ name: 'home' }">
    </b-navbar-item>
  </template>
  <template slot="end">
    <b-navbar-item v-for="item in menuItems"
                   :key="item.title"
                   tag="router-link"
                   :to="{ name: item.path }">
      <span class="is-uppercase is-size-5">{{item.title}}</span>
    </b-navbar-item>
    <b-navbar-dropdown v-if="isAuthenticated"
                       right
                       hoverable
                       class="is-size-5">
      <template slot="label">
        <span class="is-uppercase">Profil</span>
      </template>
      <b-navbar-item tag="router-link"
                     :to="{ name: 'profile' }">
        Mon profil
      </b-navbar-item>
      <b-navbar-item tag="router-link"
                     :to="{ name: 'recharge' }">
        Recharger mon compte
      </b-navbar-item>
      <b-navbar-item @click="logout"> Se déconnecter </b-navbar-item>
    </b-navbar-dropdown>
    <b-navbar-item v-if="!isAuthenticated"
                   tag="div">
      <b-button icon-left="account"
                type="is-primary"
                @click="loginModal = true">
        Se connecter
      </b-button>
      <b-modal :active.sync="loginModal"
               :width="500"
               has-modal-card
               trap-focus
               aria-role="dialog"
               aria-modal
               :can-cancel="['escape', 'x']">
        <auth-modal />
      </b-modal>
      </div>
    </b-navbar-item>

  </template>
</b-navbar>
</template>

<script>
import AuthModal from '@/components/layout/AuthModal.vue'
import { mapGetters } from 'vuex'
export default {
  name: "NavbarComponent",
  components: {
    'auth-modal': AuthModal
  },
  data() {
    return {
      appTitle: 'Exos',
      loginModal: false,
      menuItems: [
        {
          title: 'Accueil',
          path: 'home',
        },
      ],
      items_profil: [{
          title: 'Mon profil'
        },
        {
          title: 'Se déconnecter'
        }
      ],
    }
  },
  computed: {
    ...mapGetters('authentication', ['isAuthenticated']),
  },
  methods: {
    logout() {
      this.$store.dispatch('authentication/authLogout')
    }
  }
}
</script>

<style>
a {
  text-decoration: none !important;
}

.icon-nav {
  margin-right: 3em;
}
</style>
