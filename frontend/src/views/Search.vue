<template>
<div>
  <div class="container">
    <form @submit.prevent="searchExercices()">
      <b-field grouped>

        <b-field label="Niveau de l'exercice">
          <b-select v-model="form.classe"
                    placeholder="Choisir un niveau">
            <option v-for="(classe, index) in classes"
                    :value="index">{{classe}}</option>
          </b-select>
        </b-field>

      </b-field>

      <b-field grouped>
        <b-field label="Catégorie">
          <b-select v-model="form.category"
                    placeholder="Choisir une catégorie">
            <option v-for="option in categories[form.classe]">
              {{option}}
            </option>
          </b-select>
        </b-field>
      </b-field>

      <b-field grouped>

        <b-field label="Manuel">
          <b-select v-model="form.manuel"
                    placeholder="Choisir un manuel">
            <option value="Sesamath">Sesamath</option>
            <option value="Autres">Autres</option>
          </b-select>
        </b-field>

        <b-field label="Numéro de page">
          <b-numberinput v-model="form.num_page"
                         controls-position='compact'
                         placeholder="Numéro de page"></b-numberinput>
        </b-field>

        <b-field label="Numéro d'exercice">
          <b-numberinput v-model="form.num_exo"
                         controls-position='compact'
                         placeholder="Numéro d'exercice"></b-numberinput>
        </b-field>

      </b-field>

      <button type="submit"
              class="button is-large is-primary">
        <b-icon icon="magnify"
                class="mr-1"></b-icon>
        Rechercher
      </button>

    </form>
  </div>

  <div class="container is-fluid mt-8">
    <div class="columns is-multiline">
      <div v-if="(result_files.length == 0) && (used_search)"
           class="column is-12">
        <div class="box has-text-centered">
          <p class="title">Désolé ! Cette recherche n'a renvoyé aucun résultat...</p>
          <p class="is-subtitle">Vous pouvez poster un énoncé et <strong>demander une correction</strong>
            en cliquant sur le bouton ci-dessous.</p>
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
           class="column is-6"
           :key="exo.id">

        <div class="card">
          <div class="card-content">
            <div class="media">
              <div class="media-left pa-1 has-background-warning">
                <b-icon icon="lock"></b-icon>
              </div>
              <div class="media-content">
                <p>
                  <span class="title is-4">{{classes[exo.classe]}} - {{exo.category}}</span>
                </p>
                <span class="subtitle is-6">{{exo.manuel}} - Page {{exo.num_page}} - Exercice {{exo.num_exo}}
                </span>

              </div>
            </div>
            <div class="level">
              <div class="level-left">
                <div class="level-item">
                </div>
              </div>

              <div class="level-right">
                <b-button type="is-success"
                          icon-left="arrow-right"
                          @click="$router.push({name: 'exercice', params: {id: exo.id}})">
                  Accéder
                </b-button>
              </div>
            </div>
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
export default {
  name: 'search',
  data() {
    return {
      used_search: false,
      result_files: [],

      categories: categories,
      classes: classes,

      form: {
        classe: null,
        category: null,
        manuel: null,
        num_page: null,
        num_exo: null
      }
    }
  },
  computed: {
    text_query: function() {
      let text = '?'
      for (let [key, value] of Object.entries(this.form)) {
        if (value) {
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
</style>
