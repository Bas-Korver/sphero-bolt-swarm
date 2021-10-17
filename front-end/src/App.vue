<template>
  <div id="app" class="relative w-screen h-screen overflow-hidden font-sans">
    <div v-if="!bolts.length" class="fixed w-full h-full z-50">
      <NotConnected @connected="connectedToBOLT" />
    </div>
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
