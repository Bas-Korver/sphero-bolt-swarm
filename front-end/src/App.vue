<template>
  <div id="app" class="relative w-screen h-screen overflow-hidden font-sans">
    <transition name="transition-not-connected">
      <div v-if="!bolts.length" class="fixed w-full h-full z-50">
        <div
          v-if="loading.active"
          class="w-full h-full flex flex-col items-center justify-center"
        >
          <h1 class="text-xl font-bold text-gray-900 mb-8">
            {{ loading.text }}
          </h1>

          <Loading />
        </div>
        <NotConnected v-else @connected="connectedToBOLT" />
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
import Loading from "./components/others/Loading";
export default {
  name: "App",
  data() {
    return {
      bolts: [],
      loading: {
        active: false,
        text: "",
      },
      errors: false,
    };
  },
  components: {
    Loading,
    Index,
    NotConnected,
  },
  methods: {
    connectedToBOLT(bolts) {
      this.bolts = bolts;
    },
  },
  mounted() {
    this.loading = {
      active: true,
      text: "Fetching connected BOLTs...",
    };

    this.$http
      .get("")
      .then((response) => {
        this.bolts = response.data;
      })
      .catch((error) => {
        this.errors = true;

        console.log(error);
      })
      .finally(() => {
        this.loading = {
          active: false,
          text: "",
        };
      });
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
