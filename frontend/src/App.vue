<template>
<div>
  <NavbarComponent />
  <div class="app-container">
    <transition name="fade"
                mode="out-in">
      <keep-alive include="search">
        <router-view :key="$route.path +
        ($route.params.id ? $route.params.id : '').toString()" />
      </keep-alive>
    </transition>
  </div>
  <footer class="footer has-background-primary"
          style="margin-top:50px;"></footer>
</div>
</template>

<script>
require("@/assets/css/animate.css");
import { mapState } from "vuex";
import NavbarComponent from "@/components/layout/Navbar.vue";

export default {
  name: "App",
  components: {
    NavbarComponent
  },
  created() {
    this.$store.dispatch("authentication/getProfileUser");
    this.$store.dispatch("general/updateConstants");
    this.$store.dispatch("exercices/loadPostedExercices");
    this.$store.dispatch("exercices/loadLikedExercices");
    this.$store.dispatch("corrections/loadPostedCorrections");
    this.$store.dispatch("corrections/loadUnlockedCorrections");
  },
};
</script>

<style lang="scss">
@import "@/assets/scss/core.scss";
</style>

<style lang="css">
.app-container {
  position: relative;
  width: 100%;
  min-height: 1000px;
  margin-top: 0px;
  padding-top: 50px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
