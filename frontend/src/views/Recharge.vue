<template>
<div class="container">
  <header class="modal-card-head">
    <p class="modal-card-title">Rechargez votre compte</p>
  </header>
  <section class="modal-card-body">
    <form @submit.prevent="recharge()">
      <b-field label="Montant">
        <b-field>
          <b-input v-model="amount">
          </b-input>
          <p class="control">
            <span class="button is-static">€</span>
          </p>
        </b-field>
      </b-field>

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
      </b-field>

      <b-field label="Code postal">
        <b-input v-model="postal_code"></b-input>
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


      <button class="button is-primary is-fullwidth"
              type="submit">Recharger</button>
    </form>

  </section>
</div>
</template>

<script>
import { mapState } from 'vuex';
import usersService from '@/services/usersService';
let stripe = Stripe('pk_test_IXadVylpLM9tE8ENmliIkZHB00vhacO7Tu')


export default {
  name: "Recharge",
  data() {
    return {
      amount: 5,
      last_name: '',
      first_name: '',
      postal_code: null,

      client_secret: null,

      card_number: null,
      card_expiry: null,
      card_cvc: null
    }
  },
  mounted() {
    this.$store.dispatch('files/loadFiles')
    var elements = stripe.elements()
    this.card_number = elements.create('cardNumber')
    this.card_expiry = elements.create('cardExpiry')
    this.card_cvc = elements.create('cardCvc')
    this.card_number.mount(this.$refs['card-number']);
    this.card_expiry.mount(this.$refs['card-expiry']);
    this.card_cvc.mount(this.$refs['card-cvc']);
  },
  computed: {},
  methods: {
    recharge() {
      let payload = {
        amount: parseFloat(this.amount),
        currency: 'eur',
      }
      usersService.getClientSecret(payload)
        .then(data => {
          this.client_secret = data.client_secret;
        })
        .then((data) => {
          this.confirmPayment()
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
      stripe.confirmCardPayment(this.client_secret, data)
        .then(function(result) {
          if (result.error) {
            console.log(result.error.message);
          } else {
            if (result.paymentIntent.status === 'succeeded') {
              alert('success')
            }
          }
        });
    }

  },
}
</script>

<style>
</style>
