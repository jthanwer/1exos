<template>
  <div>
    <div v-if="imgIsLoaded" class="field is-grouped is-grouped-centered">
      <div class="control">
        <b-button
          type="is-tertiary"
          icon-left="rotate-left"
          @click="rotateLeft()"
        ></b-button>
      </div>
      <div class="control">
        <b-button
          type="is-tertiary"
          icon-left="rotate-right"
          @click="rotateRight()"
        ></b-button>
      </div>
    </div>
    <div
      ref="container"
      :style="
        `height: ${heightContainer}px; align-items: center; justify-content: center;`
      "
      class="is-flex"
    >
      <img
        ref="img"
        :style="
          `transform: rotate(${rotationImage}deg); height: ${heightImage}px; width: ${widthImage}px;`
        "
        :src="value"
        @load="getDimensions()"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'ImageContainer',
  props: {
    value: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      rotationImage: 0,
      imgIsLoaded: false,
      initialWidthImage: null,
      initialHeightImage: null,
      heightImage: null,
      widthImage: null,
      heightContainer: null,
      widthContainer: null,
      initialHeightContainer: null,
      initialWidthContainer: null,
      aspectRatio: null
    }
  },
  methods: {
    rotateRight() {
      this.rotationImage += 90

      if (Math.abs(this.rotationImage % 180) == 90) {
        if (this.aspectRatio >= 1) {
          this.heightContainer = this.widthImage
        } else {
          this.heightImage = this.widthContainer
          this.widthImage = this.heightImage * this.aspectRatio
          this.heightContainer = this.widthImage
        }
      } else {
        this.heightContainer = this.initialHeightContainer
        this.heightImage = this.initialHeightImage
        this.widthImage = this.initialWidthImage
      }
    },
    rotateLeft() {
      this.rotationImage -= 90

      if (Math.abs(this.rotationImage % 180) == 90) {
        if (this.aspectRatio >= 1) {
          this.heightContainer = this.widthImage
        } else {
          this.heightImage = this.widthContainer
          this.widthImage = this.heightImage * this.aspectRatio
          this.heightContainer = this.widthImage
        }
      } else {
        this.heightContainer = this.initialHeightContainer
        this.heightImage = this.initialHeightImage
        this.widthImage = this.initialWidthImage
      }
    },
    getDimensions() {
      let img = this.$refs['img']
      let naturalWidth = img.naturalWidth
      let naturalHeight = img.naturalHeight
      this.aspectRatio = naturalWidth / naturalHeight

      let container = this.$refs['container']
      this.heightContainer = container.clientHeight
      this.widthContainer = container.clientWidth

      this.widthImage = this.widthContainer
      this.heightImage = this.widthImage / this.aspectRatio
      this.heightContainer = this.heightImage

      this.initialWidthImage = this.widthImage
      this.initialHeightImage = this.heightImage
      this.initialHeightContainer = this.heightContainer
      this.initialWidthContainer = this.widthContainer

      this.imgIsLoaded = true
    }
  }
}
</script>

<style></style>
