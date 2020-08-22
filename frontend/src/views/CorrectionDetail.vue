<template>
  <div class="container is-fluid">
    <!-- <div class="has-text-centered"> -->
    <!-- <p class="title is-2">Correction {{id}}</p> -->
    <!-- </div> -->
    <div class="mt-2"></div>
    <div class="columns">
      <div class="column is-8">
        <div v-if="correc">
          <div v-if="correc.file">
            <div
              v-if="['png', 'jpg', 'jpeg'].includes(correc.filetype)"
              class="correc-container"
            >
              <img :src="correc.file" />
            </div>
            <div v-else>
              <div class="field is-grouped is-grouped-centered">
                <div class="control">
                  <b-button
                    type="is-secondary"
                    icon-left="rotate-left"
                    @click="rotate -= 90"
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
                    type="is-secondary"
                    icon-left="rotate-right"
                    @click="rotate += 90"
                  ></b-button>
                </div>
              </div>

              <pdf
                ref="pdf"
                class="correc-container"
                :src="correc.file"
                :page="page"
                :rotate="rotate"
                @progress="loadedRatio = $event"
                @num-pages="numPages = $event"
              ></pdf>
            </div>
          </div>
        </div>
      </div>

      <div class="column is-3 is-offset-1">
        <div class="correc-info box pa-5 mb-8 has-text-centered">
          <div v-if="correc">
            <div class="columns is-centered is-multiline">
              <div class="column is-7 has-text-centered">
                <p class="heading">Ajoutée par</p>
                <p class="title is-6">{{ correc.correcteur }}</p>
              </div>
              <!-- <div class="column is-7 has-text-centered">
                <p class="heading">Le</p>
                <p class="title is-6">
                  {{ correc.date_created | dateFormatter }}
                </p>
              </div> -->
              <div class="column is-7 has-text-centered">
                <p class="heading">Note moyenne</p>
                <b-rate
                  v-if="correc.mean_rating"
                  v-model="correc.mean_rating"
                  size="is-medium"
                  disabled
                  style="justify-content: center;"
                ></b-rate>
                <p v-else class="title is-6">
                  Aucune note donnée
                </p>
              </div>
            </div>
          </div>
        </div>
        <div v-if="correc">
          <div
            v-if="correc.enonce.livre"
            class="has-text-centered correc-info box "
          >
            <div class="level">
              <div class="level-item has-text-centered">
                <div>
                  <p>
                    <span class="title is-size-4"
                      >N° {{ correc.enonce.num_exo }} Page
                      {{ correc.enonce.num_page }}
                    </span>
                  </p>
                </div>
              </div>
            </div>
            <div class="level">
              <div class="level-item has-text-centered">
                <img
                  style="height: 400px;"
                  :src="
                    require('@/assets/images/livres/' +
                      correc.enonce.livre +
                      '.jpg')
                  "
                  alt="Image indisponible"
                />
              </div>
            </div>
          </div>
          <div v-else>
            <b-button
              class="mt-6"
              type="is-primary"
              expanded
              icon-left="book-open-page-variant"
              @click="
                $router.push({
                  name: 'exercice',
                  params: { id: correc.enonce.id }
                })
              "
            >
              Voir l'énoncé
            </b-button>
          </div>
        </div>
        <div v-if="user && correc">
          <b-button
            v-if="user_rating && user.username != correc.correcteur"
            class="mt-6"
            type="is-secondary"
            expanded
            icon-left="star"
            @click="modal_modify_rating = true"
          >
            Modifier ta note
          </b-button>
          <b-button
            v-if="!user_rating && user.username != correc.correcteur"
            class="mt-6"
            type="is-secondary"
            expanded
            icon-left="star"
            @click="modal_new_rating = true"
          >
            Noter
          </b-button>
          <b-button
            v-if="correc && user.username == correc.correcteur"
            class="mt-6"
            type="is-danger"
            expanded
            icon-left="delete"
            @click="confirmDelete()"
          >
            Supprimer
          </b-button>
        </div>

        <b-modal
          v-if="user && correc"
          :active.sync="modal_new_rating"
          has-modal-card
          trap-focus
          aria-role="dialog"
          aria-modal
        >
          <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">Noter cette correction</p>
            </header>
            <div class="modal-card-body">
              <b-rate
                v-model="vote_value"
                spaced
                style="justify-content: center;"
                size="is-large"
              ></b-rate>
              <div
                v-if="user.username === correc.enonce.posteur.username"
                class="has-text-centered"
              >
                Une note inférieure ou égale à 3 étoiles venant de ta part
                entraînera la suppression de cette correction.
              </div>
              <b-button
                class="mb-2 mt-6"
                expanded
                type="is-primary"
                @click="confirmRating('post')"
              >
                Noter
              </b-button>
            </div>
          </div>
        </b-modal>

        <b-modal
          v-if="user && correc"
          :active.sync="modal_modify_rating"
          has-modal-card
          trap-focus
          aria-role="dialog"
          aria-modal
        >
          <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">Modifie ta note</p>
            </header>
            <div class="modal-card-body">
              <b-rate
                v-model="vote_value"
                spaced
                style="justify-content: center;"
                size="is-large"
              ></b-rate>
              <div
                v-if="user.username === correc.enonce.posteur.username"
                class="has-text-centered"
              >
                Une note inférieure ou égale à 3 étoiles venant de ta part
                entraînera la suppression de cette correction.
              </div>
              <b-button
                class="mb-2 mt-6"
                expanded
                type="is-primary"
                @click="confirmRating('patch')"
              >
                Modifier
              </b-button>
            </div>
          </div>
        </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import pdf from 'vue-pdf'
import classes from '@/data/niveaux.json'
import correctionsService from '@/services/correctionsService'
import ratingsService from '@/services/ratingsService'
export default {
  name: 'CorrectionDetail',
  components: {
    pdf
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
      correc: null,

      modal_new_rating: false,
      vote_value: 2,
      ratings: [],
      voters: [],
      modal_modify_rating: false,

      page: 1,
      numPages: 0,
      rotate: 0
    }
  },
  computed: {
    ...mapState('authentication', ['user']),
    user_rating() {
      if (!this.user) {
        return
      }
      let user_rating = this.ratings.filter(object => {
        return object.voter == this.user.username
      })
      if (user_rating.length > 0) {
        user_rating = user_rating[0]
      } else {
        user_rating = null
      }
      return user_rating
    }
  },
  watch: {
    user_rating(val) {
      if (val) {
        this.vote_value = val.value
      }
    }
  },
  created() {
    this.retrieveCorrec()
    this.getRatings()
  },
  methods: {
    getRatings() {
      correctionsService.getRatings(this.id).then(data => {
        this.ratings.push(...data)
        this.voters = data.map(function(value) {
          return value['voter']
        })
      })
    },
    retrieveCorrec() {
      correctionsService.getCorrection(this.id).then(data => {
        this.correc = data
        this.vote_value = this.correc.mean_rating
      })
    },
    confirmRating(method) {
      if (
        this.user.username == this.correc.enonce.posteur.username &&
        this.vote_value < 4
      ) {
        this.$buefy.dialog.confirm({
          title: 'Confirmer la note',
          message: `Es-tu sûr de vouloir mettre une <strong>note aussi basse ?</strong>
          Cette correction sera supprimée. <br> Si une autre correction a été postée avant la date limite, 
          les points seront transférés à son correcteur. <br> Sinon, tu récupéreras tes points.`,
          confirmText: 'Confirmer',
          cancelText: 'Annuler',
          type: 'is-danger',
          hasIcon: true,
          onConfirm: () => {
            if (method === 'post') {
              this.createRating()
            } else {
              this.modifyRating()
            }
          }
        })
      } else {
        {
          if (method === 'post') {
            this.createRating()
          } else {
            this.modifyRating()
          }
        }
      }
    },
    createRating() {
      this.modal_new_rating = false
      const fd = new FormData()
      fd.append('correc_id', this.correc.id)
      fd.append('value', this.vote_value)
      ratingsService
        .create_rating(fd)
        .then(() => {
          return correctionsService.getCorrection(this.id)
        })
        .then(data => {
          this.correc = data
          this.getRatings()
        })
        .catch(err => {
          let status = err.response.status
          switch (status) {
            case 404:
              this.$store.dispatch('authentication/getProfileUser')
              this.$router.push({
                name: 'exo-corrections',
                params: { id: this.correc.enonce.id }
              })
          }
        })
    },
    modifyRating() {
      this.modal_modify_rating = false
      const fd = new FormData()
      fd.append('value', this.vote_value)
      ratingsService
        .modify_rating(this.user_rating.id, fd)
        .then(() => {
          return correctionsService.getCorrection(this.id)
        })
        .then(data => {
          this.correc = data
          this.getRatings()
        })
        .catch(err => {
          let status = err.response.status
          switch (status) {
            case 404:
              this.$router.push({
                name: 'exo-corrections',
                params: { id: this.correc.enonce.id }
              })
          }
        })
    },
    confirmDelete() {
      this.$buefy.dialog.confirm({
        title: 'Confirmer la suppression',
        message: `Es-tu sûr de vouloir supprimer cette correction ? <br> 
          Les points que tu as gagnés en la postant te seront retirés.`,
        confirmText: 'Confirmer',
        cancelText: 'Annuler',
        type: 'is-danger',
        hasIcon: true,
        onConfirm: () => this.deleteCorrec()
      })
    },
    deleteCorrec() {
      this.$store
        .dispatch('corrections/deleteCorrection', this.correc)
        .then(() => {
          return this.$store.dispatch('authentication/getProfileUser')
        })
        .then(() => {
          this.$router.push({
            name: 'exercice',
            params: { id: this.correc.enonce.id }
          })
        })
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

.correc-container {
  border: 2px solid black;
}

.correc-info {
  border: 2px solid black;
  background-color: white;
}
</style>
