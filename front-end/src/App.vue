<template>
  <div id="app" class="relative w-screen h-screen overflow-hidden font-sans">
    <div @click="bolts = ['For testing purposes']" v-if="!bolts.length">
      <NotConnected />
    </div>
    <div v-else class="relative w-full h-full">
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
};
</script>
