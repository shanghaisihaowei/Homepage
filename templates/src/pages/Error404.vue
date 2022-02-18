<template>
  <div class="fullscreen bg-blue flex flex-center">
    <div class="text-center">
      <lottie
        width="1000"
        @click="this.$router.push('/')"
        :options="defaultOptions"
        v-on:animCreated="handleAnimation"
      />
      <q-btn
        class="q-mt-xl text-h6"
        color="white"
        text-color="blue"
        unelevated
        to="/"
        label="Go Home"
        no-caps
      />
    </div>
  </div>
</template>

<script>
import lottie from "vue-lottie";
import notFind from "../../public/statics/404/404.json";

export default {
  name: "Error404",
  components: {
    lottie,
  },
  data() {
    return {
      defaultOptions: {
        animationData: notFind,
        loop: true,
        autoplay: true,
        style: "width:100px;height:100px",
      },
      defaultAnim: "",
    };
  },

  methods: {
    handleAnimation(anim) {
      this.defaultAnim = anim;
    },
  },
};
</script>
