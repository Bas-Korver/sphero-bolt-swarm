<template>
  <modal :name="'settings-' + name" classes="p-5 rounded-lg">
    <h1 class="text-lg font-medium text-gray-800">Editing {{ name }}</h1>

    <form @submit="sendForm" action="/" method="POST">
      <div class="flex">
        <label for="name" class="w-1/4 mr-4">Name</label>
        <input type="text" id="name" name="name" v-model="name" class="w-full" disabled />
      </div>
      <div class="flex">
        <label for="address" class="w-1/4 mr-4">MAC-address</label>
        <input type="text" id="address" name="address" v-model="address" class="w-full" disabled />
      </div>
    </form>
  </modal>
</template>

<script>
export default {
  name: "SettingsBoltModal",
  props: {
    name: String,
  },
  data() {
    return {
      address: "C1:7B:85:80:4D:1E",
      color: [255, 251, 0],
      lowHsv: [18, 65, 200],
      highHsv: [60, 255, 255],
    };
  },
  methods: {
    sendForm() {},
  },
};
</script>
