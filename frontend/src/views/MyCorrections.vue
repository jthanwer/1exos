<template>
<div class="container is-fluid">
  <div class="columns">
    <div class="column is-6">
      <div v-for="(correc, index) in myCorrections"
           class="mb-2"
           :key="correc.id">

        <b-collapse class="card"
                    aria-id="contentId">
          <div slot="trigger"
               slot-scope="props"
               class="card-header"
               role="button"
               aria-controls="contentId">

            <div class="card-header-title is-size-5">
              <span>{{correc.name}}</span>
            </div>

            <a class="card-header-icon">
              <b-button icon-right="delete"
                        type="is-light"
                        size="is-medium"
                        @click.native.stop="deleteCorrection(correc.id, index)" />
            </a>

            <a class="card-header-icon">
              <b-button icon-right="arrow-right-drop-circle"
                        type="is-light"
                        size="is-medium"
                        @click.native.stop="$router.push({name: 'correction', params: {id: correc.id}})" />
            </a>
          </div>
        </b-collapse>
      </div>
    </div>
  </div>

</div>
</template>

<script>
import correctionsService from '@/services/correctionsService'
import { mapState } from 'vuex'
export default {
  name: 'MyCorrections',
  data() {
    return {}
  },
  mounted() {
    this.$store.dispatch('corrections/loadMyCorrections')
  },
  computed: {
    ...mapState('corrections', ['myCorrections'])
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
