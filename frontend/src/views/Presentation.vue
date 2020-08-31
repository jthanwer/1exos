<template>
  <section class="section">
    <div class="container">
      <div class="content">
        <h1 class="title has-text-primary has-text-centered is-2">
          Présentation du site
        </h1>
        <h2 class="subtitle has-text-tertiary">
          1 - Comment ça marche ?
        </h2>
        <ol class="is-size-6" style="line-height: 1.5em;">
          <li>
            Inscris-toi sur le site puis connecte-toi. 4 points te sont offerts
            lors de ton inscription.
          </li>
          <li>
            Cherche ton exo sur le site à l'aide des différents filtres proposés
            :
            <ul>
              <li>
                <strong
                  >Si tu le trouves et qu'une correction est disponible</strong
                >, tu peux la débloquer en utilisant tes points.
              </li>
              <li>
                <strong
                  >Si tu le trouves mais qu'aucune correction n'est
                  disponible</strong
                >, il te faudra attendre que quelqu'un poste une correction.
              </li>
              <li>
                <strong>Si tu ne le trouves pas</strong>, tu peux demander une
                correction en offrant un certain nombre de points en échange.
              </li>
            </ul>
          </li>
          <li>
            Si tu n’as pas assez de points, tu peux recharger ta tirelire :
            <ul>
              <li>Soit avec de l’argent réel (1 € = 4 points).</li>
              <li>
                Soit en corrigeant des exos postés par d'autres utilisateurs.
              </li>
            </ul>
          </li>
        </ol>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Presentation',
  data() {
    return {}
  },
  computed: {}
}
</script>

<style></style>
