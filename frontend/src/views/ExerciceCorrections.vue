<template>
  <div class="container is-fluid">
    <div class="columns is-centered">
      <div
        v-for="(correc, index) in corrections"
        class="column is-6"
        :key="correc.id"
      >
        <div class="card">
          <div class="card-content">
            <div class="media">
              <div class="media-left pa-1 has-background-warning">
                <b-icon icon="lock"></b-icon>
              </div>
              <div class="media-content">
                <p>
                  <span class="title is-4">Correction</span>
                </p>
                <span class="subtitle is-6"
                  >par {{ correc.correcteur }}
                  <span>
                    <b-rate :max="5" :disabled="true"></b-rate>
                  </span>
                </span>
              </div>
              <div class="media-right">
                <b-tag type="is-info" size="is-medium"
                  >{{ correc.prix }} pts</b-tag
                >
              </div>
            </div>
            <div class="level">
              <div class="level-left">
                <div class="level-item">
                  <b-tag type="is-success" size="is-medium">
                    <b-icon
                      icon="check"
                      class="mr-1"
                      size="is-small"
                    />Correction vérifiée
                  </b-tag>
                </div>
              </div>

              <div class="level-right">
                <b-button
                  v-if="user.correc.includes(correc.id)"
                  type="is-success"
                  icon-left="arrow-right"
                  @click="
                    $router.push({
                      name: 'correction',
                      params: { id: correc.id }
                    })
                  "
                >
                  Accéder
                </b-button>
                <b-button
                  v-else
                  type="is-warning"
                  icon-left="lock-open"
                  @click="confirm_modal = true"
                >
                  Débloquer
                </b-button>
                <b-modal
                  :active.sync="confirm_modal"
                  has-modal-card
                  trap-focus
                  aria-role="dialog"
                  aria-modal
                >
                  <div class="modal-card" style="width: auto">
                    <header class="modal-card-head">
                      <p class="modal-card-title">Confirmer le prélèvement</p>
                    </header>
                    <div class="modal-card-body">
                      Es-tu sûr de vouloir prélever le montant de
                      {{ correc.prix }} pts sur ta tirelire ? <br />
                      Il te restera {{ user.tirelire - correc.prix }} pts.
                    </div>
                    <footer class="modal-card-foot">
                      <b-button @click="confirm_modal = false"
                        >Annuler</b-button
                      >
                      <b-button
                        @click="confirmUnlock(correc.id, correc.prix)"
                        type="is-success"
                        >Confirmer</b-button
                      >
                    </footer>
                  </div>
                </b-modal>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import exercicesService from "@/services/exercicesService";
import correctionsService from "@/services/correctionsService";
import { mapState } from "vuex";
export default {
  name: "ExerciceCorrections",
  props: {
    id: [Number, String]
  },
  data() {
    return {
      corrections: [],
      confirm_modal: false
    };
  },
  created() {
    exercicesService.getExerciceCorrections(this.id).then(data => {
      this.corrections = data.results;
    });
  },
  computed: {
    ...mapState("authentication", ["user"])
  },
  methods: {
    confirmUnlock(correc_id, prix) {
      this.confirm_modal = false;
      this.collectAndUnlock(correc_id, prix);
    },
    collectAndUnlock(correc_id, prix) {
      let payload = { prix: prix };
      correctionsService.collectAndUnlock(correc_id, payload).then(data => {
        this.$store.dispatch("authentication/getProfileUser");
      });
    }
  }
};
</script>

<style></style>
