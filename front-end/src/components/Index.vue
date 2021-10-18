<template>
  <div class="w-full h-full">
    <img
      src=""
      alt="Webcam feed"
      class="w-full h-full bg-gray-200"
      draggable="false"
    />

    <img
      src="https://upload.wikimedia.org/wikipedia/commons/4/45/LogoZUYD.png"
      alt="Zuyd Hogeschool logo"
      class="absolute w-20 right-10 top-10"
      draggable="false"
    />

    <ActionBar />
    <SettingsModal />
  </div>
</template>

<script>
import ActionBar from "./ActionBar.vue";
import SettingsModal from "./modals/SettingsModal.vue";
export default {
  name: "Index",
  components: {
    ActionBar,
    SettingsModal,
  },
};
</script>
