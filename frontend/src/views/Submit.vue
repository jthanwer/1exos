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

          <b-step-item label="Infos"
                       :style="{'min-height': height}"
                       clickable>
            <hr>
            <h1 class="title has-text-centered">Infos</h1>
            <hr>
            <b-field label="De quoi traite cet exo ?">
              <b-select v-if="user"
                        v-model="form.category"
                        placeholder="Choisir une catégorie">
                <option v-for="option in categories[user.classe]">
                  {{option}}
                </option>
              </b-select>
            </b-field>
            <b-field label="Cet exo est-il directement issu d'un livre scolaire ?">
              <b-switch v-model="form.is_from_livre">
                {{is_from_livre_text}}
              </b-switch>
            </b-field>
            <b-field label="De quel type d'exo s'agit-il ?">
              <b-select v-model="form.type"
                        placeholder="Choisir un type d'exo">
                <option> Exo simple </option>
                <option> DM </option>
                <option> DHC </option>
                <option> DS </option>
              </b-select>
            </b-field>
          </b-step-item>

          <b-step-item label="Prix et Délai"
                       :style="{'min-height': height}"
                       clickable>
            <hr>
            <h1 class="title has-text-centered">Prix et Délai</h1>
            <hr>
            <b-field grouped>
              <b-field v-model="form.prix"
                       label="Prix"
                       message="Combien de points es-tu prêt à donner pour obtenir la correction de ton exo ?">
                <b-numberinput v-model="form.prix"
                               :min="1">
                </b-numberinput>
              </b-field>
            </b-field>

            <b-field grouped>
              <b-field label="Délai"
                       message="Quel jour souhaiterais-tu avoir ta correction ?">
                <b-datetimepicker v-model="form.date_limite"
                                  placeholder="Choisir une date limite"
                                  :min-datetime="minDatetime"
                                  icon="calendar-today"
                                  horizontal-time-picker>
                </b-datetimepicker>
              </b-field>
            </b-field>

          </b-step-item>

          <b-step-item v-if="!form.is_from_livre"
                       :style="{'min-height': height}"
                       label="Énoncé"
                       clickable>
            <hr>
            <h1 class="title has-text-centered">Énoncé</h1>
            <hr>
            <Upload v-model="drop_file" />
          </b-step-item>

          <b-step-item v-else
                       :style="{'min-height': height}"
                       label="Manuel"
                       clickable>
            <hr>

            <h1 class="title has-text-centered">Manuel</h1>
            <hr>
            <b-field label="De quel livre scolaire cet énoncé est-il issu ?">
              <b-select v-model="form.livre.name"
                        placeholder="Choisir un livre">
                <option value="Sesamath">Sesamath</option>
                <option value="Autres">Autres</option>
              </b-select>
            </b-field>
            <b-field grouped>
              <b-field label="Quel numéro de page ?">
                <b-numberinput v-model="form.livre.num_page"
                               :min="1"></b-numberinput>
              </b-field>
            </b-field>
            <b-field grouped>
              <b-field label="Quel numéro d'exercice ?">
                <b-numberinput v-model="form.livre.num_exo"
                               :min="1"></b-numberinput>
              </b-field>
            </b-field>
          </b-step-item>

          <b-step-item label="Aperçu"
                       :style="{'min-height': height}">
            <hr>
            <h1 class="title has-text-centered">Aperçu</h1>
            <hr class="mb-10">
            <div class="columns is-centered">
              <div class="column is-6">
                <ExercicePreview :exo="exo"
                                 :activated="true"></ExercicePreview>
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
                 @click.prevent="next.action">
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
import { mapState } from 'vuex'
import moment from 'moment'
import categories from "@/data/categories.json"
import classes from "@/data/classes.json"
import Upload from '@/components/Upload.vue'
import ExercicePreview from '@/components/ExercicePreview.vue'
export default {
  name: 'submit',
  components: {
    Upload,
    ExercicePreview
  },
  data() {
    const min = new Date(moment().toISOString(true))
    return {
      categories: categories,
      classes: classes,
      height: "400px",
      minDatetime: min,

      is_loading: false,

      activeStep: null,
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
    is_from_livre_text() {
      if (this.form.is_from_livre) {
        return "Oui"
      } else {
        return "Non"
      }
    },
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
        date_created: moment(),
        date_limite: this.date_limite,
        corrections: [],
      }
    },
    date_limite() {
      let formattedTime = moment(this.form.date_limite).toISOString(true)
      return formattedTime
    }
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
  },
}
</script>

<style>
.upload,
.upload-draggable {
  width: 100%;
}
</style>
