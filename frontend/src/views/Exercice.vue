<template>
<div class="container is-fluid">
  <div class="has-text-centered">
    <p class="title is-2">Exercice {{file_id}}</p>
    <!-- <p>{{file.file}}</p> -->
  </div>
  <div>
    <pdf src="http://www.africau.edu/images/default/sample.pdf"
         :page="1">
      <template slot="loading">
        loading content here...
      </template>
    </pdf>
  </div>
  <div class="mt-8"></div>
  <div class="columns">
    <div class="column is-6">
    </div>

    <div class="column is-6">
      <div v-if="file"
           class="data">
        <p class="title is-5">
          <span>Ajouté par : </span>
          <span class="is-pulled-right"></span>
        </p>
        <p class="title is-5">
          <span>Le : </span>
          <span class="is-pulled-right">{{file.since_added | dateFormatter}}</span>
        </p>
        <p class="title is-5">
          <span>Niveau : </span>
          <span class="is-pulled-right">1ère</span>
        </p>
        <p class="title is-5">
          <span>Difficulté : </span>
          <span class="is-pulled-right">3/4</span>
        </p>
        <p class="title is-5">
          <span>Taille : </span>
          <span class="is-pulled-right">{{file.size | sizeFormatter}}</span>
        </p>
      </div>
      <div class="download-buttons">
        <b-button class="m-6"
                  type="is-primary"
                  icon-left="download"
                  @click="downloadFile()">
          Télécharger l'énoncé
        </b-button>
        <b-button v-if="correction_bought"
                  class="m-6"
                  type="is-secondary"
                  icon-left="download"
                  @click="">
          Télécharger la correction
        </b-button>
        <b-button v-else
                  class="m-6"
                  type="is-secondary"
                  icon-left="currency-eur"
                  @click="">
          Acheter la correction
        </b-button>
      </div>
      <div class="upload-button">
        <b-button class="m-6"
                  type="is-success"
                  icon-left="upload"
                  @click="">
          Soumettre une correction
        </b-button>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import pdf from 'pdfvuer'
import filesService from "@/services/filesService"
export default {
  name: "Exercice",
  components: {
    pdf
  },
  props: {
    file_id: [Number, String]
  },
  data() {
    return {
      file: null,
      correction_bought: false,
      currentPage: 0,
      pageCount: 0,
    }
  },
  created() {
    filesService.getFile(this.file_id)
      .then(data => {
        this.file = data
      })
  },
  methods: {
    downloadFile() {
      this.$store.dispatch('files/downloadFile', this.file)
    },
  },
}
</script>

<style scoped>
.download-buttons button {
  width: 300px;
}

.upload-button button {
  width: 300px;
}
</style>
