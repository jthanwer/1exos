<template>
<div class="container is-fluid">
  <div class="columns is-gapless"
       style="min-height: 800px;">
    <div class="column is-4 card">
      <div class="card-content">
        <b-menu>
          <b-menu-list label="Mes corrections">
            <b-menu-item icon="account"
                         :active="isActive"
                         @click="selected = 1"
                         label="Mes corrections postées">
            </b-menu-item>
            <b-menu-item icon="account"
                         @click="selected = 2"
                         label="Mes corrections débloquées">
            </b-menu-item>
          </b-menu-list>
        </b-menu>
      </div>
    </div>

    <div class="column is-8 card">
      <div v-if="selected === 1">
        <header class="card-header is-centered">
          <p class="card-header-title has-background-primary has-text-white is-size-3">
            Mes corrections postées
          </p>
        </header>
        <div class="card-content">
          <div class="columns is-multiline">
            <div class="column">
              <div v-for="(correc, index) in postedCorrections"
                   class="column is-12"
                   :key="correc.id">
                <CorrectionPreview :correc="correc"
                                   :user="user"
                                   :unlocked="correc.id && user.unlocked_correcs.includes(correc.id)">
                </CorrectionPreview>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="selected === 2">
        <header class="card-header is-centered">
          <p class="card-header-title has-background-primary has-text-white is-size-3">
            Mes corrections débloquées
          </p>
        </header>
        <div class="card-content">
          <div class="columns is-multiline">
            <div class="column">
              <div v-for="(correc, index) in unlockedCorrections"
                   class="column is-12"
                   :key="correc.id">
                <CorrectionPreview :correc="correc"
                                   :user="user"
                                   :unlocked="correc.id && user.unlocked_correcs.includes(correc.id)">
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
import { mapState } from "vuex";
import correctionsService from "@/services/correctionsService";
import CorrectionPreview from "@/components/CorrectionPreview.vue";
export default {
  name: "MyCorrections",
  components: {
    CorrectionPreview
  },
  data() {
    return {
      isActive: true,
      selected: 1,
    };
  },
  computed: {
    ...mapState("corrections", ["postedCorrections", "unlockedCorrections"]),
    ...mapState("authentication", ["user"])
  },
  methods: {}
};
</script>

<style>
</style>
