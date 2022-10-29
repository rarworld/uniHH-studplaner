<template>
  <table id="testomat" class="table table-bordered">
    <thead>
      <th>Hours</th>
      <th v-for="day in timeTable.days" :key="'th_' + day.name" :colspan="day.width">{{ day.name }}</th>
    </thead>
    <tbody>
      <tr v-for="h in timeTable.hours" :key="'row_' + h.id">
        <td> {{ h.name }}</td>
        <dayColumn v-for="day in timeTable.days" :key="day.name + '_' + h.id" :blankWidht="day.hours[h.id].blanks"
          :maxWidth="day.width" :lectionList="day.hours[h.id].vl" @box-hover="onHover" @box-click="onClick"
          :hover="hover" />
      </tr>
    </tbody>
  </table>
</template>

<script>
import dayColumn from "./DayColumn.vue";

export default {
  name: "schedule",
  props: ["timeTable", "hover"],
  components: {
    dayColumn
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


<style>
.smallText {
  text-align: left !important;
  font-size: 0.7rem !important;
}

#testomat tr {
  line-height: 1em;
  height: 100%;
}
#testomat td {
  height: 100%;
}
</style>

