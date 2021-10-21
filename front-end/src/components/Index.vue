<template>
  <div class="w-full h-full">
    <img
      src="http://127.0.0.1:5000/feed"
      alt="Webcam feed"
      class="fixed left-1/2 h-full bg-gray-200 object-cover"
      style="transform: translateX(-50%)"
      draggable="false"
    />

    <img
      src="https://upload.wikimedia.org/wikipedia/commons/4/45/LogoZUYD.png"
      alt="Zuyd Hogeschool logo"
      class="absolute w-20 right-10 top-10"
      draggable="false"
    />

    <ActionBar />
  </div>
</template>

<script>
import ActionBar from "./ActionBar.vue";
export default {
  name: "Index",
  components: {
    ActionBar,
  },
};
</script>
