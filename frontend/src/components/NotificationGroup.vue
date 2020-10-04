<template>
  <div class="notification-group">
    <div class="box notif-title has-text-centered has-background-tertiary">
      <h1 class="title is-size-5 has-text-white">Notifications</h1>
    </div>
    <div
      v-if="notifications.length == 0"
      class="box notif-title has-text-centered"
    >
      <h1 class="title is-size-6">Aucune notification</h1>
    </div>
    <Notification
      v-for="notification in notifications"
      v-else
      :key="notification.id"
      :notif="notification"
      @update:open="$emit('update:active', $event)"
    />
  </div>
</template>

<script>
import Notification from '@/components/Notification.vue'
export default {
  name: 'NotificationGroupComponent',
  components: {
    Notification
  },
  props: {
    value: {
      type: Array,
      default: null
    },
    active: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      notifications: this.value
    }
  },
  computed: {},
  methods: {}
}
</script>

<style lang="scss">
.notification-group {
  position: absolute;
  right: 0px;
  z-index: 25;
  border: 2px solid $primary;
  min-width: 40%;
  max-width: 40%;
  @media (max-width: 1028px) {
    min-width: 100%;
    max-width: 100%;
  }
}

.notif-title {
  margin-bottom: 0 !important;
  border-radius: 0 !important;
}
</style>
