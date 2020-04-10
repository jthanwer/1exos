<template>
<div class="card"
     style="width: 30%; margin: auto; margin-top: 130px;">
  <header class="card-header">
    <p class="card-header-title is-centered has-background-primary has-text-white">
      Se connecter
    </p>
  </header>
  <section class="card-content">
    <form @submit.prevent="validate">
      <b-field label="Adresse e-mail">
        <b-input v-model="form.email"
                 type="email"
                 placeholder="Adresse e-mail">
        </b-input>
      </b-field>

      <b-field label="Mot de passe">
        <b-input v-model="form.password"
                 type="password"
                 placeholder="Mot de passe"
                 password-reveal></b-input>
      </b-field>

      <button class="button is-primary is-fullwidth"
              type="submit">Connexion</button>
    </form>
  </section>
  <section class="card-footer">
    <div class="card-footer-item has-text-centered">
      Vous n'avez pas de compte ?
      <router-link :to="{ name: 'register' }"
                   style="padding-left: 0.3em;">
        Vous pouvez en créer un ici.
      </router-link>
    </div>
  </section>
</div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      valid: true,
      form: {
        email: null,
        password: null,
      },
      error: false,
    }
  },
  methods: {
    validate() {
      this.form.email = this.form.email.toLowerCase();
      let { email, password } = this.form;
      this.$store.dispatch('authentication/authRequest', { email, password })
        .then(() => { this.$router.push('/') })
        .catch(() => { this.error = true });
    }
  }
}
</script>

<style scoped>

</style>
