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
      <div class="media-content">
        <p class="title is-4">
          n° {{correc.enonce.num_page}} p. {{correc.enonce.num_exo}} - {{correc.enonce.livre}}
        </p>
        <div class="subtitle is-size-6">
          <p>Posté par <strong>{{correc.enonce.posteur.username}}</strong> le {{correc.date_created | dateFormatter}}</p>
          <p>Niveau : {{classes[correc.enonce.posteur.classe]}}</p>
        </div>
      </div>
      <div class="media-right">
        <b-tag v-if="!unlocked"
               type="is-info"
               size="is-medium">Prix : {{correc.prix}} pts</b-tag>
      </div>
    </div>
    <div class="level">
      <div class="level-left">
      </div>

      <div class="level-right">
        <b-button v-if="unlocked"
                  type="is-success"
                  size="is-medium"
                  icon-left="arrow-right"
                  @click="$router.push({name: 'correction', params: {id: correc.id}})">
          Voir
        </b-button>
        <b-button v-else
                  type="is-warning"
                  icon-left="lock-open"
                  @click="confirm_modal = true">
          Débloquer
        </b-button>
        <b-modal :active.sync="confirm_modal"
                 has-modal-card
                 trap-focus
                 aria-role="dialog"
                 aria-modal>
          <div class="modal-card"
               style="width: auto">
            <header class="modal-card-head">
              <p class="modal-card-title">Confirmer le prélèvement</p>
            </header>
            <div class="modal-card-body">
              Es-tu sûr de vouloir prélever le montant de {{correc.prix}} pts sur
              ta tirelire ? <br> Il te restera {{user.tirelire - correc.prix}} pts.
            </div>
            <footer class="modal-card-foot">
              <b-button @click="confirm_modal = false">Annuler</b-button>
              <b-button @click="confirmUnlock(correc.id, correc.prix)"
                        type="is-success">Confirmer</b-button>
            </footer>
          </div>
        </b-modal>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import classes from "@/data/classes.json"
import exercicesService from '@/services/exercicesService'
import correctionsService from '@/services/correctionsService'
export default {
  name: 'CorrectionPreview',
  props: {
    correc: Object,
    user: Object,
    unlocked: {
      type: Boolean,
      default: false
    },
  },
  data() {
    return {
      classes: classes,
      confirm_modal: false
    }
  },
  methods: {
    confirmUnlock(correc_id, prix) {
      this.confirm_modal = false
      this.collectAndUnlock(correc_id, prix)
    },
    collectAndUnlock(correc_id, prix) {
      let payload = { 'prix': prix }
      correctionsService.collectAndUnlock(correc_id, payload)
        .then(data => {
          this.$store.dispatch('authentication/getProfileUser')
        })
    }
  },
}
</script>

<style>
</style>
