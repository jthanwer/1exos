<template>
<div class="columns is-centered">
  <div class="column is-4">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title is-centered has-background-primary has-text-white">
          Se connecter
        </p>
      </header>
      <div class="content">
        <section class="card-content">
          <form @submit.prevent="validate()">
            <b-field label="Nom d'utilisateur">
              <b-input v-model="form.username"
                       required="required"
                       type="username"
                       placeholder="Nom d'utilisateur">
              </b-input>
            </b-field>

            <b-field label="Mot de passe">
              <b-input v-model="form.password"
                       type="password"
                       required="required"
                       placeholder="Mot de passe"
                       password-reveal></b-input>
            </b-field>

            <button class="button is-primary is-fullwidth"
                    type="submit">Connexion</button>

            <div v-if="error">
              Problème d'authentification
            </div>
          </form>
        </section>
        <footer class="card-footer">
          <div class="card-footer-item has-text-centered">
            <span class="has-text-black">Tu n'as pas encore de compte ?</span>
            <router-link class="pl-1"
                         :to="{ name: 'register' }">
              <span @click="$parent.close()">Crées-en un ici</span>
            </router-link>
          </div>
        </footer>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'Login',
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
      console.log({ username, password })
      this.$store.dispatch('authentication/authRequest', { username, password })
        .then(() => { this.$router.push('/') })
        .catch(() => { this.error = true })
    }
  }
}
</script>

<style scoped>

</style>
