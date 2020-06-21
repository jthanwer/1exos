<template>
  <section>
    <b-field expanded>
      <b-upload
        :value="value"
        expanded
        @input="$emit('input', $event)"
        :type="type_upload"
        drag-drop
      >
        <section class="section">
          <div class="content has-text-centered">
            <p>
              <b-icon v-if="!value && !error" icon="upload" size="is-large">
              </b-icon>
              <b-icon
                v-else-if="value"
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
            <div v-if="!value">
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
              @close.prevent="value = null"
            >
              {{ value.name }}
            </b-tag>
          </div>
        </section>
      </b-upload>
    </b-field>
  </section>
</template>

<script>
export default {
  name: "Upload",
  props: {
    value: {
      type: File
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
    return {};
  },
  computed: {
    type_upload() {
      if (!this.value && this.error) {
        return "is-danger";
      } else if (this.value) {
        return "is-success";
      } else {
        return "is-primary";
      }
    }
  },
  methods: {}
};
</script>

<style>
.help-box {
  border: 1px dashed grey;
}
</style>
