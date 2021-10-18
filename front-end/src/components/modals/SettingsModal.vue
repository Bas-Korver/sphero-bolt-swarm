<template>
  <modal
    @before-open="loadBolts"
    name="settings"
    width="800px"
    height="auto"
    classes="px-10 py-8 rounded-lg"
  >
    <div
      v-if="loading.active"
      class="w-full h-full flex flex-col items-center justify-center"
    >
      <h1 class="text-xl font-bold text-gray-900 mb-8">
        {{ loading.text }}
      </h1>

      <Loading />
    </div>
    <div v-else>
      <h1 class="text-3xl font-bold text-gray-900 mb-1">Settings</h1>
      <p class="mb-6 text-gray-700">
        Below is an overview of all the connected BOLTs. By clicking on the
        pencil you will be able to edit the selected BOLT. Click on the remove
        button if you wish to connect or disconnect to this BOLT.
      </p>

      <div v-if="errors && !bolts.length">
        <p class="text-sm font-medium text-red-600">
          Not able to retrieve the connected BOLTs right now, please check the
          server is running correctly.
        </p>
      </div>
      <div v-else>
        <div v-if="!bolts.length">
          <p class="text-sm font-medium text-gray-700">
            There are currently no BOLTs available.
          </p>
        </div>
        <div v-else class="grid grid-cols-3 gap-5">
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

            <SettingsBoltModal @update="loadBolts" :name="bolt.name" />
          </div>
        </div>
      </div>
    </div>
  </modal>
</template>

<script>
import SettingsBoltModal from "./SettingsBoltModal.vue";
import Loading from "@/components/others/Loading";

export default {
  name: "SettingsModal",
  components: {
    Loading,
    SettingsBoltModal,
  },
  data() {
    return {
      bolts: [
        {
          name: "SB-1D4E",
          colors: [255, 0, 0],
        },
      ],
      loading: {
        active: false,
        text: "",
      },
      errors: false,
    };
  },
  methods: {
    editBolt(name) {
      console.log(name);

      // this.$modal.hide("settings");

      this.$modal.show("settings-" + name);
    },
    loadBolts() {
      console.log("[!] Loading BOLTs...");
      this.loading = {
        active: true,
        text: "Fetching available BOLTs...",
      };

      this.$http
        .get("/")
        .then((response) => {
          // TODO: Handle response.

          console.log(response);
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
  },
};
</script>
