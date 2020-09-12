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
        <div class="media-content is-clipped">
          <p v-if="correc.enonce.livre" class="subtitle">
            <span class="title is-5 has-text-grey"
              >{{ correc.enonce.id }}.</span
            >
            {{ correc.enonce.type }}
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
          </div>
        </div>
        <div class="level-right">
          <div class="level-item">
            <b-rate
              v-model="correc.mean_rating"
              class="ml-3"
              size="is-medium"
              disabled
              style="align-items: center;"
            ></b-rate>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import classes from '@/data/niveaux.json'
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
          message: `Es-tu sûr de vouloir prélever le montant de <strong>${
            this.correc.prix
          } pt(s)</strong> sur ta tirelire ? <br> Il te restera <strong>${this
            .user.tirelire -
            this.correc
              .prix} pt(s)</strong> et toutes les corrections de cet exo seront alors débloquées.`,
          confirmText: 'Confirmer',
          cancelText: 'Annuler',
          type: 'is-warning',
          hasIcon: true,
          onConfirm: () => this.collectAndUnlock()
        })
      } else {
        this.$buefy.dialog.confirm({
          title: 'Pas assez de crédit',
          message: `Tu n'as pas assez de crédit dans ta tirelire pour acheter cette correction.`,
          type: 'is-danger',
          hasIcon: true,
          cancelText: 'Fermer',
          confirmText: 'Recharge ta tirelire',
          onConfirm: () => this.$router.push({ name: 'tirelire' })
        })
      }
    },
    collectAndUnlock() {
      this.$store
        .dispatch('corrections/collectAndUnlock', this.correc.id)
        .then(() => {
          this.$store.dispatch('authentication/getProfileUser')
        })

      // correctionsService.collectAndUnlock(this.correc.id, payload).then(() => {
      //   this.$store.dispatch('authentication/getProfileUser')
      // })
    }
  }
}
</script>

<style></style>
