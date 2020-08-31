<template>
  <div class="container is-fluid">
    <b-loading is-full-page :active.sync="is_loading"></b-loading>
    <div class="columns is-centered">
      <div class="column is-10">
        <div class="box">
          <b-steps v-model="activeStep" animated has-navigation>
            <b-step-item
              label="Montant"
              :style="{ 'min-height': height }"
              clickable
            >
              <ValidationObserver ref="firstStep">
                <hr />
                <h1 class="title has-text-centered">Montant</h1>
                <hr class="mb-5" />

                <div class="columns is-vcentered">
                  <div class="column is-4">
                    <div class="has-text-centered">
                      <div>
                        <img
                          src="@/assets/images/paiement/stripe-secure.png"
                          style="height: 40px;"
                        />
                      </div>
                      <div class="mb-6">
                        <img src="@/assets/images/paiement/mastercard.png" />
                        <img src="@/assets/images/paiement/visa.png" />
                        <img src="@/assets/images/paiement/amex.png" />
                      </div>
                      <div
                        class="box has-background-primary has-text-centered"
                        style="display: inline-block;"
                      >
                        <span
                          v-if="constants"
                          class="has-text-centered title is-5 my-4 has-text-white"
                        >
                          1 € = {{ constants['CHANGE'] }}
                          {{ constants['CHANGE'] > 1 ? 'pts' : 'pt' }}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div class="column is-8">
                    <div>
                      <b-field position="is-centered">
                        <b-radio-button
                          v-model="choice_amount"
                          :native-value="5"
                          :disabled="!!specific_amount"
                          size="is-medium"
                          type="is-tertiary"
                        >
                          <span>5 €</span>
                        </b-radio-button>
                        <b-radio-button
                          v-model="choice_amount"
                          :native-value="10"
                          :disabled="!!specific_amount"
                          size="is-medium"
                          type="is-tertiary"
                        >
                          <span>10 €</span>
                        </b-radio-button>
                        <b-radio-button
                          v-model="choice_amount"
                          :native-value="20"
                          :disabled="!!specific_amount"
                          size="is-medium"
                          type="is-tertiary"
                        >
                          <span>20 €</span>
                        </b-radio-button>
                        <b-radio-button
                          v-model="choice_amount"
                          :native-value="50"
                          :disabled="!!specific_amount"
                          size="is-medium"
                          type="is-tertiary"
                        >
                          <span>50 €</span>
                        </b-radio-button>
                        <b-radio-button
                          v-model="choice_amount"
                          :native-value="100"
                          :disabled="!!specific_amount"
                          size="is-medium"
                          type="is-tertiary"
                        >
                          <span>100 €</span>
                        </b-radio-button>
                      </b-field>

                      <div
                        class="has-text-centered mt-4 mb-2 is-size-5 has-text-weight-bold"
                      >
                        Autre montant ?
                      </div>
                      <ValidationProvider
                        v-slot="{ errors }"
                        slim
                        rules="integer|min_value:5"
                      >
                        <b-field position="is-centered" grouped>
                          <b-field
                            :message="errors"
                            :type="{ 'is-danger': errors[0] }"
                          >
                            <b-input
                              v-model="specific_amount"
                              size="is-medium"
                              @input="typeSpecificAmount()"
                            >
                            </b-input>
                          </b-field>
                          <p class="control">
                            <span class="button is-medium is-static">€</span>
                          </p>
                        </b-field>
                      </ValidationProvider>
                      <p class=" mb-1 mt-4 has-text-centered subtitle">
                        <span class="has-text-weight-bold">
                          {{ amount }} €
                        </span>
                        = {{ gross_amount_points }} pts + {{ bonus_points }} pts
                        bonus =
                        <span class="has-text-weight-bold has-text-danger">
                          {{ net_amount_points }} pts
                        </span>
                      </p>
                    </div>
                  </div>
                </div>
                <hr />
              </ValidationObserver>
            </b-step-item>

            <b-step-item
              :style="{ 'min-height': height }"
              label="Informations bancaires"
              clickable
            >
              <ValidationObserver ref="secondStep">
                <hr />
                <h1 class="title has-text-centered">Informations bancaires</h1>
                <hr />
                <div class="columns is-vcentered">
                  <div class="column is-4">
                    <div class="has-text-centered mb-5">
                      <div>
                        <img
                          src="@/assets/images/paiement/stripe-secure.png"
                          style="height: 40px;"
                        />
                      </div>
                      <div class="mb-6">
                        <img src="@/assets/images/paiement/mastercard.png" />
                        <img src="@/assets/images/paiement/visa.png" />
                        <img src="@/assets/images/paiement/amex.png" />
                      </div>
                    </div>
                  </div>

                  <div class="column is-8">
                    <b-field
                      label="Numéro de carte bancaire"
                      :type="{ 'is-danger': stripeFinalErrors.card_number }"
                      :message="stripeFinalErrors.card_number"
                    >
                      <div ref="card-number"></div>
                    </b-field>

                    <b-field>
                      <ValidationProvider
                        v-slot="{ errors, valid }"
                        slim
                        rules="required"
                      >
                        <b-field
                          expanded
                          :message="errors"
                          :type="{
                            'is-danger': errors[0],
                            'is-success': valid
                          }"
                        >
                          <template slot="label">
                            Nom
                            <b-tooltip
                              type="is-dark"
                              label="Nom associé à la carte bancaire"
                              multilined
                            >
                              <b-icon
                                size="is-small"
                                icon="help-circle-outline"
                              ></b-icon>
                            </b-tooltip>
                          </template>
                          <b-input
                            v-model="name"
                            placeholder="Jean Dupont"
                          ></b-input>
                        </b-field>
                      </ValidationProvider>
                      <!-- <ValidationProvider slim rules="required"
                                        v-slot="{ errors, valid }">
                      <b-field label="Code postal"
                               :message="errors"
                               :type="{'is-danger': errors[0],'is-success': valid}">
                        <b-input v-model="postal_code"></b-input>
                      </b-field>
                    </ValidationProvider> -->
                    </b-field>

                    <b-field
                      label="Date d'expiration"
                      :message="stripeFinalErrors.card_expiry"
                      :type="{ 'is-danger': stripeFinalErrors.card_expiry }"
                    >
                      <div ref="card-expiry"></div>
                    </b-field>

                    <b-field
                      :message="stripeFinalErrors.card_cvc"
                      :type="{ 'is-danger': stripeFinalErrors.card_cvc }"
                    >
                      <template slot="label">
                        CVC
                        <b-tooltip
                          type="is-dark"
                          label="Série de 3 (ou parfois 4) chiffres au dos de la carte"
                          multilined
                        >
                          <b-icon
                            size="is-small"
                            icon="help-circle-outline"
                          ></b-icon>
                        </b-tooltip>
                      </template>
                      <div ref="card-cvc"></div>
                    </b-field>

                    <ValidationProvider
                      v-slot="{ errors, valid }"
                      slim
                      rules="email"
                    >
                      <b-field
                        expanded
                        :message="errors"
                        :type="{
                          'is-danger': errors[0]
                        }"
                      >
                        <template slot="label">
                          Adresse e-mail
                          <b-tooltip
                            type="is-dark"
                            label="Adresse utilisée pour éditer et envoyer la facture de l'achat"
                            multilined
                          >
                            <b-icon
                              size="is-small"
                              icon="help-circle-outline"
                            ></b-icon>
                          </b-tooltip>
                        </template>
                        <b-input v-model="email" expanded></b-input>
                      </b-field>
                    </ValidationProvider>

                    <b-field
                      class="mt-4"
                      expanded
                      :type="{ 'is-danger': !!conditions_error }"
                    >
                      <b-checkbox v-model="conditions_agreed" expanded>
                        <p :class="{ 'has-text-danger': !!conditions_error }">
                          J’accepte les conditions générales de vente de ce
                          site.
                        </p>
                      </b-checkbox>
                    </b-field>
                  </div>
                </div>
                <hr />
              </ValidationObserver>
            </b-step-item>

            <b-step-item label="Résumé" :style="{ 'min-height': height }">
              <hr />
              <h1 class="title has-text-centered">Résumé</h1>
              <hr />
              <div class="has-text-centered">
                <b-icon
                  class="my-5 has-background-success has-text-white icon-rounded"
                  size="is-large"
                  icon="check"
                ></b-icon>
                <p v-if="user" class="subtitle">
                  <span class="has-text-weight-bold">{{ user.username }}</span
                  >, ta cagnotte a été créditée de {{ net_amount_points }} pts !
                </p>
                <p>Merci pour ton achat !</p>
                <b-button
                  tag="router-link"
                  type="is-success"
                  class="m-3"
                  icon-left="home"
                  :to="{ name: 'home' }"
                >
                  Revenir à l'accueil
                </b-button>
              </div>
            </b-step-item>

            <template slot="navigation" slot-scope="{ previous, next }">
              <div class="has-text-centered">
                <a
                  v-if="activeStep != 2"
                  role="button"
                  class="button pagination-previous is-medium"
                  :disabled="previous.disabled"
                  @click.prevent="previous.action"
                >
                  <b-icon icon="chevron-left" />
                </a>
                <a
                  v-if="activeStep == 0"
                  role="button"
                  class="button pagination-next is-medium has-background-success has-text-white"
                  @click.prevent="goNext(next, activeStep)"
                >
                  Valider le montant
                </a>
                <a
                  v-else-if="activeStep == 1"
                  role="button"
                  class="button pagination-next is-medium has-background-success has-text-white"
                  :disabled="next.disabled"
                  @click.prevent="goNext(next, activeStep)"
                >
                  Payer {{ amount }} €
                </a>
              </div>
            </template>
          </b-steps>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ValidationObserver, ValidationProvider } from 'vee-validate'
import { mapState } from 'vuex'
import usersService from '@/services/usersService'
let stripe = Stripe('pk_test_d7oJWEZuJuHZ9L9EDgA2fz2O00LHJU09PY')

var styles = {
  base: {
    iconColor: '#F99A52',
    color: '#32315E',
    fontWeight: 400,
    fontFamily: '"Open Sans", "Helvetica Neue", "Helvetica", sans-serif',
    fontSize: '15px',
    '::placeholder': {
      color: '#CFD7DF'
    }
  },
  invalid: {
    color: '#32315E',
    iconColor: '#fa755a',
    ':-webkit-autofill': {
      color: '#fa755a'
    }
  }
}

export default {
  name: 'Recharge',
  components: {
    ValidationObserver,
    ValidationProvider
  },
  data() {
    return {
      height: '300px',
      activeStep: 0,

      specific_amount: null,
      choice_amount: 5,
      name: null,
      email: null,
      postal_code: null,
      conditions_agreed: null,
      conditions_error: false,

      is_loading: false,

      client_secret: null,
      payment_id: null,

      card_number: null,
      card_expiry: null,
      card_cvc: null,

      stripeErrors: {
        card_number: '',
        card_expiry: '',
        card_cvc: ''
      },

      stripeFinalErrors: {
        card_number: '',
        card_expiry: '',
        card_cvc: ''
      },

      stripeEmpty: {
        card_number: true,
        card_expiry: true,
        card_cvc: true
      }
    }
  },
  computed: {
    ...mapState('authentication', ['user']),
    ...mapState('general', ['constants']),
    amount() {
      if (this.specific_amount) {
        return this.specific_amount
      } else {
        return this.choice_amount
      }
    },
    gross_amount_points() {
      return this.amount * this.constants['CHANGE']
    },
    bonus_points() {
      return Math.floor(
        this.amount * this.constants['CHANGE'] * this.constants['BONUS']
      )
    },
    net_amount_points() {
      return Math.floor(
        this.amount * this.constants['CHANGE'] * (1 + this.constants['BONUS'])
      )
    }
  },
  watch: {
    amount: function() {
      if (this.specific_amount) {
        this.choice_amount = null
      }
    }
  },
  mounted() {
    var elements = stripe.elements()
    this.card_number = elements.create('cardNumber', { style: styles })
    this.card_expiry = elements.create('cardExpiry', { style: styles })
    this.card_cvc = elements.create('cardCvc', { style: styles })
    this.card_number.mount(this.$refs['card-number'])
    this.card_expiry.mount(this.$refs['card-expiry'])
    this.card_cvc.mount(this.$refs['card-cvc'])
    this.listenForErrors()
  },
  methods: {
    typeSpecificAmount() {
      if (!this.specific_amount) {
        this.choice_amount = 5
      }
    },
    listenForErrors() {
      const vm = this
      this.card_number.addEventListener('change', function(event) {
        vm.toggleError('card_number', event)
      })
      this.card_expiry.addEventListener('change', function(event) {
        vm.toggleError('card_expiry', event)
      })
      this.card_cvc.addEventListener('change', function(event) {
        vm.toggleError('card_cvc', event)
      })
    },
    toggleError(type, event) {
      if (event.error) {
        this.stripeErrors[type] = event.error.message
      } else {
        if (event.empty) {
          this.stripeErrors[type] = 'Ce champ est requis'
          this.stripeEmpty[type] = true
        } else {
          this.stripeErrors[type] = ''
          this.stripeEmpty[type] = false
        }
      }
    },
    goNext(next, activeStep) {
      let se = this.stripeErrors
      let sfe = this.stripeFinalErrors
      switch (activeStep) {
        case 0:
          this.$refs.firstStep.validate().then(success => {
            if (success) {
              window.scrollTo({ top: 0, left: 0, behavior: 'smooth' })
              this.confirmAmount(next)
            }
          })
          break
        case 1:
          sfe = Object.assign(sfe, se)
          this.$refs.secondStep.validate().then(success => {
            let cond =
              !se['card_number'] && !se['card_expiry'] && !se['card_cvc']
            for (const [key, value] of Object.entries(this.stripeEmpty)) {
              if (value) {
                sfe[key] = 'Ce champ est requis'
              }
            }
            if (!this.conditions_agreed) {
              this.conditions_error = true
              return
            }
            if (success && cond) {
              window.scrollTo({ top: 0, left: 0, behavior: 'smooth' })
              this.confirmPayment(next)
            }
          })
      }
    },
    confirmAmount(next) {
      next.action()
      let payload = {
        amount: parseInt(this.amount),
        currency: 'eur',
        email: this.email
      }
      usersService.stripe_createPaymentIntent(payload).then(data => {
        this.payment_id = data.id
      })
    },
    confirmPayment(next) {
      this.$buefy.dialog.confirm({
        title: 'Confirmer le paiement',
        message: `Es-tu sûr de vouloir payer <strong>${this.amount} €</strong> ? <br>
        Ta cagnotte sera créditée de <strong>${this.net_amount_points} pts.</strong> `,
        cancelText: 'Annuler',
        confirmText: 'Confirmer',
        type: 'is-warning',
        hasIcon: true,
        onConfirm: () => this.Pay(next)
      })
    },
    Pay(next) {
      this.is_loading = true
      let data = {
        type: 'card',
        card: this.card_number,
        billing_details: {
          name: this.name
        }
      }
      stripe
        .createPaymentMethod(data)
        .then(result => {
          let payload = {
            payment_id: this.payment_id,
            payment_method_id: result.paymentMethod['id'],
            email: this.email
          }
          usersService.stripe_validatePayment(payload).then(response => {
            this.handleServerResponse(response)
            next.action()
          })
        })
        .catch(() => {
          this.is_loading = false
          this.$buefy.toast.open({
            duration: 5000,
            message: `Le paiment n'a pas abouti !
                    Ta carte n'a pas été débitée. <br>
                    Vérifie les informations données.`,
            type: 'is-danger'
          })
        })
    },
    handleServerResponse(response) {
      if (response.data.requires_action) {
        stripe
          .handleCardAction(response.data.payment_intent_client_secret)
          .then(this.handleStripeJsResult)
      } else {
        this.$store.dispatch('authentication/getProfileUser').then(() => {
          this.is_loading = false
          this.$buefy.toast.open({
            duration: 3000,
            message: `Le paiment a bien été effectué !
                      Ta tirelire a été créditée. <br>`,
            type: 'is-success'
          })
        })
      }
    },
    handleStripeJsResult() {
      let payload = {
        payment_id: this.payment_id
      }
      usersService
        .stripe_validatePayment(payload)
        .then(this.handleServerResponse)
        .catch(() => {
          this.is_loading = false
          this.$buefy.toast.open({
            duration: 5000,
            message: `Le paiment n'a pas abouti !
                    Ta carte n'a pas été débitée. <br>
                    Vérifie les informations données.`,
            type: 'is-danger'
          })
        })
    }
  }
}
</script>

<style scoped lang="scss">
.label {
  color: green !important;
}

.help {
  visibility: hidden !important;
  color: blue !important;
}

.StripeElement {
  padding: calc(0.6em - 1px) calc(0.625em - 1px);
  border-radius: 4px;
  border: 1px solid #dbdbdb !important;
  box-shadow: inset 0 1px 2px rgba(10, 10, 10, 0.1) !important;
  -webkit-box-shadow: inset 0 1px 2px rgba(10, 10, 10, 0.1) !important;
}

.StripeElement--invalid {
  border-color: $danger !important;
}

img {
  height: 30px;
}
</style>
