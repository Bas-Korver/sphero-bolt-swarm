<template>
  <div class="relative w-full">
    <div
      class="absolute w-full h-1 bg-gray-200 rounded-full"
      :style="`background: linear-gradient(
          to right,
          #dadae5 ${(minValue / 255) * 100}%,
          #3264fe ${(minValue / 255) * 100}%,
          #3264fe ${(maxValue / 255) * 100}%,
          #dadae5 ${(maxValue / 255) * 100}%
        );`"
    ></div>
    <input
      type="range"
      min="0"
      max="255"
      v-model="minValue"
      @input="onInputMin"
    />

    <input
      type="range"
      min="0"
      max="255"
      v-model="maxValue"
      @input="onInputMax"
    />
  </div>
</template>

<script>
export default {
  name: "Slider",
  data() {
    return {
      minValue: this.value[0],
      maxValue: this.value[1],
    };
  },
  props: ["value"],
  methods: {
    onInputMin() {
      if (parseInt(this.minValue) > parseInt(this.maxValue)) {
        this.minValue = this.maxValue;
      }

      this.onInput();
    },
    onInputMax() {
      if (parseInt(this.maxValue) < parseInt(this.minValue)) {
        this.maxValue = this.minValue;
      }

      this.onInput();
    },
    onInput() {
      this.$emit("input", [parseInt(this.minValue), parseInt(this.maxValue)]);
      this.$emit("change");
    },
  },
};
</script>

<style scoped>
input[type="range"] {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 100%;
  outline: none;
  position: absolute;
  margin: auto;
  top: 0;
  bottom: 0;
  background-color: transparent;
  pointer-events: none;
}
input[type="range"]::-webkit-slider-runnable-track {
  -webkit-appearance: none;
  height: 5px;
}
input[type="range"]::-moz-range-track {
  -moz-appearance: none;
  height: 5px;
}
input[type="range"]::-ms-track {
  appearance: none;
  height: 5px;
}
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  height: 1.7em;
  width: 1.7em;
  background-color: #3264fe;
  cursor: pointer;
  margin-top: -9px;
  pointer-events: auto;
  border-radius: 50%;
}
input[type="range"]::-moz-range-thumb {
  -webkit-appearance: none;
  height: 1.7em;
  width: 1.7em;
  cursor: pointer;
  border-radius: 50%;
  background-color: #3264fe;
  pointer-events: auto;
}
input[type="range"]::-ms-thumb {
  appearance: none;
  height: 1.7em;
  width: 1.7em;
  cursor: pointer;
  border-radius: 50%;
  background-color: #3264fe;
  pointer-events: auto;
}
input[type="range"]:active::-webkit-slider-thumb {
  background-color: #ffffff;
  border: 3px solid #3264fe;
}
</style>
