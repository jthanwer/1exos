<template>
<b-navbar type="is-primary"
          shadow>
  <template slot="brand">
    <b-navbar-item tag="router-link"
                   :to="{ name: 'home' }">
      <img src="~@/assets/images/logo_void.png"
           alt="1exo">
    </b-navbar-item>
  </template>
  <template slot="start"
            v-if="user">
    <b-navbar-item tag="div"
                   class="ml-10 has-text-weight-bold">
      Bonjour {{user.username}}
    </b-navbar-item>
  </template>
  <template slot="end">
    <b-navbar-item v-for="item in menuItems"
                   :key="item.title"
                   tag="router-link"
                   :to="{ name: item.path }">
      <b-icon class="mr-1"
              :icon="item.icon"></b-icon>
      <span class="is-uppercase is-size-6">{{item.title}}</span>
    </b-navbar-item>
    <b-navbar-dropdown v-if="isAuthenticated"
                       right
                       hoverable
                       class="is-size-6">
      <template slot="label">
        <b-icon class="mr-1"
                icon="account"></b-icon>
        <span class="is-uppercase">Menu</span>
      </template>
      <b-navbar-item tag="router-link"
                     :to="{ name: 'profile' }">
        Mon profil
      </b-navbar-item>
      <b-navbar-item tag="router-link"
                     :to="{ name: 'tirelire' }">
        Ma tirelire
      </b-navbar-item>
      <b-navbar-item tag="router-link"
                     :to="{ name: 'mes-exercices' }">
        Mes exercices
      </b-navbar-item>
      <b-navbar-item tag="router-link"
                     :to="{ name: 'mes-corrections' }">
        Mes corrections
      </b-navbar-item>
      <hr class="navbar-divider">
      <b-navbar-item @click="logout"> Se déconnecter </b-navbar-item>
    </b-navbar-dropdown>
    <b-navbar-item v-if="!isAuthenticated"
                   tag="div">
      <b-button icon-left="account"
                type="is-primary"
                @click="$router.push({ name: 'login' })"
                inverted>
        Se connecter
      </b-button>
    </b-navbar-item>
    <b-navbar-item v-if="isAuthenticated && user"
                   tag="div">
      <b-button type="is-primary"
                @click="$router.push({ name: 'tirelire' })"
                inverted>
        {{user.tirelire}} pts
      </b-button>
      </div>
    </b-navbar-item>

  </template>
</b-navbar>
</template>

<script>
import AuthModal from '@/components/layout/AuthModal.vue'
import { mapGetters, mapState } from 'vuex'
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
          icon: 'home'
        },
        {
          title: 'Rechercher un exo',
          path: 'search',
          icon: 'magnify'
        },
        {
          title: 'Poster un énoncé',
          path: 'submit',
          icon: 'upload'
        },
      ],
    }
  },
  computed: {
    ...mapGetters('authentication', ['isAuthenticated', '']),
    ...mapState('authentication', ['user'])
  },
  methods: {
    logout() {
      this.$store.dispatch('authentication/authLogout')
        .then(this.$router.push({ name: 'home' }))
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
