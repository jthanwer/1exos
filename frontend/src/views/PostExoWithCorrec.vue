<template>
  <section class="section">
    <div class="container">
      <b-loading is-full-page :active.sync="is_loading"></b-loading>
      <div class="columns is-centered">
        <div class="column is-10">
          <div class="box">
            <b-steps v-model="activeStep" animated has-navigation>
              <b-step-item
                id="firstStep"
                label="Infos"
                :style="{ 'min-height': height }"
                clickable
              >
                <hr />
                <h1 class="title has-text-centered">Généralités</h1>
                <hr />
                <div class="columns is-centered">
                  <div class="column is-half">
                    <ValidationObserver ref="firstStep">
                      <ValidationProvider
                        v-slot="{ errors, valid }"
                        slim
                        rules="required"
                      >
                        <b-field
                          label="Chapitre"
                          :message="errors"
                          :type="{
                            'is-danger': errors[0],
                            'is-success': valid
                          }"
                        >
                          <b-select
                            v-if="user"
                            v-model="form.chapitre"
                            expanded
                            placeholder="Choisir un chapitre"
                          >
                            <option
                              v-for="(option, index) in chapitres[user.niveau]"
                              :key="index"
                            >
                              {{ option }}
                            </option>
                          </b-select>
                        </b-field>
                      </ValidationProvider>
                      <ValidationProvider
                        v-slot="{ errors, valid }"
                        slim
                        rules="required"
                      >
                        <b-field
                          label="Provenance"
                          :message="errors"
                          :type="{
                            'is-danger': errors[0],
                            'is-success': valid
                          }"
                        >
                          <b-select
                            v-model="form.is_from_livre"
                            expanded
                            placeholder="Choisir la provenance"
                          >
                            <option :value="false"> Sur feuille</option>
                            <option :value="true"> Livre scolaire</option>
                          </b-select>
                        </b-field>
                      </ValidationProvider>
                      <ValidationProvider
                        v-slot="{ errors, valid }"
                        slim
                        rules="required"
                      >
                        <b-field
                          label="Type d'exo"
                          :message="errors"
                          :type="{
                            'is-danger': errors[0],
                            'is-success': valid
                          }"
                        >
                          <b-select
                            v-model="form.type"
                            expanded
                            placeholder="Choisir un type d'exo"
                          >
                            <option> Exo </option>
                            <option> Activité </option>
                          </b-select>
                        </b-field>
                      </ValidationProvider>
                    </ValidationObserver>
                  </div>
                </div>
              </b-step-item>

              <b-step-item
                v-if="!form.is_from_livre"
                id="secondStep1"
                :style="{ 'min-height': height }"
                label="Énoncé"
                clickable
              >
                <ValidationObserver ref="secondStep">
                  <hr />
                  <h1 class="title has-text-centered">Énoncé</h1>
                  <hr />
                  <div class="notification is-warning is-light">
                    <div class="media">
                      <div class="media-left">
                        <b-icon icon="alert"></b-icon>
                      </div>
                      <div class="media-content">
                        Pour des raisons relatives au droit d’auteur, il est
                        interdit d’uploader un énoncé provenant d’un livre.
                      </div>
                    </div>
                  </div>
                  <ValidationProvider v-slot="{ errors }" slim rules="required">
                    <Upload v-model="drop_file_exo" :error="errors[0]" />
                  </ValidationProvider>
                </ValidationObserver>
              </b-step-item>

              <b-step-item
                v-else
                id="secondStep2"
                :style="{ 'min-height': height }"
                label="Livre"
                clickable
              >
                <hr />
                <h1 class="title has-text-centered">Livre</h1>
                <hr />
                <div class="columns">
                  <div class="column is-6">
                    <ValidationObserver ref="secondStep">
                      <ValidationProvider
                        v-slot="{ errors, valid }"
                        slim
                        rules="required"
                      >
                        <b-field
                          label="Livre"
                          :message="errors"
                          :type="{
                            'is-danger': errors[0],
                            'is-success': valid
                          }"
                        >
                          <b-select
                            v-model="form.livre.name"
                            expanded
                            placeholder="Choisir un livre"
                          >
                            <option
                              v-for="(livre, index) in livres[user.niveau]"
                              :key="index"
                              :value="livre.name"
                            >
                              {{ livre.name.split('_').join(' - ') }}
                            </option>
                          </b-select>
                        </b-field>
                      </ValidationProvider>
                      <ValidationProvider
                        v-slot="{ errors, valid }"
                        slim
                        rules="required"
                      >
                        <b-field
                          label="Numéro"
                          :message="errors"
                          :type="{
                            'is-danger': errors[0],
                            'is-success': valid
                          }"
                        >
                          <b-numberinput
                            v-model="form.livre.num_exo"
                            expanded
                            :min="1"
                            placeholder="Choisir un numéro d'exercice"
                          ></b-numberinput>
                        </b-field>
                      </ValidationProvider>
                      <ValidationProvider
                        v-slot="{ errors, valid }"
                        slim
                        rules="required"
                      >
                        <b-field
                          label="Page"
                          :message="errors"
                          :type="{
                            'is-danger': errors[0],
                            'is-success': valid
                          }"
                        >
                          <b-numberinput
                            v-model="form.livre.num_page"
                            expanded
                            :min="1"
                            placeholder="Choisir un numéro de page"
                          ></b-numberinput>
                        </b-field>
                      </ValidationProvider>
                    </ValidationObserver>
                  </div>
                  <div class="column is-half has-text-centered">
                    <img
                      v-if="form.livre.name"
                      style="height: 400px;"
                      :src="
                        require('@/assets/images/livres/' +
                          form.livre.name +
                          '.jpg')
                      "
                      alt="Image indisponible"
                    />
                  </div>
                </div>
              </b-step-item>

              <b-step-item
                id="thirdStep"
                :style="{ 'min-height': height }"
                label="Correction"
                clickable
              >
                <ValidationObserver ref="thirdStep">
                  <hr />
                  <h1 class="title has-text-centered">Correction</h1>
                  <hr />
                  <ValidationProvider v-slot="{ errors }" slim rules="required">
                    <div class="notification is-warning is-light">
                      <div class="media">
                        <div class="media-left">
                          <b-icon icon="alert"></b-icon>
                        </div>
                        <div class="media-content">
                          Pour des raisons relatives au droit d’auteur, il est
                          interdit d’uploader une correction provenant d’un
                          livre.
                        </div>
                      </div>
                    </div>
                    <Upload
                      v-model="drop_file_correc"
                      :exo="false"
                      :error="errors[0]"
                    />
                  </ValidationProvider>
                </ValidationObserver>
              </b-step-item>

              <b-step-item
                label="Récapitulatif"
                :style="{ 'min-height': height }"
              >
                <hr />
                <h1 class="title has-text-centered">Récapitulatif</h1>
                <hr class="mb-10" />
                <div class="notification is-tertiary is-light">
                  <div class="media">
                    <div class="media-left">
                      <b-icon icon="information"></b-icon>
                    </div>
                    <div class="media-content">
                      Voici comment ton exo apparaîtra. <br />
                      En postant cet exo et sa correction,
                      <strong
                        >tu gagneras
                        {{ constants['SELFCORREC_POINTS'] }} points</strong
                      >.
                    </div>
                  </div>
                </div>
                <ExercicePreview :exo="exo" :activated="false" />
              </b-step-item>
              <template slot="navigation" slot-scope="{ previous, next }">
                <div
                  class="is-flex"
                  style="align-items: center; justify-content: center;"
                >
                  <b-button
                    type="is-danger"
                    class="mr-3"
                    outlined
                    :disabled="previous.disabled"
                    @click.prevent="previous.action"
                  >
                    Revenir en arrière
                  </b-button>
                  <b-button
                    v-if="activeStep < 3"
                    type="is-tertiary"
                    :disabled="next.disabled"
                    @click.prevent="goNext(next, activeStep)"
                  >
                    Continuer
                  </b-button>
                  <b-button
                    v-else
                    type="is-success"
                    size="is-large"
                    @click.prevent="postExo()"
                  >
                    Poster cet exo
                  </b-button>
                </div>
              </template>
            </b-steps>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { ValidationObserver, ValidationProvider } from 'vee-validate'
import { mapState } from 'vuex'
import moment from 'moment'
import chapitres from '@/data/chapitres.json'
import classes from '@/data/niveaux.json'
import livres from '@/data/livres.json'
import Upload from '@/components/Upload.vue'
import ExercicePreview from '@/components/ExercicePreview.vue'
export default {
  name: 'PostExoWithCorrec',
  components: {
    Upload,
    ExercicePreview,
    ValidationObserver,
    ValidationProvider
  },
  data() {
    const min = new Date(moment().toISOString(true))
    return {
      chapitres: chapitres,
      classes: classes,
      livres: livres,
      height: '400px',
      minDatetime: min,

      is_loading: false,

      activeStep: 0,
      drop_file_exo: null,
      drop_file_correc: null,
      form: {
        chapitre: null,
        type: null,
        is_from_livre: null,
        livre: {
          name: null,
          num_page: null,
          num_exo: null
        }
      }
    }
  },
  computed: {
    ...mapState('authentication', ['user']),
    ...mapState('general', ['constants']),
    exo() {
      return {
        id: 1,
        posteur: this.user,
        chapitre: this.form.chapitre,
        type: this.form.type,
        file: this.drop_file,
        livre: this.form.livre.name,
        num_page: this.form.livre.num_page,
        num_exo: this.form.livre.num_exo,
        date_created: moment(),
        corrections: [1]
      }
    }
  },
  methods: {
    postExo() {
      this.is_loading = true
      const fd = new FormData()
      fd.append('classe', parseInt(this.form.classe))
      fd.append('chapitre', this.form.chapitre)
      fd.append('type', this.form.type)
      if (this.form.is_from_livre) {
        fd.append('livre', this.form.livre.name)
        fd.append('num_page', parseInt(this.form.livre.num_page))
        fd.append('num_exo', parseInt(this.form.livre.num_exo))
      } else {
        fd.append('file', this.drop_file_exo)
      }
      this.$store
        .dispatch('exercices/postExercice', fd)
        .then(data => {
          return this.postCorrection(data.id)
        })
        .then(data => {
          this.is_loading = false
          this.$store.dispatch('authentication/getProfileUser')
          this.$router.push({
            name: 'exercice',
            params: { id: data.enonce.id }
          })
        })
        .catch(() => {
          this.is_loading = false
          this.$buefy.toast.open({
            duration: 5000,
            message: `L'exo et sa correction n'ont pas pu être postés.
            Il manque sûrement des informations essentielles.`,
            type: 'is-danger'
          })
        })
    },
    postCorrection(id) {
      const fd = new FormData()
      fd.append('enonce_id', id)
      fd.append('file', this.drop_file_correc)
      return this.$store.dispatch('corrections/postCorrection', fd)
    },
    goNext(next, activeStep) {
      switch (activeStep) {
        case 0:
          var ref = this.$refs.firstStep
          break
        case 1:
          ref = this.$refs.secondStep
          break
        case 2:
          ref = this.$refs.thirdStep
          break
        default:
          ref = this.$refs.firstStep
      }
      ref.validate().then(success => {
        if (success) {
          next.action()
        }
      })
    }
  }
}
</script>

<style></style>
