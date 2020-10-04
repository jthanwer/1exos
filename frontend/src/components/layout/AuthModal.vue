<template>
  <div class="card">
    <header class="modal-card-head">
      <p class="modal-card-title">Connecte-toi</p>
    </header>
    <section class="modal-card-body">
      <form @submit.prevent="validate()">
        <b-field label="Nom d'utilisateur">
          <b-input
            v-model="form.username"
            required="required"
            type="username"
            placeholder="Nom d'utilisateur"
          >
          </b-input>
        </b-field>

        <b-field label="Mot de passe">
          <b-input
            v-model="form.password"
            type="password"
            required="required"
            placeholder="Mot de passe"
            password-reveal
          ></b-input>
        </b-field>

        <button class="button is-primary is-fullwidth" type="submit">
          Connexion
        </button>

        <div v-if="error">
          Problème d'authentification
        </div>
      </form>
      <div class="mt-3 has-text-centered">
        <span class="has-text-black">Tu n'as pas encore de compte ?</span>
        <router-link class="pl-1" :to="{ name: 'register' }">
          <span @click="$parent.close()">Créez-en un ici</span>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'AuthModal',
  data() {
    return {
      form: {
        username: null,
        password: null
      },
      error: false
    }
  },
  methods: {
    validate() {
      let { username, password } = this.form
      this.$store
        .dispatch('authentication/authRequest', { username, password })
        .then(() => {
          this.$parent.close()
        })
        .then(() => {
          this.$router.push('/')
        })
        .catch(() => {
          this.error = true
        })
    }
  }
}
</script>
