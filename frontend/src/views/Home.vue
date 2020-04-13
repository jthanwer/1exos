<template>
<div class="container is-fluid">
  <div class="mt-5">
    <div class="columns">
      <div class="column is-6">
        <section>
          <b-field expanded>
            <b-upload v-model="drop_file"
                      drag-drop>
              <section class="section">
                <div class="content has-text-centered">
                  <p>
                    <b-icon icon="upload"
                            size="is-large">
                    </b-icon>
                  </p>
                  <p>
                    <strong>Glissez vos fichiers</strong> dans cette zone <br>
                    ou <br>
                    <strong>Cliquez dessus</strong> pour choisir les fichiers à importer
                  </p>
                </div>
              </section>
            </b-upload>
          </b-field>

          <div class="tags">
            <span class="tag is-medium is-primary"
                  v-if="drop_file">
              {{ drop_file.name }} | {{ drop_file.size }} octets
              <button class="delete is-small"
                      type="button"
                      @click="drop_file = null">
              </button>
            </span>
          </div>

          <b-button type="is-success"
                    :disabled="!drop_file"
                    expanded
                    @click="uploadFile()">
            Importer le fichier
          </b-button>
        </section>
      </div>

      <div class="column is-6">
        <div v-for="(file, index) in rowData"
             class="column is-10"
             :key="file.id">
          <b-collapse class="card"
                      aria-id="contentId">
            <div slot="trigger"
                 slot-scope="props"
                 class="card-header"
                 role="button"
                 aria-controls="contentId">

              <div class="card-header-title is-size-5">
                <span>{{file.name}}</span>
              </div>

              <a class="card-header-icon">
                <b-button icon-left="delete"
                          type="is-light"
                          size="is-medium"
                          @click.native.stop="deleteFile(file.file_id, index)" />
              </a>

              <a class="card-header-icon">
                <b-button icon-left="download"
                          type="is-light"
                          size="is-medium"
                          @click.native.stop="downloadFile(file)" />
              </a>
            </div>

          </b-collapse>
        </div>

      </div>
    </div>
  </div>
</div>
</template>

<script>
import { mapState } from 'vuex';
export default {
  data() {
    return {
      drop_file: null
    }
  },
  mounted() {
    this.$store.dispatch('files/loadFiles')
  },
  computed: {
    ...mapState('files', ['rowData'])
  },
  methods: {
    uploadFile() {
      if (this.drop_file) {
        if (this.drop_file.size < 5 * 1024 * 1024) {
          const fd = new FormData()
          fd.append('file', this.drop_file)
          this.$store.dispatch('files/postFile', fd)
            .then(() => {
              alert("Le fichier a été importé")
              this.drop_file = null
            })
            .catch(err => alert("Problème d'importation"))
        } else {
          alert("La taille du fichier ne doit pas excéder 5MB")
        }
      } else {
        alert("Aucun fichier sélectionné")
      }
    },
    deleteFile(file_id, data_index) {
      this.$store.dispatch('files/deleteFile', file_id, data_index)
    },
    downloadFile(file) {
      this.$store.dispatch('files/downloadFile', file)
    }
  },
}
</script>

<style>
.upload,
.upload-draggable {
  width: 100%;
}
</style>
