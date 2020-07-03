<template>
<div>
  <b-loading is-full-page
             :active.sync="is_loading"></b-loading>
  <div class="columns">
    <div class="column is-3">
      <b-sidebar position="static"
                 mobile="fullwidth"
                 fullheight
                 fullwidth
                 type="is-light"
                 open>
        <div class="p-2">
          <div class="mb-5">
            <b-button type="is-primary"
                      size="is-large"
                      icon-left="magnify"
                      expanded
                      @click="searchExercices()">
              Filtrer
            </b-button>
          </div>
          <b-menu class="is-custom-mobile">

            <b-field class="mb-3">
              <b-switch type="is-success"
                        size="is-large"
                        passive-type="is-danger"
                        v-model="form.is_corrected">
                {{form.is_corrected ? "AVEC correction" : "SANS correction"}}
              </b-switch>
            </b-field>
            <b-field class="mb-3">
              <b-switch type="is-primary"
                        size="is-large"
                        passive-type="is-secondary"
                        v-model="form.is_from_livre">
                {{form.is_from_livre ? "Sur livre" : "Sur feuille"}}
              </b-switch>
            </b-field>
            <b-menu-list label="Général">
              <b-field>
                <b-checkbox type="is-secondary"
                            v-model="filter.niveau">
                  Niveau
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.niveau">
                <b-select v-model="form.niveau"
                          placeholder="Choisir un niveau">
                  <option v-for="(classe, index) in classes"
                          :value="index">{{
                      classe
                    }}</option>
                </b-select>
              </b-field>

              <b-field>
                <b-checkbox type="is-secondary"
                            v-model="filter.type">
                  Type
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.type">
                <b-select v-model="form.type"
                          placeholder="Choisir un type d'exo">
                  <option> Exo </option>
                  <option> Activité </option>
                </b-select>
              </b-field>

              <b-field>
                <b-checkbox type="is-secondary"
                            v-model="filter.chapitre">
                  Chapitre
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.chapitre">
                <b-select v-if="form.niveau && filter.niveau"
                          v-model="form.chapitre"
                          placeholder="Choisis un chapitre">
                  <option v-for="option in chapitres[form.niveau]">
                    {{ option }}
                  </option>
                </b-select>
                <p class="has-text-danger"
                   v-else>Vous devez d'abord renseigner un niveau.</p>
              </b-field>
            </b-menu-list>

            <b-menu-list v-if="form.is_from_livre"
                         label="Livre scolaire">
              <b-field>
                <b-checkbox type="is-secondary"
                            v-model="filter.livre">
                  Éditeur
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.livre">
                <b-select v-model="form.livre"
                          placeholder="Choisir un livre">
                  <option v-for="livre in livres[6]"
                          :value="livre.name">
                    {{ livre.name.split("_").slice(1).join(" - ") }}
                  </option>
                </b-select>
              </b-field>
              <div class="has-text-centered">
                <img v-if="filter.livre && form.livre"
                     class="mb-3"
                     style="height: 150px;"
                     :src="require('@/assets/images/livres/' + form.livre + '.jpg')"
                     alt="Image indisponible" />
              </div>
              <b-field>
                <b-checkbox type="is-secondary"
                            v-model="filter.num_exo">
                  Numéro d'exercice
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.num_exo">
                <b-numberinput v-model="form.num_exo"
                               controls-position="compact"
                               placeholder="Numéro d'exercice"></b-numberinput>
              </b-field>

              <b-field>
                <b-checkbox type="is-secondary"
                            v-model="filter.num_page">
                  Numéro de page
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.num_page">
                <b-numberinput v-model="form.num_page"
                               controls-position="compact"
                               placeholder="Numéro de page"></b-numberinput>
              </b-field>
            </b-menu-list>

            <b-menu-list label="Etablissement">
              <b-field>
                <b-checkbox type="is-secondary"
                            v-model="filter.nom_etablissement">
                  Nom de l'établissement
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.nom_etablissement">
                <b-autocomplete v-model="etablissement_input"
                                placeholder="Choisir un établissement..."
                                :data="etablissement_items"
                                field="nom_etablissement"
                                keep-first
                                dropdown-position="top"
                                @select="option =>
                                form.nom_etablissement = option.nom_etablissement">
                  <template slot="empty">
                    Aucun résultat parmi les exercices
                  </template>
                  <template slot-scope="props">
                    <div class="is-pulled-left has-text-weight-bold">
                      {{ props.option.nom_etablissement }}
                    </div>
                    <br />
                    <small>
                      {{ props.option.ville_etablissement }}
                    </small>
                  </template>
                </b-autocomplete>
              </b-field>
              <b-field>
                <b-checkbox type="is-secondary"
                            v-model="filter.nom_prof">
                  Nom du professeur de mathématiques
                </b-checkbox>
              </b-field>
              <b-field v-if="filter.nom_prof">
                <b-select v-model="form.prefix_prof"
                          placeholder="Titre">
                  <option :value="true">M.</option>
                  <option :value="false">Mme</option>
                </b-select>
                <b-autocomplete v-model="prof_input"
                                placeholder="Choisir un prof..."
                                :data="profs_items"
                                field="nom_prof"
                                keep-first
                                dropdown-position="top"
                                @select="option =>
                                  form.nom_prof = option.nom_prof">
                  <template slot="empty">
                    Aucun résultat parmi les exercices
                  </template>
                  <template slot-scope="props">
                    <span>
                      {{ props.option.prefix_prof ? 'M.' : 'Mme'}}
                    </span>
                    <span>{{ props.option.nom_prof }}</span>
                  </template>
                </b-autocomplete>
              </b-field>
            </b-menu-list>

          </b-menu>
        </div>
      </b-sidebar>
    </div>

    <div class="column is-9">
      <div class="container is-fluid">
        <div class="columns is-multiline">
          <div v-if="result_files.length == 0 && used_search && !is_loading"
               class="column is-12">
            <div class="box has-text-centered">
              <p class="title">
                Aucun exo répondant à ces critères ne peut être trouvé...
              </p>
              <p class="is-subtitle">
                Demande la correction de ton exo
                en cliquant sur le bouton ci-dessous !
              </p>
              <b-button tag="router-link"
                        type="is-secondary"
                        class="mt-5 big-button"
                        size="is-large"
                        icon-left="hand"
                        :to="{ name: 'post-exo' }">
                Demander une correction
              </b-button>
            </div>
          </div>

          <div v-if="result_files.length > 0"
               v-for="(exo, index) in result_files"
               class="column is-12"
               :key="exo.id">
            <ExercicePreview :exo="exo"
                             :liked="likedExercices.some(ex => ex.id === exo.id )">
            </ExercicePreview>
          </div>
        </div>

        <div v-if="result_files.length > 0"
             class="column is-12">
          <b-pagination :total="count_elements"
                        :current.sync="current_page"
                        range-before="1"
                        range-after="1"
                        order="is-right"
                        size="is-medium"
                        per-page="5"
                        icon-prev="chevron-left"
                        icon-next="chevron-right"
                        aria-next-label="Next page"
                        aria-previous-label="Previous page"
                        aria-page-label="Page"
                        aria-current-label="Current page">
          </b-pagination>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import { mapState } from "vuex";
import exercicesService from "@/services/exercicesService";
import chapitres from "@/data/chapitres.json";
import classes from "@/data/classes.json";
import livres from "@/data/livres.json";
import ExercicePreview from "@/components/ExercicePreview.vue";

export default {
  name: "search",
  components: {
    ExercicePreview
  },
  props: {
    id: {
      type: Number,
      default: 1
    },
    is_corrected: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      used_search: false,
      is_loading: false,
      result_files: [],

      chapitres: chapitres,
      classes: classes,
      livres: livres,

      filter: {
        niveau: null,
        chapitre: null,
        type: null,
        livre: null,
        num_page: null,
        num_exo: null,
        nom_etablissement: null,
        prefix_prof: null,
        nom_prof: null,
        is_from_livre: true,
        is_corrected: true
      },

      form: {
        niveau: null,
        chapitre: null,
        type: null,
        livre: null,
        num_page: null,
        num_exo: null,
        nom_etablissement: null,
        prefix_prof: null,
        nom_prof: null,
        is_from_livre: false,
        is_corrected: this.is_corrected
      },

      etablissements: [],
      etablissement_items: [],
      etablissement_input: "",
      selected: null,
      profs: [],
      profs_items: [],
      prof_input: "",

      count_elements: 0,
      current_page: 1
    };
  },
  created() {
    exercicesService.getEtablissements()
      .then(data => {
        this.etablissements = data;
      })
    exercicesService.getProfs()
      .then(data => {
        this.profs = data;
      })
    this.searchExercices()
  },
  computed: {
    ...mapState("exercices", ["likedExercices"]),
    text_query: function() {
      this.filter.prefix_prof = this.filter.nom_prof
      if (!this.form.is_from_livre) {
        this.filter.livre = false;
        this.filter.num_page = false;
        this.filter.num_exo = false;
      }
      if (!this.form.niveau) {
        this.filter.chapitre = false;
        this.filter.livre = false;
      }
      let text = "?";
      for (let [key, value] of Object.entries(this.form)) {
        if (value === "") {
          this.form[key] = null;
        }
      }
      for (let [key, value] of Object.entries(this.form)) {
        if (value !== null && this.filter[key]) {
          let encoded_value = encodeURI(value);
          text += `${key}=${encoded_value}&`;
        }
      }
      text += `page=${this.current_page}`;
      return text;
    }
  },
  methods: {
    searchExercices() {
      this.used_search = true;
      this.is_loading = true;
      exercicesService.searchExercices(this.text_query).then(data => {
        this.count_elements = data.count;
        this.result_files = [];
        this.result_files.push(...data.results);
        this.used_search = true;
        this.is_loading = false;
      });
    },
    filterEtablissements(v) {
      this.etablissement_items = this.etablissements.filter(object => {
        return (
          (object.nom_etablissement || "")
          .toLowerCase()
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "")
          .indexOf(
            (v || "")
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
          ) > -1
        );
      });
    },
    filterProfs(v) {
      this.profs_items = this.profs.filter(object => {
        return (
          (object.nom_prof || "")
          .toLowerCase()
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "")
          .indexOf(
            (v || "")
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
          ) > -1
        );
      });
    }
  },
  watch: {
    current_page(val) {
      this.searchExercices();
    },
    etablissement_input: function(input) {
      input && this.filterEtablissements(input);
    },
    prof_input: function(input) {
      input && this.filterProfs(input);
    },
  }
};
</script>

<style lang="scss" scoped>
.b-checkbox.checkbox + .checkbox {
    margin-left: 0 !important;
}

.menu-label {
    font-size: 1em;
    color: $primary;
    border-bottom: 1px solid $primary;
    width: 70%;
}
</style>
