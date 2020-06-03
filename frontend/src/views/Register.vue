<template>
<div class="container is-fluid">
  <ValidationObserver ref="form"
                      v-slot="{ handleSubmit }">

    <div class="columns is-centered">
      <div class="column is-10">
        <div class="card">
          <header class="card-header">
            <p class="card-header-title is-centered has-background-primary has-text-white">
              Crée ton compte
            </p>
          </header>
          <section class="card-content">
            <form @submit.prevent="validate()">
              <b-field grouped>
                <ValidationProvider class="is-flex"
                                    ref="username_validator"
                                    rules="required|unique_username"
                                    v-slot="{ errors, valid, failed, pending, failedRules }">
                  <b-field label="Ton pseudo"
                           :message="errors"
                           :loading="pending"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-input v-model="form.username"
                             type="text"
                             @input="reset_validation_username(failed) "
                             placeholder="xxXLeMatheuxXxx">
                    </b-input>
                  </b-field>
                  <b-field v-if="failedRules.hasOwnProperty('unique_username')"
                           :label="'Tu es ' +  input_username + ' ?'"
                           addons>
                    <div class="control">
                      <b-button type="is-primary"
                                @click="$router.push({ name: 'login' })">
                        Connecte-toi ici !
                      </b-button>
                    </div>
                  </b-field>
                </ValidationProvider>
              </b-field>

              <b-field grouped>
                <ValidationProvider rules="required"
                                    v-slot="{ errors, valid }">
                  <b-field label="Ta classe"
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-select v-model="form.classe"
                              placeholder="Choisis ta classe...">
                      <option v-for="(value, key) in classes"
                              :value="key">{{value}}</option>
                    </b-select>
                  </b-field>
                </ValidationProvider>
              </b-field>

              <b-field label="Ton établissement"></b-field>
              <!-- <b-field>
                <ValidationProvider rules="required"
                                    v-slot="{ errors, valid }">
                  <b-field :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-select v-model="form.type_etablissement"
                              placeholder="Type d'établissement">
                      <option>Collège</option>
                      <option>Lycée</option>
                    </b-select>
                  </b-field>
                </ValidationProvider>
              </b-field> -->

              <b-field>
                <ValidationProvider rules="required"
                                    v-slot="{ errors, valid }">
                  <b-field expanded
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-autocomplete expanded
                                    v-model="etablissement_input"
                                    :loading="autocomplete_loading"
                                    placeholder="Cherche ton établissement..."
                                    :data="etablissement_items"
                                    field="n"
                                    keep-first>
                      <template slot="empty">
                        <span v-if="etablissement_input.length > 5">Aucun résultat</span>
                        <span v-else>Tapes au moins 6 caractères</span>
                      </template>
                      <template slot-scope="props">
                        <div class="is-pulled-left has-text-weight-bold">
                          {{ props.option.n }}
                        </div>
                        <br>
                        <small>
                          {{ props.option.c }}
                        </small>
                      </template>
                    </b-autocomplete>
                  </b-field>
                </ValidationProvider>
              </b-field>

              <b-field label="Ton/ta prof de maths"></b-field>
              <b-field grouped>
                <ValidationProvider rules="required"
                                    v-slot="{ errors, valid }">
                  <b-field :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-select v-model="form.sexe_prof"
                              placeholder="M. ou Mme">
                      <option :value="true">M.</option>
                      <option :value="false">Mme</option>
                    </b-select>
                  </b-field>
                </ValidationProvider>
                <ValidationProvider rules="required"
                                    v-slot="{ errors, valid }">
                  <b-field :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-input v-model="form.nom_prof"
                             type="text"
                             placeholder="Dupont">
                    </b-input>
                  </b-field>
                </ValidationProvider>
              </b-field>

              <b-field grouped>
                <ValidationProvider rules="required|email|unique_email"
                                    ref="email_validator"
                                    name="email1"
                                    v-slot="{ errors, failed, valid, pending }">
                  <b-field label="Ton adresse e-mail"
                           :message="errors"
                           :loading="pending"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-input v-model="form.email1"
                             placeholder="Example@domaine.fr"
                             @input="reset_validation_email(failed) "></b-input>
                  </b-field>
                </ValidationProvider>
                <ValidationProvider rules="required|same_email:@email1"
                                    v-slot="{ errors, valid }">
                  <b-field label="Confirmation"
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-input v-model="form.email2"
                             placeholder="Retape ton adresse e-mail..."></b-input>
                  </b-field>
                </ValidationProvider>
              </b-field>

              <b-field grouped>
                <ValidationProvider rules="required|min:6"
                                    name="password1"
                                    v-slot="{ errors, valid }">
                  <b-field label="Ton mot de passe"
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-input v-model="form.password1"
                             type="password"
                             placeholder="Mot de passe"></b-input>
                  </b-field>
                </ValidationProvider>
                <ValidationProvider rules="required|same_password:@password1"
                                    v-slot="{ errors, valid }">
                  <b-field label="Confirmation"
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-input v-model="form.password2"
                             type="password"
                             @keydown.enter="validate"
                             placeholder="Retape ton mot de passe..."></b-input>
                  </b-field>
                </ValidationProvider>
              </b-field>

              <div class="has-text-centered">
                <button class="button is-primary is-medium"
                        type="submit">Valider</button>
              </div>

            </form>

          </section>

          <section class="card-footer">
            <div class="card-footer-item has-text-centered">
              Tu as déjà un compte ?
              <router-link :to="{ name: 'login' }"
                           style="padding-left: 0.3em;">
                Connecte-toi ici.
              </router-link>
            </div>
          </section>
        </div>
      </div>
    </div>
  </ValidationObserver>
</div>
</template>

<script>
import { ValidationObserver, ValidationProvider } from "vee-validate";
import classes from '@/data/classes.json'
import etablissements from '@/data/etablissements.json'
import usersService from "@/services/usersService"

export default {
  name: "Register",
  components: {
    ValidationObserver,
    ValidationProvider
  },
  data() {
    return {
      classes: classes,
      height: "400px",
      input_username: null,

      activeStep: null,

      // form: {
      //   username: null,
      //   email1: null,
      //   email2: null,
      //   password1: null,
      //   password2: null,
      //   classe: null,
      //   etablissement: null,
      //   sexe_prof: null,
      //   nom_prof: null,
      // },

      form: {
        username: 'cassosdu34',
        email1: 'cassosdu34@gmail.com',
        email2: 'cassosdu34@gmail.com',
        password1: 'Zdv:89??',
        password2: 'Zdv:89??',
        classe: 0,
        etablissement: null,
        sexe_prof: 0,
        nom_prof: 'Dupont',
      },

      etablissements: etablissements,
      etablissement_items: [],
      etablissement_input: '',
      autocomplete_loading: false,

      error: false,
    }
  },
  methods: {
    reset_validation_username(failed) {
      if (failed) {
        this.$refs.username_validator.reset()
      }
    },
    reset_validation_email(failed) {
      if (failed) {
        this.$refs.email_validator.reset()
      }
    },
    validate() {
      this.$refs.form.validate().then(success => {
        this.input_username = this.form.username;
        if (!success) {
          return;
        }
        this.submit()
      })
    },
    submit() {
      this.form.etablissement = this.etablissement_input;
      let email = this.form.email1.toLowerCase();
      const fd = new FormData()
      fd.append('username', this.form.username)
      fd.append('email', email)
      fd.append('password', this.form.password1)
      fd.append('classe', parseInt(this.form.classe))
      fd.append('etablissement', this.form.etablissement)
      fd.append('nom_prof', this.form.nom_prof)
      fd.append('sexe_prof', this.form.sexe_prof)
      this.$store.dispatch("authentication/registerUser", fd)
        .then(res => {
          this.$buefy.dialog.alert({
            title: 'Confirme ton adresse e-mail',
            type: 'is-success',
            message: `Merci d'avoir créé ton compte! <br>
            <b>Un lien de confirmation</b> a été envoyé à l\'adresse e-mail
            indiquée. <b>Clique sur ce lien</b> pour activer ton compte.<br>
            Tu ne pourras pas te connecter avant d'avoir fait cela.`,
            confirmText: 'OK',
            onConfirm: () => this.$router.push('/')
          })
        }).catch(err => {
          this.error = true;
        })
    },
    filterEtablissements(v) {
      this.etablissement_items = this.etablissements.filter(object => {
        return (object.n || '').toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "")
          .indexOf((v || '').toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "")) > -1
      });
    },
  },
  watch: {
    etablissement_input: function(input) {
      input && input.length > 5 && this.filterEtablissements(input);
    }
  }
}
</script>

<style scoped>
.field.is-grouped .field {
  margin-right: 0.75rem;
}
</style>
