<template>
  <div class="container is-fluid">
    <div class="columns" style="min-height: 800px;">
      <div class="column is-3 card">
        <div class="card-content">
          <b-menu>
            <b-menu-list label="Mes exercices">
              <b-menu-item
                icon="account"
                :active="isActive"
                label="Mes exercices postés"
                @click="selected = 1"
              >
              </b-menu-item>
              <b-menu-item
                icon="account"
                label="Mes exercices favoris"
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
                Mes exercices postés
              </p>
              <hr class="has-background-tertiary" />
            </div>
          </div>
          <div class="card-content">
            <div class="columns is-multiline">
              <div class="column">
                <div
                  v-for="exo in displayedPostedExercices"
                  :key="exo.id"
                  class="column is-12"
                >
                  <ExercicePreview
                    :exo="exo"
                    :liked="likedExercices.some(ex => ex.id === exo.id)"
                  >
                  </ExercicePreview>
                </div>
              </div>
            </div>
            <div class="column is-12">
              <b-pagination
                :total="postedExercices.length"
                :current.sync="current_page_posted"
                range-before="1"
                range-after="1"
                order="is-right"
                size="is-medium"
                :per-page="elements_per_page"
                icon-prev="chevron-left"
                icon-next="chevron-right"
                aria-next-label="Next page"
                aria-previous-label="Previous page"
                aria-page-label="Page"
                aria-current-label="Current page"
              ></b-pagination>
            </div>
          </div>
        </div>
        <div v-if="selected === 2">
          <div class="columns is-centered">
            <div class="column is-8">
              <p class="card-header-title has-text-tertiary is-size-2">
                Mes exercices favoris
              </p>
              <hr class="has-background-tertiary" />
            </div>
          </div>
          <div class="card-content">
            <div class="columns is-multiline">
              <div class="column">
                <div
                  v-for="exo in displayedLikedExercices"
                  :key="exo.id"
                  class="column is-12"
                >
                  <ExercicePreview
                    :exo="exo"
                    :activated="true"
                    :liked="likedExercices.some(ex => ex.id === exo.id)"
                  >
                  </ExercicePreview>
                </div>
              </div>
            </div>
            <div class="column is-12">
              <b-pagination
                :total="likedExercices.length"
                :current.sync="current_page_liked"
                range-before="1"
                range-after="1"
                order="is-right"
                size="is-medium"
                :per-page="elements_per_page"
                icon-prev="chevron-left"
                icon-next="chevron-right"
                aria-next-label="Next page"
                aria-previous-label="Previous page"
                aria-page-label="Page"
                aria-current-label="Current page"
              ></b-pagination>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import ExercicePreview from '@/components/ExercicePreview.vue'
export default {
  name: 'PostedExercices',
  components: {
    ExercicePreview
  },
  data() {
    return {
      isActive: true,
      selected: 1,

      elements_per_page: 10,
      current_page_posted: 1,
      current_page_liked: 1
    }
  },
  computed: {
    ...mapState('exercices', ['postedExercices', 'likedExercices']),
    displayedPostedExercices() {
      return this.postedExercices.slice(
        (this.current_page_posted - 1) * this.elements_per_page,
        this.current_page_posted * this.elements_per_page
      )
    },
    displayedLikedExercices() {
      return this.likedExercices.slice(
        (this.current_page_liked - 1) * this.elements_per_page,
        this.current_page_liked * this.elements_per_page
      )
    }
  },
  methods: {}
}
</script>

<style scoped>
hr {
  margin: 1em 0 !important;
}
</style>
