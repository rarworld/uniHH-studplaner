<template>
  <td :rowspan="height">
    <table class="innerTable table table-bordered">
      <tbody>
        <tr v-for="i in height" :key="day.name+'-'+hourId+'_'+i" :id="'i'+day.name+'-'+hourId+'_'+i">
          <td v-for="vl in day.hours[i+hourId-1].vl" :key="day.name+'-'+hourId+'_'+i+'_'+vl.id" :rowspan="vl.size">
            <vorlesungsBox :data="vl" @box-hoover="onHoover" :hover="hover" @box-click="onClick"></vorlesungsBox>
          </td>
        </tr>
      </tbody>
    </table>
  </td>
</template>

<script>
import vorlesungsBox from "./VorlesungsBox.vue";

export default {
  name: "innerTable",
  props: ['day', "hourId", "height", "hover"],
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
<style>
.innerTable {
  margin: 0px;
  padding: 0px;
}

/* .innerTable tr {
  height: 30px;
} */

.innerTable td {
  padding: 0px;
}
</style>

