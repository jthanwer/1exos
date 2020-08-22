<template>
  <div class="exercice-preview">
    <b-modal v-if="exo.livre" :active.sync="isLivreModalActive" :width="320">
      <figure class="image is-3by4">
        <img
          :src="require('@/assets/images/livres/' + exo.livre + '.jpg')"
          alt="Image indisponible"
        />
      </figure>
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
              {{ exo.type === 'Exo' ? 'Exo ' : 'Act.' }}
              {{ exo.num_exo }} - Page {{ exo.num_page }} - Sur livre
            </p>
            <p v-else class="title is-4">
              <span class="title is-3 has-text-grey">{{ exo.id }}.</span>
              {{ exo.type === 'Exo' ? 'Exo ' : 'Act.' }} {{ exo.num_exo }}
              - Sur feuille
            </p>
            <div v-if="exo.posteur" class="subtitle is-size-6">
              <!-- <p>
              Posté par <strong>{{ exo.posteur.username }}</strong> le
              {{ exo.date_created | dateFormatter }}
            </p> -->
              <p>Niveau : {{ classes[exo.niveau] }}</p>
              <p v-if="exo.devoir">Fait partie d'un : {{ exo.devoir }}</p>
              <p v-if="exo.livre">
                <span>Livre : </span>
                <a @click="isLivreModalActive = true">
                  {{ exo.livre.split('_').join(' - ') }}
                </a>
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
          <!-- <div v-if="!has_correc" class="media-right">
            <b-tag type="is-success" size="is-medium">
              {{ correc_points }} {{ correc_points > 1 ? 'pts' : 'pt' }} à
              gagner
            </b-tag>
          </div> -->
        </div>
        <div class="level">
          <div class="level-left">
            <div class="level-item">
              <b-taglist>
                <b-tag v-if="!has_correc" type="is-secondary" size="is-medium">
                  <span class="has-text-white">{{ delai }}</span>
                </b-tag>
                <b-tag v-if="!has_correc" type="is-secondary" size="is-medium">
                  {{ correc_points }} {{ correc_points > 1 ? 'pts' : 'pt' }} à
                  gagner
                  <span v-if="activated && exo && user">
                    {{
                      exo.posteur.username !== user.username
                        ? ''
                        : '(posté par toi)'
                    }}</span
                  >
                </b-tag>
                <b-tag v-else type="is-primary" size="is-medium">
                  Corrigé
                </b-tag>
              </b-taglist>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import moment from 'moment'
import classes from '@/data/niveaux.json'
export default {
  name: 'ExercicePreview',
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
    }
  },
  data() {
    return {
      classes: classes,
      isLivreModalActive: false,

      isLiked: this.liked
    }
  },
  computed: {
    ...mapState('authentication', ['user']),
    ...mapState('general', ['constants']),
    has_correc() {
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
      let diffMinutes = date2.diff(date1, 'hours')
      return diffMinutes
    },
    diff_days() {
      let date1 = moment()
      let date2 = moment(this.exo.date_limite)
      let diffMinutes = date2.diff(date1, 'days')
      return diffMinutes
    },
    delai() {
      if (this.diff_minutes < 0) {
        return 'Le délai est dépassé'
      } else if (this.diff_hours < 1) {
        return (
          'À corriger : il reste ' + this.diff_minutes.toString() + ' minute(s)'
        )
      } else if (this.diff_days < 2) {
        return (
          'À corriger : il reste ' + this.diff_hours.toString() + ' heure(s)'
        )
      } else {
        return 'À corriger : il reste ' + this.diff_days.toString() + ' jour(s)'
      }
    },
    correc_points() {
      if (!this.activated || !this.user || !this.exo.posteur) {
        return this.exo.prix
      }
      let delai_depasse = false
      if (this.diff_hours <= 0) {
        delai_depasse = true
      }
      let condition =
        this.exo.posteur.username !== this.user.username &&
        delai_depasse === false &&
        this.exo.correcs.length === 0
      if (condition) {
        return this.exo.prix
      }
      if (this.exo.posteur.username === this.user.username) {
        return this.constants['SELFCORREC_POINTS']
      } else if (delai_depasse) {
        return this.constants['DEADLINE_POINTS']
      } else {
        return this.constants['MULTIPLECORREC_POINTS']
      }
    }
  },
  methods: {
    redirectExo() {
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
