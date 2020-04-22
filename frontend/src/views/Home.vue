<template>
<div>
  <section class="hero is-bold">
    <div class="hero-body">
      <div class="container">
        <h1 class="title">
          Bienvenue sur 1Exo !
        </h1>
        <div class="columns">
          <div class="column is-8">
            <h2 class="subtitle">
              1Exo est une base de données communautaire d'énoncés et
              de corrections d'exercices de mathématiques accessibles par tous les élèves
              du secondaire de France.
            </h2>
          </div>
        </div>
      </div>

      <div class="has-text-centered mt-5">
        <b-button tag="router-link"
                  type="is-primary"
                  class="m-3"
                  size="is-large"
                  icon-left="magnify"
                  :to="{name: 'search'}">Rechercher un exercice</b-button>
        <b-button tag="router-link"
                  type="is-secondary"
                  class="m-3"
                  size="is-large"
                  icon-left="upload"
                  :to="{name: 'submit'}">Poster un énoncé</b-button>
      </div>
    </div>

  </section>

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
