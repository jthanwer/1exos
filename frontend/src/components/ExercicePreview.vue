<template>
  <div v-if="exo" class="exercice-preview">
    <b-modal v-if="exo.livre" :active.sync="isLivreModalActive" :width="320">
      <figure class="image is-3by4">
        <img
          :src="require('@/assets/images/livres/' + exo.livre + '.jpg')"
          alt="Image indisponible"
        />
      </figure>
    </b-modal>
    <b-modal has-modal-card full-screen :active.sync="isExoModalActive">
      <ModalExerciceComponent :id="exo.id" />
    </b-modal>
    <div
      :class="[has_correc ? 'border-primary' : 'border-danger', 'card']"
      style="border-radius: 20px;"
      @click="redirectExo()"
    >
      <div class="card-content">
        <div class="media">
          <div class="media-content is-clipped">
            <p v-if="exo.livre" class="title is-4">
              <span class="title is-3 has-text-grey">{{ exo.id }}.</span>
              {{ types[exo.type] }}
              {{ exo.num_exo }} - Page {{ exo.num_page }} - Sur livre
            </p>
            <p v-else class="title is-4">
              <span class="title is-3 has-text-grey">{{ exo.id }}.</span>
              {{ types[exo.type] }} {{ exo.num_exo }}
              - Sur feuille
            </p>
            <div v-if="exo.posteur" class="subtitle is-size-6">
              <p><strong> Niveau : </strong>{{ niveaux[exo.niveau] }}</p>
              <p><strong>Chapitre :</strong> {{ exo.chapitre }}</p>
              <p v-if="exo.devoir">
                <strong>Fait partie d'un :</strong> {{ exo.devoir }}
              </p>
              <p v-if="exo.livre">
                <span
                  ><strong>Livre : </strong
                  >{{ exo.livre.split('_').join(' - ') }}</span
                >
              </p>
            </div>
          </div>
          <div class="media-right">
            <b-icon
              :icon="isLiked ? 'heart' : 'heart-outline'"
              type="is-danger"
              size="is-medium"
              @click.native.stop="like()"
            >
            </b-icon>
          </div>
        </div>
        <div class="level">
          <div class="level-left">
            <div class="level-item">
              <b-taglist>
                <b-tag
                  v-if="displayDateLimite && !has_correc"
                  type="is-secondary"
                  size="is-medium"
                >
                  <span class="has-text-white">{{ delai_text }}</span>
                </b-tag>
                <b-tag
                  v-if="!has_correc && !delai_depasse"
                  type="is-secondary"
                  size="is-medium"
                >
                  {{ exo.prix }} {{ exo.prix > 1 ? 'pts' : 'pt' }} à gagner
                </b-tag>
                <b-tag
                  v-if="!has_correc && delai_depasse"
                  type="is-secondary"
                  size="is-medium"
                >
                  {{ correc_points }} {{ correc_points > 1 ? 'pts' : 'pt' }} à
                  gagner
                </b-tag>
                <b-tag
                  v-if="displayDateLimite && has_correc && !delai_depasse"
                  type="is-primary"
                  size="is-medium"
                >
                  <span class="has-text-white">{{ delai_text }}</span>
                </b-tag>
                <b-tag v-if="has_correc" type="is-primary" size="is-medium">
                  Corrigé
                </b-tag>
              </b-taglist>
            </div>
          </div>
          <div v-if="has_correc" class="level-right">
            <div class="level-item">
              <b-rate
                v-model="exo.correcs[0].mean_rating"
                class="ml-3"
                size="is-medium"
                disabled
                style="align-items: center;"
              ></b-rate>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import ModalExerciceComponent from '@/components/ModalExercice.vue'
import moment from 'moment'
import niveaux from '@/data/niveaux.json'
import types from '@/data/types.json'
export default {
  name: 'ExercicePreview',
  components: {
    ModalExerciceComponent
  },
  props: {
    exo: {
      type: Object,
      default: () => {}
    },
    liked: {
      type: Boolean,
      default: false
    },
    activated: {
      type: Boolean,
      default: true
    },
    displayDateLimite: {
      type: Boolean,
      default: true
    },
    showModal: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      niveaux: niveaux,
      types: types,
      isLivreModalActive: false,
      isLiked: this.liked,
      isExoModalActive: false
    }
  },
  computed: {
    ...mapState('authentication', ['user']),
    ...mapState('general', ['constants']),
    has_correc() {
      if (!this.exo) {
        return
      }
      return this.exo.correcs.length !== 0
    },
    diff_minutes() {
      let date1 = moment()
      let date2 = moment(this.exo.date_limite)
      let diffMinutes = date2.diff(date1, 'minutes')
      return diffMinutes
    },
    diff_hours() {
      let date1 = moment()
      let date2 = moment(this.exo.date_limite)
      let diffHours = date2.diff(date1, 'hours')
      return diffHours
    },
    diff_days() {
      let date1 = moment()
      let date2 = moment(this.exo.date_limite)
      let diffDays = date2.diff(date1, 'days')
      return diffDays
    },
    delai_text() {
      if (this.diff_minutes < 0) {
        return 'Le délai est dépassé'
      } else if (this.diff_hours < 1) {
        return 'Il reste ' + this.diff_minutes.toString() + ' minute(s)'
      } else if (this.diff_days < 2) {
        return 'Il reste ' + this.diff_hours.toString() + ' heure(s)'
      } else {
        return 'Il reste ' + this.diff_days.toString() + ' jour(s)'
      }
    },
    delai_depasse() {
      if (this.diff_minutes < 0) {
        return true
      }
      return false
    },
    correc_points() {
      if (!this.exo || !this.user) {
        if (this.delai_depasse === false) {
          return this.exo.prix
        }
        return this.constants['DEADLINE_POINTS']
      }
      if (!this.activated) {
        return this.exo.prix
      }

      let condition =
        this.delai_depasse === false &&
        this.exo.correcs.length === 0 &&
        this.exo.posteur.username !== this.user.username
      if (condition) {
        return this.exo.prix
      }
      if (this.delai_depasse) {
        return this.constants['DEADLINE_POINTS']
      } else if (this.exo.posteur.username === this.user.username) {
        return this.constants['SELFCORREC_POINTS']
      } else {
        return this.constants['MULTIPLECORREC_POINTS']
      }
    }
  },
  methods: {
    redirectExo() {
      if (this.showModal) {
        this.isExoModalActive = true
        return
      }
      if (this.activated) {
        this.$router.push({ name: 'exercice', params: { id: this.exo.id } })
      }
    },
    like() {
      this.isLiked = !this.isLiked
      let message = ''
      if (!this.activated) {
        return
      }
      if (this.isLiked) {
        message = `L'exo a été ajouté à tes exos favoris.`
        this.$store.dispatch('exercices/likeExercice', this.exo)
      } else {
        message = `L'exo a été enlevé de tes exos favoris.`
        this.$store.dispatch('exercices/dislikeExercice', this.exo)
      }
      this.$buefy.toast.open({
        duration: 2000,
        message: message,
        type: 'is-tertiary'
      })
    }
  }
}
</script>

<style scoped lang="scss"></style>
