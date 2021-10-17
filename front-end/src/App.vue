<template>
  <div id="app" class="relative w-screen h-screen overflow-hidden font-sans">
    <transition name="transition-not-connected">
      <div v-if="!bolts.length" class="fixed w-full h-full z-50">
        <NotConnected @connected="connectedToBOLT" />
      </div>
    </transition>
    <div class="relative w-full h-full">
      <Index />
    </div>
  </div>
</template>

<script>
import Index from "./components/Index.vue";
import NotConnected from "./components/NotConnected.vue";
export default {
  name: "App",
  data() {
    return {
      bolts: [],
    };
  },
  components: {
    Index,
    NotConnected,
  },
  methods: {
    connectedToBOLT(bolts) {
      this.bolts = bolts;
    },
  },
};
</script>

<style scoped>
.transition-not-connected-enter-active,
.transition-not-connected-leave-active {
  transition: all 400ms;
}
.transition-not-connected-enter,
.transition-not-connected-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
