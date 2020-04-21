<template>
<div class="container is-fluid">
  <div class="has-text-centered mb-10">
    <span class="title is-1">Bienvenue sur 1Exo !</span>
  </div>
  <div class="columns is-mobile is-centered">
    <div class="column is-half">
      <div class="has-text-centered mb-10">
        <span class="">
          1Exo a pour vocation d'être une base de données communautaire d'énoncés et
          de corrections d'exercices de mathématiques accessibles par tous les élèves
          du secondaire de France.
        </span>
      </div>
    </div>
  </div>
  <div class="has-text-centered mb-20">
    <b-button tag="router-link"
              type="is-primary"
              class="m-3"
              size="is-large"
              icon-left="magnify"
              :to="{name: 'search'}">Rechercher un exo</b-button>
    <b-button tag="router-link"
              type="is-secondary"
              class="m-3"
              size="is-large"
              icon-left="upload"
              :to="{name: 'submit'}">Poster un énoncé</b-button>
  </div>
  <div class="columns">
    <div class="column is-6">
      <div v-for="(file, index) in allFiles"
           class="mb-2"
           :key="file.id">
        <b-collapse class="card"
                    aria-id="contentId">
          <div slot="trigger"
               slot-scope="props"
               class="card-header"
               role="button"
               aria-controls="contentId">

            <div class="card-header-title is-size-5">
              <span>{{file.name}}</span>
            </div>

            <a class="card-header-icon">
              <b-button icon-right="delete"
                        type="is-light"
                        size="is-medium"
                        @click.native.stop="deleteExercice(file.id, index)" />
            </a>

            <a class="card-header-icon">
              <b-button icon-right="arrow-right-drop-circle"
                        type="is-light"
                        size="is-medium"
                        @click.native.stop="$router.push({name: 'exercice', params: {id: file.id}})" />
            </a>
          </div>
        </b-collapse>
      </div>
    </div>
  </div>

</div>
</template>

<script>
import exercicesService from '@/services/exercicesService'
import { mapState } from 'vuex'
import Upload from '@/components/Upload.vue'
export default {
  name: 'home',
  components: {
    Upload
  },
  data() {
    return {
      text_query: null,
      used_search: false,
      result_files: [],

      allFiles: []
    }
  },
  computed: {},
  mounted() {
    exercicesService.getAllExercices()
      .then((data) => {
        this.allFiles = data.results
      })
  },
  methods: {
    deleteExercice(id, data_index) {
      this.$store.dispatch('exercices/deleteExercice', { id, data_index })
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
