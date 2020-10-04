<template>
  <footer class="footer has-background-primary" style="margin-top:50px;">
    <div class="columns is-centered">
      <div class="column is-3">
        <h1 class="title is-3 has-text-white-ter">À propos</h1>
        <router-link class="has-text-white" :to="{ name: 'presentation' }">
          <h2>Présentation du site</h2>
        </router-link>
        <router-link class="has-text-white" :to="{ name: 'standards-qualite' }">
          <h2>Comment bien poster ?</h2>
        </router-link>
      </div>
      <div class="column is-3">
        <h1 class="title is-3 has-text-white-ter">Nous contacter</h1>
        <router-link class="has-text-white" :to="{ name: 'home' }">
          <h2>support@1exo.fr</h2>
        </router-link>
      </div>
      <div class="column is-3">
        <h1 class="title is-3 has-text-white-ter">Cadre légal</h1>
        <router-link class="has-text-white" :to="{ name: 'mentions-legales' }">
          <h2>Mentions légales</h2>
        </router-link>
        <router-link class="has-text-white" :to="{ name: 'cgv' }">
          <h2>CGV</h2>
        </router-link>
        <router-link class="has-text-white" :to="{ name: 'cgu' }">
          <h2>CGU</h2>
        </router-link>
        <router-link class="has-text-white" :to="{ name: 'pdc' }">
          <h2>Politique de confidentialité</h2>
        </router-link>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FooterComponent'
}
</script>

<style></style>
