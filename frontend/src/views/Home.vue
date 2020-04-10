<template>
<div class="container">
  <section class="mt-3">
    <b-field>
      <b-upload v-model="dropFile"
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
            v-if="dropFile">
        {{ dropFile.name }}
      </span>
    </div>


  </section>
</div>
</template>

<script>
export default {
  data() {
    return {
      dropFiles: [],
      dropFile: null
    }
  },
  methods: {
    deleteDropFile(index) {
      console.log(this.dropFiles)
      this.dropFiles.splice(index, 1)
    }
  }
}
</script>
