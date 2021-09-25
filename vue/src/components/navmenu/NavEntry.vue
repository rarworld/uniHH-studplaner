<template>

  <div class="form-check">
    <input class="form-check-input" type="checkbox" :id="'cb_'+data.id" :value="data.id" v-model="checked">
    <label class="form-check-label" for="flexCheckDefault">
      {{data.id}}: {{data.name}}
    </label>
  </div>
  
</template>

<script>

export default {
  name: "navEntry",
  props: ['data','activeVorlesungen'],
  emits: ['navEntryInput'],
  computed: {
    checked: {
      get() {
        return this.activeVorlesungen;
      },
      set(val) {
        this.$emit('navEntryInput', val);
      }
    }
  }
}
</script>

