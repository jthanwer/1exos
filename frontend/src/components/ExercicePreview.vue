<template>
<div class="card">
  <div class="card-content">
    <div class="media">
      <div v-if="exo.corrections.length === 0"
           class="media-left pa-1 has-background-danger">
        <b-icon icon="close"></b-icon>
      </div>
      <div v-else
           class="media-left pa-1 has-background-success">
        <b-icon icon="check"></b-icon>
      </div>
      <div class="media-content">
        <p v-if="exo.livre"
           class="title is-4">
          <span class="title is-3 has-text-grey">{{exo.id}}.</span>
          n° {{exo.num_page}} p. {{exo.num_exo}} - {{exo.livre}}
        </p>
        <p v-else="exo.livre"
           class="title is-4">
          <span class="title is-3 has-text-grey">{{exo.id}}.
          </span> {{exo.type}} (enoncé sur feuille)
        </p>
        <div v-if="exo.posteur"
             class="subtitle is-size-6">
          <p>Posté par <strong>{{exo.posteur.username}}</strong> le {{exo.date_created | dateFormatter}}</p>
          <p>Niveau : {{classes[exo.posteur.classe]}}</p>
        </div>
      </div>
      <div class="media-right">
        <b-tag v-if="exo.corrections.length === 0 && !delai_depasse"
               type="is-success"
               size="is-medium">
          + {{exo.prix}} pts
        </b-tag>
        <b-tag v-else-if="exo.corrections.length === 0 && delai_depasse"
               type="is-success"
               size="is-medium">
          + 1 pts
        </b-tag>
      </div>
    </div>
    <div class="level">
      <div class="level-left">
        <div class="level-item">
          <b-tag v-if="exo.corrections.length === 0 && !delai_depasse"
                 type="is-danger"
                 size="is-medium">
            À corriger : il reste
            <strong class="has-text-white">{{delai}}</strong>
          </b-tag>
          <b-tag v-else-if="exo.corrections.length === 0 && delai_depasse"
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
                    @click="$router.push({name: 'exercice', params: {id: exo.id}})">
            Voir
          </b-button>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import moment from 'moment'
import classes from "@/data/classes.json"
export default {
  name: 'ExercicePreview',
  props: {
    exo: Object,
    activated: {
      type: Boolean,
      default: true
    },
  },
  data() {
    return {
      classes: classes,
      delai_depasse: false,
    }
  },
  computed: {
    delai() {
      let date1 = moment()
      let date2 = moment(this.exo.date_limite)
      let diffHours = date2.diff(date1, 'hours');
      if (diffHours < 0) {
        this.delai_depasse = true
      } else if (diffHours < 1) {
        let diffMinutes = date2.diff(date1, 'minutes');
        return diffMinutes.toString() + ' minutes'
      } else if (diffHours < 48) {
        return diffHours.toString() + ' heures'
      } else {
        let diffDays = date2.diff(date1, 'days');
        return diffDays.toString() + ' jours';
      }
    }
  },
  methods: {},
}
</script>

<style>
</style>
