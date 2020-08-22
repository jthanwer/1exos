<template>
  <b-navbar type="is-primary" shadow>
    <template slot="brand">
      <b-navbar-item tag="router-link" :to="{ name: 'home' }">
        <img src="~@/assets/images/logo_void.png" alt="1exo" />
      </b-navbar-item>
    </template>
    <template v-if="user" slot="start">
      <b-navbar-item tag="div" class="ml-10 has-text-weight-bold">
        Bonjour {{ user.username }}
      </b-navbar-item>
    </template>
    <template slot="end">
      <b-navbar-item tag="router-link" :to="{ name: 'home' }">
        <b-icon class="mr-1" icon="home"></b-icon>
        <span class="is-uppercase is-size-6">Accueil</span>
      </b-navbar-item>
      <b-navbar-dropdown right hoverable class="is-size-6">
        <template slot="label">
          <b-icon class="mr-1" icon="information"></b-icon>
          <span class="is-uppercase">À propos</span>
        </template>
        <b-navbar-item tag="router-link" :to="{ name: 'presentation' }">
          Présentation du site
        </b-navbar-item>
        <b-navbar-item tag="router-link" :to="{ name: 'search' }">
          L'équipe
        </b-navbar-item>
      </b-navbar-dropdown>
      <b-navbar-item tag="router-link" :to="{ name: 'search' }">
        <b-icon class="mr-1" icon="magnify"></b-icon>
        <span class="is-uppercase is-size-6">Rechercher un exo</span>
      </b-navbar-item>
      <b-navbar-dropdown
        v-if="isAuthenticated"
        right
        hoverable
        class="is-size-6"
      >
        <template slot="label">
          <b-icon class="mr-1" icon="account"></b-icon>
          <span class="is-uppercase">Mon compte</span>
        </template>
        <b-navbar-item tag="router-link" :to="{ name: 'profile' }">
          Mon profil
        </b-navbar-item>
        <b-navbar-item tag="router-link" :to="{ name: 'tirelire' }">
          Ma tirelire
        </b-navbar-item>
        <b-navbar-item tag="router-link" :to="{ name: 'mes-exercices' }">
          Mes exercices
        </b-navbar-item>
        <b-navbar-item tag="router-link" :to="{ name: 'mes-corrections' }">
          Mes corrections
        </b-navbar-item>
        <hr class="navbar-divider" />
        <b-navbar-item @click="logout"> Se déconnecter </b-navbar-item>
      </b-navbar-dropdown>
      <b-navbar-item v-if="!isAuthenticated" tag="div">
        <b-button
          icon-left="account"
          type="is-primary"
          inverted
          @click="$router.push({ name: 'login' })"
        >
          Se connecter
        </b-button>
      </b-navbar-item>
      <b-navbar-item v-if="isAuthenticated && user" tag="div">
        <b-button
          type="is-primary"
          inverted
          @click="$router.push({ name: 'tirelire' })"
        >
          {{ user.tirelire }} {{ user.tirelire > 1 ? 'pts' : 'pt' }}
        </b-button>
      </b-navbar-item>
    </template>
  </b-navbar>
</template>

<script>
import { mapGetters, mapState } from 'vuex'
export default {
  name: 'NavbarComponent',
  components: {},
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
        }
        // {
        //   title: 'Poster un exo',
        //   path: 'post-exo',
        //   icon: 'magnify'
        // },
      ]
    }
  },
  computed: {
    ...mapGetters('authentication', ['isAuthenticated', '']),
    ...mapState('authentication', ['user'])
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
