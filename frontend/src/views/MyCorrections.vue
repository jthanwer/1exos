<template>
<div class="container is-fluid">
  <div class="columns is-multiline">
    <div v-for="(correc, index) in myCorrections"
         class="column is-6"
         :key="correc.id">

      <CorrectionPreview :correc="correc"
                         :user="user"
                         :unlocked="true"></CorrectionPreview>

    </div>
  </div>

</div>
</template>

<script>
import correctionsService from '@/services/correctionsService'
import CorrectionPreview from '@/components/CorrectionPreview.vue'
import { mapState } from 'vuex'
export default {
  name: 'MyCorrections',
  components: {
    CorrectionPreview
  },
  data() {
    return {}
  },
  mounted() {
    this.$store.dispatch('corrections/loadMyCorrections')
  },
  computed: {
    ...mapState('corrections', ['myCorrections']),
    ...mapState('authentication', ['user'])
  },
  methods: {
    deleteCorrection(id, data_index) {
      this.$store.dispatch('corrections/deleteCorrection', { id, data_index })
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
