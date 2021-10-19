<template>
  <div class="w-full h-full" style="background-color: rgba(0, 0, 0, 0.2)">
    <div
      class="
        absolute
        left-1/2
        top-1/2
        vm--modal
        px-10
        py-5
        rounded-lg
        overflow-hidden
        z-50
      "
      style="width: 650px; height: auto; transform: translate(-50%, -50%)"
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
        <h1 class="text-3xl font-bold text-gray-900 mb-1">Connect to BOLTs</h1>
        <p class="mb-6 text-gray-700">
          Select the BOLTs you want to connect with and click on the connect
          button.
        </p>
        <form @submit.prevent="connect" action="/" method="POST">
          <div v-if="errors && !availableBolts.length" class="mb-4">
            <p class="text-sm font-medium text-red-600">
              Not able to retrieve the available BOLTs right now, please check
              the server is running correctly.
            </p>
          </div>

          <div v-else>
            <div v-if="!availableBolts.length" class="mb-4">
              <p class="text-sm font-medium text-gray-700">
                There are currently no BOLTs available.
              </p>
            </div>
            <select
              v-else
              v-model="selectedBolts"
              class="mb-2 w-full"
              name="bolts"
              id="bolts"
              multiple
            >
              <option
                v-for="bolt in availableBolts"
                :key="bolt.name"
                :value="bolt.name"
                class="flex"
              >
                <div class="h-4 w-4 rounded-full bg-red-500 ml-2"></div>
                <p>{{ bolt.name }}</p>
              </option>
            </select>

            <div v-if="errors === true" class="mb-4">
              <p class="text-sm font-medium text-red-600">
                Not able to connect to the selected BOLTs right now, please try
                again later.
              </p>
            </div>

            <div v-if="errors === 500" class="mb-4">
              <p class="text-sm font-medium text-red-600">
                {{this.errorMessage}}                
              </p>
            </div>

            <button
              :disabled="!selectedBolts.length"
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
              Connect
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import Loading from "@/components/others/Loading";

export default {
  name: "NotConnected",
  components: {
    Loading,
  },
  data() {
    return {
      availableBolts: [],
      selectedBolts: [],
      loading: {
        active: false,
        text: "",
      },
      errors: false,
    };
  },
  methods: {
    connect() {
      this.loading = {
        active: true,
        text: "Connecting to selected BOLTs...",
      };

      this.$http
        .post("connect", this.selectedBolts)
        .then(() => {
          this.$emit("connected", this.selectedBolts);
        })
        .catch((error) => {
          console.log(error.response)
          switch (error.response.status) {
            case 500:
              this.errors = error.response.status;
              this.errorMessage = error.response.data;
              break;

            default:
              this.errors = true;
          }
        })
        .finally(() => {
          this.loading = {
            active: false,
            text: "",
          };
        });
    },
  },
  mounted() {
    this.loading = {
      active: true,
      text: "Fetching available BOLTs...",
    };

    this.$http
      .get("available")
      .then((response) => {
        this.availableBolts = response.data;
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
