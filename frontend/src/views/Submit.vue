<template>
<div class="container is-fluid">
  <div class="columns is-centered">
    <div class="column is-10">
      <div class="box">
        <b-steps v-model="activeStep"
                 animated
                 has-navigation>

          <b-step-item label="Général"
                       :style="{'min-height': height}"
                       clickable>
            <hr>
            <h1 class="title has-text-centered">Général</h1>
            <hr>
            <b-field label="Quel est le niveau de cet exercice ?">
              <b-select v-model="form.classe"
                        placeholder="Choisir une classe">
                <option v-for="(classe, index) in classes"
                        :value="index">{{classe}}</option>
              </b-select>
            </b-field>
            <b-field label="De quoi traite cet exercice ?">
              <b-select v-model="form.category"
                        placeholder="Choisir une catégorie">
                <option v-for="option in categories[form.classe]">
                  {{option}}
                </option>
              </b-select>
            </b-field>
            <b-field label="Cet exercice est-il directement issu d'un manuel scolaire ?">
              <b-switch v-model="form.is_from_manuel">
                {{is_from_manuel_text}}
              </b-switch>
            </b-field>
          </b-step-item>

          <b-step-item v-if="!form.is_from_manuel"
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

            <h1 class="title has-text-centered">{{activeStep}} Manuel</h1>
            <hr>
            <b-field label="De quel manuel scolaire cet énoncé est-il issu ?">
              <b-select v-model="form.manuel.name"
                        placeholder="Choisir un manuel">
                <option value="Sesamath">Sesamath</option>
                <option value="Autres">Autres</option>
              </b-select>
            </b-field>
            <b-field label="Quel numéro de page ?">
              <b-numberinput v-model="form.manuel.num_page"
                             :min="1"></b-numberinput>
            </b-field>
            <b-field label="Quel numéro d'exercice ?">
              <b-numberinput v-model="form.manuel.num_exo"
                             :min="1"></b-numberinput>
            </b-field>
          </b-step-item>

          <b-step-item label="Confirmation"
                       :style="{'min-height': height}"
                       clickable>
            <hr>
            <h1 class="title has-text-centered">Confirmation</h1>
            <hr class="mb-10">
            <div class="columns">
              <div class="column is-4">
                <div class="has-text-centered mb-6">
                  <p class="heading">Classe</p>
                  <p class="title is-5">{{classes[form.classe]}}</p>
                </div>
                <div v-if="form.is_from_manuel"
                     class="has-text-centered">
                  <p class="heading">Manuel</p>
                  <p class="title is-5">{{form.manuel.name}}</p>
                </div>
              </div>
              <div class="column is-4">
                <div class="has-text-centered mb-6">
                  <p class="heading">Catégorie</p>
                  <p class="title is-5">{{form.category}}</p>
                </div>
                <div v-if="form.is_from_manuel"
                     class="has-text-centered">
                  <p class="heading">Numéro de la page</p>
                  <p class="title is-5">{{form.manuel.num_page}}</p>
                </div>
              </div>
              <div class="column is-4">
                <div class="has-text-centered mb-6">
                  <p class="heading">Extrait d'un manuel</p>
                  <p class="title is-5">{{is_from_manuel_text}}</p>
                </div>
                <div v-if="form.is_from_manuel"
                     class="has-text-centered">
                  <p class="heading">Numéro de l'exercice</p>
                  <p class="title is-5">{{form.manuel.num_exo}}</p>
                </div>
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
              <a v-if="activeStep < 2"
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
                Valider le formulaire
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
import categories from "@/data/categories.json"
import classes from "@/data/classes.json"
import Upload from '@/components/Upload.vue'
export default {
  name: 'submit',
  components: {
    Upload
  },
  data() {
    return {
      categories: categories,
      classes: classes,
      height: "400px",

      activeStep: null,
      drop_file: null,
      form: {
        classe: null,
        category: null,
        is_from_manuel: false,
        manuel: {
          name: null,
          num_page: 1,
          num_exo: 1
        }
      }
    }
  },
  computed: {
    is_from_manuel_text() {
      if (this.form.is_from_manuel) {
        return "Oui"
      } else {
        return "Non"
      }
    }
  },
  methods: {
    submit() {
      const fd = new FormData()
      fd.append('classe', parseInt(this.form.classe))
      fd.append('category', this.form.category)
      if (this.form.is_from_manuel) {
        fd.append('manuel', this.form.manuel.name)
        fd.append('num_page', parseInt(this.form.manuel.num_page))
        fd.append('num_exo', parseInt(this.form.manuel.num_exo))
      } else {
        fd.append('file', this.drop_file)
      }
      this.$store.dispatch('exercices/postExercice', fd)
        .then(data => {
          console.log(data)
          this.$router.push({ name: 'exercice', params: { id: data.id } })
        })
        .catch(err => alert("Problème d'importation"))
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
