<template>
  <div>
    <b-loading is-full-page :active.sync="is_loading"></b-loading>
    <div class="container mb-10">
      <div class="columns is-centered is-vcentered">
        <div class="column is-10">
          <section>
            <p class="title is-1 has-text-primary has-text-centered mb-8">
              Les meilleures corrections de maths du net
            </p>

            <div class="columns is-centered is-multiline">
              <div class="column is-half">
                <b-button
                  tag="router-link"
                  class="has-radius-border big-button mt-5"
                  icon-left="hand"
                  type="is-tertiary"
                  expanded
                  size="is-large"
                  :to="{
                    name: 'post-exo'
                  }"
                >
                  Demander une correction
                </b-button>
              </div>
              <div v-if="isAuthenticated" class="column is-half">
                <b-button
                  tag="router-link"
                  class="has-radius-border big-button mt-5"
                  icon-left="book-open"
                  type="is-secondary"
                  expanded
                  size="is-large"
                  :to="{ name: 'mes-exercices' }"
                >
                  Mes exercices
                </b-button>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
    <div class="columns is-centered">
      <div class="column is-3">
        <b-sidebar
          position="static"
          mobile="fullwidth"
          fullheight
          fullwidth
          type="is-light"
          open
        >
          <div class="p-2">
            <b-menu class="">
              <h1 class="title mt-2 has-text-primary has-text-centered">
                <b-icon class="mr-1" icon="filter" size="is-medium"></b-icon
                >Filtrer
              </h1>
              <hr class="has-background-primary" />
              <b-field position="is-centered">
                <b-radio-button
                  v-model="form.is_corrected"
                  size="is-medium"
                  :native-value="false"
                  type="is-secondary"
                >
                  <b-icon size="is-medium" icon="close"></b-icon>
                </b-radio-button>

                <b-radio-button
                  v-model="form.is_corrected"
                  type="is-success"
                  size="is-medium"
                  :native-value="null"
                >
                  <b-icon size="is-medium" icon="minus"></b-icon>
                </b-radio-button>

                <b-radio-button
                  v-model="form.is_corrected"
                  size="is-medium"
                  :native-value="true"
                >
                  <b-icon size="is-medium" icon="check"></b-icon>
                </b-radio-button>
              </b-field>
              <p class="has-text-centered is-size-5 mb-4">
                {{ text_is_corrected }}
              </p>
              <b-field position="is-centered">
                <b-radio-button
                  v-model="form.is_from_livre"
                  size="is-medium"
                  :native-value="false"
                  type="is-secondary"
                >
                  <b-icon size="is-medium" icon="file-outline"></b-icon>
                </b-radio-button>

                <b-radio-button
                  v-model="form.is_from_livre"
                  size="is-medium"
                  type="is-tertiary"
                  :native-value="null"
                >
                  <b-icon size="is-medium" icon="minus"></b-icon>
                </b-radio-button>

                <b-radio-button
                  v-model="form.is_from_livre"
                  size="is-medium"
                  :native-value="true"
                >
                  <b-icon
                    size="is-medium"
                    icon="book-open-page-variant"
                  ></b-icon>
                </b-radio-button>
              </b-field>
              <p class="has-text-centered is-size-5 mb-4">
                {{ text_is_from_livre }}
              </p>
              <b-field position="is-centered">
                <b-radio-button
                  v-model="form.is_delai_depasse"
                  size="is-medium"
                  :native-value="true"
                  type="is-secondary"
                >
                  <b-icon size="is-medium" icon="clock-alert"></b-icon>
                </b-radio-button>

                <b-radio-button
                  v-model="form.is_delai_depasse"
                  size="is-medium"
                  :native-value="null"
                  type="is-tertiary"
                >
                  <b-icon size="is-medium" icon="minus"></b-icon>
                </b-radio-button>

                <b-radio-button
                  v-model="form.is_delai_depasse"
                  size="is-medium"
                  :native-value="false"
                >
                  <b-icon size="is-medium" icon="clock-check"></b-icon>
                </b-radio-button>
              </b-field>
              <p class="has-text-centered is-size-5 mb-4">
                {{ text_is_delai_depasse }}
              </p>

              <b-menu-list label="Général">
                <b-field>
                  <b-checkbox v-model="filter.niveau" type="is-secondary"
                    >Niveau</b-checkbox
                  >
                </b-field>
                <b-field v-if="filter.niveau">
                  <b-select
                    v-model="form.niveau"
                    placeholder="Choisir un niveau"
                    expanded
                  >
                    <option
                      v-for="(classe, index) in classes"
                      :key="classe"
                      :value="index"
                      >{{ classe }}</option
                    >
                  </b-select>
                </b-field>

                <b-field v-if="[0, 1].includes(parseInt(form.niveau))">
                  <b-checkbox v-model="filter.voie" type="is-secondary"
                    >Voie</b-checkbox
                  >
                </b-field>
                <b-field
                  v-if="[0, 1].includes(parseInt(form.niveau)) && filter.voie"
                >
                  <b-select
                    v-model="form.voie"
                    placeholder="Choisir une voie"
                    expanded
                  >
                    <option v-for="voie in voies" :key="voie" :value="voie">{{
                      voie
                    }}</option>
                  </b-select>
                </b-field>

                <b-field v-if="form.niveau == 0">
                  <b-checkbox v-model="filter.option" type="is-secondary"
                    >Option</b-checkbox
                  >
                </b-field>
                <b-field v-if="form.niveau == 0 && filter.option">
                  <b-select
                    v-model="form.option"
                    placeholder="Choisir une option"
                    expanded
                  >
                    <option
                      v-for="option in options"
                      :key="option"
                      :value="option"
                      >{{ option }}</option
                    >
                  </b-select>
                </b-field>

                <b-field>
                  <b-checkbox v-model="filter.type" type="is-secondary"
                    >Type</b-checkbox
                  >
                </b-field>
                <b-field v-if="filter.type">
                  <b-select
                    v-model="form.type"
                    placeholder="Choisir un type d'exo"
                    expanded
                  >
                    <option
                      v-for="value in Object.keys(types)"
                      :key="value"
                      :value="value"
                      >{{ value }}</option
                    >
                  </b-select>
                </b-field>

                <b-field>
                  <b-checkbox v-model="filter.devoir" type="is-secondary"
                    >Fait partie d'un devoir ?</b-checkbox
                  >
                </b-field>
                <b-field v-if="filter.devoir">
                  <b-select
                    v-model="form.devoir"
                    placeholder="Choisir un devoir"
                    expanded
                  >
                    <option>DM</option>
                    <option>DHC</option>
                    <option>DS</option>
                  </b-select>
                </b-field>

                <b-field>
                  <b-checkbox v-model="filter.chapitre" type="is-secondary"
                    >Chapitre</b-checkbox
                  >
                </b-field>
                <b-field v-if="filter.chapitre">
                  <b-select
                    v-if="form.niveau && filter.niveau"
                    v-model="form.chapitre"
                    placeholder="Choisis un chapitre"
                    expanded
                  >
                    <option
                      v-for="option in chapitres[form.niveau]"
                      :key="option"
                      >{{ option }}</option
                    >
                  </b-select>
                  <p v-else class="has-text-danger">
                    Tu dois d'abord renseigner un niveau.
                  </p>
                </b-field>
                <b-field v-if="!form.is_from_livre">
                  <b-checkbox v-model="filter.num_exo" type="is-secondary"
                    >Numéro d'exercice</b-checkbox
                  >
                </b-field>
                <b-field v-if="!form.is_from_livre && filter.num_exo">
                  <b-numberinput
                    v-model="form.num_exo"
                    controls-position="compact"
                    placeholder="Numéro d'exercice"
                    expanded
                  ></b-numberinput>
                </b-field>
              </b-menu-list>

              <b-menu-list v-if="form.is_from_livre" label="Livre scolaire">
                <b-field>
                  <b-checkbox v-model="filter.livre" type="is-secondary"
                    >Livre</b-checkbox
                  >
                </b-field>
                <b-field v-if="filter.livre">
                  <b-select
                    v-if="form.niveau"
                    v-model="form.livre"
                    placeholder="Choisir un livre"
                    expanded
                  >
                    <option
                      v-for="livre in livres[form.niveau]"
                      :key="livre"
                      :value="livre"
                      >{{ livre.split('_').join(' - ') }}</option
                    >
                  </b-select>
                  <p v-else class="has-text-danger">
                    Tu dois d'abord renseigner un niveau.
                  </p>
                </b-field>
                <div class="has-text-centered">
                  <img
                    v-if="filter.livre && form.livre"
                    class="mb-3"
                    style="height: 150px;"
                    :src="
                      require('@/assets/images/livres/' + form.livre + '.jpg')
                    "
                    alt="Image indisponible"
                  />
                </div>
                <b-field>
                  <b-checkbox v-model="filter.num_page" type="is-secondary"
                    >Numéro de page</b-checkbox
                  >
                </b-field>
                <b-field v-if="filter.num_page">
                  <b-numberinput
                    v-model="form.num_page"
                    controls-position="compact"
                    :min="1"
                    placeholder="Numéro de page"
                    expanded
                  ></b-numberinput>
                </b-field>
                <b-field v-if="form.is_from_livre">
                  <b-checkbox v-model="filter.num_exo" type="is-secondary"
                    >Numéro d'exercice</b-checkbox
                  >
                </b-field>
                <b-field v-if="form.is_from_livre && filter.num_exo">
                  <b-numberinput
                    v-model="form.num_exo"
                    controls-position="compact"
                    placeholder="Numéro d'exercice"
                    expanded
                  ></b-numberinput>
                </b-field>
              </b-menu-list>

              <b-menu-list label="Etablissement">
                <b-field>
                  <b-checkbox
                    v-model="filter.nom_etablissement"
                    type="is-secondary"
                    >Nom de l'établissement</b-checkbox
                  >
                </b-field>
                <b-field v-if="filter.nom_etablissement">
                  <b-autocomplete
                    v-model="etablissement_input"
                    placeholder="Choisir un établissement..."
                    :data="etablissement_items"
                    field="nom_etablissement"
                    keep-first
                    dropdown-position="top"
                    expanded
                    @select="
                      option =>
                        (form.nom_etablissement = option.nom_etablissement)
                    "
                  >
                    <template slot="empty"
                      >Aucun résultat parmi les exercices</template
                    >
                    <template slot-scope="props">
                      <div class="is-pulled-left has-text-weight-bold">
                        {{ props.option.nom_etablissement }}
                      </div>
                      <br />
                      <small>{{ props.option.ville_etablissement }}</small>
                    </template>
                  </b-autocomplete>
                </b-field>
                <b-field>
                  <b-checkbox v-model="filter.nom_prof" type="is-secondary"
                    >Nom du professeur de mathématiques</b-checkbox
                  >
                </b-field>
                <b-field v-if="filter.nom_prof">
                  <b-select v-model="form.prefix_prof" placeholder="Titre">
                    <option :value="true">M.</option>
                    <option :value="false">Mme</option>
                  </b-select>
                  <b-autocomplete
                    v-model="prof_input"
                    placeholder="Choisir un professeur..."
                    :data="profs_items"
                    field="nom_prof"
                    keep-first
                    dropdown-position="top"
                    expanded
                    @select="
                      option => {
                        form.nom_prof = option.nom_prof
                        form.prefix_prof = option.prefix_prof
                      }
                    "
                  >
                    <template slot="empty"
                      >Aucun résultat parmi les exercices</template
                    >
                    <template slot-scope="props">
                      <span class="mr-1">{{
                        props.option.prefix_prof ? 'M.' : 'Mme'
                      }}</span>
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
          <div
            v-if="result_files.length == 0 && used_search && !is_loading"
            class="column is-12"
          >
            <div class="box has-text-centered">
              <p class="title">
                Aucun exo répondant à ces critères n'a été trouvé...
              </p>
              <p class="is-subtitle is-size-4">
                Demande la correction de ton exo !
              </p>
            </div>
          </div>

          <div v-else>
            <div class="box has-background-light">
              <div class="columns is-vcentered is-size-5">
                <div
                  class="column is-3 has-text-primary has-text-weight-bold is-flex"
                  style="align-items: center;"
                >
                  <b-button
                    type="is-light"
                    :class="{
                      'has-text-tertiary': order['date_created'] !== null
                    }"
                    :icon-right="order_icons['date_created']"
                    @click="changeOrder('date_created')"
                    >Date de création</b-button
                  >
                </div>
                <div
                  class="column is-3 has-text-primary has-text-weight-bold is-flex"
                  style="align-items: center;"
                >
                  <b-button
                    type="is-light"
                    :class="{
                      'has-text-tertiary': order['prix'] !== null
                    }"
                    :icon-right="order_icons['prix']"
                    @click="changeOrder('prix')"
                    >Points cédés</b-button
                  >
                </div>
                <div
                  class="column is-3 has-text-primary has-text-weight-bold is-flex"
                  style="align-items: center;"
                >
                  <b-button
                    type="is-light"
                    :class="{
                      'has-text-tertiary': order['date_limite'] !== null
                    }"
                    :icon-right="order_icons['date_limite']"
                    @click="changeOrder('date_limite')"
                    >Délai</b-button
                  >
                </div>
              </div>
            </div>
            <div class="columns is-multiline">
              <div
                v-for="exo in result_files"
                :key="exo.id"
                class="column is-12"
              >
                <ExercicePreview
                  :exo="exo"
                  :liked="likedExercices.some(ex => ex.id === exo.id)"
                >
                </ExercicePreview>
              </div>
            </div>
          </div>

          <div v-if="result_files.length > 0" class="column is-12 mt-4">
            <b-pagination
              :total="count_elements"
              :current.sync="current_page"
              range-before="1"
              range-after="1"
              order="is-right"
              size="is-medium"
              per-page="10"
              icon-prev="chevron-left"
              icon-next="chevron-right"
              aria-next-label="Next page"
              aria-previous-label="Previous page"
              aria-page-label="Page"
              aria-current-label="Current page"
            ></b-pagination>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import usersService from '@/services/usersService'
import exercicesService from '@/services/exercicesService'
import chapitres from '@/data/chapitres.json'
import classes from '@/data/niveaux.json'
import options from '@/data/options.json'
import voies from '@/data/voies.json'
import types from '@/data/types.json'
import livres from '@/data/livres.json'
import ExercicePreview from '@/components/ExercicePreview.vue'

export default {
  name: 'Search',
  components: {
    ExercicePreview
  },
  props: {
    id: {
      type: Number,
      default: 1
    },
    isCorrected: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      used_search: false,
      is_loading: false,
      result_files: [],

      chapitres: chapitres,
      classes: classes,
      options: options,
      voies: voies,
      types: types,
      livres: livres,

      order: {
        date_created: null,
        prix: false,
        date_limite: null
      },

      order_icons: {
        date_created: 'chevron-up',
        prix: 'chevron-up-circle',
        date_limite: 'chevron-up'
      },

      filter: {
        niveau: false,
        option: false,
        voie: false,
        chapitre: false,
        type: false,
        devoir: false,
        livre: false,
        num_page: false,
        num_exo: false,
        nom_etablissement: false,
        prefix_prof: false,
        nom_prof: false,
        is_from_livre: true,
        is_corrected: true,
        is_delai_depasse: true
      },

      form: {
        niveau: null,
        option: null,
        voie: null,
        chapitre: null,
        type: null,
        devoir: null,
        livre: null,
        num_page: null,
        num_exo: null,
        nom_etablissement: null,
        prefix_prof: null,
        nom_prof: null,
        is_from_livre: null,
        is_corrected: this.isCorrected,
        is_delai_depasse: false
      },

      etablissements: [],
      etablissement_items: [],
      etablissement_input: '',
      selected: null,
      profs: [],
      profs_items: [],
      prof_input: '',

      count_elements: 0,
      current_page: 1
    }
  },
  computed: {
    ...mapGetters('authentication', ['isAuthenticated']),
    ...mapState('exercices', ['likedExercices']),
    ...mapState('authentication', ['user']),
    text_is_corrected: function() {
      switch (this.form.is_corrected) {
        case false:
          return 'À corriger'
        case true:
          return 'Corrigé'
        default:
          return 'À corriger/Corrigé'
      }
    },
    text_is_from_livre: function() {
      switch (this.form.is_from_livre) {
        case false:
          return 'Sur feuille'
        case true:
          return 'Sur livre'
        default:
          return 'Sur feuille/Sur livre'
      }
    },
    text_is_delai_depasse: function() {
      switch (this.form.is_delai_depasse) {
        case true:
          return 'Délai dépassé'
        case false:
          return 'Délai non dépassé'
        default:
          return 'Délai dépassé/non dépassé'
      }
    },
    text_query_order: function() {
      let text = ''
      for (let [key, value] of Object.entries(this.order)) {
        if (value !== null) {
          if (value === true) {
            text += 'ordering=' + key + '&'
          } else {
            text += 'ordering=-' + key + '&'
          }
        }
      }
      return text
    },
    text_query_filter: function() {
      let text = ''
      for (let [key, value] of Object.entries(this.form)) {
        if (value !== null && this.filter[key]) {
          let encoded_value = encodeURI(value)
          text += `${key}=${encoded_value}&`
        }
      }
      return text
    },
    text_query: function() {
      let text = '?'
      text += this.text_query_filter
      text += this.text_query_order
      text += `page=${this.current_page}`
      return text
    }
  },
  watch: {
    $route(to) {
      if (to.name == 'home') {
        this.searchExercices()
      }
      if (to.name == 'post-exo') {
        this.$store.dispatch('authentication/getProfileUser')
      }
    },
    filter: {
      handler(inputs) {
        inputs.prefix_prof = inputs.nom_prof
        for (let [key, value] of Object.entries(inputs)) {
          if (value == false) {
            this.form[key] = null
            if (key == 'nom_etablissement') {
              this.etablissement_input = null
            }
            if (key == 'nom_prof') {
              this.prof_input = null
            }
          }
        }
        this.current_page = 1
        this.searchExercices()
      },
      deep: true
    },
    form: {
      handler(inputs) {
        if (!inputs.is_from_livre) {
          this.filter.livre = false
          this.filter.num_page = false
        }
        if (inputs.niveau != 0) {
          this.filter.option = false
        }
        if (inputs.niveau != 0 && inputs.niveau != 1) {
          this.filter.voie = false
        }
        for (let [key, value] of Object.entries(inputs)) {
          if (value === '') {
            this.form[key] = null
          }
        }
        this.current_page = 1
        this.searchExercices()
      },
      deep: true
    },
    order: {
      handler() {
        this.current_page = 1
        this.searchExercices()
      },
      deep: true
    },
    current_page: function() {
      this.searchExercices()
    },
    etablissement_input: function(input) {
      input && this.filterEtablissements(input)
    },
    prof_input: function(input) {
      input && this.filterProfs(input)
    }
  },
  mounted() {
    usersService
      .getEtablissements()
      .then(etablissements => {
        this.etablissements = etablissements
        return exercicesService.getProfs()
      })
      .then(profs => {
        this.profs = profs
      })
      .finally(() => {
        this.searchExercices()
      })
  },
  methods: {
    searchExercices() {
      this.used_search = true
      this.is_loading = true
      exercicesService
        .searchExercices(this.text_query)
        .then(data => {
          this.count_elements = data.count
          this.result_files = []
          this.result_files.push(...data.results)
          this.used_search = true
          this.is_loading = false
        })
        .catch(() => {
          this.is_loading = false
        })
    },
    changeOrder(value) {
      let formerValue = this.order[value]
      for (let key of Object.keys(this.order)) {
        this.order[key] = null
        this.order_icons[key] = 'chevron-up'
      }
      if (formerValue === null) {
        this.order[value] = false
        this.order_icons[value] = 'chevron-up-circle'
      } else if (formerValue === false) {
        this.order[value] = true
        this.order_icons[value] = 'chevron-down-circle'
      } else {
        this.order[value] = false
        this.order_icons[value] = 'chevron-up-circle'
      }
    },
    filterEtablissements(v) {
      this.etablissement_items = this.etablissements.filter(object => {
        return (
          (object.nom_etablissement || '')
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .indexOf(
              (v || '')
                .toLowerCase()
                .normalize('NFD')
                .replace(/[\u0300-\u036f]/g, '')
            ) > -1
        )
      })
    },
    filterProfs(v) {
      this.profs_items = this.profs.filter(object => {
        return (
          (object.nom_prof || '')
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .indexOf(
              (v || '')
                .toLowerCase()
                .normalize('NFD')
                .replace(/[\u0300-\u036f]/g, '')
            ) > -1
        )
      })
    }
  }
}
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

.button .icon:first-child:not(:last-child) {
  margin-left: calc(-0.375em - 1px);
  margin-right: calc(-0.375em - 1px);
}
</style>
