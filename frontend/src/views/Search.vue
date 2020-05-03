<template>
<div>
  <div class="columns">
    <div class="column is-3">
      <b-sidebar position="static"
                 mobile="fullwidth"
                 fullwidth
                 type="is-light"
                 open>
        <div class="p-2">
          <div class="block">
            <h1 class="title">Filtrer</h1>
            <h2 class="subtitle is-6 mb-4">Coche les filtres que tu veux appliquer <br />
              Puis sélectionne la valeur du filtre.
            </h2>
          </div>
          <b-menu class="is-custom-mobile">
            <b-menu-list label="Général">
              <b-field>
                <b-checkbox v-model="filter.posteur__classe">
                  Niveau
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.posteur__classe">
                <b-select v-model="form.posteur__classe"
                          placeholder="Choisir un niveau">
                  <option v-for="(classe, index) in classes"
                          :value="index">{{classe}}</option>
                </b-select>
              </b-field>

              <b-field>
                <b-checkbox v-model="filter.category">
                  Catégorie
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.category">
                <b-select v-model="form.category"
                          placeholder="Choisir une catégorie">
                  <option v-for="option in categories[form.posteur__classe]">
                    {{option}}
                  </option>
                </b-select>
              </b-field>

              <b-field>
                <b-checkbox v-model="filter.type">
                  Type
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.type">
                <b-select v-model="form.type"
                          placeholder="Choisir un type d'exo">
                  <option> Exo simple </option>
                  <option> DM </option>
                  <option> DHC </option>
                  <option> DS </option>
                </b-select>
              </b-field>
            </b-menu-list>

            <b-menu-list label="Livre scolaire">
              <b-field>
                <b-checkbox v-model="filter.livre">
                  Nom du livre
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.livre">
                <b-select v-model="form.livre"
                          placeholder="Choisir un livre">
                  <option value="Sesamath">Sesamath</option>
                  <option value="Autres">Autres</option>
                </b-select>
              </b-field>
              <b-field>
                <b-checkbox v-model="filter.num_page">
                  Numéro de page
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.num_page">
                <b-numberinput v-model="form.num_page"
                               controls-position='compact'
                               placeholder="Numéro de page"></b-numberinput>
              </b-field>
              <b-field>
                <b-checkbox v-model="filter.num_exo">
                  Numéro d'exercice
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.num_exo">
                <b-numberinput v-model="form.num_exo"
                               controls-position='compact'
                               placeholder="Numéro d'exercice"></b-numberinput>
              </b-field>
            </b-menu-list>


            <b-menu-list label="Etablissement">
              <b-field>
                <b-checkbox v-model="filter.posteur__etablissement">
                  Nom de l'établissement
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.posteur__etablissement">
                <b-input v-model="form.posteur__etablissement"></b-input>
              </b-field>
              <b-field>
                <b-checkbox v-model="filter.posteur__prof">
                  Nom du prof
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.posteur__prof">
                <b-input v-model="form.posteur__prof"></b-input>
              </b-field>
            </b-menu-list>

          </b-menu>
        </div>
        <div class="p-1 mt-3">
          <b-button type="is-primary"
                    icon-left="magnify"
                    expanded
                    @click="searchExercices()">Rechercher</b-button>
        </div>
      </b-sidebar>
    </div>

    <div class="column is-9">
      <div class="container is-fluid">
        <div class="columns is-multiline">

          <div v-if="(result_files.length == 0) && (used_search)"
               class="column is-12">
            <div class="box has-text-centered">
              <p class="title">
                Ton Exo ne fait pas encore partie de la base de données...
              </p>
              <p class="is-subtitle">
                Poste ton Exo pour obtenir une correction en cliquant sur le bouton ci-dessous !
              </p>
              <b-button tag="router-link"
                        type="is-secondary"
                        class="mt-5"
                        size="is-large"
                        icon-left="upload"
                        :to="{name: 'submit'}">
                Poster un énoncé
              </b-button>
            </div>
          </div>

          <div v-if="(result_files.length > 0)"
               v-for="(exo, index) in result_files"
               class="column is-12"
               :key="exo.id">

            <ExercicePreview :exo="exo"></ExercicePreview>
          </div>

        </div>
      </div>
    </div>


  </div>

</div>
</template>

<script>
import exercicesService from '@/services/exercicesService'
import categories from "@/data/categories.json"
import classes from "@/data/classes.json"
import ExercicePreview from '@/components/ExercicePreview.vue'

export default {
  name: 'search',
  components: {
    ExercicePreview
  },
  data() {
    return {
      used_search: false,
      result_files: [],

      categories: categories,
      classes: classes,

      filter: {
        posteur__classe: null,
        category: null,
        type: null,
        livre: null,
        posteur_page: null,
        posteur_exo: null,
        posteur__etablissement: null,
        posteur__prof: null,
      },

      form: {
        posteur__classe: null,
        category: null,
        type: null,
        livre: null,
        num_page: null,
        num_exo: null,
        posteur__etablissement: null,
        posteur__prof: null
      }
    }
  },
  computed: {
    text_query: function() {
      let text = '?'
      for (let [key, value] of Object.entries(this.form)) {
        if (value && this.filter[key]) {
          let encoded_value = encodeURI(value)
          text += `${key}=${encoded_value}&`
        }
      }
      return text.slice(0, -1)
    }
  },
  methods: {
    searchExercices() {
      this.used_search = true
      exercicesService.searchExercices(this.text_query)
        .then((data) => {
          this.result_files = []
          this.result_files.push(...data.results)
          this.used_search = true
        })
    },
  },
}
</script>

<style>
.b-checkbox.checkbox+.checkbox {
  margin-left: 0px !important;
}
</style>
