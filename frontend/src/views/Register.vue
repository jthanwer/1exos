<template>
<div class="card"
     style="width: 30%; margin: auto; margin-top: 130px;">
  <header class="card-header">
    <p class="card-header-title is-centered has-background-primary has-text-white">
      Créer un compte
    </p>
  </header>
  <div class="content">
    <section class="card-content">
      <form @submit.prevent="validate">
        <b-field label="Laboratoire d'affiliation">
          <b-checkbox v-model="nolab">
            Aucune affililation
          </b-checkbox>
        </b-field>

        <b-field label="Adresse e-mail">
          <b-input v-model="form.email"
                   type="email"
                   placeholder="Example@lsce.ipsl.fr">
          </b-input>
        </b-field>

        <b-field label="Mot de passe">
          <b-input v-model="form.password1"
                   type="password"
                   placeholder="Mot de passe"></b-input>
        </b-field>

        <b-field label="Confirmation du mot de passe">
          <b-input v-model="form.password2"
                   type="password"
                   @keydown.enter="validate"
                   placeholder="Retapez votre mot de passe"></b-input>
        </b-field>

        <button class="button is-primary is-fullwidth"
                type="submit">S'enregistrer</button>
      </form>
    </section>
    <section class="card-footer">
      <div class="card-footer-item has-text-centered">
        Vous avez déjà compte ?
        <router-link :to="{ name: 'login' }"
                     style="padding-left: 0.3em;">
          Connectez-vous ici.
        </router-link>
      </div>
    </section>
  </div>

</div>
</template>

<script>
export default {
  name: "Register",
  data() {
    return {
      form: {
        email: null,
        password1: null,
        password2: null,
      },

      error: false,
    }
  },
  methods: {
    validate() {
      let endpoint = '/api/auth/registration/';
      this.form.email = this.form.email.toLowerCase();
      let email = this.form.email;
      let password = this.form.password1;
      this.$http(endpoint, 'POST', this.form)
        .then(() => {
          return this.$store.dispatch('authentication/authRequest', { email, password })
        }).then(() => {
          this.$router.push('/');
        }).catch(() => {
          this.error = true;
        })
    },
  },
  watch: {}
}
</script>

<style scoped>

</style>
