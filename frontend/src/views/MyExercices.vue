<template>
<div class="container is-fluid">
  <div class="columns is-multiline">
    <div class="column is-6">
      <div class="box">
        <h1 class="title"> Mes exercices postés</h1>
      </div>
      <div v-for="(exo, index) in myExercices"
           class="column is-12"
           :key="exo.id">

        <ExercicePreview :exo="exo"></ExercicePreview>

      </div>
    </div>

  </div>

</div>
</template>

<script>
import { mapState } from 'vuex'
import exercicesService from '@/services/exercicesService'
import ExercicePreview from '@/components/ExercicePreview.vue'
export default {
  name: 'MyExercices',
  components: {
    ExercicePreview
  },
  data() {
    return {}
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
