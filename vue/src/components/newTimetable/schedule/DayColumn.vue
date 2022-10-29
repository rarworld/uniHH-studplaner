<template>
  <td v-for="(vl, index) in lectionList" :key="'filled_' + index" :rowspan="vl.size">
    <vorlesungsBox :data="vl" :hover="hover" @box-hover="onHover" @box-click="onClick"></vorlesungsBox>
  </td>
  <td v-if="missingEmptyColumns" :colspan="missingEmptyColumns"></td>
</template>

<script>
import vorlesungsBox from "./../VorlesungsBox.vue";

export default {
  name: "dayColumn",
  props: ['blankWidht', 'maxWidth', "lectionList", "hover"],
  components: {
    vorlesungsBox
  },
  computed: {
    missingEmptyColumns() {
      let missingColumns = this.maxWidth - (this.lectionList.length + this.blankWidht)
      return missingColumns < 0 ? 0 : missingColumns
    }
  },
  methods: {
    onHover(vId) {
      this.$emit("box-hover", vId)
    },
    onClick(vId) {
      this.$emit("box-click", vId)
    }
  },
  emits: ['box-hover', 'box-click']
}
</script>

