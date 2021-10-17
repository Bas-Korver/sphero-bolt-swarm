<template>
  <modal
    @before-open="loadSettings"
    :name="'settings-' + name"
    width="600px"
    height="auto"
    classes="px-8 py-6 rounded-lg"
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
      <h1 class="text-3xl font-bold text-gray-900 mb-2">
        Settings for {{ name }}
      </h1>
      <p class="mb-6 text-gray-700">
        Below is an overview of all the settings. Change a setting and click on
        'Save' to save your changes.
      </p>

      <div v-if="errors && Object.keys(bolt).length === 0">
        <p class="text-sm font-medium text-red-600">
          Not able to fetch the settings for BOLT {{ name }}, please try again
          later.
        </p>
      </div>
      <form v-else @submit="sendForm" action="/" method="POST">
        <div class="flex items-center mb-4">
          <label for="name" class="w-1/4 font-medium text-gray-800 mr-4"
            >Name</label
          >

          <input
            v-model="bolt.name"
            type="text"
            id="name"
            name="name"
            class="w-full"
            disabled
          />
        </div>

        <div class="flex items-center mb-4">
          <label for="address" class="w-1/4 font-medium text-gray-800 mr-4"
            >MAC-address</label
          >

          <input
            v-model="bolt.address"
            type="text"
            id="address"
            name="address"
            class="w-full"
            disabled
          />
        </div>

        <div class="flex items-center mb-4">
          <label for="color" class="w-1/4 font-medium text-gray-800 mr-4"
            >Color</label
          >

          <input
            v-model="bolt.color"
            type="color"
            id="color"
            name="color"
            class="w-full"
          />
        </div>

        <div class="flex items-center mb-4">
          <label for="hue" class="w-1/4 font-medium text-gray-800 mr-4"
            >Hue</label
          >

          <input
            v-model="bolt.hue"
            type="range"
            id="hue"
            name="hue"
            class="w-full"
          />
        </div>

        <div class="flex items-center mb-4">
          <label for="saturation" class="w-1/4 font-medium text-gray-800 mr-4"
            >Saturation</label
          >

          <input
            v-model="bolt.saturation"
            type="range"
            id="saturation"
            name="saturation"
            class="w-full"
          />
        </div>

        <div class="flex items-center mb-4">
          <label for="value" class="w-1/4 font-medium text-gray-800 mr-4"
            >Value</label
          >

          <input
            v-model="bolt.value"
            type="range"
            id="value"
            name="value"
            class="w-full"
          />
        </div>

        <div class="flex items-center">
          <div class="w-1/4 mr-4"></div>
          <div class="w-full">
            <div v-if="errors" class="mb-4">
              <p class="text-sm font-medium text-red-600">
                Not able to save the changes made right now, please try again
                later.
              </p>
            </div>
            <button
              type="submit"
              class="
                block
                px-5
                py-2
                border border-transparent
                text-base
                font-medium
                rounded-md
                text-white
                bg-blue-500
                hover:bg-blue-600
                disabled:opacity-50 disabled:cursor-not-allowed
              "
            >
              Save
            </button>
          </div>
        </div>
      </form>
    </div>
  </modal>
</template>

<script>
import Loading from "@/components/others/Loading";

export default {
  name: "SettingsBoltModal",
  components: { Loading },
  props: {
    name: String,
  },
  data() {
    return {
      bolt: {
        name: "",
        address: "",
        color: [],
        hue: [],
        saturation: [],
        value: [],
      },
      loading: {
        active: false,
        text: "",
      },
      errors: false,
    };
  },
  methods: {
    loadSettings() {
      this.loading = {
        active: true,
        text: "Fetching settings for BOLT " + this.name + "...",
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
    sendForm() {
      this.loading = {
        active: true,
        text: "Saving changed settings for BOLT " + this.name + "...",
      };

      this.$http
        .post("/" + this.bolt.name)
        .then((response) => {
          // TODO: Handle response.

          console.log(response);

          this.$emit("update");
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
