<template>
<div class="container is-fluid">
  <b-loading is-full-page
             :active.sync="is_loading"></b-loading>
  <div class="columns is-centered">
    <div class="column is-10">
      <div class="box">
        <b-steps v-model="activeStep"
                 animated
                 has-navigation>
          <b-step-item id="firstStep"
                       label="Généralités"
                       :style="{ 'min-height': height }"
                       clickable>
            <hr />
            <h1 class="title has-text-centered">Généralités</h1>
            <hr />
            <div class="columns is-centered">
              <div class="column is-half">
                <ValidationObserver ref="firstStep">
                  <ValidationProvider rules="required"
                                      v-slot="{ errors, valid }">
                    <b-field label="Chapitre"
                             :message="errors"
                             :type="{ 'is-danger': errors[0], 'is-success': valid }">
                      <b-select v-if="user"
                                expanded
                                v-model="form.chapitre"
                                placeholder="Choisir un chapitre">
                        <option v-for="option in chapitres[user.classe]">
                          {{ option }}
                        </option>
                      </b-select>
                    </b-field>
                  </ValidationProvider>
                  <ValidationProvider rules="required"
                                      v-slot="{ errors, valid }">
                    <b-field label="Provenance"
                             :message="errors"
                             :type="{ 'is-danger': errors[0], 'is-success': valid }">
                      <b-select v-model="form.is_from_livre"
                                expanded
                                placeholder="Choisir la provenance">
                        <option :value="false"> Sur feuille</option>
                        <option :value="true">
                          Livre scolaire</option>
                      </b-select>
                    </b-field>
                  </ValidationProvider>
                  <ValidationProvider rules="required"
                                      v-slot="{ errors, valid }">
                    <b-field label="Type d'exo"
                             :message="errors"
                             :type="{ 'is-danger': errors[0], 'is-success': valid }">
                      <b-select v-model="form.type"
                                expanded
                                placeholder="Choisir un type d'exo">
                        <option> Exo </option>
                        <option> Activité </option>
                      </b-select>
                    </b-field>
                  </ValidationProvider>
                </ValidationObserver>
              </div>
            </div>

          </b-step-item>

          <b-step-item id="secondStep"
                       label="Points et Délai"
                       :style="{ 'min-height': height }">
            <hr />
            <h1 class="title has-text-centered">Points et Délai</h1>
            <hr />
            <div class="notification is-info is-light">
              <div class="media">
                <div class="media-left">
                  <b-icon icon="information"></b-icon>
                </div>
                <div v-if="user && constants && constants['MEAN_PRICES'][user.classe] > 0"
                     class="media-content">
                  Les exos de niveau {{classes[user.classe]}} se corrigent
                  actuellement pour {{constants['MEAN_PRICES'][user.classe]}} points.
                </div>
                <div v-else
                     class="media-content">
                  Aucun exercice de ce niveau n'est en ligne pour le moment.
                  Calcul de la moyenne impossible.
                </div>
              </div>
            </div>
            <div v-if="user"
                 class="columns is-centered">
              <div class="column is-half">
                <ValidationObserver ref="secondStep">
                  <ValidationProvider :rules="{
                      required: true,
                      min_value: 1,
                      max_cagnotte_value: user.tirelire,
                      integer: true
                    }"
                                      v-slot="{ errors, valid }">
                    <b-field :message="errors"
                             :type="{ 'is-danger': errors[0], 'is-success': valid }">
                      <template slot="label">
                        Points
                        <b-tooltip type="is-dark"
                                   label="Quel est le nombre de points que tu es prêt à céder pour obtenir la correction de ton exo ?"
                                   multilined>
                          <b-icon size="is-small"
                                  icon="help-circle-outline"></b-icon>
                        </b-tooltip>
                      </template>
                      <b-numberinput v-model="form.prix"
                                     :min="1"
                                     :max="user.tirelire"
                                     placeholder="Choisir un nombre de points">
                      </b-numberinput>
                    </b-field>
                  </ValidationProvider>

                  <ValidationProvider rules="required"
                                      v-slot="{ errors, valid }">
                    <b-field :message="errors"
                             :type="{ 'is-danger': errors[0], 'is-success': valid }">
                      <template slot="label">
                        À faire pour...
                        <b-tooltip type="is-dark"
                                   label="Quelle est la date avant laquelle tu aimerais préférentiellement obtenir ta correction ?"
                                   multilined>
                          <b-icon size="is-small"
                                  icon="help-circle-outline"></b-icon>
                        </b-tooltip>
                      </template>
                      <b-datetimepicker v-model="form.date_limite"
                                        placeholder="Choisir une date limite"
                                        :min-datetime="minDatetime"
                                        icon="calendar-today"
                                        horizontal-time-picker>
                      </b-datetimepicker>
                    </b-field>
                  </ValidationProvider>
                </ValidationObserver>
              </div>
            </div>
          </b-step-item>

          <b-step-item id="thirdStep1"
                       v-if="!form.is_from_livre"
                       :style="{ 'min-height': height }"
                       label="Énoncé">
            <hr />
            <h1 class="title has-text-centered">Énoncé</h1>
            <hr />
            <div class="notification is-warning is-light">
              <div class="media">
                <div class="media-left">
                  <b-icon icon="alert"></b-icon>
                </div>
                <div class="media-content">
                  Pour des raisons relatives au droit d’auteur, il est interdit d’uploader un énoncé provenant d’un livre.
                </div>
              </div>
            </div>
            <ValidationObserver ref="thirdStep">
              <ValidationProvider rules="required"
                                  v-slot="{ errors }">
                <Upload v-model="drop_file"
                        :error="errors[0]" />
              </ValidationProvider>
            </ValidationObserver>
          </b-step-item>

          <b-step-item id="thirdStep2"
                       v-else
                       :style="{ 'min-height': height }"
                       label="Livre">
            <hr />
            <h1 class="title has-text-centered">Livre</h1>
            <hr />
            <div class="columns">
              <div class="column is-half">
                <ValidationObserver ref="thirdStep">
                  <ValidationProvider rules="required"
                                      v-slot="{ errors, valid }">
                    <b-field label="Livre"
                             expand
                             :message="errors"
                             :type="{'is-danger': errors[0],'is-success': valid}">
                      <b-select v-model="form.livre.name"
                                expanded
                                placeholder="Choisir un livre">
                        <option v-for="livre in livres[6]"
                                :value="livre.name">
                          {{ livre.name.split("_").slice(1).join(" - ") }}
                        </option>
                      </b-select>
                    </b-field>
                  </ValidationProvider>
                  <ValidationProvider rules="required"
                                      v-slot="{ errors, valid }">
                    <b-field label="Numéro"
                             :message="errors"
                             :type="{'is-danger': errors[0], 'is-success': valid}">
                      <b-numberinput v-model="form.livre.num_exo"
                                     expanded
                                     :min="1"
                                     placeholder="Choisir un numéro d'exercice"></b-numberinput>
                    </b-field>
                  </ValidationProvider>
                  <ValidationProvider rules="required"
                                      v-slot="{ errors, valid }">
                    <b-field label="Page"
                             :message="errors"
                             :type="{'is-danger': errors[0],'is-success': valid}">
                      <b-numberinput v-model="form.livre.num_page"
                                     expanded
                                     :min="1"
                                     placeholder="Choisir un numéro de page"></b-numberinput>
                    </b-field>
                  </ValidationProvider>
                </ValidationObserver>
              </div>

              <div class="column is-half has-text-centered">
                <img v-if="form.livre.name"
                     style="height: 300px;"
                     :src="require('@/assets/images/livres/' + form.livre.name + '.jpg')"
                     alt="Image indisponible" />
              </div>
            </div>
          </b-step-item>

          <b-step-item label="Récapitulatif"
                       :style="{ 'min-height': height }">
            <hr />
            <h1 class="title has-text-centered">Récapitulatif</h1>
            <hr />
            <div class="notification is-info is-light">
              <div class="media">
                <div class="media-left">
                  <b-icon icon="information"></b-icon>
                </div>
                <div class="media-content">
                  Voici comment ton exo apparaîtra.
                </div>
              </div>
            </div>
            <ExercicePreview :exo="exo"
                             :activated="false"></ExercicePreview>
          </b-step-item>

          <template slot="navigation"
                    slot-scope="{ previous, next }">
            <div class="is-flex"
                 style="align-items: center; justify-content: center;">
              <b-button type="is-danger"
                        class="mr-3"
                        outlined
                        :disabled="previous.disabled"
                        @click.prevent="previous.action">
                Revenir en arrière
              </b-button>
              <b-button v-if="activeStep < 3"
                        type="is-info"
                        :disabled="next.disabled"
                        @click.prevent="goNext(next, activeStep)">
                Continuer
              </b-button>
              <b-button v-else
                        type="is-success"
                        size="is-large"
                        @click.prevent="submit()">
                Demander la correction
              </b-button>
            </div>
          </template>
        </b-steps>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import { ValidationObserver, ValidationProvider } from "vee-validate";
import { mapState } from "vuex";
import moment from "moment";
import chapitres from "@/data/chapitres.json";
import classes from "@/data/classes.json";
import livres from "@/data/livres.json";
import Upload from "@/components/Upload.vue";
import ExercicePreview from "@/components/ExercicePreview.vue";
export default {
  name: "PostExo",
  components: {
    Upload,
    ExercicePreview,
    ValidationObserver,
    ValidationProvider
  },
  data() {
    const min = new Date(moment().toISOString(true));
    return {
      chapitres: chapitres,
      classes: classes,
      livres: livres,
      height: "400px",
      minDatetime: min,

      is_loading: false,

      activeStep: 0,
      drop_file: null,
      form: {
        chapitre: null,
        type: null,
        is_from_livre: null,
        livre: {
          name: null,
          num_page: null,
          num_exo: null
        },
        date_limite: null,
        prix: null
      }
    };
  },
  computed: {
    ...mapState("authentication", ["user"]),
    ...mapState("general", ["constants"]),
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
        prix: this.form.prix,
        date_limite: moment(this.form.date_limite).toISOString(true),
        date_created: moment(),
        correcs: []
      };
    }
  },
  methods: {
    submit() {
      this.is_loading = true;
      const fd = new FormData();
      fd.append("chapitre", this.form.chapitre);
      fd.append("type", this.form.type);
      fd.append("prix", parseInt(this.form.prix));
      fd.append("date_limite", moment(this.form.date_limite).toISOString(true));
      if (this.form.is_from_livre) {
        fd.append("livre", this.form.livre.name);
        fd.append("num_page", parseInt(this.form.livre.num_page));
        fd.append("num_exo", parseInt(this.form.livre.num_exo));
      } else {
        fd.append("file", this.drop_file);
      }
      this.$store.dispatch("exercices/postExercice", fd)
        .then(data => {
          this.is_loading = false;
          this.$router.push({ name: "exercice", params: { id: data.id } });
        })
        .catch(err => {
          this.is_loading = false;
          this.$buefy.toast.open({
            duration: 5000,
            message: `L'exo n'a pas pu être posté.
            Il manque sûrement des informations essentielles.`,
            type: "is-danger"
          });
        });
    },
    goNext(next, activeStep) {
      switch (activeStep) {
        case 0:
          var ref = this.$refs.firstStep;
          break;
        case 1:
          var ref = this.$refs.secondStep;
          break;
        case 2:
          var ref = this.$refs.thirdStep;
          break;
        default:
          var ref = this.$refs.firstStep;
      }
      ref.validate().then(success => {
        if (success) {
          next.action();
        }
      });
    }
  }
};
</script>

<style>
span .field {
  margin-bottom: 0.75rem;
}
</style>
