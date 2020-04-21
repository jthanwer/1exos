<template>
<div class="container is-fluid">
  <form @submit.prevent="searchExercices()"
        class="m-5">
    <b-field position="is-centered">
      <b-input v-model="text_query"
               placeholder="Rechercher un exercice..."
               size="is-large"
               type="search"
               icon="magnify">
      </b-input>
      <p class="control">
        <button type="submit"
                class="button is-large is-info">Rechercher</button>
      </p>
    </b-field>
  </form>

  <div class="columns">
    <div class="column is-6">
      <div v-if="(result_files.length == 0) && (used_search)">
        Cette recherche n'a renvoyé aucun résultat
      </div>
      <div v-if="(result_files.length > 0)"
           v-for="(file, index) in result_files"
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
export default {
  name: 'search',
  data() {
    return {
      text_query: null,
      used_search: false,
      result_files: [],
    }
  },
  methods: {
    searchExercices() {
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
