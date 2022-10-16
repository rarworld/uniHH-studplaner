<template>
  <td>
      <vorlesungsBox :data="vl" @box-hoover="onHoover" :hover="hover" @box-click="onClick"></vorlesungsBox>
  </td>
</template>

<script>
import vorlesungsBox from "./VorlesungsBox.vue";

export default {
  name: "tableColumn",
  props: ['vl', "hover"],
  components: {
    vorlesungsBox
  },
  methods: {
    onHoover(vId) {
      this.$emit("box-hoover", vId)
    },
    onClick(vId) {
      this.$emit("box-click", vId)
    }
  },
  emits: ['box-hoover', 'box-click']
}
</script>

