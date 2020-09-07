<template>
  <div class="container is-fluid">
    <b-loading is-full-page :active.sync="is_loading"></b-loading>
    <div v-if="has_loaded">
      <div v-if="corrections.length > 0" class="columns is-multiline">
        <div
          v-for="(correc, index) in corrections"
          :key="correc.id"
          class="column is-offset-3 is-6"
        >
          <h1 class="title has-text-tertiary">Correction {{ index + 1 }}</h1>
          <CorrectionPreview
            v-if="correc && user"
            :correc="correc"
            :user="user"
            :title="false"
            :unlocked="user.unlocked_correcs.includes(correc.id)"
          />
        </div>
      </div>
      <div v-else class="has-text-centered">
        <p class="title is-3">Aucune correction n'est disponible.</p>
        <b-button
          type="is-tertiary"
          @click="$router.push({ name: 'exercice', params: { id: id } })"
        >
          Retourner à l'énoncé
        </b-button>
      </div>
    </div>
  </div>
</template>

<script>
import exercicesService from '@/services/exercicesService'
import correctionsService from '@/services/correctionsService'
import CorrectionPreview from '@/components/CorrectionPreview.vue'
import { mapState } from 'vuex'
export default {
  name: 'ExerciceCorrections',
  components: {
    CorrectionPreview
  },
  props: {
    id: {
      type: [Number, String],
      default: null
    }
  },
  data() {
    return {
      corrections: [],
      confirm_modal: false,
      has_loaded: false,
      is_loading: true
    }
  },
  computed: {
    ...mapState('authentication', ['user'])
  },
  created() {
    this.is_loading = true
    exercicesService.getExerciceCorrections(this.id).then(data => {
      this.corrections = data.results
      this.is_loading = false
      this.has_loaded = true
    })
  },
  methods: {
    confirmUnlock(correc_id, prix) {
      this.confirm_modal = false
      this.collectAndUnlock(correc_id, prix)
    },
    collectAndUnlock(correc_id, prix) {
      let payload = { prix: prix }
      correctionsService.collectAndUnlock(correc_id, payload).then(() => {
        this.$store.dispatch('authentication/getProfileUser')
      })
    }
  }
}
</script>

<style></style>
