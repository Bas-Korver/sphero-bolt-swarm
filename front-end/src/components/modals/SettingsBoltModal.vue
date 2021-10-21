<template>
  <modal
    @before-open="loadSettings"
    :name="'settings-' + name"
    width="75%"
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
      <form
        v-else
        @submit="sendForm"
        action="/"
        method="POST"
      >
        <div class="w-full grid grid-cols-2 gap-x-5 mb-4">
          <div>
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
          </div>
          <div>
            <img
              :src="`http://127.0.0.1:5000/bolts/${bolt.name}/feed`"
              :alt="`HSV preview feed for ${bolt.name}`"
              class="w-full bg-gray-200 mb-4"
            />

            <div class="flex items-center mb-4">
              <label class="w-1/4 font-medium text-gray-800 mr-4">Hue</label>

              <Slider @change="sendHSV" v-model="bolt.hue" class="w-full" />
            </div>

            <div class="flex items-center mb-4">
              <label class="w-1/4 font-medium text-gray-800 mr-4"
                >Saturation</label
              >

              <Slider @change="sendHSV" v-model="bolt.saturation" class="w-full" />
            </div>

            <div class="flex items-center mb-4">
              <label class="w-1/4 font-medium text-gray-800 mr-4">Value</label>

              <Slider @change="sendHSV" v-model="bolt.value" class="w-full" />
            </div>
          </div>
        </div>
        <div class="w-full">
          <div class="flex flex-row-reverse w-full justify-between items-center">
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
            <div v-if="errors">
              <p class="text-sm font-medium text-red-600">
                Not able to save the changes made right now, please try again
                later.
              </p>
            </div>
          </div>
        </div>
      </form>
    </div>
  </modal>
</template>

<script>
import Loading from "@/components/others/Loading";
import Slider from "@/components/others/Slider";
import _ from "lodash";

export default {
  name: "SettingsBoltModal",
  components: { Slider, Loading },
  props: {
    name: String,
  },
  data() {
    return {
      bolt: {},
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
        .get("/" + this.name)
        .then((response) => {
          this.bolt = {
            name: response.data.name,
            address: response.data.address,
            color: this.rgbToHex(
              response.data.color[0],
              response.data.color[1],
              response.data.color[2]
            ),
            hue: [response.data.low_hsv[0], response.data.high_hsv[0]],
            saturation: [response.data.low_hsv[1], response.data.high_hsv[1]],
            value: [response.data.low_hsv[2], response.data.high_hsv[2]],
          };
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
        .post("/" + this.bolt.name, {
          color: this.hexToRGB(this.bolt.color),
          low_hsv: [
            this.bolt.hue[0],
            this.bolt.saturation[0],
            this.bolt.value[0],
          ],
          high_hsv: [
            this.bolt.hue[1],
            this.bolt.saturation[1],
            this.bolt.value[1],
          ],
        })
        .then(() => {
          this.$emit("update");

          this.$modal.hide("settings-" + this.name);
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
    sendHSV: _.debounce(function () {
      console.log("[!] Updating HSV data for preview...");

      this.$http.post("/" + this.bolt.name + "/hsv", {
        hue: this.bolt.hue,
        saturation: this.bolt.saturation,
        value: this.bolt.value,
      });
    }, 250),
    rgbToHex(red, green, blue) {
      return (
        "#" +
        ((1 << 24) + (red << 16) + (green << 8) + blue).toString(16).slice(1)
      );
    },
    hexToRGB(hex) {
      let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result
        ? [
            parseInt(result[1], 16),
            parseInt(result[2], 16),
            parseInt(result[3], 16),
          ]
        : null;
    },
  },
};
</script>
