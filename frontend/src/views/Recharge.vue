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

          <b-step-item label="Montant"
                       :style="{'min-height': height}"
                       clickable>
            <hr>
            <h1 class="title has-text-centered">Montant</h1>
            <hr class="mb-10">
            <b-field position="is-centered">
              <b-radio-button v-model="amount"
                              native-value="5"
                              :disabled="specific_amount"
                              size='is-large'
                              type="is-info">
                <span>5 €</span>
              </b-radio-button>
              <b-radio-button v-model="amount"
                              native-value="10"
                              :disabled="specific_amount"
                              size='is-large'
                              type="is-info">
                <span>10 €</span>
              </b-radio-button>
              <b-radio-button v-model="amount"
                              native-value="15"
                              :disabled="specific_amount"
                              size='is-large'
                              type="is-info">
                <span>15 €</span>
              </b-radio-button>
              <b-radio-button v-model="amount"
                              native-value="20"
                              :disabled="specific_amount"
                              size='is-large'
                              type="is-info">
                <span>20 €</span>
              </b-radio-button>
              <b-button @click="specific_amount = !specific_amount"
                        class="ml-2"
                        size='is-large'
                        :type="{'is-info': specific_amount}">
                <span>Autre montant</span>
              </b-button>
            </b-field>

            <b-field v-if="specific_amount"
                     position="is-centered">
              <b-input size="is-large"
                       v-model="amount"
                       placeholder="Entrez le montant voulu">
              </b-input>
              <p class="control">
                <span class="button is-large is-static">€</span>
              </p>
            </b-field>
          </b-step-item>

          <b-step-item :style="{'min-height': height}"
                       label="Informations bancaires"
                       clickable>
            <hr>
            <h1 class="title has-text-centered"> Informations bancaires</h1>
            <hr>
            <b-field label="Numéro de carte">
              <div v-model="card_number"
                   class="m-3"
                   ref="card-number"></div>
            </b-field>

            <b-field grouped>
              <b-field label="Nom (sur la carte bancaire)">
                <b-input v-model="last_name"></b-input>
              </b-field>
              <b-field label="Prénom">
                <b-input v-model="first_name"></b-input>
              </b-field>
              <b-field label="Code postal">
                <b-input v-model="postal_code"></b-input>
              </b-field>
            </b-field>

            <b-field label="Date d'expiration">
              <div v-model="card_expiry"
                   class="m-3"
                   ref="card-expiry"></div>
            </b-field>

            <b-field label="CVC">
              <div v-model="card_cvc"
                   class="m-3"
                   ref="card-cvc"></div>
            </b-field>
          </b-step-item>

          <b-step-item label="Confirmation"
                       :style="{'min-height': height}">
            <hr>
            <h1 class="title has-text-centered">Confirmation</h1>
            <hr>
            <div class="columns is-centered">
              <div class="column is-6">
                <p class="subtitle">Utilisateur : <span class="is-pulled-right">{{user.username}}</span></p>
                <p class="subtitle">Montant : <span class="is-pulled-right">{{amount}} €</span></p>
              </div>
            </div>

          </b-step-item>

          <template slot="navigation"
                    slot-scope="{previous, next}">
            <div class="has-text-centered">
              <a role="button"
                 class="pagination-previous"
                 :disabled="previous.disabled"
                 @click.prevent="previous.action">
                <b-icon icon="chevron-left" />
              </a>
              <a v-if="activeStep == 0"
                 role="button"
                 :disabled="!amount"
                 class="pagination-next has-background-info has-text-white"
                 @click.prevent="confirmAmount(next)">
                Valider le montant
              </a>
              <a v-else-if="activeStep == 1"
                 role="button"
                 class="pagination-next has-background-info has-text-white"
                 :disabled="next.disabled"
                 @click.prevent="next.action">
                Voir le résumé
              </a>
              <a v-else
                 role="button"
                 class="pagination-next has-background-success has-text-white"
                 @click.prevent="confirmPayment()">
                Valider le paiement
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
import { mapState } from 'vuex';
import usersService from '@/services/usersService';
let stripe = Stripe('pk_test_IXadVylpLM9tE8ENmliIkZHB00vhacO7Tu')

var styles = {
  base: {
    iconColor: '#F99A52',
    color: '#32315E',
    lineHeight: '48px',
    fontWeight: 400,
    fontFamily: '"Open Sans", "Helvetica Neue", "Helvetica", sans-serif',
    fontSize: '15px',

    '::placeholder': {
      color: '#CFD7DF',
    }
  },
}

export default {
  name: "Recharge",
  data() {
    return {
      height: '300px',
      activeStep: 0,

      specific_amount: false,
      amount: null,
      last_name: 'Thanwerdas',
      first_name: 'Joel',
      postal_code: 92160,

      is_loading: false,

      client_secret: null,

      card_number: null,
      card_expiry: null,
      card_cvc: null
    }
  },
  mounted() {
    var elements = stripe.elements()
    this.card_number = elements.create('cardNumber', { style: styles })
    this.card_expiry = elements.create('cardExpiry')
    this.card_cvc = elements.create('cardCvc')
    this.card_number.mount(this.$refs['card-number']);
    this.card_expiry.mount(this.$refs['card-expiry']);
    this.card_cvc.mount(this.$refs['card-cvc']);
  },
  computed: {
    ...mapState('authentication', ['user'])
  },
  methods: {
    confirmAmount(next) {
      next.action()
      let payload = {
        amount: parseFloat(this.amount),
        currency: 'eur',
      }
      usersService.getClientSecret(payload)
        .then(data => {
          this.client_secret = data.client_secret;
        })
    },
    confirmPayment() {
      let data = {
        payment_method: {
          card: this.card_number,
          billing_details: {
            name: `${this.first_name} ${this.last_name}`,
            address: {
              postal_code: this.postal_code
            }
          }
        }
      }
      this.is_loading = true
      stripe.confirmCardPayment(this.client_secret, data)
        .then(result => {
          if (result.error) {
            console.log(result.error.message);
            this.is_loading = false;
            this.$buefy.toast.open({
              duration: 5000,
              message: `Le paiment n'a pas abouti !
              Votre carte n'a pas été créditée. <br>
              Vérifiez les informations données.`,
              type: 'is-danger'
            })
          } else {
            if (result.paymentIntent.status === 'succeeded') {
              usersService.validatePayment(result.paymentIntent)
                .then((data) => {
                  return this.$store.dispatch('authentication/getProfileUser')
                }).then((data) => {
                  this.is_loading = false;
                  this.$buefy.toast.open({
                    message: `Le paiment a bien été effectué !
                     Votre tirelire a été créditée. <br>
                     Vous êtes maintenant redirigé.`,
                    type: 'is-success'
                  })
                  setTimeout(() => this.$router.push({ name: 'moneybox' }), 1000);
                })
            }
          }
        });
    }

  },
}
</script>

<style>
div.StripeElement {
  border-radius: 4px;
  border: 1px solid #dbdbdb !important;
  -webkit-box-shadow: inset 0 1px 2px rgba(10, 10, 10, 0.1);
  height: 40px;
}
</style>
