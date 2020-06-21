<template>
  <div class="container is-fluid">
    <div class="columns is-multiline">
      <div class="column is-6">
        <div class="box">
          <h1 class="title">Mes corrections postées</h1>
        </div>
        <div
          v-for="(correc, index) in postedCorrections"
          class="column is-12"
          :key="correc.id"
        >
          <CorrectionPreview
            :correc="correc"
            :user="user"
            :unlocked="false"
          ></CorrectionPreview>
        </div>
      </div>
      <div class="column is-6">
        <div class="box">
          <h1 class="title">Mes corrections débloquées</h1>
        </div>
        <div
          v-for="(correc, index) in unlockedCorrections"
          class="column is-12"
          :key="correc.id"
        >
          <CorrectionPreview
            :correc="correc"
            :user="user"
            :unlocked="false"
          ></CorrectionPreview>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import correctionsService from "@/services/correctionsService";
import CorrectionPreview from "@/components/CorrectionPreview.vue";
import { mapState } from "vuex";
export default {
  name: "MyCorrections",
  components: {
    CorrectionPreview
  },
  data() {
    return {};
  },
  mounted() {
    this.$store.dispatch("corrections/loadPostedCorrections");
    this.$store.dispatch("corrections/loadUnlockedCorrections");
  },
  computed: {
    ...mapState("corrections", ["postedCorrections"]),
    ...mapState("corrections", ["unlockedCorrections"]),
    ...mapState("authentication", ["user"])
  },
  methods: {
    deleteCorrection(id, data_index) {
      this.$store.dispatch("corrections/deleteCorrection", { id, data_index });
    }
  }
};
</script>

<style>
.upload,
.upload-draggable {
  width: 100%;
}
</style>
