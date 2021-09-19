<template>

  <div class="form-check">
    <input class="form-check-input" type="checkbox" @change="$emit('nav-cb',data.id, checked)" :id="'cb_'+data.id" :value="data.id" v-model="checked">
    <label class="form-check-label" for="flexCheckDefault">
      {{data.id}}: {{data.name}}
    </label>
  </div>
  
</template>

<script>

export default {
    name: "navEntry",
    props: ['data','activeVorlesungen'],
    emits: ['nav-cb'],
    data() {
      return {
        'checked': this.activeVorlesungen.includes(this.data.id)
      }
    }
}
</script>

