<template>
  <div class="absolute w-full bottom-0 lg:bottom-10">
    <div
      class="
        container
        max-w-6xl
        mx-auto
        grid grid-cols-4
        shadow-2xl
        lg:rounded-full
        overflow-hidden
      "
    >
      <button
        @click="clickCircle()"
        class="
          group
          flex
          items-center
          justify-center
          px-5
          py-5
          bg-green-500
          text-white
        "
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="
            h-20
            w-20
            transform
            group-hover:scale-125
            transition-transform
            duration-500
            ease-in-out
          "
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 12C21 13.1819 20.7672 14.3522 20.3149 15.4442C19.8626 16.5361 19.1997 17.5282 18.364 18.364C17.5282 19.1997 16.5361 19.8626 15.4442 20.3149C14.3522 20.7672 13.1819 21 12 21C10.8181 21 9.64778 20.7672 8.55585 20.3149C7.46392 19.8626 6.47177 19.1997 5.63604 18.364C4.80031 17.5282 4.13738 16.5361 3.68508 15.4442C3.23279 14.3522 3 13.1819 3 12C3 9.61305 3.94821 7.32387 5.63604 5.63604C7.32387 3.94821 9.61305 3 12 3C14.3869 3 16.6761 3.94821 18.364 5.63604C20.0518 7.32387 21 9.61305 21 12Z"
          />
        </svg>
      </button>
      <button
        @click="clickTriangle()"
        class="
          group
          flex
          items-center
          justify-center
          px-5
          py-5
          bg-blue-500
          text-white
        "
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="
            h-20
            w-20
            transform
            group-hover:scale-125
            transition-transform
            duration-500
            ease-in-out
          "
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5.072 19H18.928C20.468 19 21.43 17.333 20.66 16L13.732 4C12.962 2.667 11.038 2.667 10.268 4L3.34 16C2.57 17.333 3.532 19 5.072 19Z"
          />
        </svg>
      </button>
      <button
        @click="clickSquare()"
        class="
          group
          flex
          items-center
          justify-center
          px-5
          py-5
          bg-red-500
          text-white
        "
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="
            h-20
            w-20
            transform
            group-hover:scale-125
            transition-transform
            duration-500
            ease-in-out
          "
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M6 20H18C18.5304 20 19.0391 19.7893 19.4142 19.4142C19.7893 19.0391 20 18.5304 20 18V6C20 5.46957 19.7893 4.96086 19.4142 4.58579C19.0391 4.21071 18.5304 4 18 4H6C5.46957 4 4.96086 4.21071 4.58579 4.58579C4.21071 4.96086 4 5.46957 4 6V18C4 18.5304 4.21071 19.0391 4.58579 19.4142C4.96086 19.7893 5.46957 20 6 20Z"
          />
        </svg>
      </button>
      <button
        @click="clickSettings"
        class="
          group
          flex
          items-center
          justify-center
          px-5
          py-5
          bg-yellow-500
          text-white
        "
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="
            h-20
            w-20
            transform
            group-hover:scale-125
            transition-transform
            duration-500
            ease-in-out
          "
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
          />
        </svg>
      </button>
    </div>

    <SettingsModal />
  </div>
</template>

<script>
import SettingsModal from "./modals/SettingsModal";
export default {
  name: "ActionBar",
  components: {SettingsModal},
  methods: {
    clickCircle() {
      this.$http
        .get("actions/circle")
        .then(() => {
          console.log("Making circle...");
        })
        .catch((error) => {
          console.log(error);
        });
    },
    clickSquare() {
      this.$http
        .get("actions/square")
        .then(() => {
          console.log("Making square...");
        })
        .catch((error) => {
          console.log(error);
        });
    },
    clickTriangle() {
      this.$http
        .get("actions/triangle")
        .then(() => {
          console.log("Making triangle...");
        })
        .catch((error) => {
          console.log(error);
        });
    },
    clickSettings() {
      this.$modal.show("settings");
    },
  },
};
</script>
