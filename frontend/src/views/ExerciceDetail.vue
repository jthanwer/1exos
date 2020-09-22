<template>
  <div>
    <b-loading is-full-page :active.sync="is_loading"></b-loading>
    <b-modal
      v-if="exo"
      :active.sync="modal_correc_points"
      has-modal-card
      trap-focus
      aria-role="dialog"
      aria-modal
    >
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">
            Calcul des points gagnés
          </p>
          <button
            type="button"
            class="delete"
            @click="modal_correc_points = false"
          />
        </header>
        <section class="modal-card-body content">
          <p>
            Les points que tu gagnes en soumettant une correction dépendent de
            plusieurs facteurs:
          </p>
          <ul>
            <li>
              Si tu es le posteur de l'exo,
              <strong>tu ne gagneras qu'un seul point. </strong>
            </li>
            <li>
              Si la date limite renseignée par le posteur a déjà été dépassée,
              <strong>tu ne gagneras qu'un seul point.</strong>
            </li>
            <li>
              Si une autre correction a déjà été postée avant toi et qu'elle a
              reçu une bonne note de la part du posteur de l'exo,
              <strong>tu ne gagneras qu'un seul point.</strong>
            </li>
            <li>
              Si aucune de ces conditions n'est vérifiée, tu gagneras le prix
              concédé par le posteur de l'exo,
              <strong>c'est à dire {{ exo.prix }} pt(s).</strong>
            </li>
          </ul>
          Garde bien en tête deux choses :
          <ol>
            <li>
              Si ta correction est jugée mauvaise (3 étoiles ou moins) par le
              posteur de l'exo, elle sera supprimée et
              <strong>les points que tu avais gagnés te seront retirés</strong>
              . Donc n'utilise pas trop vite tes points gagnés et pense à
              soumettre une correction de qualité !
            </li>
            <li>
              Si tu n'est pas le premier à avoir posté une correction et que tu
              l'as postée avant la date limite, tu ne gagneras qu'un seul point
              sur le moment
              <strong
                >mais il est toujours possible pour toi de gagner les points
                cédés par le posteur de l'exo ({{ exo.prix }} pts).
              </strong>
              Pour cela, il faut que le posteur de l'exo donne une mauvaise note
              à toutes les corrections qui ont été postées avant la tienne. Si
              c'est le cas, tu recevras les points à ce moment-là.
            </li>
          </ol>
        </section>
      </div>
    </b-modal>
    <div class="columns is-centered is-vcentered">
      <div class="column is-6">
        <b-button
          v-if="has_correc"
          expanded
          class="big-button"
          size="is-large"
          type="is-tertiary"
          icon-left="arrow-right"
          @click="
            $router.push({ name: 'exo-corrections', params: { id: exo.id } })
          "
        >
          Voir les corrections
        </b-button>
        <div v-if="exo && !has_correc" class="card">
          <header class="card-header">
            <p
              class="card-header-title is-size-4 has-background-secondary has-text-white"
            >
              Aucune correction n'est disponible
            </p>
          </header>
        </div>
      </div>
    </div>

    <div class="columns is-centered mt-5">
      <div class="column is-8">
        <div v-if="exo">
          <div v-if="exo.file">
            <div v-if="exo.filetype == 'pdf'">
              <div class="field is-grouped is-grouped-centered">
                <div class="control">
                  <b-button
                    type="is-tertiary"
                    icon-left="rotate-left"
                    @click="rotatePDF -= 90"
                  ></b-button>
                </div>
                <div class="field">
                  <div class="b-numberinput field has-addons ">
                    <p class="control">
                      <b-button
                        :disabled="page == 1"
                        type="is-primary"
                        icon-left="chevron-left"
                        @click="page -= 1"
                      />
                    </p>
                    <div class="control clear-fix">
                      <input
                        v-model.number="page"
                        class="input"
                        type="number"
                        placeholder="Text input"
                        min="1"
                        :max="numPages"
                      />
                    </div>
                    <p class="control">
                      <b-button
                        :disabled="page == numPages"
                        type="is-primary"
                        icon-left="chevron-right"
                        @click="page += 1"
                      />
                    </p>
                  </div>
                </div>
                <div class="control">
                  <b-button
                    type="is-tertiary"
                    icon-left="rotate-right"
                    @click="rotatePDF += 90"
                  ></b-button>
                </div>
              </div>

              <pdf
                ref="pdf"
                class="exo-container"
                :src="exo.file"
                :page="page"
                :rotate="rotatePDF"
                @num-pages="numPages = $event"
              ></pdf>
            </div>
            <div v-else>
              <ImageContainer v-model="exo.file" />
            </div>
          </div>
          <div v-else class="exo-info pa-9 has-text-centered">
            <div class="level">
              <div class="level-item has-text-centered">
                <div>
                  <p>
                    <span class="title is-size-4"
                      >N° {{ exo.num_exo }} Page {{ exo.num_page }}
                    </span>
                  </p>
                </div>
              </div>
            </div>
            <div class="level">
              <div class="level-item has-text-centered">
                <div>
                  <img
                    style="height: 400px;"
                    :src="
                      require('@/assets/images/livres/' + exo.livre + '.jpg')
                    "
                    alt="Image indisponible"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div>
      <b-modal
        :active.sync="modal_correction"
        has-modal-card
        trap-focus
        aria-role="dialog"
        aria-modal
      >
        <div class="modal-card">
          <header class="modal-card-head">
            <p class="modal-card-title">
              Soumettre une correction
            </p>
          </header>
          <div class="modal-card-body">
            <Upload v-if="!is_loading" v-model="correction_file" :exo="false" />
            <b-progress
              v-if="is_loading"
              :value="uploadPercentage"
              size="is-large"
              show-value
              format="percent"
              type="is-tertiary"
            ></b-progress>
            <div v-if="is_loading" class="has-text-centered">
              Ta correction est en train d'être soumise. Ne quitte pas la page
              avant que le processus soit terminé !
            </div>
            <b-button
              v-if="!is_loading"
              class="my-2"
              expanded
              type="is-tertiary"
              @click="submitCorrection()"
            >
              Soumettre
            </b-button>
          </div>
        </div>
      </b-modal>
    </div>

    <div
      v-if="display_submit"
      class="columns is-centered is-vcentered is-multiline my-8 py-8 has-background-white-ter"
    >
      <div class="column is-4 has-text-centered">
        <b-button
          v-if="display_submit"
          class="big-button"
          type="is-primary"
          size="is-large"
          icon-left="upload"
          @click="modal_correction = !modal_correction"
        >
          Soumettre une correction
        </b-button>
      </div>
      <div class="column is-4 has-text-centered ">
        <div>
          <div class="subtitle has-text-primary is-4">
            Tu peux gagner
            <strong class="has-text-primary"
              >{{ correc_points }}
              {{ correc_points > 1 ? ' points !' : ' point !' }}</strong
            >
          </div>
          <div class="mt-3 is-size-7" @click="modal_correc_points = true">
            <a
              ><b-icon size="is-small" icon="help-circle-outline"></b-icon>
              Comment les points gagnés sont-ils calculés ?
            </a>
          </div>
          <div class="subtitle has-text-tertiary is-7">
            <strong class="has-text-tertiary">Explication</strong> :
            {{ correc_points_reason }}
          </div>
        </div>
      </div>
      <!-- <div class="column is-10">
        <hr class="has-background-primary" />
      </div> -->
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import pdf from 'vue-pdf'
import moment from 'moment'
import Upload from '@/components/Upload.vue'
import ImageContainer from '@/components/ImageContainer.vue'
import classes from '@/data/niveaux.json'
import exercicesService from '@/services/exercicesService'
export default {
  name: 'ExerciceDetail',
  components: {
    pdf,
    Upload,
    ImageContainer
  },
  props: {
    id: {
      type: [Number, String],
      default: null
    }
  },
  data() {
    return {
      classes: classes,
      exo: null,
      modal_correction: false,
      modal_correc_points: false,
      correction_file: null,

      is_loading: false,
      uploadPercentage: 0,

      has_correc: null,
      mark: 3,

      page: 1,
      numPages: 0,
      rotatePDF: 0,
      rotateImage: 0
    }
  },
  computed: {
    ...mapState('authentication', ['user']),
    ...mapState('general', ['constants']),
    display_submit() {
      if (!this.user || !this.exo) {
        return
      }
      let user_correcs = this.exo.correcs.filter(obj => {
        return obj.correcteur === this.user.id
      })
      if (user_correcs.length > 0) {
        return false
      }
      return true
    },
    condition() {
      if (!this.user || !this.exo) {
        return
      }
      let delai_depasse = false
      let date1 = moment()
      let date2 = moment(this.exo.date_limite)
      let diffMin = date2.diff(date1, 'minutes')
      if (diffMin < 0) {
        delai_depasse = true
      }
      let condition =
        this.exo.posteur.username !== this.user.username &&
        delai_depasse === false &&
        this.exo.correcs.length === 0
      if (condition) {
        return 'PRIX'
      }
      if (this.exo.posteur.username === this.user.username) {
        return 'SELFCORREC_POINTS'
      } else if (delai_depasse) {
        return 'DEADLINE_POINTS'
      } else {
        return 'MULTIPLECORREC_POINTS'
      }
    },
    correc_points() {
      switch (this.condition) {
        case 'SELFCORREC_POINTS':
          return this.constants['SELFCORREC_POINTS']
        case 'DEADLINE_POINTS':
          return this.constants['DEADLINE_POINTS']
        case 'MULTIPLECORREC_POINTS':
          return this.constants['MULTIPLECORREC_POINTS']
        default:
          return this.exo.prix
      }
    },
    correc_points_reason() {
      switch (this.condition) {
        case 'SELFCORREC_POINTS':
          return `tu es le posteur de l'exo.`
        case 'DEADLINE_POINTS':
          return `la date limite a été dépassée.`
        case 'MULTIPLECORREC_POINTS':
          return `une ou plusieurs corrections ont déjà été postées.`
        default:
          return `ce sont les points cédés par le posteur de l'exo.`
      }
    }
  },
  created() {
    this.updateExo()
  },
  methods: {
    updateExo() {
      exercicesService.getExercice(this.id).then(exo => {
        this.exo = exo
        if (exo.correcs.length > 0) {
          this.has_correc = true
        }
      })
    },
    submitCorrection() {
      if (this.correction_file) {
        this.is_loading = true
        this.uploadPercentage = 0
        const fd = new FormData()
        fd.append('enonce_id', this.exo.id)
        fd.append('file', this.correction_file)
        const config = {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          timeout: 120000,
          onUploadProgress: function(progressEvent) {
            this.uploadPercentage = parseInt(
              Math.round((progressEvent.loaded / progressEvent.total) * 100)
            )
          }.bind(this)
        }
        this.$store
          .dispatch('corrections/postCorrection', { fd, config })
          .then(() => {
            this.is_loading = false
            this.modal_correction = false
            this.updateExo()
            this.$store.dispatch('authentication/getProfileUser')
            this.$buefy.toast.open({
              duration: 5000,
              message: `Tu viens de gagner ${this.correc_points} ${
                this.correc_points > 1 ? 'points' : 'point'
              } !`,
              type: 'is-success'
            })
          })
          .catch(() => {
            this.is_loading = false
            this.modal_correction = false
            this.$buefy.toast.open({
              duration: 5000,
              message: `La correction n'a pas pu être postée. Reéssaye plus tard.`,
              type: 'is-danger'
            })
          })
      } else {
        this.$buefy.toast.open({
          duration: 5000,
          message: `Aucun fichier sélectionné.`,
          type: 'is-danger'
        })
      }
    },
    downloadFile() {
      this.$store.dispatch('exercices/downloadFile', this.exo)
    }
  }
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
