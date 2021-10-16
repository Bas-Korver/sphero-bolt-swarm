<template>
  <modal name="settings" width="50%" classes="px-10 py-5 rounded-lg">
    <h1 class="text-3xl font-bold text-gray-900 mb-5">Settings</h1>
    <div class="grid grid-cols-3 gap-5">
      <div
        v-for="bolt in bolts"
        :key="bolt.name"
        class="
          relative
          flex
          justify-between
          p-2
          rounded-lg
          shadow
          overflow-hidden
        "
      >
        <div class="flex items-center">
          <div
            class="h-4 w-4 rounded-full bg-red-500 mr-2"
            :style="{
              'background-color': `rgb(${bolt.colors[0]}, ${bolt.colors[1]}, ${bolt.colors[2]})`,
            }"
          ></div>
          <h2 class="text-gray-700 font-medium">{{ bolt.name }}</h2>
        </div>

        <div>
          <button @click="editBolt(bolt.name)" class="text-gray-700">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"
              />
            </svg>
          </button>
          <button>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>

        <SettingsBoltModal :name="bolt.name" />
      </div>
    </div>
  </modal>
</template>

<script>
import SettingsBoltModal from "./SettingsBoltModal.vue";

export default {
  name: "SettingsModal",
  components: {
    SettingsBoltModal,
  },
  data() {
    return {
      bolts: [
        {
          name: "SB-4D1E",
          colors: [255, 251, 0],
        },
        {
          name: "SB-67EA",
          colors: [0, 255, 0],
        },
      ],
    };
  },
  methods: {
    editBolt(name) {
      this.$modal.show("settings-" + name);
    },
  },
};
</script>
