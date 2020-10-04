<template>
  <div
    v-if="notif.action_object"
    :class="[
      notif.unread ? 'unread' : 'read',
      'box',
      'notif',
      'has-text-weight-box'
    ]"
    @click="redirect()"
  >
    <div
      v-if="notif.verb == 'correction_posted'"
      style="align-items: center;"
      class="media"
    >
      <div class="media-left">
        <b-icon icon="check" type="is-primary"></b-icon>
      </div>
      <div class="media-content">
        <div class="content is-size-5">
          <p>
            Ton exo n°{{ notif.target.id }} a été corrigé
            <span
              v-if="notif.action_object.before_deadline"
              class="has-text-weight-bold"
              >avant la date limite</span
            >
            <span v-else>après la date limite</span>.
          </p>
        </div>
      </div>
      <div
        v-if="notif.action_object"
        class="media-right has-text-danger has-text-weight-bold"
      >
        <p class="">
          -
          {{ notif.action_object.before_deadline ? notif.target.prix : 0 }} pts
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotificationComponent',
  props: {
    notif: {
      type: Object,
      default: null
    }
  },
  data() {
    return {}
  },
  computed: {},
  methods: {
    redirect() {
      let verb = this.notif.verb
      this.$emit('update:open', false)
      switch (verb) {
        case 'correction_posted':
          this.$store
            .dispatch('authentication/setNotificationRead', this.notif.id)
            .then(
              this.$router.push({
                name: 'exercice',
                params: { id: this.notif.target.id }
              })
            )
          return
        default:
          return
      }
    }
  }
}
</script>

<style lang="scss">
.notif {
  cursor: pointer;
  margin-bottom: 0 !important;
  border-radius: 0 !important;

  &.read:hover {
    background-color: whitesmoke !important;
  }

  &.unread {
    background-color: tint($tertiary, 90%) !important;

    &:hover {
      background-color: tint($tertiary, 80%) !important;
    }
  }

  &:hover {
    -webkit-box-shadow: 8px 7px 21px -3px rgba(0, 0, 0, 0.75);
    -moz-box-shadow: 8px 7px 21px -3px rgba(0, 0, 0, 0.75);
    box-shadow: 8px 7px 21px -3px rgba(0, 0, 0, 0.75);
  }
}
</style>
