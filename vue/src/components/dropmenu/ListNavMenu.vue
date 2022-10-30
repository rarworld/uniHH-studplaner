<template>
  <div>
    <div v-for="opt in vorlesungsListe" :key="opt.id" class="form-check">
      <input class="form-check-input" type="checkbox" @change="changeHandler" :id="'cb_' + opt.id" :value="opt.id"
        v-model="activeVorlesungen">
      <label class="form-check-label" for="flexCheckDefault">
        {{ opt.id }}: {{ opt.name }}
      </label>
    </div>
  </div>
</template>

<script>

export default {
  name: "listNavMenu",
  props: ['vorlesungsListe'],
  components: {},
  data() {
    return {
      test: undefined
    }
  },
  methods: {
    changeHandler(event) {
      if(event.type == "change"){
        let vId = event.currentTarget.defaultValue
        let value = event.returnValue
        this.$emit("listNavChange", vId, value)
      }
    }
  },
  emits: ['listNavChange']
}
</script>

