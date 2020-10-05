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
        <div class="content is-size-5" style="line-height: 1em;">
          <p>
            Ton exo n°{{ notif.target.id }} a été corrigé
            <span
              v-if="notif.action_object.before_deadline"
              class="has-text-weight-bold"
              >avant la date limite</span
            >
            <span v-else>après la date limite</span>.
            <br />
            <span class="is-size-7 has-text-grey">{{ elapsed_time_text }}</span>
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
import moment from 'moment'
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
  computed: {
    diff_secondes() {
      let date1 = moment()
      let date2 = moment(this.notif.timestamp)
      let diffSecondes = date1.diff(date2, 'seconds')
      return diffSecondes
    },
    diff_minutes() {
      let date1 = moment()
      let date2 = moment(this.notif.timestamp)
      let diffMinutes = date1.diff(date2, 'minutes')
      return diffMinutes
    },
    diff_hours() {
      let date1 = moment()
      let date2 = moment(this.notif.timestamp)
      let diffHours = date1.diff(date2, 'hours')
      return diffHours
    },
    diff_days() {
      let date1 = moment()
      let date2 = moment(this.notif.timestamp)
      let diffDays = date1.diff(date2, 'days')
      return diffDays
    },
    elapsed_time_text() {
      if (this.diff_minutes < 1) {
        return 'Il y a ' + this.diff_secondes.toString() + ' seconde(s)'
      } else if (this.diff_hours < 1) {
        return 'Il y a ' + this.diff_minutes.toString() + ' minute(s)'
      } else if (this.diff_days < 2) {
        return 'Il y a ' + this.diff_hours.toString() + ' heure(s)'
      } else {
        return 'Il y a ' + this.diff_days.toString() + ' jour(s)'
      }
    }
  },
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
