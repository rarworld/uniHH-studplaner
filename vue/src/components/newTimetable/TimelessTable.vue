<template>
  <div class="container table border">
    <div class="row bg-secondary bg-gradient" id="timelessHead">
      <div class="col">
        Timeless
      </div>
    </div>
    <div class="row row-cols-auto" id="timelessRow">
      <div class="col" v-for="(vorl,i) in lectureList" scope="col" :id="'col_TL_'+i" :key="vorl.id">
        <vorlesungsBox :data="vorl" @box-hover="onHover" :hover="hover" @box-click="onClick"></vorlesungsBox>
      </div>
    </div>
  </div>
</template>

<script>
import vorlesungsBox from "./VorlesungsBox.vue";

export default {
  name: "timelessTable",
  props: ["hover", "lectureList"],
  components: {
    vorlesungsBox
  },
  data: function () {
    return {
    }
  },
  methods: {
    onHover(vId) {
      this.$emit("box-hover", vId);
    },
    onClick(vId) {
      this.$emit("box-click", vId);
    },
  },
  emits: ['box-hover', 'box-click']
}
</script>

