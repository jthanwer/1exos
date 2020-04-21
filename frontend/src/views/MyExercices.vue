<template>
<div class="container is-fluid">
  <div class="columns">
    <div class="column is-6">
      <div v-for="(exo, index) in myExercices"
           class="mb-2"
           :key="exo.id">

        <b-collapse class="card"
                    aria-id="contentId">
          <div slot="trigger"
               slot-scope="props"
               class="card-header"
               role="button"
               aria-controls="contentId">

            <div class="card-header-title is-size-5">
              <span>{{exo.id}}</span>
            </div>

            <a class="card-header-icon">
              <b-button icon-right="delete"
                        type="is-light"
                        size="is-medium"
                        @click.native.stop="deleteExercice(exo.id, index)" />
            </a>

            <a class="card-header-icon">
              <b-button icon-right="arrow-right-drop-circle"
                        type="is-light"
                        size="is-medium"
                        @click.native.stop="$router.push({name: 'exercice', params: {id: exo.id}})" />
            </a>
          </div>
        </b-collapse>
      </div>
    </div>
  </div>

</div>
</template>

<script>
import exercicesService from '@/services/exercicesService'
import { mapState } from 'vuex'
export default {
  name: 'MyExercices',
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
