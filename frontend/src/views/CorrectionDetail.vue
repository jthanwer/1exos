<template>
<div class="container is-fluid">
  <!-- <div class="has-text-centered"> -->
  <!-- <p class="title is-2">Correction {{id}}</p> -->
  <!-- </div> -->
  <div class="mt-2"></div>
  <div class="columns">
    <div class="column is-6">
      <div v-if="correc">
        <div v-if="correc.file">
          <div class="correc-container"
               v-if="['png', 'jpg', 'jpeg'].includes(correc.filetype)">
            <img :src="correc.file">
          </div>
          <div v-else-if="correc.filetype == 'pdf'">
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
                 class="correc-container"
                 :src="correc.file"
                 :page="page"
                 :rotate="rotate"
                 @progress="loadedRatio = $event"
                 @num-pages="numPages = $event"></pdf>
          </div>
        </div>
        <div v-else
             class="correc-info pa-9 has-text-centered">
          <div class="level">
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Manuel</p>
                <p class="title is-5">{{correc.enonce.livre}}</p>
              </div>
            </div>
          </div>
          <div class="level">
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Page</p>
                <p class="title is-5">{{correc.enonce.num_page}}</p>
              </div>
            </div>
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Numéro</p>
                <p class="title is-5">{{correc.enonce.num_correc}}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="column is-5 is-offset-1">
      <div class="correc-info pa-9 mb-8 has-text-centered">
        <div v-if="correc">
          <div class="columns is-centered is-multiline">
            <div class="column is-6 has-text-centered">
              <p class="heading">Ajouté par</p>
              <p class="title is-5">{{correc.correcteur}}</p>
            </div>
            <div class="column is-6 has-text-centered">
              <p class="heading">Le</p>
              <p class="title is-5">{{correc.date_created | dateFormatter}}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="correc-info pa-9 has-text-centered">
        <div v-if="correc">
          <div v-if="correc.enonce.livre"
               class="columns is-centered is-multiline">
            <div class="column is-12 has-text-centered">
              <p class="heading">Manuel</p>
              <p class="title is-5">{{correc.enonce.livre}}</p>
            </div>
            <div class="column is-6 has-text-centered">
              <p class="heading">Page</p>
              <p class="title is-5">{{correc.enonce.num_page}}</p>
            </div>
            <div class="column is-6 has-text-centered">
              <p class="heading">Numéro</p>
              <p class="title is-5">{{correc.enonce.num_exo}}</p>
            </div>
          </div>
          <div v-else>
            <b-button class="mt-6"
                      type="is-primary"
                      expanded
                      icon-left="book-open-page-variant"
                      @click="$router.push({name: 'exercice', params: {id: correc.enonce.id}})">
              Voir l'énoncé associé
            </b-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</div>
</template>

<script>
import pdf from 'vue-pdf'
import Upload from '@/components/Upload.vue'
import classes from '@/data/classes.json'
import correctionsService from "@/services/correctionsService"
export default {
  name: "CorrectionDetail",
  components: {
    pdf,
    Upload
  },
  props: {
    id: [Number, String]
  },
  data() {
    return {
      classes: classes,
      correc: null,
      correction_bought: false,
      modal_correction: false,
      correction_file: null,

      mark: 3,

      page: 1,
      numPages: 0,
      rotate: 0,
    }
  },
  created() {
    correctionsService.getCorrection(this.id)
      .then(data => {
        this.correc = data
      })
  },
  methods: {
    submitCorrection() {
      if (this.correction_file) {
        const fd = new FormData()
        fd.append('enonce_id', this.correc.id)
        fd.append('file', this.correction_file)
        this.$store.dispatch('corrections/postCorrection', fd)
          .then(data => {
            this.modal_correction = false
          })
          .catch(err => alert("Problème d'importation"))
      } else {
        alert("Aucun fichier sélectionné")
      }
    },
    downloadFile() {
      this.$store.dispatch('corrections/downloadFile', this.correc)
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

.correc-container {
  border: 2px solid black;
}

.correc-info {
  border: 2px solid black;
  background-color: white;
}
</style>
