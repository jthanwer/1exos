<template>
  <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">Exo n°{{ exo.id }}</p>
      <button type="button" class="delete" @click="$parent.close()" />
    </header>
    <section class="modal-card-body content">
      <div class="columns is-centered">
        <div v-if="exo" class="column is-8 has-text-centered">
          <b-button class="my-4" type="is-secondary" @click="redirect()">
            Accéder à la page de l'exo</b-button
          >
          <div v-if="exo.file">
            <div v-if="exo.filetype == 'pdf'">
              <div class="field is-grouped is-grouped-centered">
                <div class="control">
                  <b-button
                    type="is-tertiary"
                    icon-left="rotate-left"
                    @click="rotatePDF -= 90"
                  ></b-button>
                </div>
                <div class="field">
                  <div class="b-numberinput field has-addons ">
                    <p class="control">
                      <b-button
                        :disabled="page == 1"
                        type="is-primary"
                        icon-left="chevron-left"
                        @click="page -= 1"
                      />
                    </p>
                    <div class="control clear-fix">
                      <input
                        v-model.number="page"
                        class="input"
                        type="number"
                        placeholder="Text input"
                        min="1"
                        :max="numPages"
                      />
                    </div>
                    <p class="control">
                      <b-button
                        :disabled="page == numPages"
                        type="is-primary"
                        icon-left="chevron-right"
                        @click="page += 1"
                      />
                    </p>
                  </div>
                </div>
                <div class="control">
                  <b-button
                    type="is-tertiary"
                    icon-left="rotate-right"
                    @click="rotatePDF += 90"
                  ></b-button>
                </div>
              </div>

              <pdf
                ref="pdf"
                class="exo-container"
                :src="exo.file"
                :page="page"
                :rotate="rotatePDF"
                @num-pages="numPages = $event"
              ></pdf>
            </div>
            <div v-else>
              <ImageContainer v-model="exo.file" />
            </div>
          </div>
          <div v-else class="exo-info pa-9 has-text-centered">
            <div class="level">
              <div class="level-item has-text-centered">
                <div>
                  <p>
                    <span class="title is-size-4"
                      >N° {{ exo.num_exo }} Page {{ exo.num_page }}
                    </span>
                  </p>
                </div>
              </div>
            </div>
            <div class="level">
              <div class="level-item has-text-centered">
                <div>
                  <img
                    style="height: 400px;"
                    :src="
                      require('@/assets/images/livres/' + exo.livre + '.jpg')
                    "
                    alt="Image indisponible"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <footer class="modal-card-foot">
      <b-button @click="$parent.close()">
        Fermer
      </b-button>
    </footer>
  </div>
</template>

<script>
import pdf from 'vue-pdf'
import ImageContainer from '@/components/ImageContainer.vue'
import classes from '@/data/niveaux.json'
import exercicesService from '@/services/exercicesService'
export default {
  name: 'ModalExerciceComponent',
  components: {
    pdf,
    ImageContainer
  },
  props: {
    id: {
      type: [Number, String],
      default: null
    }
  },
  data() {
    return {
      classes: classes,
      exo: null,

      page: 1,
      numPages: 0,
      rotatePDF: 0,
      rotateImage: 0
    }
  },
  computed: {},
  created() {
    this.updateExo()
  },
  methods: {
    redirect() {
      this.$parent.close()
      this.$router.push({ name: 'exercice', params: { id: this.exo.id } })
    },
    updateExo() {
      exercicesService.getExercice(this.id).then(exo => {
        this.exo = exo
        if (exo.correcs.length > 0) {
          this.has_correc = true
        }
      })
    }
  }
}
</script>

<style scoped>
.download-buttons button {
  width: 250px;
}

.upload-button button {
  width: 250px;
}

.exo-container {
  border: 2px solid black;
}

.exo-info {
  border: 2px solid black;
  background-color: white;
}
</style>
