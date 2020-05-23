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

          <b-step-item id="secondStep"
                       label="Prix et Délai"
                       :style="{'min-height': height}"
                       clickable>
            <ValidationObserver ref="secondStep">
              <hr>
              <h1 class="title has-text-centered">Prix et Délai</h1>
              <hr>
              <b-field grouped>
                <ValidationProvider rules="required"
                                    v-slot="{ errors, valid }">
                  <b-field label="Prix"
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-numberinput v-model="form.prix"
                                   :min="1">
                    </b-numberinput>
                  </b-field>
                  <div class="is-size-7">
                    Combien de points es-tu prêt à donner pour obtenir la correction de ton exo ?
                  </div>
                </ValidationProvider>
              </b-field>

              <b-field grouped>
                <ValidationProvider rules="required"
                                    v-slot="{ errors, valid }">
                  <b-field label="Délai"
                           :message="errors"
                           :type="{ 'is-danger': errors[0], 'is-success': valid }">
                    <b-datetimepicker v-model="form.date_limite"
                                      placeholder="Choisir une date limite"
                                      :month-names="month_names"
                                      :min-datetime="minDatetime"
                                      icon="calendar-today"
                                      horizontal-time-picker>
                    </b-datetimepicker>
                  </b-field>
                  <div class="is-size-7">
                    <p>Combien de temps es-tu prêt à laisser pour que la correction soit postée ?</p>
                    <p>Renseigne une date et une heure limites.</p>
                  </div>
                </ValidationProvider>
              </b-field>
            </ValidationObserver>
          </b-step-item>

          <b-step-item id="thirdStep1"
                       v-if="!form.is_from_livre"
                       :style="{'min-height': height}"
                       label="Énoncé"
                       clickable>
            <ValidationObserver ref="thirdStep">
              <hr>
              <h1 class="title has-text-centered">Énoncé</h1>
              <hr>
              <ValidationProvider rules="required"
                                  v-slot="{ errors }">
                <Upload v-model="drop_file"
                        :error="errors[0]" />
              </ValidationProvider>
            </ValidationObserver>
          </b-step-item>

          <b-step-item id="thirdStep2"
                       v-else
                       :style="{'min-height': height}"
                       label="Manuel"
                       clickable>
            <ValidationObserver ref="thirdStep">
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

          <b-step-item label="Aperçu"
                       :style="{'min-height': height}">
            <hr>
            <h1 class="title has-text-centered">Aperçu</h1>
            <hr class="mb-10">
            <div class="columns is-centered">
              <div class="column is-6">
                <ExercicePreview :exo="exo"
                                 :activated="false"></ExercicePreview>
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
                 @click.prevent="submit()">
                Poster l'exo
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
  name: 'PostExo',
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
      drop_file: null,
      form: {
        category: null,
        type: null,
        is_from_livre: false,
        livre: {
          name: null,
          num_page: 1,
          num_exo: 1
        },
        date_limite: new Date(),
        prix: 2,
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
        prix: this.form.prix,
        date_limite: this.date_limite,
        date_created: moment(),
        corrections: [],
      }
    },
  },
  methods: {
    submit() {
      this.is_loading = true
      const fd = new FormData()
      fd.append('classe', parseInt(this.form.classe))
      fd.append('category', this.form.category)
      fd.append('type', this.form.type)
      fd.append('prix', parseInt(this.form.prix))
      fd.append('date_limite', moment(this.form.date_limite).toISOString(true))
      if (this.form.is_from_livre) {
        fd.append('livre', this.form.livre.name)
        fd.append('num_page', parseInt(this.form.livre.num_page))
        fd.append('num_exo', parseInt(this.form.livre.num_exo))
      } else {
        fd.append('file', this.drop_file)
      }
      this.$store.dispatch('exercices/postExercice', fd)
        .then(data => {
          this.is_loading = false
          this.$router.push({ name: 'exercice', params: { id: data.id } })
        })
        .catch(err => {
          this.is_loading = false
          this.$buefy.toast.open({
            duration: 5000,
            message: `L'exo n'a pas pu être posté.
            Il manque sûrement des informations essentielles.`,
            type: 'is-danger'
          })
        })
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
