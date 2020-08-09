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
                  (.pdf, .jpg, .png)
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
                  <span>1 énoncé = 1 fichier </span> <br />
                  <span>Bonne lisibilité </span> <br />
                  <span>Bon cadrage</span> <br />
                  <span>Dans le bon sens</span> <br />
                  <span>Taille maximale = 5 Mo</span> <br />
                </p>

                <p class="is-size-7">
                  Si ces conditions ne sont pas remplies, ton exo ne sera
                  sûrement pas corrigé, voire sera supprimé.
                </p>
              </div>
            </div>

            <!-- <div class="has-text-grey is-size-7">
              <p>
                Si
                <span v-if="exo">
                  <strong :class="{'has-text-danger': error}">ton énoncé</strong>
                  est composé
                </span>
                <span v-else>
                  <strong :class="{'has-text-danger': error}">ta correction</strong>
                  est composée
                </span>
                de plusieurs fichiers, groupe-les d'abord
                <strong>sous un même pdf</strong>. <br>
                Nous n'acceptons que les fichiers uniques.
              </p>

              <p>
                Dans le cas d'une photo, elle doit être <strong>bien cadrée</strong>
                et le <strong>texte parfaitement lisible.</strong> <br>
                Sinon, ton exo risque de ne pas être corrigé. Merci !
              </p>
            </div>
          </div> -->

            <b-tag
              v-else
              class="mb-3"
              type="is-primary"
              size="is-large"
              closable
              aria-close-label="Close tag"
              @close.prevent="file = null"
            >
              {{ file.name }}
            </b-tag>
          </div>
        </section>
      </b-upload>
    </b-field>
  </section>
</template>

<script>
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
      file: this.value
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
      if (file.size > 5 * 1024 * 1024) {
        this.$buefy.toast.open({
          duration: 5000,
          message: `La taille du fichier doit être inférieure à 5 Mo`,
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
