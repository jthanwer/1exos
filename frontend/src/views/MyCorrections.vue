<template>
<div class="container is-fluid">
  <div class="columns is-multiline">
    <div v-for="(correc, index) in myCorrections"
         class="column is-6"
         :key="correc.id">

      <div class="card">
        <div class="card-content">
          <div class="media">
            <div class="media-left pa-1 has-background-warning">
              <b-icon icon="lock"></b-icon>
            </div>
            <div class="media-content">
              <p>
                <span class="title is-4">Correction {{index + 1}}</span>
              </p>
              <span class="subtitle is-6">par {{correc.user}}
                <span>
                  <b-rate :max="5"
                          :disabled="true"></b-rate>
                </span>
              </span>

            </div>
            <div class="media-right">
              <b-tag type="is-info"
                     size="is-medium">{{correc.price}} €</b-tag>
            </div>
          </div>
          <div class="level">
            <div class="level-left">
              <div class="level-item">
                <b-tag type="is-success"
                       size="is-medium">
                  <b-icon icon="check"
                          class="mr-1"
                          size="is-small" />Correction vérifiée
                </b-tag>
              </div>
            </div>

            <div class="level-right">
              <b-button type="is-success"
                        icon-left="arrow-right"
                        @click="$router.push({name: 'correction', params: {id: correc.id}})">
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
