<template>
  <div
    :class="[
      unlocked ? 'border-primary' : 'border-warning',
      'card',
      'correction-preview'
    ]"
    @click="confirmUnlock()"
  >
    <div class="card-content">
      <div v-if="title" class="media">
        <div class="media-content">
          <p v-if="correc.enonce.livre" class="subtitle">
            <span class="title is-5 has-text-grey"
              >{{ correc.enonce.id }}.</span
            >
            {{ correc.enonce.type === 'Exo' ? 'Exo' : 'Act.' }}
            {{ correc.enonce.num_exo }} - Page {{ correc.enonce.num_page }} -
            Sur livre
          </p>
          <p v-else class="subtitle">
            <span class="title is-5 has-text-grey"
              >{{ correc.enonce.id }}.</span
            >
            {{ correc.enonce.type === 'Exo' ? 'Exo' : 'Act.' }}
            {{ correc.enonce.num_exo }}
            - Sur feuille
          </p>
        </div>
      </div>
      <div class="level">
        <div class="level-left">
          <div class="level-item">
            <b-tag v-if="unlocked" type="is-primary" size="is-medium">
              <span class="has-text-white">Débloquée</span>
            </b-tag>
            <b-tag v-else type="is-warning" size="is-medium">
              <span class="has-text-white">À débloquer</span>
            </b-tag>
            <b-rate
              v-model="correc.mean_rating"
              class="ml-3"
              size="is-medium"
              disabled
              style="align-items: center;"
            ></b-rate>
          </div>
        </div>
        <!-- <div class="media-right">
          <b-button
            v-if="unlocked"
            type="is-primary"
            size="is-medium"
            icon-left="arrow-right"
            @click="
              $router.push({ name: 'correction', params: { id: correc.id } })
            "
          >
            Voir
          </b-button>
          <b-button
            v-else
            type="is-warning"
            icon-left="lock-open"
            @click="confirmUnlock()"
          >
            Débloquer ({{ correc.prix }} {{ correc.prix > 1 ? 'pts' : 'pt' }})
          </b-button>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import classes from '@/data/niveaux.json'
import correctionsService from '@/services/correctionsService'
export default {
  name: 'CorrectionPreview',
  props: {
    correc: {
      type: Object,
      default: () => {}
    },
    user: {
      type: Object,
      default: () => {}
    },
    title: {
      type: Boolean,
      default: true
    },
    unlocked: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      classes: classes
    }
  },
  methods: {
    confirmUnlock() {
      if (this.unlocked) {
        this.$router.push({
          name: 'correction',
          params: { id: this.correc.id }
        })
        return
      }
      if (this.user.tirelire >= this.correc.prix) {
        this.$buefy.dialog.confirm({
          title: 'Confirmer le prélèvement',
          message: `Es-tu sûr de vouloir prélever le montant de ${
            this.correc.prix
          } pts sur
                  ta tirelire ? <br> Il te restera ${this.user.tirelire -
                    this.correc.prix} pts.`,
          confirmText: 'Confirmer',
          cancelText: 'Annuler',
          type: 'is-warning',
          hasIcon: true,
          onConfirm: () => this.collectAndUnlock()
        })
      } else {
        this.$buefy.dialog.confirm({
          title: 'Pas assez de crédit',
          message: `Tu n'as pas assez de crédit sur ta cagnotte pour acheter cette correction.`,
          type: 'is-danger',
          hasIcon: true,
          cancelText: 'Fermer',
          confirmText: 'Recharge ta cagnotte',
          onConfirm: () => this.$router.push({ name: 'tirelire' })
        })
      }
    },
    collectAndUnlock() {
      let payload = { prix: this.correc.prix }
      correctionsService.collectAndUnlock(this.correc.id, payload).then(() => {
        this.$store.dispatch('authentication/getProfileUser')
      })
    }
  }
}
</script>

<style></style>
