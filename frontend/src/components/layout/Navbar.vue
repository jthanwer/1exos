<template>
<b-navbar id="main-navbar"
          class="has-background-primary"
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
    <b-navbar-dropdown right
                       hoverable
                       class="is-size-5">
      <template slot="label">
        <span class="is-uppercase">Profil</span>
      </template>
      <b-navbar-item tag="router-link"
                     :to="{ name: 'profile' }">
        Mon profil
      </b-navbar-item>
      <b-navbar-item @click="logout"> Se déconnecter </b-navbar-item>
    </b-navbar-dropdown>
  </template>
</b-navbar>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: "NavbarComponent",
  data() {
    return {
      appTitle: 'Exos',
      sidebar: false,
      menuItems: [{
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
      this.$store.dispatch('authentication/authLogout').then(() => { this.$router.push('/login') })
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
