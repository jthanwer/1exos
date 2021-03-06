<template>
  <div class="container is-fluid">
    <b-loading is-full-page :active.sync="is_loading"></b-loading>
    <ValidationObserver ref="form" v-slot="{ handleSubmit }">
      <div class="columns is-centered">
        <div class="column is-6">
          <div class="card">
            <header class="card-header">
              <p
                class="card-header-title is-centered has-background-primary has-text-white"
              >
                Créer un compte
              </p>
            </header>
            <section class="card-content">
              <form @submit.prevent="validate()">
                <ValidationProvider
                  ref="username_validator"
                  v-slot="{ errors, valid, failed, pending, failedRules }"
                  slim
                  rules="required|unique_username"
                >
                  <b-field grouped>
                    <b-field
                      label="Pseudo"
                      expanded
                      :message="errors"
                      :loading="pending"
                      :type="{ 'is-danger': errors[0], 'is-success': valid }"
                    >
                      <b-input
                        v-model="form.username"
                        expanded
                        type="text"
                        placeholder="Choisis ton pseudo..."
                        @input="reset_validation_username(failed)"
                      >
                      </b-input>
                    </b-field>
                    <b-field
                      v-if="failedRules.hasOwnProperty('unique_username')"
                      :label="'Tu es ' + input_username + ' ?'"
                      addons
                    >
                      <div class="control">
                        <b-button
                          type="is-primary"
                          @click="$router.push({ name: 'login' })"
                        >
                          Connecte-toi ici !
                        </b-button>
                      </div>
                    </b-field>
                  </b-field>
                </ValidationProvider>

                <ValidationProvider
                  v-slot="{ errors, valid }"
                  slim
                  rules="required"
                >
                  <b-field
                    label="Niveau"
                    :message="errors"
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
                  >
                    <b-select
                      v-model="form.niveau"
                      expanded
                      placeholder="Choisis ton niveau..."
                    >
                      <option
                        v-for="(value, key) in niveaux"
                        :key="value"
                        :value="key"
                        >{{ value }}</option
                      >
                      <option value="100">Enseignant</option>
                    </b-select>
                  </b-field>
                </ValidationProvider>

                <ValidationProvider
                  v-if="[0, 1].includes(parseInt(form.niveau))"
                  v-slot="{ errors, valid }"
                  slim
                  rules="required"
                >
                  <b-field
                    v-if="[0, 1].includes(parseInt(form.niveau))"
                    label="Voie"
                    :message="errors"
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
                  >
                    <b-select
                      v-model="form.voie"
                      expanded
                      placeholder="Choisis ta voie..."
                    >
                      <option v-for="voie in voies" :key="voie" :value="voie">{{
                        voie
                      }}</option>
                    </b-select>
                  </b-field>
                </ValidationProvider>

                <ValidationProvider
                  v-if="form.niveau == 0 && form.voie == 'Générale'"
                  v-slot="{ errors, valid }"
                  slim
                  rules="required"
                >
                  <b-field
                    v-if="form.niveau == 0 && form.voie == 'Générale'"
                    label="Option"
                    :message="errors"
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
                  >
                    <b-select
                      v-model="form.option"
                      expanded
                      placeholder="Choisis ton option..."
                    >
                      <option
                        v-for="option in options"
                        :key="option"
                        :value="option"
                        >{{ option }}</option
                      >
                    </b-select>
                  </b-field>
                </ValidationProvider>

                <ValidationProvider
                  v-slot="{ errors, valid }"
                  slim
                  rules="required|ville"
                  name="ville"
                >
                  <b-field
                    label="Ville"
                    :message="errors"
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
                  >
                    <b-autocomplete
                      v-model="ville_input"
                      expanded
                      icon="magnify"
                      placeholder="Cherche ta ville..."
                      :data="ville_items"
                      keep-first
                      open-on-focus
                    >
                      <template slot="empty">
                        <span v-if="ville_input.length > 3"
                          >Aucun résultat</span
                        >
                        <span v-else>Tapes au moins 3 caractères</span>
                      </template>
                    </b-autocomplete>
                  </b-field>
                </ValidationProvider>

                <ValidationProvider
                  v-slot="{ errors, valid }"
                  slim
                  rules="required|etablissement:@ville"
                  name="etablissement"
                >
                  <b-field
                    label="Établissement"
                    :message="errors"
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
                  >
                    <b-autocomplete
                      v-model="etablissement_input"
                      expanded
                      icon="magnify"
                      :loading="autocomplete_loading"
                      placeholder="Cherche ton établissement..."
                      :data="etablissement_items"
                      keep-first
                      open-on-focus
                    >
                      <template v-if="ville_input" slot="empty">
                        Aucun résultat
                      </template>
                      <template v-else slot="empty">
                        Renseigne avant cela une ville
                      </template>
                    </b-autocomplete>
                  </b-field>
                  <p class="mb-3 is-size-7">
                    Tu ne trouves pas ta ville ou ton établissement dans les
                    choix proposés ?
                    <b-tooltip label="support@1exo.fr" dashed
                      >Contacte-nous !
                    </b-tooltip>
                  </p>
                </ValidationProvider>

                <b-field
                  :label="
                    form.niveau != 100 ? 'Professeur de mathématiques' : 'Nom'
                  "
                ></b-field>
                <b-field grouped>
                  <ValidationProvider
                    v-slot="{ errors, valid }"
                    slim
                    rules="required"
                  >
                    <b-field
                      :message="errors"
                      :type="{ 'is-danger': errors[0], 'is-success': valid }"
                    >
                      <b-select v-model="form.prefix_prof" placeholder="Titre">
                        <option :value="true">M.</option>
                        <option :value="false">Mme</option>
                      </b-select>
                    </b-field>
                  </ValidationProvider>
                  <ValidationProvider
                    v-slot="{ errors, valid }"
                    slim
                    :rules="{
                      required: true,
                      prof: /^[0-9A-ZÀÂÇÉÈÊËÏÎÔa-zàâçéèêëïîô-]+$/
                    }"
                  >
                    <!-- /^[0-9A-ZÀÂÇÉÈÊËÏÎÔa-zàâçéèêëïîô\-]*$ -->
                    <b-field
                      :message="errors"
                      expanded
                      :type="{ 'is-danger': errors[0], 'is-success': valid }"
                    >
                      <b-autocomplete
                        v-model="prof_input"
                        :placeholder="
                          form.niveau != 100
                            ? 'Renseigne ton professeur...'
                            : 'Renseigne ton nom'
                        "
                        icon="magnify"
                        :data="prof_items"
                        field="nom_prof"
                        keep-first
                        dropdown-position="bottom"
                        expanded
                        @select="
                          option => {
                            form.nom_prof = option.nom_prof
                            form.prefix_prof = option.prefix_prof
                          }
                        "
                      >
                        <template slot="empty"
                          >Aucun résultat : ce nom sera ajouté</template
                        >
                        <template slot-scope="props">
                          <span class="mr-1">{{
                            props.option.prefix_prof ? 'M.' : 'Mme'
                          }}</span>
                          <span>{{ props.option.nom_prof }}</span>
                        </template>
                      </b-autocomplete>
                    </b-field>
                  </ValidationProvider>
                </b-field>
                <p class="mb-3 is-size-7 has-text-danger">
                  Ces informations sont nécessaires pour classer correctement
                  les exos sur ce site. <br />
                  Si elles ne sont pas honnêtes, ton inscription sera rapidement
                  annulée et tous tes exos seront supprimés.
                </p>

                <b-field grouped>
                  <ValidationProvider
                    ref="email_validator"
                    v-slot="{ errors, failed, valid, pending }"
                    slim
                    rules="required|email|unique_email"
                    name="email1"
                  >
                    <b-field
                      label="Adresse e-mail"
                      expanded
                      :message="errors"
                      :loading="pending"
                      :type="{ 'is-danger': errors[0], 'is-success': valid }"
                    >
                      <b-input
                        v-model.trim="form.email1"
                        expanded
                        placeholder="Example@domaine.fr"
                        @input="reset_validation_email(failed)"
                      ></b-input>
                    </b-field>
                  </ValidationProvider>
                  <ValidationProvider
                    v-slot="{ errors, valid }"
                    slim
                    rules="required|same_email:@email1"
                  >
                    <b-field
                      label="Confirmation"
                      expanded
                      :message="errors"
                      :type="{ 'is-danger': errors[0], 'is-success': valid }"
                    >
                      <b-input v-model.trim="form.email2" expanded></b-input>
                    </b-field>
                  </ValidationProvider>
                </b-field>

                <b-field grouped>
                  <ValidationProvider
                    v-slot="{ errors, valid }"
                    slim
                    rules="required|min:6"
                    name="password1"
                  >
                    <b-field
                      label="Mot de passe"
                      expanded
                      :message="errors"
                      :type="{ 'is-danger': errors[0], 'is-success': valid }"
                    >
                      <b-input
                        v-model="form.password1"
                        expanded
                        type="password"
                      ></b-input>
                    </b-field>
                  </ValidationProvider>
                  <ValidationProvider
                    v-slot="{ errors, valid }"
                    slim
                    rules="required|same_password:@password1"
                  >
                    <b-field
                      label="Confirmation"
                      expanded
                      :message="errors"
                      :type="{ 'is-danger': errors[0], 'is-success': valid }"
                    >
                      <b-input
                        v-model="form.password2"
                        expanded
                        type="password"
                        @keydown.enter="validate"
                      ></b-input>
                    </b-field>
                  </ValidationProvider>
                </b-field>

                <b-field expanded :type="{ 'is-danger': !!conditions_error }">
                  <b-checkbox v-model="form.conditions_agreed" expanded>
                    <p :class="{ 'has-text-danger': !!conditions_error }">
                      J’accepte la politique de confidentialité et les
                      conditions générales d’utilisation de ce site.
                    </p>
                  </b-checkbox>
                </b-field>

                <div class="has-text-centered mt-3 ">
                  <button class="button is-primary is-medium" type="submit">
                    Valider
                  </button>
                </div>
              </form>
            </section>

            <section class="card-footer">
              <div class="card-footer-item has-text-centered">
                Tu as déjà un compte ?
                <router-link
                  :to="{ name: 'login' }"
                  style="padding-left: 0.3em;"
                >
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
import { ValidationObserver, ValidationProvider } from 'vee-validate'
import niveaux from '@/data/niveaux.json'
import options from '@/data/options.json'
import voies from '@/data/voies.json'
import usersService from '@/services/usersService'

export default {
  name: 'Register',
  components: {
    ValidationObserver,
    ValidationProvider
  },
  data() {
    return {
      niveaux: niveaux,
      options: options,
      voies: voies,
      input_username: null,
      is_loading: false,

      activeStep: null,
      conditions_error: null,

      form: {
        username: null,
        email1: null,
        email2: null,
        password1: null,
        password2: null,
        niveau: null,
        voie: null,
        option: null,
        ville_etablissement: null,
        nom_etablissement: null,
        prefix_prof: null,
        nom_prof: null,
        conditions_agreed: false
      },

      villes: [],
      ville_items: [],
      ville_input: '',
      etablissements: [],
      etablissement_items: [],
      etablissement_input: '',
      profs: [],
      prof_items: [],
      prof_input: '',
      autocomplete_loading: false,

      error: false
    }
  },
  computed: {
    profs_etablissement() {
      return this.profs.filter(object => {
        return (
          object.nom_etablissement
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .indexOf(
              this.etablissement_input
                .toLowerCase()
                .normalize('NFD')
                .replace(/[\u0300-\u036f]/g, '')
            ) > -1
        )
      })
    }
  },
  watch: {
    ville_input: function(input) {
      input && input.length > 2 && this.filterVilles(input)
    },
    etablissement_input: function(input) {
      input && this.filterEtablissements(input)
    },
    prof_input: function(input) {
      input && this.filterProfs(input)
    }
  },
  created() {
    fetch('data/villes.json')
      .then(r => r.json())
      .then(json => {
        this.villes = json
      })
    fetch('data/etablissements.json')
      .then(r => r.json())
      .then(json => {
        this.etablissements = json
      })
    usersService.getProfs().then(profs => {
      this.profs = profs
    })
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
        this.input_username = this.form.username
        if (!success) {
          return
        }
        if (!this.form.conditions_agreed) {
          this.conditions_error = true
          return
        }

        this.submit()
      })
    },
    submit() {
      this.is_loading = true
      this.form.nom_etablissement = this.etablissement_input
      this.form.ville_etablissement = this.ville_input
      if (!this.form.nom_prof) {
        this.form.nom_prof =
          this.prof_input.charAt(0).toUpperCase() + this.prof_input.slice(1)
      }
      let email = this.form.email1.toLowerCase()
      const fd = new FormData()
      fd.append('username', this.form.username)
      fd.append('email', email)
      fd.append('password', this.form.password1)
      fd.append('niveau', parseInt(this.form.niveau))
      if (this.form.voie && [0, 1].includes(parseInt(this.form.niveau))) {
        fd.append('voie', this.form.voie)
      }
      if (
        this.form.option &&
        this.form.voie == 'Générale' &&
        this.form.niveau == 0
      ) {
        fd.append('option', this.form.option)
      }
      fd.append('nom_etablissement', this.form.nom_etablissement)
      fd.append('ville_etablissement', this.form.ville_etablissement)
      fd.append('nom_prof', this.form.nom_prof)
      fd.append('prefix_prof', this.form.prefix_prof)

      this.$store
        .dispatch('authentication/registerUser', fd)
        .then(() => {
          this.is_loading = false
          this.$buefy.dialog.alert({
            title: 'Confirme ton adresse e-mail',
            type: 'is-success',
            message: `Merci d'avoir créé ton compte! <br>
            <b>Un lien de confirmation</b> a été envoyé à l'adresse e-mail
            indiquée.`,
            confirmText: 'OK',
            onConfirm: () => this.$router.push('/')
          })
        })
        .catch(() => {
          this.is_loading = false
          this.$buefy.toast.open({
            duration: 5000,
            message: `Un problème est survenu. Réessaye plus tard.`,
            type: 'is-danger'
          })
        })
    },
    filterVilles(v) {
      this.ville_items = this.villes.filter(object => {
        return (
          (object || '')
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .indexOf(
              (v || '')
                .toLowerCase()
                .normalize('NFD')
                .replace(/[\u0300-\u036f]/g, '')
            ) > -1
        )
      })
    },
    filterEtablissements(v) {
      if (this.ville_input) {
        this.etablissement_items = this.etablissements[this.ville_input].filter(
          object => {
            return (
              (object || '')
                .toLowerCase()
                .normalize('NFD')
                .replace(/[\u0300-\u036f]/g, '')
                .indexOf(
                  (v || '')
                    .toLowerCase()
                    .normalize('NFD')
                    .replace(/[\u0300-\u036f]/g, '')
                ) > -1
            )
          }
        )
      }
    },
    filterProfs(v) {
      this.prof_items = this.profs_etablissement.filter(object => {
        return (
          (object.nom_prof || '')
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .indexOf(
              (v || '')
                .toLowerCase()
                .normalize('NFD')
                .replace(/[\u0300-\u036f]/g, '')
            ) > -1
        )
      })
    }
  }
}
</script>

<style scoped></style>
