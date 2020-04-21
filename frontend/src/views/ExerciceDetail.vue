<template>
<div class="container is-fluid">
  <!-- <div class="has-text-centered"> -->
  <!-- <p class="title is-2">Exercice {{id}}</p> -->
  <!-- </div> -->
  <div class="mt-8"></div>
  <div class="columns">
    <div class="column is-6">
      <div v-if="exo">
        <div class="exo-container"
             v-if="['png', 'jpg', 'jpeg'].includes(exo.filetype)">
          <img :src="exo.file">
        </div>
        <div v-else-if="exo.filetype == 'pdf'">
          <div class="field is-grouped is-grouped-centered">
            <div class="control">
              <b-button @click="rotate -= 90"
                        type="is-secondary"
                        icon-left="rotate-left"></b-button>
            </div>
            <div class="field">
              <div class="b-numberinput field has-addons ">
                <p class="control">
                  <b-button @click="page -= 1"
                            :disabled="page == 1"
                            type="is-primary"
                            icon-left="chevron-left" />
                </p>
                <div class="control clear-fix">
                  <input v-model.number="page"
                         class="input"
                         type="number"
                         placeholder="Text input"
                         min="1"
                         :max="numPages">
                </div>
                <p class="control">
                  <b-button @click="page += 1"
                            :disabled="page == numPages"
                            type="is-primary"
                            icon-left="chevron-right" />
                </p>
              </div>
            </div>
            <div class="control">
              <b-button @click="rotate += 90"
                        type="is-secondary"
                        icon-left="rotate-right"></b-button>
            </div>
          </div>

          <pdf ref="pdf"
               class="exo-container"
               :src="exo.file"
               :page="page"
               :rotate="rotate"
               @progress="loadedRatio = $event"
               @num-pages="numPages = $event"></pdf>
        </div>
      </div>
    </div>

    <div class="column is-5 is-offset-1">
      <div class="exo-info has-text-centered">
        <div v-if="exo"
             class="level">
          <div class="level-item has-text-centered">
            <div>
              <p class="heading">Ajouté par</p>
              <p class="title is-5">{{exo.user}}</p>
            </div>
          </div>
          <div class="level-item has-text-centered">
            <div>
              <p class="heading">Le</p>
              <p class="title is-5">{{exo.date_created | dateFormatter}}</p>
            </div>
          </div>
        </div>
        <div v-if="exo"
             class="level">
          <div class="level-item has-text-centered">
            <div>
              <p class="heading">Niveau</p>
              <p class="title is-5">1ère</p>
            </div>
          </div>
          <div class="level-item has-text-centered">
            <div>
              <p class="heading">Difficulté</p>
              <b-rate v-model="mark"
                      :max="5"
                      :disabled="true"></b-rate>
            </div>
          </div>
        </div>
        <div class="download-buttons">
          <b-button class="mt-6"
                    type="is-primary"
                    icon-left="download"
                    @click="downloadFile()">
            Télécharger l'énoncé
          </b-button>
          <b-button v-if="correction_bought"
                    class="mt-6 ml-2"
                    type="is-secondary"
                    icon-left="download"
                    @click="">
            Télécharger la correction
          </b-button>
          <b-button v-else
                    class="mt-6 ml-2"
                    type="is-secondary"
                    icon-left="lock-open"
                    @click="">
            Débloquer une correction
          </b-button>
        </div>
        <div class="upload-button">
          <b-button class="mt-6 sm-trans"
                    :type="{'is-success': submitCorrection}"
                    icon-left="upload"
                    @click="submitCorrection = !submitCorrection">
            Soumettre une correction
          </b-button>
        </div>
      </div>
      <div class="mt-8">
        <Upload v-if="submitCorrection" />
      </div>
    </div>
  </div>
</div>
</template>

<script>
import pdf from 'vue-pdf'
import Upload from '@/components/Upload.vue'
import exercicesService from "@/services/exercicesService"
export default {
  name: "ExerciceDetail",
  components: {
    pdf,
    Upload
  },
  props: {
    id: [Number, String]
  },
  data() {
    return {
      exo: null,
      correction_bought: false,
      submitCorrection: false,

      mark: 3,

      page: 1,
      numPages: 0,
      rotate: 0,
    }
  },
  created() {
    exercicesService.getExercice(this.id)
      .then(data => {
        this.exo = data
      })
  },
  methods: {
    downloadFile() {
      this.$store.dispatch('exercices/downloadFile', this.exo)
    },
  },
}
</script>

<style scoped>
.download-buttons button {
  width: 250px;
}

.upload-button button {
  width: 250px;
}

.exo-container {
  border: 2px solid black;
}

.exo-info {
  padding: 50px 10px;
  border: 2px solid black;
}
</style>
