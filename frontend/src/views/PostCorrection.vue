<template>
  <div class="container is-fluid">
    <b-loading is-full-page :active.sync="is_loading"></b-loading>
    <div v-if="user && user.is_new" class="card has-text-centered">
      <div class="card-content">
        <div class="is-size-5">
          <p>
            Avant de poster pour la première fois, nous te demandons de
            <strong>cliquer sur le bouton ci-dessous</strong> afin
            <strong>d'apprendre à poster un énoncé de bonne qualité.</strong>
          </p>
          <p class="mt-3 has-text-danger has-text-weight-bold">
            Un énoncé ou une correction ne respectant pas ces recommandations se
            verra supprimé.
          </p>
        </div>

        <b-button
          class="has-radius-border big-button mt-5"
          icon-left="hand"
          type="is-tertiary"
          size="is-large"
          @click="redirectStandards()"
        >
          Comment bien poster ?
        </b-button>
      </div>
    </div>
    <div v-else-if="user && !user.is_new">
      <b-steps v-model="activeStep" animated has-navigation>
        <b-step-item
          id="firstStep"
          label="Caractéristiques de l'exo"
          :style="{ 'min-height': height }"
          clickable
        >
          <hr ref="scroll1" />
          <h1 class="title has-text-centered">
            Caractéristiques de l'exo
          </h1>
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
                    label="Type d'exo"
                    :message="errors"
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
                  >
                    <b-select
                      v-model="form.type"
                      expanded
                      placeholder="Choisir un type d'exo"
                    >
                      <option
                        v-for="value in Object.keys(types)"
                        :key="value"
                        :value="value"
                        >{{ value }}</option
                      >
                    </b-select>
                  </b-field>
                </ValidationProvider>

                <b-field grouped>
                  <ValidationProvider
                    v-slot="{ errors, valid }"
                    slim
                    rules="required"
                  >
                    <b-field
                      label="Provenance"
                      expanded
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
                  <!-- <ValidationProvider
                        v-if="form.is_from_livre === false"
                        v-slot="{ errors, valid }"
                        slim
                        rules="integer|min_value:1"
                      >
                        <b-field
                          v-if="form.is_from_livre === false"
                          label="Numéro d'exo"
                          expanded
                          message="Ce champ n'est pas obligatoire"
                        >
                          <b-numberinput
                            v-model="form.num_exo"
                            expanded
                            min="1"
                            placeholder="Numéro d'exercice"
                          >
                          </b-numberinput>
                        </b-field>
                      </ValidationProvider> -->
                </b-field>

                <b-field
                  v-if="form.is_from_livre === false"
                  label="L'exo a un numéro ?"
                >
                  <b-switch
                    v-model="form.has_num"
                    type="is-success"
                    passive-type="is-danger"
                    expanded
                  >
                    {{ form.has_num ? 'Oui' : 'Non' }}
                  </b-switch>
                </b-field>
                <ValidationProvider
                  v-if="form.has_num && form.is_from_livre === false"
                  v-slot="{ errors, valid }"
                  slim
                  rules="required|integer|min_value:1"
                >
                  <b-field
                    v-if="form.has_num && form.is_from_livre === false"
                    expanded
                    :message="errors"
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
                  >
                    <b-numberinput
                      v-model="form.num_exo"
                      expanded
                      min="1"
                      placeholder="Numéro"
                    >
                    </b-numberinput>
                  </b-field>
                </ValidationProvider>

                <b-field label="Fait partie d'un devoir ?">
                  <b-switch
                    v-model="form.is_from_devoir"
                    type="is-success"
                    passive-type="is-danger"
                    expanded
                  >
                    {{ form.is_from_devoir ? 'Oui' : 'Non' }}
                  </b-switch>
                </b-field>
                <ValidationProvider
                  v-if="form.is_from_devoir"
                  v-slot="{ errors, valid }"
                  slim
                  rules="required"
                >
                  <b-field
                    v-if="form.is_from_devoir"
                    expanded
                    :message="errors"
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
                  >
                    <b-select
                      v-model="form.devoir"
                      placeholder="Choisir un devoir"
                      expanded
                    >
                      <option> DM </option>
                      <option> DHC </option>
                      <option> DS </option>
                    </b-select>
                  </b-field>
                </ValidationProvider>

                <ValidationProvider
                  v-if="user && user.niveau == 100"
                  v-slot="{ errors, valid }"
                  slim
                  rules="required"
                >
                  <b-field
                    v-if="user && user.niveau == 100"
                    label="Niveau de l'exo"
                    :message="errors"
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
                  >
                    <b-select
                      v-model="form.niveau"
                      placeholder="Choisir un niveau"
                      expanded
                    >
                      <option
                        v-for="(value, key) in niveaux"
                        :key="value"
                        :value="key"
                        >{{ value }}</option
                      ></b-select
                    >
                  </b-field>
                </ValidationProvider>

                <ValidationProvider
                  v-if="
                    user &&
                      [0, 1].includes(parseInt(form.niveau)) &&
                      user.niveau == 100
                  "
                  v-slot="{ errors, valid }"
                  slim
                  rules="required"
                >
                  <b-field
                    v-if="
                      user &&
                        [0, 1].includes(parseInt(form.niveau)) &&
                        user.niveau == 100
                    "
                    label="Voie"
                    :message="errors"
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
                  >
                    <b-select
                      v-model="form.voie"
                      expanded
                      placeholder="Choisis la voie..."
                    >
                      <option v-for="voie in voies" :key="voie" :value="voie">{{
                        voie
                      }}</option>
                    </b-select>
                  </b-field>
                </ValidationProvider>

                <ValidationProvider
                  v-if="
                    user &&
                      form.niveau == 0 &&
                      form.voie == 'Générale' &&
                      user.niveau == 100
                  "
                  v-slot="{ errors, valid }"
                  slim
                  rules="required"
                >
                  <b-field
                    v-if="
                      user &&
                        form.niveau == 0 &&
                        form.voie == 'Générale' &&
                        user.niveau == 100
                    "
                    label="Option"
                    :message="errors"
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
                  >
                    <b-select
                      v-model="form.option"
                      expanded
                      placeholder="Choisis l'option..."
                    >
                      <option
                        v-for="option in options"
                        :key="option"
                        :value="option"
                        >{{ option }}</option
                      >
                    </b-select>
                  </b-field>
                </ValidationProvider>

                <ValidationProvider
                  v-slot="{ errors, valid }"
                  slim
                  rules="required"
                >
                  <b-field
                    label="Chapitre"
                    :message="errors"
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
                  >
                    <b-select
                      v-if="user && user.niveau != 100"
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
                    <b-select
                      v-if="user && user.niveau == 100"
                      v-model="form.chapitre"
                      expanded
                      placeholder="Choisir un chapitre"
                    >
                      <option
                        v-for="option in chapitres[form.niveau]"
                        :key="option"
                      >
                        {{ option }}
                      </option>
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
        >
          <hr ref="scroll2" />
          <h1 class="title has-text-centered">Énoncé</h1>
          <hr />
          <div class="notification is-secondary is-light">
            <div class="media">
              <div class="media-left">
                <b-icon icon="alert"></b-icon>
              </div>
              <div class="media-content">
                Pour des raisons relatives au droit d’auteur, il est interdit
                d’uploader un énoncé provenant d’un livre.
              </div>
            </div>
          </div>
          <ValidationObserver ref="secondStep">
            <ValidationProvider v-slot="{ errors }" slim rules="required">
              <Upload v-model="enonce_file" :error="errors[0]" />
            </ValidationProvider>
          </ValidationObserver>
        </b-step-item>

        <b-step-item
          v-else
          id="secondStep2"
          :style="{ 'min-height': height }"
          label="Livre"
        >
          <hr ref="scroll2" />
          <h1 class="title has-text-centered">Livre</h1>
          <hr />
          <div class="columns">
            <div class="column is-half">
              <ValidationObserver ref="secondStep" slim>
                <ValidationProvider
                  v-slot="{ errors, valid }"
                  slim
                  rules="required"
                >
                  <b-field
                    label="Livre"
                    expand
                    :message="errors"
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
                  >
                    <b-select
                      v-if="user && user.niveau != 100"
                      v-model="form.livre.name"
                      expanded
                      placeholder="Choisir un livre"
                    >
                      <option
                        v-for="(livre, index) in livres[user.niveau]"
                        :key="index"
                        :value="livre"
                      >
                        {{ livre.split('_').join(' - ') }}
                      </option>
                    </b-select>
                    <b-select
                      v-if="user && user.niveau == 100"
                      v-model="form.livre.name"
                      expanded
                      placeholder="Choisir un livre"
                    >
                      <option
                        v-for="livre in livres[form.niveau]"
                        :key="livre"
                        :value="livre"
                      >
                        {{ livre.split('_').join(' - ') }}
                      </option>
                    </b-select>
                  </b-field>
                  <p class="mb-3">
                    Tu ne trouves pas ton livre dans la liste ?
                    <b-tooltip label="support@1exo.fr" dashed
                      >Contacte-nous
                    </b-tooltip>
                    en envoyant la référence de ton livre !
                  </p>
                </ValidationProvider>
                <ValidationProvider
                  v-slot="{ errors, valid }"
                  slim
                  rules="required"
                >
                  <b-field
                    label="Numéro"
                    :message="errors"
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
                  >
                    <b-numberinput
                      v-model="form.num_exo"
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
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
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

            <!-- <div class="column is-half has-text-centered">
                <img v-if="form.livre.name"
                     style="height: 300px;"
                     :src="require('@/assets/images/livres/' + form.livre.name + '.jpg'"
                     alt="Image indisponible" />
              </div> -->
            <div class="column is-half has-text-centered">
              <img
                v-if="form.livre.name"
                style="height: 300px;"
                :src="
                  require('@/assets/images/livres/' + form.livre.name + '.jpg')
                "
                alt="Image indisponible"
              />
            </div>
          </div>
        </b-step-item>

        <b-step-item
          id="thirdStep"
          label="Vérification"
          :style="{ 'min-height': height }"
        >
          <hr ref="scroll3" />
          <h1 class="title has-text-centered">Vérification</h1>
          <hr />
          <div class="notification is-tertiary is-light">
            <div class="media">
              <div class="media-left">
                <b-icon icon="information"></b-icon>
              </div>
              <div
                v-if="count_elements > 0"
                class="media-content has-text-weight-bold"
              >
                Des exos semblables au tien ont déjà été corrigés. Vérifie qu'il
                ne figure pas parmi eux.
              </div>
              <div v-else class="media-content has-text-weight-bold">
                Aucun exo semblable au tien n'a encore été corrigé. Tu peux
                continuer.
              </div>
            </div>
          </div>
          <div class="columns is-multiline">
            <ValidationObserver ref="thirdStep" />
            <div
              v-for="result_exo in result_exos"
              :key="result_exo.id"
              class="column is-12"
            >
              <ExercicePreview :exo="result_exo" :show-modal="true">
              </ExercicePreview>
            </div>
          </div>
        </b-step-item>

        <b-step-item
          v-if="!hasCorrection"
          id="fourthStep"
          label="Délai"
          :style="{ 'min-height': height }"
        >
          <hr ref="scroll4" />
          <h1 class="title has-text-centered">Délai</h1>
          <hr />
          <div v-if="user" class="columns is-centered">
            <div class="column is-half">
              <ValidationObserver ref="fourthStep">
                <ValidationProvider
                  v-slot="{ errors, valid }"
                  slim
                  rules="required"
                >
                  <b-field
                    :message="errors"
                    :type="{ 'is-danger': errors[0], 'is-success': valid }"
                  >
                    <template slot="label">
                      À faire pour...
                      <b-tooltip
                        type="is-dark"
                        label="Combien de temps peux-tu donner au correcteur ? 
                            "
                        multilined
                      >
                        <b-icon
                          size="is-small"
                          icon="help-circle-outline"
                        ></b-icon>
                      </b-tooltip>
                    </template>
                    <b-datetimepicker
                      ref="datetimepicker"
                      v-model="form.date_limite"
                      expanded
                      placeholder="Choisir une date limite"
                      :datepicker="datepicker_attrs"
                      :min-datetime="minDatetime"
                      icon="calendar-today"
                    >
                      <template slot="right">
                        <button
                          class="button is-primary"
                          @click="$refs.datetimepicker.toggle()"
                        >
                          <b-icon icon="check"></b-icon>
                          <span>Valider</span>
                        </button>
                      </template>
                    </b-datetimepicker>
                  </b-field>
                  <div
                    v-if="form.date_limite"
                    class="has-text-weight-bold is-size-5 mt-5"
                  >
                    Tu as choisi un délai de : {{ delai_text }}
                  </div>
                  <div class="has-text-grey is-size-6 mt-2">
                    Attention : plus le délai est court, plus il y a de risques
                    de ne pas avoir de correction... mets un délai raisonnable.
                  </div>
                </ValidationProvider>
              </ValidationObserver>
            </div>
          </div>
        </b-step-item>

        <b-step-item
          v-if="!hasCorrection"
          id="fithStep"
          label="Points"
          :style="{ 'min-height': height }"
        >
          <hr ref="scroll5" />
          <h1 class="title has-text-centered">Points</h1>
          <hr />
          <!-- <div class="notification is-primary is-light">
            <div class="media">
              <div class="media-left">
                <b-icon icon="information"></b-icon>
              </div>
              <div
                v-if="
                  user &&
                    constants &&
                    constants['MEAN_PRICES'][user.niveau] > 0 &&
                    user.niveau != 100
                "
                class="media-content"
              >
                <strong>
                  Les exos de niveau {{ niveaux[user.niveau] }} se corrigent
                  actuellement pour
                  {{ constants['MAX_PRICES'][user.niveau] }}
                  {{ constants['MAX_PRICES'][user.niveau] > 1 ? 'pts' : 'pt' }}
                </strong>
                (en moyenne).
              </div>
              <div
                v-else-if="
                  user &&
                    constants &&
                    constants['MAX_PRICES'][form.niveau] > 0 &&
                    user.niveau == 100
                "
                class="media-content"
              >
                <strong
                  >Les exos de niveau {{ niveaux[form.niveau] }} se corrigent
                  actuellement pour
                  {{ constants['MAX_PRICES'][form.niveau] }}
                  {{
                    constants['MAX_PRICES'][form.niveau] > 1 ? 'pts' : 'pt'
                  }}</strong
                >
                (en moyenne).
              </div>
              <div v-else class="media-content">
                Aucun exercice de ce niveau n'est en ligne pour le moment.
                Calcul de la moyenne impossible.
              </div>
            </div>
          </div> -->
          <div class="columns is-centered my-8">
            <div class="columns is-half">
              <b-field position="is-centered" grouped group-multiline>
                <b-radio-button
                  v-model="is_free"
                  :native-value="true"
                  type="is-secondary"
                  size="is-large"
                >
                  Correction basique
                </b-radio-button>

                <b-radio-button
                  v-model="is_free"
                  :native-value="false"
                  type="is-tertiary"
                  size="is-large"
                >
                  Correction boostée
                </b-radio-button>
              </b-field>
            </div>
          </div>
          <div class="columns is-centered mb-2">
            <div class="column is-half has-text-centered">
              <p v-if="is_free" class="is-size-5 has-text-weight-bold">
                Tu as
                <span class="has-text-danger"> 20 % de chances</span>
                d'obtenir une correction.
              </p>

              <p v-else class="is-size-5 has-text-weight-bold">
                Avec
                <span class="has-text-danger">{{ form.prix }} pt(s)</span> , tu
                as
                <span class="has-text-danger"> {{ chances }} % de chances</span>
                d'obtenir une correction. <br />
              </p>
            </div>
          </div>
          <div v-if="user" class="columns is-centered is-vcentered mb-5">
            <div class="column is-half">
              <ValidationObserver ref="fifthStep">
                <div :class="{ hidden: is_free }">
                  <ValidationProvider
                    v-slot="{ errors, valid }"
                    slim
                    :rules="{
                      required: true,
                      min_value: 0,
                      max_tirelire_value: [user.tirelire_avail, user.tirelire],
                      integer: true
                    }"
                  >
                    <b-field
                      :message="errors"
                      :type="{ 'is-danger': errors[0] }"
                    >
                      <template slot="label">
                        Points
                        <b-tooltip
                          type="is-dark"
                          label="Quel est le nombre de points que tu es prêt à céder pour obtenir la correction de ton exo ?"
                          multilined
                        >
                          <b-icon
                            size="is-small"
                            icon="help-circle-outline"
                          ></b-icon>
                        </b-tooltip>
                      </template>
                      <b-numberinput
                        v-model="form.prix"
                        :disabled="is_free"
                        :min="1"
                        placeholder="Choisir un nombre de points"
                      >
                      </b-numberinput>
                    </b-field>
                  </ValidationProvider>
                  <div class="has-text-grey is-size-6">
                    Si tu n’obtiens pas de correction à la fin de ton délai, tu
                    ne perds pas de points.
                  </div>
                  <div
                    :class="{
                      hidden: form.prix <= 0.9 * user.tirelire_avail
                    }"
                  >
                    <b-button
                      tag="router-link"
                      type="is-secondary"
                      icon-left="credit-card"
                      class="mt-6 has-radius-border big-button"
                      expanded
                      :to="{ name: 'tirelire' }"
                    >
                      Recharge ta tirelire
                    </b-button>
                  </div>
                </div>
              </ValidationObserver>
            </div>
          </div>
        </b-step-item>

        <b-step-item
          v-if="hasCorrection"
          id="sixthStep"
          :style="{ 'min-height': height }"
          label="Correction"
        >
          <hr ref="scroll6" />
          <h1 class="title has-text-centered">Correction</h1>
          <hr />
          <div class="notification is-secondary is-light">
            <div class="media">
              <div class="media-left">
                <b-icon icon="alert"></b-icon>
              </div>
              <div class="media-content">
                Pour des raisons relatives au droit d’auteur, il est interdit
                d’uploader une correction provenant d’un livre.
              </div>
            </div>
          </div>
          <ValidationObserver ref="sixthStep">
            <ValidationProvider v-slot="{ errors }" slim rules="required">
              <Upload
                v-model="correction_file"
                :error="errors[0]"
                :exo="false"
              />
            </ValidationProvider>
          </ValidationObserver>
        </b-step-item>

        <b-step-item label="Récapitulatif" :style="{ 'min-height': height }">
          <hr ref="scroll7" />
          <h1 class="title has-text-centered">Récapitulatif</h1>
          <hr />
          <div class="notification is-tertiary is-light">
            <div class="media">
              <div class="media-left">
                <b-icon icon="information"></b-icon>
              </div>
              <div class="media-content">
                Voici comment ton exo apparaîtra.
              </div>
            </div>
          </div>
          <ExercicePreview
            :exo="exo"
            :activated="false"
            :display-date-limite="!hasCorrection"
          ></ExercicePreview>
          <b-progress
            v-if="is_loading"
            class="mt-2"
            :value="uploadPercentage"
            size="is-large"
            show-value
            format="percent"
            type="is-tertiary"
          ></b-progress>
          <div v-if="is_loading" class="has-text-centered">
            Ton exercice est en train d'être soumis. Ne quitte pas la page avant
            que le processus soit terminé !
          </div>
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
              v-if="hasCorrection && activeStep < 4"
              type="is-tertiary"
              :disabled="next.disabled"
              @click.prevent="goNext(next, activeStep)"
            >
              Continuer
            </b-button>
            <b-button
              v-else-if="!hasCorrection && activeStep < 5"
              type="is-tertiary"
              :disabled="next.disabled"
              @click.prevent="goNext(next, activeStep)"
            >
              Continuer
            </b-button>
            <b-button
              v-else-if="hasCorrection && activeStep >= 4"
              type="is-success"
              @click.prevent="submitExo()"
            >
              Poster
            </b-button>
            <b-button v-else type="is-success" @click.prevent="submitExo()">
              Poster
            </b-button>
          </div>
        </template>
      </b-steps>
    </div>
  </div>
</template>

<script>
import { ValidationObserver, ValidationProvider } from 'vee-validate'
import { mapState } from 'vuex'
import exercicesService from '@/services/exercicesService'
import moment from 'moment'
import chapitres from '@/data/chapitres.json'
import niveaux from '@/data/niveaux.json'
import voies from '@/data/voies.json'
import options from '@/data/options.json'
import types from '@/data/types.json'
import livres from '@/data/livres.json'
import Upload from '@/components/Upload.vue'
import ExercicePreview from '@/components/ExercicePreview.vue'
export default {
  name: 'PostCorrection',
  components: {
    Upload,
    ExercicePreview,
    ValidationObserver,
    ValidationProvider
  },
  props: {
    hasCorrection: {
      type: Boolean,
      default: true
    }
  },
  data() {
    const minDate = new Date(
      moment()
        .add(2, 'hours')
        .add(1, 'minutes')
        .toISOString(true)
    )
    return {
      chapitres: chapitres,
      niveaux: niveaux,
      voies: voies,
      options: options,
      types: types,
      livres: livres,
      height: '400px',
      minDatetime: minDate,

      result_exos: [],
      count_elements: 0,
      current_page: 1,
      is_loading: false,
      uploadPercentage: 0,

      datepicker_attrs: {
        'month-names': [
          'Janvier',
          'Février',
          'Mars',
          'Avril',
          'Mai',
          'Juin',
          'Juillet',
          'Août',
          'Septembre',
          'Octobre',
          'Novembre',
          'Décembre'
        ],
        'day-names': ['Dim', 'Lu', 'Ma', 'Mer', 'Jeu', 'Ven', 'Sa'],
        'first-day-of-week': 1
      },

      activeStep: 0,
      enonce_file: null,
      correction_file: null,
      is_free: true,
      form: {
        type: null,
        is_from_livre: null,
        chapitre: null,
        niveau: null,
        voie: null,
        option: null,
        has_num: null,
        is_from_devoir: null,
        num_exo: null,
        livre: {
          name: null,
          num_page: null
        },
        date_limite: null,
        prix: 0
      }
    }
  },
  computed: {
    ...mapState('authentication', ['user']),
    ...mapState('general', ['constants']),
    all_chapitres() {
      return [].concat.apply([], Object.values(this.chapitres))
    },
    exo() {
      if (!this.user) {
        return
      }
      let niveau = null
      let voie = null
      let option = null
      if (this.user.niveau == 100) {
        niveau = this.form.niveau
        voie = this.form.voie
        option = this.form.option
      } else {
        niveau = this.user.niveau
        voie = this.user.voie
        option = this.user.option
      }
      return {
        id: 'ID',
        posteur: this.user,
        niveau: niveau,
        voie: voie,
        option: option,
        type: this.form.type,
        chapitre: this.form.chapitre,
        livre: this.form.is_from_livre ? this.form.livre.name : null,
        devoir: this.form.is_from_devoir ? this.form.devoir : null,
        file: this.enonce_file,
        num_page: this.form.is_from_livre ? this.form.livre.num_page : null,
        num_exo:
          this.form.is_from_livre ||
          (!this.form.is_from_livre && this.form.has_num)
            ? this.form.num_exo
            : null,
        prix: this.form.prix,
        date_limite: moment(this.form.date_limite).toISOString(true),
        date_created: moment(),
        correcs: this.hasCorrection ? [{ id: 1 }] : []
      }
    },
    text_query() {
      let lookup_keys = [
        'niveau',
        'option',
        'type',
        'chapitre',
        'livre',
        'devoir',
        'num_page',
        'num_exo'
      ]
      let text = '?'
      for (let [key, value] of Object.entries(this.exo)) {
        if (value !== null && lookup_keys.includes(key)) {
          let encoded_value = encodeURI(value)
          text += `${key}=${encoded_value}&`
        }
      }
      text += 'is_corrected=true'
      return text
    },
    chances() {
      if (this.constants['MAX_PRICE'] > 0) {
        return Math.ceil(
          Math.min((this.form.prix / this.constants['MAX_PRICE']) * 100, 95)
        )
      } else if (
        this.constants['MAX_PRICE'] < 0 &&
        this.constants['MEAN_PRICE'] > 0
      ) {
        return Math.ceil(
          Math.min((this.form.prix / this.constants['MEAN_PRICE']) * 100, 95)
        )
      } else {
        return Math.min(20 * this.form.prix + 10, 95)
      }
    },
    diff_minutes() {
      let date1 = moment()
      let date2 = moment(this.form.date_limite)
      let diffMinutes = date2.diff(date1, 'minutes')
      return diffMinutes
    },
    diff_hours() {
      let date1 = moment()
      let date2 = moment(this.form.date_limite)
      let diffHours = date2.diff(date1, 'hours')
      return diffHours
    },
    diff_days() {
      let date1 = moment()
      let date2 = moment(this.form.date_limite)
      let diffDays = date2.diff(date1, 'days')
      return diffDays
    },
    delai_text() {
      if (this.diff_hours < 1) {
        return this.diff_minutes.toString() + ' minute(s)'
      } else if (this.diff_days < 2) {
        return this.diff_hours.toString() + ' heure(s)'
      } else {
        return this.diff_days.toString() + ' jour(s)'
      }
    }
  },
  watch: {
    $route(to, from) {
      console.log(from)
    },
    is_free: function(input) {
      if (!input) {
        this.form.prix = 1
      } else {
        this.form.prix = 0
      }
    },
    form: {
      handler(inputs) {
        if (inputs.prix == 0) {
          this.is_free = true
        }
      },
      deep: true
    }
  },
  mounted() {
    this.$store.dispatch('authentication/getProfileUser')
  },
  methods: {
    redirectStandards() {
      this.$router.push({ name: 'standards-qualite' })
    },
    searchExercices() {
      return new Promise(resolve => {
        exercicesService.searchExercices(this.text_query).then(data => {
          this.count_elements = data.count
          this.result_exos = []
          this.result_exos.push(...data.results)
          resolve(this.count_elements)
        })
      })
    },
    submitExo() {
      this.is_loading = true
      const fd = new FormData()
      fd.append('chapitre', this.form.chapitre)
      fd.append('type', this.form.type)
      if (this.form.is_from_devoir) {
        fd.append('devoir', this.form.devoir)
      }
      if (
        this.form.is_from_livre ||
        (!this.form.is_from_livre && this.form.has_num)
      ) {
        fd.append('num_exo', parseInt(this.form.num_exo))
      }
      if (this.user.niveau == 100) {
        fd.append('niveau', parseInt(this.form.niveau))
        fd.append('voie', this.form.voie)
        fd.append('option', this.form.option)
      } else {
        fd.append('niveau', parseInt(this.user.niveau))
        fd.append('voie', this.user.voie)
        fd.append('option', this.user.option)
      }
      fd.append('prix', this.hasCorrection ? 0 : parseInt(this.form.prix))
      fd.append(
        'date_limite',
        this.hasCorrection
          ? this.minDatetime.toISOString(true)
          : moment(this.form.date_limite).toISOString(true)
      )
      if (this.form.is_from_livre) {
        fd.append('livre', this.form.livre.name)
        fd.append('num_page', parseInt(this.form.livre.num_page))
      } else {
        fd.append('file', this.enonce_file)
      }
      const config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 120000,
        onUploadProgress: function(progressEvent) {
          this.uploadPercentage = parseInt(
            Math.round((progressEvent.loaded / progressEvent.total) * 100)
          )
        }.bind(this)
      }
      this.$store
        .dispatch('exercices/postExercice', { fd, config })
        .then(exo => {
          return new Promise(resolve => {
            this.form = {
              type: null,
              is_from_livre: null,
              chapitre: null,
              niveau: null,
              voie: null,
              option: null,
              has_num: null,
              is_from_devoir: null,
              num_exo: null,
              livre: {
                name: null,
                num_page: null
              },
              date_limite: null,
              prix: 0
            }
            this.result_exos = []
            this.count_elements = 0
            this.current_page = 1
            this.enonce_file = null
            this.is_free = true
            this.$refs.firstStep.reset()
            this.$refs.secondStep.reset()
            this.$refs.thirdStep.reset()
            this.activeStep = 0
            if (!this.hasCorrection) {
              this.$refs.fourthStep.reset()
              this.$refs.fifthStep.reset()
            }
            resolve(exo)
          })
        })
        .then(exo => {
          if (this.hasCorrection) {
            return new Promise(resolve => {
              this.is_loading = true
              this.uploadPercentage = 0
              const fd = new FormData()
              fd.append('enonce_id', exo.id)
              fd.append('file', this.correction_file)
              const config = {
                headers: {
                  'Content-Type': 'multipart/form-data'
                },
                timeout: 120000,
                onUploadProgress: function(progressEvent) {
                  this.uploadPercentage = parseInt(
                    Math.round(
                      (progressEvent.loaded / progressEvent.total) * 100
                    )
                  )
                }.bind(this)
              }
              this.$store
                .dispatch('corrections/postCorrection', { fd, config })
                .then(() => {
                  this.correction_file = null
                  if (this.hasCorrection) {
                    this.$refs.sixthStep.reset()
                  }
                  this.$buefy.toast.open({
                    duration: 5000,
                    message: `Tu viens de gagner ${
                      this.constants['SELFCORREC_POINTS']
                    } ${
                      this.constants['SELFCORREC_POINTS'] > 1
                        ? 'points'
                        : 'point'
                    } !`,
                    type: 'is-success'
                  })
                  resolve(exo)
                })
            })
          } else {
            return new Promise(resolve => {
              resolve(exo)
            })
          }
        })
        .then(exo => {
          this.is_loading = false
          this.$store.dispatch('authentication/getProfileUser').then(
            this.$router.push({
              name: 'exercice',
              params: { id: exo.id }
            })
          )
        })
        .catch(() => {
          this.is_loading = false
          this.$buefy.toast.open({
            duration: 5000,
            message: `L'exo n'a pas pu être posté.
            Il y a sûrement un problème avec le fichier joint. Contacte le support.`,
            type: 'is-danger'
          })
        })
    },
    goNext(next, activeStep) {
      switch (activeStep) {
        case 0:
          var ref = this.$refs.firstStep
          var refscrollfw = this.$refs.scroll2
          var refscrollbw = this.$refs.scroll1
          break
        case 1:
          ref = this.$refs.secondStep
          refscrollfw = this.$refs.scroll3
          refscrollbw = this.$refs.scroll2
          break
        case 2:
          ref = this.$refs.thirdStep
          this.hasCorrection
            ? (refscrollfw = this.$refs.scroll6)
            : (refscrollfw = this.$refs.scroll4)
          refscrollbw = this.$refs.scroll3
          break
        case 3:
          this.hasCorrection
            ? (ref = this.$refs.sixthStep)
            : (ref = this.$refs.fourthStep)
          this.hasCorrection
            ? (refscrollfw = this.$refs.scroll7)
            : (refscrollfw = this.$refs.scroll5)
          this.hasCorrection
            ? (refscrollbw = this.$refs.scroll3)
            : (refscrollbw = this.$refs.scroll4)
          break
        case 4:
          ref = this.$refs.fifthStep
          refscrollfw = this.$refs.scroll7
          refscrollbw = this.$refs.scroll5
          break
        default:
          ref = this.$refs.firstStep
          refscrollfw = this.$refs.scroll2
          refscrollbw = this.$refs.scroll1
      }
      ref.validate().then(success => {
        if (success) {
          if (activeStep == 1) {
            this.searchExercices().then(count => {
              next.action()
              if (count == 0) {
                next.action()
              }
            })
          } else {
            next.action()
          }
          this.$nextTick(() => {
            let toscroll =
              refscrollfw.getBoundingClientRect().top + window.pageYOffset
            window.scrollTo({ top: toscroll, left: 0, behavior: 'smooth' })
          })
        } else {
          this.$nextTick(() => {
            let toscroll =
              refscrollbw.getBoundingClientRect().top + window.pageYOffset
            window.scrollTo({ top: toscroll, left: 0, behavior: 'smooth' })
          })
        }
      })
    }
  }
}
</script>

<style>
.hidden {
  visibility: hidden;
}
</style>
