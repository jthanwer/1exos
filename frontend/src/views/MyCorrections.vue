<template>
  <div class="container is-fluid">
    <div class="columns" style="min-height: 800px;">
      <div class="column is-3 card">
        <div class="card-content">
          <b-menu>
            <b-menu-list label="Mes corrections">
              <b-menu-item
                icon="account"
                :active="isActive"
                label="Mes corrections postées"
                @click="selected = 1"
              >
              </b-menu-item>
              <b-menu-item
                icon="account"
                label="Mes corrections débloquées"
                @click="selected = 2"
              >
              </b-menu-item>
            </b-menu-list>
          </b-menu>
        </div>
      </div>

      <div class="column is-offset-1 is-8 card">
        <div v-if="selected === 1">
          <div class="columns is-centered">
            <div class="column is-8">
              <p class="card-header-title has-text-tertiary is-size-2">
                Mes corrections postées
              </p>
              <hr class="has-background-tertiary" />
            </div>
          </div>

          <div class="card-content">
            <div class="columns is-multiline">
              <div class="column">
                <div
                  v-for="correc in postedCorrections"
                  :key="correc.id"
                  class="column is-12"
                >
                  <CorrectionPreview
                    :correc="correc"
                    :user="user"
                    :unlocked="
                      correc.id && user.posted_correcs.includes(correc.id)
                    "
                  >
                  </CorrectionPreview>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="selected === 2">
          <div class="columns is-centered">
            <div class="column is-8">
              <p class="card-header-title has-text-tertiary is-size-2">
                Mes corrections débloquées
              </p>
              <hr class="has-background-tertiary" />
            </div>
          </div>
          <div class="card-content">
            <div class="columns is-multiline">
              <div class="column">
                <div
                  v-for="correc in unlockedCorrections"
                  :key="correc.id"
                  class="column is-12"
                >
                  <CorrectionPreview
                    :correc="correc"
                    :user="user"
                    :unlocked="
                      correc.id && user.unlocked_correcs.includes(correc.id)
                    "
                  >
                  </CorrectionPreview>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import CorrectionPreview from '@/components/CorrectionPreview.vue'
export default {
  name: 'MyCorrections',
  components: {
    CorrectionPreview
  },
  data() {
    return {
      isActive: true,
      selected: 1
    }
  },
  computed: {
    ...mapState('corrections', ['postedCorrections', 'unlockedCorrections']),
    ...mapState('authentication', ['user'])
  },
  methods: {}
}
</script>

<style scoped>
hr {
  margin: 1em 0 !important;
}
</style>
