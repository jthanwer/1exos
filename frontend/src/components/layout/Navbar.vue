<template>
  <div>
    <b-navbar type="is-primary" shadow>
      <template slot="brand">
        <b-navbar-item
          class="has-background-tertiary"
          tag="router-link"
          :to="{ name: 'home' }"
        >
          <img src="~@/assets/images/logo_void_white.png" alt="1exo" />
        </b-navbar-item>
        <b-navbar-item
          v-if="isAuthenticated && user"
          class="is-hidden-desktop px-1"
          style="margin-left: auto !important;"
          tag="div"
        >
          <b-button
            type="is-primary"
            style="line-height: 1em;"
            inverted
            @click="$router.push({ name: 'tirelire' })"
          >
            <span
              >{{ user.tirelire }} {{ user.tirelire > 1 ? 'pts' : 'pt' }}
            </span>
            <br />
            <span
              v-if="user.tirelire_avail != user.tirelire"
              class="has-text-warning is-size-7"
              >{{ user.tirelire_avail }}
              {{ user.tirelire_avail > 1 ? 'pts' : 'pt' }}</span
            >
          </b-button>
        </b-navbar-item>

        <b-navbar-item
          v-if="isAuthenticated && user"
          class="is-hidden-desktop px-1"
          tag="div"
        >
          <b-button
            v-if="
              notifications && notifications.some(element => element.unread)
            "
            class="bell-button"
            type="is-danger"
            :icon-left="open_notifs_mobile ? 'bell-ring-outline' : 'bell-ring'"
            @click="open_notifs_mobile = !open_notifs_mobile"
          ></b-button>
          <b-button
            v-else
            class="bell-button"
            type="is-primary"
            inverted
            :icon-left="open_notifs_mobile ? 'bell-outline' : 'bell'"
            @click="open_notifs_mobile = !open_notifs_mobile"
          ></b-button>
          <b-icon
            v-if="open_notifs_mobile"
            class="menu-down-notifs"
            type="is-primary"
            size="is-large"
            icon="menu-down"
          ></b-icon>
        </b-navbar-item>
      </template>
      <!-- <template v-if="user" slot="start">
        <b-navbar-item tag="div" class="ml-10 has-text-weight-bold">
          Bonjour {{ user.username }}
        </b-navbar-item>
      </template> -->
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
          <b-navbar-item tag="router-link" :to="{ name: 'standards-qualite' }">
            Comment bien poster ?
          </b-navbar-item>
        </b-navbar-dropdown>
        <b-navbar-item tag="router-link" :to="{ name: 'post-exo' }">
          <b-icon class="mr-1" icon="hand"></b-icon>
          <span class="is-uppercase is-size-6">Demander une correction</span>
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
        <b-navbar-item v-if="!isAuthenticated" tag="div">
          <b-button
            icon-left="account-plus"
            type="is-primary"
            inverted
            @click="$router.push({ name: 'register' })"
          >
            Créer un compte
          </b-button>
        </b-navbar-item>
        <b-navbar-item
          v-if="isAuthenticated && user"
          tag="div"
          class="is-hidden-touch"
        >
          <b-button
            style="line-height: 1em;"
            type="is-primary"
            inverted
            @click="$router.push({ name: 'tirelire' })"
          >
            <span
              >{{ user.tirelire }} {{ user.tirelire > 1 ? 'pts' : 'pt' }}
            </span>
            <br />
            <span
              v-if="user.tirelire_avail != user.tirelire"
              class="has-text-warning is-size-7"
              >{{ user.tirelire_avail }}
              {{ user.tirelire_avail > 1 ? 'pts' : 'pt' }}</span
            >
          </b-button>
        </b-navbar-item>
        <div v-click-outside="closeNotifs" class="is-hidden-touch">
          <b-navbar-item v-if="isAuthenticated && user" tag="div">
            <b-button
              v-if="
                notifications && notifications.some(element => element.unread)
              "
              class="bell-button"
              type="is-danger"
              :icon-left="open_notifs ? 'bell-ring-outline' : 'bell-ring'"
              @click="open_notifs = !open_notifs"
            ></b-button>
            <b-button
              v-else
              class="bell-button"
              type="is-primary"
              inverted
              :icon-left="open_notifs ? 'bell-outline' : 'bell'"
              @click="open_notifs = !open_notifs"
            ></b-button>
            <b-icon
              v-if="open_notifs"
              class="menu-down-notifs"
              type="is-primary"
              size="is-large"
              icon="menu-down"
            ></b-icon>
          </b-navbar-item>
          <NotificationGroupComponent
            v-if="notifications && open_notifs"
            v-model="notifications"
            :active.sync="open_notifs"
          />
        </div>
      </template>
    </b-navbar>
    <NotificationGroupComponent
      v-if="notifications && open_notifs_mobile"
      v-model="notifications"
      class="is-hidden-desktop"
      :active.sync="open_notifs_mobile"
    />
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import NotificationGroupComponent from '@/components/NotificationGroup.vue'
export default {
  name: 'NavbarComponent',
  components: {
    NotificationGroupComponent
  },
  data() {
    return {
      appTitle: 'Exos',
      open_notifs: false,
      open_notifs_mobile: false,
      menuItems: [
        {
          title: 'Accueil',
          path: 'home',
          icon: 'home'
        },
        {
          title: 'Rechercher un exo',
          path: 'home',
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
    ...mapGetters('authentication', ['isAuthenticated']),
    ...mapState('authentication', ['user', 'notifications'])
  },
  methods: {
    closeNotifs() {
      this.open_notifs = false
    },
    logout() {
      this.$store.dispatch('authentication/authLogout')
    }
  }
}
</script>

<style lang="scss">
a {
  text-decoration: none !important;
}

.bell-button {
  position: relative;
  z-index: 30;
}

.menu-down-notifs {
  position: absolute;
  padding: 0;
  padding-top: -0.5em;
  margin: 0;
  top: 2.25em;
  left: 0.5em;
  text-align: center;
  z-index: 26;
}

.icon-nav {
  margin-right: 3em;
}
</style>
