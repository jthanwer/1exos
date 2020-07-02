<template>
<div class="container is-fluid">
  <div class="columns is-gapless"
       style="min-height: 800px;">
    <div class="column is-4 card">
      <div class="card-content">
        <b-menu>
          <b-menu-list label="Mes exercices">
            <b-menu-item icon="account"
                         :active="isActive"
                         @click="selected = 1"
                         label="Mes exercices postés">
            </b-menu-item>
            <b-menu-item icon="account"
                         @click="selected = 2"
                         label="Mes exercices favoris">
            </b-menu-item>
          </b-menu-list>
        </b-menu>
      </div>
    </div>

    <div class="column is-8 card">
      <div v-if="selected === 1">
        <header class="card-header is-centered">
          <p class="card-header-title has-background-primary has-text-white is-size-3">
            Mes exercices postés
          </p>
        </header>
        <div class="card-content">
          <div class="columns is-multiline">
            <div class="column">
              <div v-for="(exo, index) in postedExercices"
                   class="column is-12"
                   :key="exo.id">
                <ExercicePreview :exo="exo"
                                 :liked="likedExercices.some(ex => ex.id === exo.id )">
                </ExercicePreview>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="selected === 2">
        <header class="card-header is-centered">
          <p class="card-header-title has-background-primary has-text-white is-size-3">
            Mes exercices favoris
          </p>
        </header>
        <div class="card-content">
          <div class="columns is-multiline">
            <div class="column">
              <div v-for="(exo, index) in likedExercices"
                   class="column is-12"
                   :key="exo.id">
                <ExercicePreview :exo="exo"
                                 :activated="true"
                                 :liked="likedExercices.some(ex => ex.id === exo.id )">
                </ExercicePreview>
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
import exercicesService from "@/services/exercicesService";
import ExercicePreview from "@/components/ExercicePreview.vue";
export default {
  name: "postedExercices",
  components: {
    ExercicePreview
  },
  data() {
    return {
      isActive: true,
      selected: 1
    };
  },
  computed: {
    ...mapState("exercices", ["postedExercices", "likedExercices"]),
  },
  methods: {}
};
</script>

<style>
</style>
