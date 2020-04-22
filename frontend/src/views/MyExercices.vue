<template>
<div class="container is-fluid">
  <div class="columns is-multiline">
    <div v-for="(exo, index) in myExercices"
         class="column is-6"
         :key="exo.id">

      <div class="card">
        <div class="card-content">
          <div class="media">
            <div class="media-left pa-1 has-background-warning">
              <b-icon icon="lock"></b-icon>
            </div>
            <div class="media-content">
              <p>
                <span class="title is-4">{{classes[exo.classe]}} - {{exo.category}}</span>
              </p>
              <span class="subtitle is-6">{{exo.manuel}} - Page {{exo.num_page}} - Exercice {{exo.num_exo}}
              </span>

            </div>
          </div>
          <div class="level">
            <div class="level-left">
              <div class="level-item">
              </div>
            </div>

            <div class="level-right">
              <b-button type="is-success"
                        icon-left="arrow-right"
                        @click="$router.push({name: 'exercice', params: {id: exo.id}})">
                Accéder
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
import classes from "@/data/classes.json"
import exercicesService from '@/services/exercicesService'
import { mapState } from 'vuex'
export default {
  name: 'MyExercices',
  data() {
    return {
      classes: classes
    }
  },
  mounted() {
    this.$store.dispatch('exercices/loadMyExercices')
  },
  computed: {
    ...mapState('exercices', ['myExercices'])
  },
  methods: {
    deleteExercice(id, data_index) {
      this.$store.dispatch('exercices/deleteExercice', { id, data_index })
    },
  },
}
</script>

<style>
.upload,
.upload-draggable {
  width: 100%;
}
</style>
