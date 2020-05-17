<template>
<div class="container is-fluid">
  <ValidationObserver ref="form"
                      v-slot="{ handleSubmit }">
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
              <form @submit.prevent="handleSubmit(validate())">
                <div class="mb-2">
                  <ValidationProvider rules="required"
                                      v-slot="{ errors, valid }">
                    <b-field label="Ton pseudo"
                             :message="errors"
                             :type="{ 'is-danger': errors[0] }">
                      <b-input expanded
                               v-model="form.username"
                               type="username"
                               placeholder="Pseudo">
                      </b-input>
                    </b-field>
                  </ValidationProvider>
                </div>

                <div class="mb-3">
                  <ValidationProvider rules="required"
                                      v-slot="{ errors, valid }">
                    <b-field label="Ton mot de passe"
                             :message="errors"
                             :type="{ 'is-danger': errors[0] }">
                      <b-input v-model="form.password"
                               type="password"
                               placeholder="Mot de passe"
                               password-reveal></b-input>
                    </b-field>
                  </ValidationProvider>
                  <a @click="askEmail()">Tu as oublié ton mot de passe ?</a>
                </div>
                <div class="error-box my-3"
                     v-if="error">
                  {{text_error}}
                </div>

                <button class="button is-primary is-fullwidth"
                        type="submit">Connexion</button>
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
  </ValidationObserver>
</div>
</template>

<script>
import { ValidationObserver, ValidationProvider } from "vee-validate";
import usersService from "@/services/usersService"
export default {
  name: 'Login',
  components: {
    ValidationObserver,
    ValidationProvider
  },
  data() {
    return {
      form: {
        username: null,
        password: null
      },
      error: false,
      text_error: '',

    }
  },
  methods: {
    validate() {
      this.$refs.form.validate().then(success => {
        let { username, password } = this.form
        if (!success) {
          return;
        }
        this.$store.dispatch('authentication/authRequest', { username, password })
          .then(() => { this.$router.push('/') })
          .catch(() => {
            this.error = true
            usersService.check_credentials({ 'username': username })
              .then((data) => {
                if (!data['unique'] && !data['is_active']) {
                  this.text_error = `Ce compte n\'a pas encore été activé. Vérifie
                    tes emails. Un lien d'activation y a normalement été envoyé.`
                } else if (data['unique']) {
                  this.text_error = `Ce pseudo n'est associé à aucun compte.`
                } else {
                  this.text_error = `Ce pseudo est bien associé à un compte mais
                  le mot de passe n'est pas valide.`
                }
              })
          })
      })
    },
    askEmail() {
      this.$buefy.dialog.prompt({
        message: `Quelle est ton adresse e-mail?`,
        inputAttrs: {
          placeholder: 'Adresse e-mail',
          maxlength: 30
        },
        cancelText: 'Annuler',
        confirmText: 'Ok',
        trapFocus: true,
        onConfirm: (value) => this.sendResetLink(value)
      })
    },
    sendResetLink(email) {
      usersService.check_credentials({ 'email': email })
        .then((data) => {
          if (data['unique']) {
            this.$buefy.dialog.confirm({
              title: 'Adresse introuvable',
              message: `Cette adresse e-mail n'est pas
                référencée dans notre base de données.`,
              cancelText: 'Annuler',
              type: 'is-danger',
              hasIcon: true,
              confirmText: 'Réessayer',
              onConfirm: (value) => this.askEmail()
            })
          } else {
            usersService.reset_password({ 'email': email })
            this.$buefy.dialog.alert({
              title: 'Change ton mot de passe',
              type: 'is-success',
              message: `<b>Un lien de réinitialisation</b> a été envoyé à
              l'adresse e-mail indiquée.<br>
              <b>Clique sur ce lien</b> pour changer ton mot de passe.`,
              confirmText: 'OK',
            })
          }
        })
    }
  }
}
</script>

<style scoped>
.error-box {
  border-left: 5px solid red;
  padding: 10px 20px;
  color: red;
  background-color: Snow;
}
</style>
