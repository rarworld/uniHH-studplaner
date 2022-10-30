<template>
  <div id="v-model-select" class="demo">
    <select v-model="selected" class="form-select">
      <option value="">Please select one</option>
      <option v-for="opt in vorlesungsListe" :key="opt.id" :value="opt.id">{{ opt.id }}: {{ opt.name }}
      </option>
    </select>
    <div class="btn-group" role="group" aria-label="Basic example">
      <button type="button" class="btn btn-primary" @click="activateVorlesung(selected)">add</button>
      <button type="button" class="btn btn-primary" @click="removeVorlesung(selected)">del</button>
      <button type="button" class="btn btn-primary" @click="showVorlesung(selected)">show</button>
    </div>
  </div>
</template>

<script>

export default {
  name: "dropdownNavMenu",
  props: ['vorlesungsListe'],
  components: {},
  data() {
    return  {
      selected: ""
    }
  },
  methods: {
    activateVorlesung(vId) {
      this.$emit("dropNavActivate", vId)
    },
    removeVorlesung(vId) {
      this.$emit("dropNavRemove", vId)
    },
    showVorlesung(vId) {
      this.$emit("dropNavShow", vId)
    }
  },
  emits: ['dropNavActivate','dropNavRemove','dropNavShow']
}
</script>

