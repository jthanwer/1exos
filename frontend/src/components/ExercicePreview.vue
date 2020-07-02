<template>
<div>
  <b-modal v-if="exo.livre"
           :active.sync="isLivreModalActive"
           :width="320">
    <figure class="image is-3by4">
      <img :src="require('@/assets/images/livres/' + exo.livre + '.jpg')"
           alt="Image indisponible" />
    </figure>
  </b-modal>
  <div :class="[has_correc ? 'border-success' : 'border-danger', 'card']">
    <div class="card-content">
      <div class="media">
        <!-- <div v-if="has_correc"
             class="media-left pa-1 has-background-success">
          <b-icon icon="check"></b-icon>
        </div> -->
        <div class="media-left">
          <b-icon :icon="isLiked ? 'heart': 'heart-outline'"
                  type="is-danger"
                  @click.native="like()"
                  size="is-medium">
          </b-icon>
        </div>
        <div class="media-content">
          <p v-if="exo.livre"
             class="title is-4">
            <span class="title is-3 has-text-grey">{{ exo.id }}.</span>
            {{exo.type === 'Exo'? 'Exo ': 'Act.' }}
            {{ exo.num_exo }} - Page {{ exo.num_page }} - Sur
            livre
          </p>
          <p v-else
             class="title is-4">
            <span class="title is-3 has-text-grey">{{ exo.id }}.</span>
            {{exo.type === 'Exo'? 'Exo ': 'Act.' }}
            sur feuille
          </p>
          <div v-if="exo.posteur"
               class="subtitle is-size-6">
            <p>
              Posté par <strong>{{ exo.posteur.username }}</strong> le
              {{ exo.date_created | dateFormatter }}
            </p>
            <p>Niveau : {{ classes[exo.posteur.classe] }}</p>
            <a @click="isLivreModalActive = true"
               v-if="exo.livre">
              Livre : {{ exo.livre.split("_").slice(1).join(" - ") }}
            </a>
          </div>
        </div>
        <div class="media-right">
          <b-tag type="is-success"
                 size="is-medium">
            {{ correc_points }} pts
          </b-tag>
        </div>
      </div>
      <div class="level">
        <div class="level-left">
          <div class="level-item">
            <b-tag v-if="exo.correcs.length === 0 && !delai_depasse"
                   type="is-danger"
                   size="is-medium">
              À corriger : il reste
              <strong class="has-text-white">{{ delai }}</strong>
            </b-tag>
            <b-tag v-else-if="exo.correcs.length === 0 && delai_depasse"
                   type="is-danger"
                   size="is-medium">
              Le délai est dépassé
            </b-tag>
            <b-tag v-else
                   type="is-success"
                   size="is-medium">
              Corrigé
            </b-tag>
          </div>
        </div>

        <div class="level-right">
          <div class="level-item">
            <b-button type="is-info"
                      :disabled="!activated"
                      size="is-medium"
                      icon-left="arrow-right"
                      @click="
                  $router.push({ name: 'exercice', params: { id: exo.id } })
                ">
              Voir
            </b-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import { mapState } from 'vuex'
import moment from "moment";
import classes from "@/data/classes.json";
export default {
  name: "ExercicePreview",
  props: {
    exo: Object,
    liked: {
      type: Boolean,
      default: false
    },
    activated: {
      type: Boolean,
      default: true
    },
  },
  data() {
    return {
      classes: classes,
      delai_depasse: false,
      isLivreModalActive: false,

      isLiked: this.liked,
    };
  },
  computed: {
    ...mapState('authentication', ['user']),
    ...mapState("general", ["constants"]),
    has_correc() {
      return this.exo.correcs.length !== 0;
    },
    delai() {
      let date1 = moment();
      let date2 = moment(this.exo.date_limite);
      let diffHours = date2.diff(date1, "hours");
      if (diffHours <= 0) {
        this.delai_depasse = true;
      } else if (diffHours < 1) {
        let diffMinutes = date2.diff(date1, "minutes");
        return diffMinutes.toString() + " minutes";
      } else if (diffHours < 48) {
        return diffHours.toString() + " heures";
      } else {
        let diffDays = date2.diff(date1, "days");
        return diffDays.toString() + " jours";
      }
    },
    correc_points() {
      let delai_depasse = false;
      let date1 = moment();
      let date2 = moment(this.exo.date_limite);
      let diffHours = date2.diff(date1, "hours");
      if (diffHours <= 0) {
        delai_depasse = true;
      }
      let condition = this.exo.posteur !== this.user && delai_depasse === false &&
        this.exo.correcs.length === 0
      if (condition) {
        return this.exo.prix
      }
      if (this.exo.posteur.id === this.user.id) {
        return this.constants["SELFCORREC_POINTS"]
      } else if (delai_depasse) {
        return this.constants["DEADLINE_POINTS"]
      } else
        return this.constants["MULTIPLECORREC_POINTS"]
    }
  },
  methods: {
    like() {
      this.isLiked = !this.isLiked;
      let message = ''
      if (!this.activated) {
        return;
      }
      if (this.isLiked) {
        message = `L'exo a été ajouté à vos exos favoris.`
        this.$store.dispatch('exercices/likeExercice', this.exo)
      } else {
        message = `L'exo a été enlevé de vos exos favoris.`
        this.$store.dispatch('exercices/dislikeExercice', this.exo)
      }
      this.$buefy.toast.open({
        duration: 2000,
        message: message,
        type: 'is-info'
      })
    }
  }
};
</script>

<style scoped lang="scss"></style>
