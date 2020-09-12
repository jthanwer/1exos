<template>
  <section>
    <b-field expanded>
      <b-upload
        :value="file"
        expanded
        :type="type_upload"
        drag-drop
        @input="input($event)"
      >
        <section class="section">
          <div class="content has-text-centered">
            <p>
              <b-icon v-if="!file && !error" icon="upload" size="is-large">
              </b-icon>
              <b-icon
                v-else-if="file"
                icon="check"
                class="has-background-success"
                style="border-radius: 50%;"
                type="is-white"
                size="is-large"
              >
              </b-icon>
              <b-icon
                v-else
                icon="close"
                class="has-background-danger"
                style="border-radius: 50%;"
                type="is-white"
                size="is-large"
              >
              </b-icon>
            </p>
            <div v-if="!file">
              <p>
                <strong :class="{ 'has-text-danger': error }">
                  Glisse
                  <span v-if="exo">ton énoncé</span>
                  <span v-else>ta correction</span>
                  (.pdf, .jpg, .jpeg, .png)
                </strong>
                dans cette zone <br />
                ou <br />
                <strong :class="{ 'has-text-danger': error }"
                  >Clique dessus</strong
                >
                pour choisir le fichier à importer
              </p>

              <div class="has-text-grey is-size-6">
                <p>
                  <span class="has-text-weight-bold">Conditions </span>
                  <br />
                  <span v-if="exo">1 exo = 1 énoncé = 1 fichier </span>
                  <span v-else>1 correction = 1 fichier </span> <br />
                  <span>Bonne lisibilité </span> <br />
                  <span>Bon cadrage</span> <br />
                  <span>Dans le bon sens</span> <br />
                  <span>Taille maximale = 5 Mo</span> <br />
                </p>

                <p
                  v-if="exo"
                  class="is-size-6 has-text-danger has-text-weight-bold"
                >
                  En postant cet énoncé, tu t’engages à respecter les standards
                  de qualité de ce site (voir section “À propos”). <br />
                  Dans le cas contraire, ton exo sera supprimée.
                </p>
                <p
                  v-else
                  class="is-size-6 has-text-danger has-text-weight-bold"
                >
                  En postant cette correction, tu t’engages à respecter les
                  standards de qualité de ce site (voir section “À propos”).
                  <br />
                  Dans le cas contraire, ta correction sera supprimée.
                </p>
              </div>
            </div>

            <div v-else>
              <b-tag
                class="mb-5"
                type="is-primary"
                size="is-large"
                closable
                aria-close-label="Close tag"
                @close.prevent="file = null"
              >
                {{ file.name }}
              </b-tag>
              <div v-if="!exo" class="media has-text-warning">
                <div class="media-left">
                  <b-icon icon="alert" size="is-large"></b-icon>
                </div>
                <div class="media-content">
                  <p>
                    Attention, si ta correction est jugée mauvaise (3 points ou
                    moins) par le posteur de l'exo,
                    <strong class="has-text-warning"
                      >elle sera supprimée et tes points gagnés te seront
                      retirés.</strong
                    >
                  </p>
                </div>
              </div>

              <p></p>
            </div>
          </div>
        </section>
      </b-upload>
    </b-field>
  </section>
</template>

<script>
import extensions from '@/data/extensions.json'
export default {
  name: 'Upload',
  props: {
    value: {
      type: File,
      default: null
    },
    error: {
      type: Boolean,
      default: false
    },
    exo: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      file: this.value,
      extensions: this.extensions
    }
  },
  computed: {
    type_upload() {
      if (!this.file && this.error) {
        return 'is-danger'
      } else if (this.file) {
        return 'is-success'
      } else {
        return 'is-primary'
      }
    }
  },
  methods: {
    input(file) {
      let file_extension = file.name.split('.').pop()
      if (!extensions.includes(file_extension)) {
        this.$buefy.toast.open({
          duration: 5000,
          message: `Ce type de fichier n'est pas accepté.`,
          type: 'is-danger'
        })
        return
      }
      if (file.size > 5 * 1024 * 1024) {
        this.$buefy.toast.open({
          duration: 5000,
          message: `La taille du fichier doit être inférieure à 5 Mo.`,
          type: 'is-danger'
        })
        return
      }
      this.file = file
      this.$emit('input', file)
    }
  }
}
</script>

<style>
.help-box {
  border: 1px dashed grey;
}
</style>
