<template>
  <div>
    <table id="testomat" class="table table-bordered">
      <thead>
        <th>Hours</th>
        <th v-for="day in studTable.days" :key="'th_'+day.name">{{ day.name }}</th>
      </thead>
      <tbody>
        <tr v-for="h in studTable.hours" :key="'row_'+h.id">
          <td> {{ h.name }}</td>
          <template v-for="day in studTable.days">
            <template v-if="day.hours[h.id].slave">
            </template>
            <template v-else-if="day.hours[h.id].vl.length > 1">
              <innerTable :key="day.name+'_'+h.id" :hourId="h.id" :day="day" :height="calcRowHeight(day,h.id)" :hover="hoover" @box-click="onClick" @box-hoover="onHoover">
              </innerTable>
            </template>
            <template v-else-if="day.hours[h.id].vl.length > 0">
              <tableColumn :key="day.name+'_'+h.id" :vl="day.hours[h.id].vl[0]" :hover="hoover" @box-click="onClick" @box-hoover="onHoover"></tableColumn>
            </template>
            <template v-else>
              <td :key="day.name+'_'+h.id"></td>
            </template>
          </template>
        </tr>
      </tbody>
    </table>
    <div class="container table border">
      <div class="row bg-secondary bg-gradient" id="timelessHead">
        <div class="col">
          Timeless
        </div>
      </div>
      <div class="row row-cols-auto" id="timelessRow">
        <div class="col" v-for="(vorl,i) in timelessTable" scope="col" :id="'col_TL_'+i" :key="vorl.id">
          <vorlesungsBox :data="vorl" @box-hoover="onHoover" :hover="hoover" @box-click="onClick"></vorlesungsBox>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import innerTable from "./InnerTable.vue";
import vorlesungsBox from "./VorlesungsBox.vue";
import tableColumn from "./TableColumn.vue";

export default {
  name: "tableTimeTable",
  props: ['studTable', 'hoover', 'selected', 'timelessTable'],
  // computed: {
  //   console: () => console,
  // },
  methods: {
    onHoover(vId) {
      this.$emit("box-hoover", vId);
    },
    onClick(vId) {
      this.$emit("box-click", vId);
    },
    calcRowHeight(day, index) {
      let hours = day.hours;
      let height = hours[index].height;
      let openHeight = height - 1;
      let run = index + 1;
      while (openHeight > 0) {
        if (hours[run].height > openHeight) {
          let diff = hours[run].height - openHeight;
          height += diff;
          openHeight += diff;
        }
        openHeight--;
        run++;
      }
      return height;
    }
  },
  components: { innerTable, vorlesungsBox, tableColumn },
  emits: ['box-hoover', 'box-click']
}
</script>
