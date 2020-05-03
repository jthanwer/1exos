<template>
<div class="container is-fluid">

  <div class="columns is-centered">
    <div class="column is-10">
      <div class="card">
        <header class="card-header">
          <p class="card-header-title is-centered has-background-primary has-text-white">
            Créer un compte
          </p>
        </header>
        <section class="card-content">
          <b-steps v-model="activeStep"
                   animated
                   has-navigation>

            <b-step-item label="Infos"
                         :style="{'min-height': height}"
                         clickable>
              <hr>
              <h1 class="title has-text-centered">Infos</h1>
              <hr>

              <b-field grouped>
                <b-field label="Nom d'utilisateur">
                  <b-input v-model="form.username"
                           type="text"
                           placeholder="xxXLeMatheuxXxx">
                  </b-input>
                </b-field>
              </b-field>

              <b-field grouped>
                <b-field label="Adresse e-mail">
                  <b-input v-model="form.email1"
                           type="email"
                           placeholder="Example@domaine.fr">
                  </b-input>
                </b-field>
                <b-field label="Confirmation de l'adresse e-mail">
                  <b-input v-model="form.emai2"
                           type="email"
                           placeholder="Retape ton adresse e-mail">
                  </b-input>
                </b-field>
              </b-field>

              <b-field grouped>
                <b-field label="Mot de passe">
                  <b-input v-model="form.password1"
                           type="password"
                           placeholder="Mot de passe"></b-input>
                </b-field>

                <b-field label="Confirmation du mot de passe">
                  <b-input v-model="form.password2"
                           type="password"
                           @keydown.enter="validate"
                           placeholder="Retape ton mot de passe"></b-input>
                </b-field>
              </b-field>

            </b-step-item>

            <b-step-item label="Confirmation"
                         :style="{'min-height': height}"
                         clickable>
              <hr>
              <h1 class="title has-text-centered">Confirmation</h1>
              <hr class="mb-10">
              <b-field grouped>
                <b-field label="Classe">
                  <b-select v-model="form.classe">
                    <option v-for="(value, key) in classes"
                            :value="key">{{value}}</option>
                  </b-select>
                </b-field>
              </b-field>
              <b-field grouped>
                <b-field label="Nom de l'établissement fréquenté">
                  <b-input v-model="form.etablissement"
                           type="text"
                           placeholder="Lycée Clément Marot">
                  </b-input>
                </b-field>
              </b-field>
              <b-field grouped>
                <b-field label="Nom du professeur de mathématiques">
                  <b-input v-model="form.prof"
                           type="text"
                           placeholder="Mme Durant ou M. Dupont">
                  </b-input>
                </b-field>
              </b-field>

            </b-step-item>

            <template slot="navigation"
                      slot-scope="{previous, next}">
              <div class="has-text-centered">
                <a role="button"
                   class="pagination-previous"
                   :disabled="previous.disabled"
                   @click.prevent="previous.action">
                  <b-icon icon="chevron-left" />
                </a>
                <a v-if="activeStep < 1"
                   role="button"
                   class="pagination-next"
                   :disabled="next.disabled"
                   @click.prevent="next.action">
                  <b-icon icon="chevron-right" />
                </a>
                <a v-else
                   role="button"
                   class="pagination-next has-background-success has-text-white"
                   type="is-success"
                   @click.prevent="validate()">
                  Créer le compte
                </a>
              </div>
            </template>
          </b-steps>
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
</div>
</template>

<script>
import classes from '@/data/classes.json'
export default {
  name: "Register",
  data() {
    return {
      classes: classes,
      height: "400px",

      activeStep: null,

      form: {
        username: null,
        email1: null,
        email2: null,
        password1: null,
        password2: null,
        classe: null,
        etablissement: null,
        prof: null,
      },

      error: false,
    }
  },
  methods: {
    validate() {
      let email = this.form.email1.toLowerCase();
      const fd = new FormData()
      fd.append('username', this.form.username)
      fd.append('email', email)
      fd.append('password', this.form.password1)
      fd.append('classe', parseInt(this.form.classe))
      fd.append('etablissement', this.form.etablissement)
      fd.append('prof', this.form.prof)
      this.$store.dispatch("authentication/registerUser", fd)
        .then(res => {
          this.$router.push('/')
        }).catch(err => {
          console.log(err)
          this.error = true;
        })
    },
  },
  watch: {}
}
</script>

<style scoped>

</style>
