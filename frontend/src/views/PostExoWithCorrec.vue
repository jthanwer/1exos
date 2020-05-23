<template>
<div class="container is-fluid">
  <b-loading is-full-page
             :active.sync="is_loading"></b-loading>
  <div class="columns is-centered">
    <div class="column is-10">
      <div class="box">
        <b-steps v-model="activeStep"
                 animated
                 has-navigation>
          <b-step-item id="firstStep"
                       label="Infos"
                       :style="{'min-height': height}"
                       clickable>
            <ValidationObserver ref="firstStep">
              <hr>
              <h1 class="title has-text-centered">Infos</h1>
              <hr>
              <b-field grouped>
                <ValidationProvider rules="required"
                                    v-slot="{ errors, valid }">
                  <b-field label="De quoi traite cet exo ?"
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-select v-if="user"
                              v-model="form.category"
                              placeholder="Choisir une catégorie">
                      <option v-for="option in categories[user.classe]">
                        {{option}}
                      </option>
                    </b-select>
                  </b-field>
                </ValidationProvider>
              </b-field>
              <b-field grouped>
                <ValidationProvider rules="required"
                                    v-slot="{ errors, valid }">
                  <b-field label="Cet exo est-il directement issu d'un livre scolaire ?"
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-switch v-model="form.is_from_livre">
                      {{ form.is_from_livre ? 'Oui' : 'Non' }}
                    </b-switch>
                  </b-field>
                </ValidationProvider>
              </b-field>
              <b-field grouped>
                <ValidationProvider rules="required"
                                    v-slot="{ errors, valid }">
                  <b-field label="De quel type d'exo s'agit-il ?"
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-select v-model="form.type"
                              placeholder="Choisir un type d'exo">
                      <option> Exo simple </option>
                      <option> DM </option>
                      <option> DHC </option>
                      <option> DS </option>
                    </b-select>
                  </b-field>
                </ValidationProvider>
              </b-field>
            </ValidationObserver>
          </b-step-item>

          <b-step-item id="secondStep1"
                       v-if="!form.is_from_livre"
                       :style="{'min-height': height}"
                       label="Énoncé"
                       clickable>
            <ValidationObserver ref="secondStep">
              <hr>
              <h1 class="title has-text-centered">Énoncé</h1>
              <hr>
              <ValidationProvider rules="required"
                                  v-slot="{ errors }">
                <Upload v-model="drop_file_exo"
                        :error="errors[0]" />
              </ValidationProvider>
            </ValidationObserver>
          </b-step-item>

          <b-step-item id="secondStep2"
                       v-else
                       :style="{'min-height': height}"
                       label="Manuel"
                       clickable>
            <ValidationObserver ref="secondStep">
              <hr>
              <h1 class="title has-text-centered">Manuel</h1>
              <hr>
              <b-field grouped>
                <ValidationProvider rules="required"
                                    v-slot="{ errors, valid }">
                  <b-field label="De quel livre scolaire cet énoncé est-il issu ?"
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-select v-model="form.livre.name"
                              placeholder="Choisir un livre">
                      <option value="Sesamath">Sesamath</option>
                      <option value="Autres">Autres</option>
                    </b-select>
                  </b-field>
                </ValidationProvider>
              </b-field>
              <b-field grouped>
                <ValidationProvider rules="required"
                                    v-slot="{ errors, valid }">
                  <b-field label="Quel numéro de page ?"
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-numberinput v-model="form.livre.num_page"
                                   :min="1"></b-numberinput>
                  </b-field>
                </ValidationProvider>
              </b-field>
              <b-field grouped>
                <ValidationProvider rules="required"
                                    v-slot="{ errors, valid }">
                  <b-field label="Quel numéro d'exercice ?"
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-numberinput v-model="form.livre.num_exo"
                                   :min="1"></b-numberinput>
                  </b-field>
                </ValidationProvider>
              </b-field>
            </ValidationObserver>
          </b-step-item>

          <b-step-item id="thirdStep"
                       :style="{'min-height': height}"
                       label="Correction"
                       clickable>
            <ValidationObserver ref="thirdStep">
              <hr>
              <h1 class="title has-text-centered">Correction</h1>
              <hr>
              <ValidationProvider rules="required"
                                  v-slot="{ errors }">
                <Upload v-model="drop_file_correc"
                        :exo="false"
                        :error="errors[0]" />
              </ValidationProvider>
            </ValidationObserver>
          </b-step-item>

          <b-step-item label="Aperçu"
                       :style="{'min-height': height}">
            <hr>
            <h1 class="title has-text-centered">Aperçu</h1>
            <hr class="mb-10">
            <div class="columns is-centered">
              <div class="column is-6">
                <ExercicePreview :exo="exo"
                                 :activated="false" />
              </div>
            </div>
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
              <a v-if="activeStep < 3"
                 role="button"
                 class="pagination-next"
                 :disabled="next.disabled"
                 @click.prevent="goNext(next, activeStep)">
                <b-icon icon="chevron-right" />
              </a>
              <a v-else
                 role="button"
                 class="pagination-next has-background-success has-text-white"
                 type="is-success"
                 @click.prevent="postExo()">
                Poster l'exo et sa correction
              </a>
            </div>
          </template>
        </b-steps>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import { ValidationObserver, ValidationProvider } from "vee-validate";
import { mapState } from 'vuex'
import moment from 'moment'
import categories from "@/data/categories.json"
import classes from "@/data/classes.json"
import Upload from '@/components/Upload.vue'
import ExercicePreview from '@/components/ExercicePreview.vue'
export default {
  name: 'PostExoWithCorrec',
  components: {
    Upload,
    ExercicePreview,
    ValidationObserver,
    ValidationProvider
  },
  data() {
    const min = new Date(moment().toISOString(true))
    return {
      categories: categories,
      classes: classes,
      height: "400px",
      minDatetime: min,

      is_loading: false,

      activeStep: 0,
      drop_file_exo: null,
      drop_file_correc: null,
      form: {
        category: null,
        type: null,
        is_from_livre: false,
        livre: {
          name: null,
          num_page: 1,
          num_exo: 1
        },
      }
    }
  },
  computed: {
    ...mapState('authentication', ['user']),
    exo() {
      return {
        id: 1,
        posteur: this.user,
        category: this.form.category,
        type: this.form.type,
        file: this.drop_file,
        livre: this.form.livre.name,
        num_page: this.form.livre.num_page,
        num_exo: this.form.livre.num_exo,
        date_created: moment(),
        corrections: [1],
      }
    },
  },
  methods: {
    postExo() {
      this.is_loading = true
      const fd = new FormData()
      fd.append('classe', parseInt(this.form.classe))
      fd.append('category', this.form.category)
      fd.append('type', this.form.type)
      if (this.form.is_from_livre) {
        fd.append('livre', this.form.livre.name)
        fd.append('num_page', parseInt(this.form.livre.num_page))
        fd.append('num_exo', parseInt(this.form.livre.num_exo))
      } else {
        fd.append('file', this.drop_file_exo)
      }
      this.$store.dispatch('exercices/postExercice', fd)
        .then(data => {
          return this.postCorrection(data.id)
        })
        .then(data => {
          this.is_loading = false
          this.$store.dispatch('authentication/getProfileUser')
          this.$router.push({ name: 'exercice', params: { id: data.enonce.id } })
        })
        .catch(err => {
          this.is_loading = false
          this.$buefy.toast.open({
            duration: 5000,
            message: `L'exo et sa correction n'ont pas pu être postés.
            Il manque sûrement des informations essentielles.`,
            type: 'is-danger'
          })
        })
    },
    postCorrection(id) {
      const fd = new FormData()
      console.log(id)
      fd.append('enonce_id', id)
      fd.append('file', this.drop_file_correc)
      return this.$store.dispatch('corrections/postCorrection', fd)
    },
    goNext(next, activeStep) {
      switch (activeStep) {
        case 0:
          var ref = this.$refs.firstStep
          break
        case 1:
          var ref = this.$refs.secondStep
          break
        case 2:
          var ref = this.$refs.thirdStep
          break
        default:
          var ref = this.$refs.firstStep
      }
      ref.validate().then(success => {
        if (success) {
          next.action()
        }
      })
    }

  },
}
</script>

<style>
</style>
