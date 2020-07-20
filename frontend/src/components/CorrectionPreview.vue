<template>
<div class="card">
  <div class="card-content">
    <div class="media">
      <div v-if="!unlocked"
           class="media-left pa-1 has-background-warning">
        <b-icon icon="lock"></b-icon>
      </div>
      <div v-else
           class="media-left pa-1 has-background-success">
        <b-icon icon="lock-open"></b-icon>
      </div>
      <!-- <div class="media-content">
        <div class="subtitle is-size-6">
          <p>
            Posté le <strong>{{ correc.date_created | dateFormatter }}</strong>
          </p>
        </div>
      </div> -->
      <div class="media-content">
        <p v-if="correc.enonce.livre"
           class="subtitle">
          <span class="title is-5 has-text-grey">{{ correc.enonce.id }}.</span>
          {{correc.enonce.type === 'correc.enonce'? 'Exo': 'Act.' }}
          {{ correc.enonce.num_exo }} - Page {{ correc.enonce.num_page }} - Sur
          livre
        </p>
        <p v-else
           class="subtitle">
          <span class="title is-5 has-text-grey">{{ correc.enonce.id }}.</span>
          {{correc.enonce.type === 'correc.enonce'? 'Exo': 'Act.' }} {{ correc.enonce.num_exo }}
          - Sur feuille
        </p>
      </div>
      <div class="media-right">
        <b-button v-if="unlocked"
                  type="is-success"
                  size="is-medium"
                  icon-left="arrow-right"
                  @click="
              $router.push({ name: 'correction', params: { id: correc.id } })
            ">
          Voir
        </b-button>
        <b-button v-else
                  type="is-warning"
                  icon-left="lock-open"
                  @click="confirmUnlock()">
          Débloquer ({{ correc.prix }} {{correc.prix > 1 ? 'pts': 'pt'}})
        </b-button>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import classes from "@/data/classes.json";
import exercicesService from "@/services/exercicesService";
import correctionsService from "@/services/correctionsService";
export default {
  name: "CorrectionPreview",
  props: {
    correc: Object,
    user: Object,
    unlocked: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      classes: classes
    };
  },
  methods: {
    confirmUnlock() {
      if (this.user.tirelire >= this.correc.prix) {
        this.$buefy.dialog.confirm({
          title: "Confirmer le prélèvement",
          message: `Es-tu sûr de vouloir prélever le montant de ${this.correc.prix} pts sur
                  ta tirelire ? <br> Il te restera ${this.user.tirelire - this.correc.prix} pts.`,
          confirmText: "Confirmer",
          cancelText: "Annuler",
          type: "is-warning",
          hasIcon: true,
          onConfirm: () => this.collectAndUnlock()
        });
      } else {
        this.$buefy.dialog.confirm({
          title: "Pas assez de crédit",
          message: `Tu n'as pas assez de crédit sur ta cagnotte pour acheter cette correction.`,
          type: "is-danger",
          hasIcon: true,
          cancelText: "Fermer",
          confirmText: "Recharge ta cagnotte",
          onConfirm: () => this.$router.push({ name: "tirelire" })
        });
      }
    },
    collectAndUnlock() {
      let payload = { prix: this.correc.prix };
      correctionsService
        .collectAndUnlock(this.correc.id, payload)
        .then(data => {
          this.$store.dispatch("authentication/getProfileUser");
        });
    }
  }
};
</script>

<style></style>
