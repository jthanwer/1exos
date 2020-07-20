<template>
<div class="container is-fluid">
  <b-loading is-full-page
             :active.sync="is_loading"></b-loading>
  <ValidationObserver ref="form"
                      v-slot="{ handleSubmit }">
    <div class="columns is-centered">
      <div class="column is-6">
        <div class="card">
          <header class="card-header">
            <p class="card-header-title is-centered has-background-primary has-text-white">
              Crée ton compte
            </p>
          </header>
          <section class="card-content">
            <form @submit.prevent="validate()">
              <b-field grouped>
                <ValidationProvider slim
                                    ref="username_validator"
                                    rules="required|unique_username"
                                    v-slot="{ errors, valid, failed, pending, failedRules }">
                  <b-field label="Pseudo"
                           expanded
                           :message="errors"
                           :loading="pending"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-input v-model="form.username"
                             type="text"
                             @input="reset_validation_username(failed)"
                             placeholder="Choisis ton pseudo...">
                    </b-input>
                  </b-field>
                  <b-field v-if="failedRules.hasOwnProperty('unique_username')"
                           :label="'Tu es ' + input_username + ' ?'"
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

              <ValidationProvider slim
                                  rules="required"
                                  v-slot="{ errors, valid }">
                <b-field grouped>
                  <b-field label="Classe"
                           expanded
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-select v-model="form.classe"
                              expanded
                              placeholder="Choisis ta classe...">
                      <option v-for="(value, key) in classes"
                              :value="key">{{
                          value
                        }}</option>
                    </b-select>
                  </b-field>
                </b-field>
              </ValidationProvider>


              <ValidationProvider slim
                                  rules="required"
                                  v-slot="{ errors, valid }">
                <b-field grouped>
                  <b-field label="Ville"
                           expanded
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-autocomplete expanded
                                    v-model="ville_input"
                                    placeholder="Cherche ta ville..."
                                    :data="ville_items"
                                    keep-first>
                      <template slot="empty">
                        <span v-if="ville_input.length > 3">Aucun résultat</span>
                        <span v-else>Tapes au moins 3 caractères</span>
                      </template>
                    </b-autocomplete>
                  </b-field>
                </b-field>
              </ValidationProvider>


              <ValidationProvider slim
                                  rules="required"
                                  v-slot="{ errors, valid }">
                <b-field grouped>
                  <b-field label="Établissement"
                           expanded
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-autocomplete expanded
                                    v-model="etablissement_input"
                                    :loading="autocomplete_loading"
                                    placeholder="Cherche ton établissement..."
                                    :data="etablissement_items"
                                    keep-first>
                      <template slot="empty">
                        Aucun résultat
                      </template>
                    </b-autocomplete>
                  </b-field>
                </b-field>
              </ValidationProvider>

              <b-field label="Prof de maths"></b-field>
              <b-field grouped>
                <ValidationProvider slim
                                    rules="required"
                                    v-slot="{ errors, valid }">
                  <b-field :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-select v-model="form.prefix_prof"
                              placeholder="M. ou Mme">
                      <option :value="true">M.</option>
                      <option :value="false">Mme</option>
                    </b-select>
                  </b-field>
                </ValidationProvider>
                <ValidationProvider slim
                                    rules="required"
                                    v-slot="{ errors, valid }">
                  <b-field :message="errors"
                           expanded
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-input v-model="form.nom_prof"
                             expanded
                             type="text"
                             placeholder="Dupont">
                    </b-input>
                  </b-field>
                </ValidationProvider>
              </b-field>

              <b-field grouped>
                <ValidationProvider slim
                                    rules="required|email|unique_email"
                                    ref="email_validator"
                                    name="email1"
                                    v-slot="{ errors, failed, valid, pending }">
                  <b-field label="Adresse e-mail"
                           expanded
                           :message="errors"
                           :loading="pending"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-input v-model="form.email1"
                             placeholder="Example@domaine.fr"
                             @input="reset_validation_email(failed)"></b-input>
                  </b-field>
                </ValidationProvider>
                <ValidationProvider slim
                                    rules="required|same_email:@email1"
                                    v-slot="{ errors, valid }">
                  <b-field label="Confirmation"
                           expanded
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-input v-model="form.email2"
                             placeholder="Retape ton adresse e-mail..."></b-input>
                  </b-field>
                </ValidationProvider>
              </b-field>

              <b-field grouped>
                <ValidationProvider slim
                                    rules="required|min:6"
                                    name="password1"
                                    v-slot="{ errors, valid }">
                  <b-field label="Mot de passe"
                           expanded
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-input v-model="form.password1"
                             type="password"
                             placeholder="Mot de passe"></b-input>
                  </b-field>
                </ValidationProvider>
                <ValidationProvider slim
                                    rules="required|same_password:@password1"
                                    v-slot="{ errors, valid }">
                  <b-field label="Confirmation"
                           expanded
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
                        type="submit">
                  Valider
                </button>
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
import classes from "@/data/classes.json";
import usersService from "@/services/usersService";

export default {
  name: "Register",
  components: {
    ValidationObserver,
    ValidationProvider
  },
  data() {
    return {
      classes: classes,
      input_username: null,
      is_loading: false,

      activeStep: null,

      form: {
        username: null,
        email1: null,
        email2: null,
        password1: null,
        password2: null,
        classe: null,
        ville_etablissement: null,
        nom_etablissement: null,
        prefix_prof: null,
        nom_prof: null
      },

      villes: [],
      ville_items: [],
      ville_input: "",
      etablissements: [],
      etablissement_items: [],
      etablissement_input: "",
      autocomplete_loading: false,

      error: false
    };
  },
  created() {
    fetch('data/villes.json')
      .then(r => r.json())
      .then(json => { this.villes = json })
    fetch('data/etablissements.json')
      .then(r => r.json())
      .then(json => { this.etablissements = json })
  },
  methods: {
    reset_validation_username(failed) {
      if (failed) {
        this.$refs.username_validator.reset();
      }
    },
    reset_validation_email(failed) {
      if (failed) {
        this.$refs.email_validator.reset();
      }
    },
    validate() {
      this.$refs.form.validate().then(success => {
        this.input_username = this.form.username;
        if (!success) {
          return;
        }
        this.submit();
      });
    },
    submit() {
      this.is_loading = true;
      this.form.nom_etablissement = this.etablissement_input;
      this.form.ville_etablissement = this.ville_input;
      let email = this.form.email1.toLowerCase();
      const fd = new FormData();
      fd.append("username", this.form.username);
      fd.append("email", email);
      fd.append("password", this.form.password1);
      fd.append("classe", parseInt(this.form.classe));
      fd.append("nom_etablissement", this.form.nom_etablissement);
      fd.append("ville_etablissement", this.form.ville_etablissement);
      fd.append("nom_prof", this.form.nom_prof);
      fd.append("prefix_prof", this.form.prefix_prof);
      this.$store
        .dispatch("authentication/registerUser", fd)
        .then(res => {
          this.is_loading = false;
          this.$buefy.dialog.alert({
            title: "Confirme ton adresse e-mail",
            type: "is-success",
            message: `Merci d'avoir créé ton compte! <br>
            <b>Un lien de confirmation</b> a été envoyé à l\'adresse e-mail
            indiquée. <b>Clique sur ce lien</b> pour activer ton compte.<br>
            Tu ne pourras pas te connecter avant d'avoir fait cela.`,
            confirmText: "OK",
            onConfirm: () => this.$router.push("/")
          });
        })
        .catch(err => {
          this.error = true;
        });
    },
    filterVilles(v) {
      this.ville_items = this.villes.filter(object => {
        return (
          (object || "")
          .toLowerCase()
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "")
          .indexOf(
            (v || "")
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
          ) > -1
        );
      });
    },
    filterEtablissements(v) {
      this.etablissement_items = this.etablissements[this.ville_input]
        .filter(object => {
          return (
            (object || "")
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .indexOf(
              (v || "")
              .toLowerCase()
              .normalize("NFD")
              .replace(/[\u0300-\u036f]/g, "")
            ) > -1
          );
        });
    },
  },
  watch: {
    ville_input: function(input) {
      input && input.length > 2 && this.filterVilles(input);
    },
    etablissement_input: function(input) {
      input && this.filterEtablissements(input);
    }
  }
};
</script>

<style scoped>
</style>
