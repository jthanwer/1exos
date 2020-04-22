<template>
<section>
  <b-field expanded>
    <b-upload :value="value"
              @input="$emit('input', $event)"
              drag-drop>
      <section class="section">
        <div class="content has-text-centered">
          <p>
            <b-icon icon="upload"
                    size="is-large">
            </b-icon>
          </p>
          <p>
            <strong>Glissez votre fichier </strong> dans cette zone <br>
            ou <br>
            <strong>Cliquez dessus</strong> pour choisir le fichier à importer
          </p>
        </div>
      </section>
    </b-upload>
  </b-field>

  <div class="tags">
    <span class="tag is-medium is-primary"
          v-if="value">
      {{ value.name }} | {{ value.size }} octets
      <button class="delete is-small"
              type="button"
              @click="$emit('input', null)">
      </button>
    </span>
  </div>
</section>
</template>

<script>
export default {
  name: 'Upload',
  props: ['value'],
  data() {
    return {}
  },
  methods: {},
}
</script>

<style>
.upload,
.upload-draggable {
  width: 100%;
}
</style>
