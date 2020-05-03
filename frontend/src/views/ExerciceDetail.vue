<template>
<div class="container is-fluid">
  <div class="mt-2"></div>
  <div class="columns">
    <div class="column is-6">
      <div v-if="exo">
        <div v-if="exo.file">
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
        <div v-else
             class="exo-info pa-9 has-text-centered">
          <div class="level">
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Manuel</p>
                <p class="title is-5">{{exo.livre}}</p>
              </div>
            </div>
          </div>
          <div class="level">
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Page</p>
                <p class="title is-5">{{exo.num_page}}</p>
              </div>
            </div>
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Numéro</p>
                <p class="title is-5">{{exo.num_exo}}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="column is-5 is-offset-1">
      <div class="exo-info pa-9 has-text-centered">
        <div v-if="exo">
          <div class="columns is-centered is-multiline">
            <div class="column is-6 has-text-centered">
              <p class="heading">Ajouté par</p>
              <p class="title is-5">{{exo.posteur.username}}</p>
            </div>
            <div class="column is-6 has-text-centered">
              <p class="heading">Le</p>
              <p class="title is-5">{{exo.date_created | dateFormatter}}</p>
            </div>
            <div class="column is-12 has-text-centered mt-6">
              <p class="heading">Catégorie</p>
              <p class="title is-5">{{exo.category}}</p>
            </div>
            <div class="column is-6 has-text-centered">
              <p class="heading">Niveau</p>
              <p class="title is-5">{{classes[exo.posteur.classe]}}</p>
            </div>
            <div class="column is-6 has-text-centered">
              <p class="heading">Difficulté</p>
              <b-rate v-model="mark"
                      style="justify-content: center;"
                      :max="5"
                      :disabled="true"></b-rate>
            </div>
          </div>
          <div>
            <b-button v-if="exo.file"
                      class="mt-6"
                      type="is-primary"
                      expanded
                      icon-left="download"
                      @click="downloadFile()">
              Télécharger l'énoncé
            </b-button>
          </div>
        </div>
      </div>
      <div>
        <div v-if="exo">
          <b-button v-if="!correc_id"
                    class="mt-6"
                    expanded
                    size="is-large"
                    type="is-danger">
            Aucune correction disponible
          </b-button>
          <b-button v-else-if="user && correc_id && user.correc.includes(correc_id)"
                    class="mt-6"
                    expanded
                    size="is-large"
                    type="is-info"
                    icon-left="arrow-right"
                    @click="$router.push({name: 'correction', params: {id: correc_id}})">
            Voir la correction
          </b-button>
          <b-button v-else
                    class="mt-6"
                    expanded
                    size="is-large"
                    type="is-warning"
                    icon-left="lock"
                    @click="confirm_unlock_modal = true">
            Débloquer la correction ({{correc_prix}} pts)
          </b-button>
          <b-modal :active.sync="confirm_unlock_modal"
                   has-modal-card
                   trap-focus
                   aria-role="dialog"
                   aria-modal>
            <div class="modal-card"
                 style="width: auto">
              <header class="modal-card-head">
                <p class="modal-card-title">Confirmer le prélèvement</p>
              </header>
              <div class="modal-card-body">
                Es-tu sûr de vouloir prélever le montant de {{correc_prix}} pts sur
                ta tirelire ? <br> Il te restera {{user.tirelire - correc_prix}} pts.
              </div>
              <footer class="modal-card-foot">
                <b-button @click="confirm_modal = false">Annuler</b-button>
                <b-button @click="collectAndUnlock()"
                          type="is-success">Confirmer</b-button>
              </footer>
            </div>
          </b-modal>
        </div>
        <b-button class="
                    mt-6"
                  expanded
                  type="is-primary"
                  size="is-large"
                  icon-left="upload"
                  @click="modal_correction = !modal_correction">
          Soumettre une correction
        </b-button>
      </div>
      <div class="mt-8">
        <b-modal :active.sync="modal_correction"
                 width="50%"
                 has-modal-card
                 trap-focus
                 aria-role="dialog"
                 aria-modal>
          <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">Soumettre une correction</p>
            </header>
            <div class="modal-card-body">
              <Upload v-model="correction_file" />
              <b-button class="my-2"
                        expanded
                        type="is-primary"
                        @click="submitCorrection()">
                Soumettre
              </b-button>
            </div>
          </div>
        </b-modal>
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
import correctionsService from '@/services/correctionsService'
import exercicesService from "@/services/exercicesService"
import { mapState } from 'vuex'
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
      classes: classes,
      exo: null,
      modal_correction: false,
      correction_file: null,

      confirm_unlock_modal: false,
      correc_id: null,
      correc_prix: null,

      mark: 3,

      page: 1,
      numPages: 0,
      rotate: 0,
    }
  },
  computed: {
    ...mapState('authentication', ['user'])
  },
  created() {
    this.updateExo()
  },
  methods: {
    updateExo() {
      exercicesService.getExercice(this.id)
        .then(data => {
          this.exo = data
          if (data.corrections.length > 0) {
            this.correc_id = data.corrections[0]['id']
            this.correc_prix = data.corrections[0]['prix']
          }
        })
    },
    submitCorrection() {
      if (this.correction_file) {
        const fd = new FormData()
        fd.append('enonce_id', this.exo.id)
        fd.append('file', this.correction_file)
        this.$store.dispatch('corrections/postCorrection', fd)
          .then(data => {
            this.modal_correction = false
            this.updateExo()
            this.$store.dispatch('authentication/getProfileUser')
          })
          .catch(err => alert("Problème d'importation"))
      } else {
        alert("Aucun fichier sélectionné")
      }
    },
    collectAndUnlock() {
      this.confirm_unlock_modal = false
      let payload = { 'prix': this.correc_prix }
      correctionsService.collectAndUnlock(this.correc_id, payload)
        .then(data => {
          this.$store.dispatch('authentication/getProfileUser')
        })
    },
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
  border: 2px solid black;
  background-color: white;
}
</style>
