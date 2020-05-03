<template>
<section>
  <b-field expanded>
    <b-upload :value="value"
              @input="$emit('input', $event)"
              drag-drop>
      <section class="section">
        <div class="content has-text-centered">
          <p>
            <b-icon v-if="!value"
                    icon="upload"
                    size="is-large">
            </b-icon>
            <b-icon v-else
                    icon="check"
                    class="has-background-success"
                    style="border-radius: 50%;"
                    type="is-white"
                    size="is-large">
            </b-icon>
          </p>
          <div v-if="!value">
            <p>
              <strong>Glisse ton fichier (.pdf, .jpg, .png) </strong> dans cette zone <br>
              ou <br>
              <strong>Clique dessus</strong> pour choisir le fichier à importer
            </p>

            <p>
              Si ton énoncé ou ta correction est composé de plusieurs fichiers, groupe-les d'abord
              <strong>sous un même pdf</strong>. <br>
              Nous n'acceptons que les fichiers uniques.
            </p>

            <p>
              Dans le cas d'une photo, elle doit être <strong>bien cadrée</strong>
              et le <strong>texte parfaitement lisible.</strong> <br>
              Sinon, ton exo risque de ne pas être corrigé. Merci !
            </p>
          </div>

          <b-tag v-else
                 class="mb-3"
                 type="is-primary"
                 size="is-large"
                 closable
                 aria-close-label="Close tag"
                 @close.prevent="value = null">
            {{value.name}}
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
