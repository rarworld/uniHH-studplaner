<template>
  <div class="table-responsive">
    <table class="table" style="width:100%;">
      <thead>
        <tr id="timetableHead">
          <th scope="col">#</th>
          <th style="width:17%" scope="col">Montag</th>
          <th style="width:17%" scope="col">Dienstag</th>
          <th style="width:17%" scope="col">Mittwoch</th>
          <th style="width:17%" scope="col">Donnerstag</th>
          <th style="width:17%" scope="col">Freitag</th>
        </tr>
      </thead>
      <tbody>
        <stundenplan-row 
            v-for="row in studTable" 
            v-bind:key="row.id"
            v-bind:row="row"
            :hover="hoover"
            @box-click="onClick"
            @box-hoover="onHoover">
        </stundenplan-row>
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

import stundenplanRow from "./StundenplanRow.vue";
import vorlesungsBox from "./VorlesungsBox.vue";

export default {
    name: "timetable",
    props: ['studTable','hoover','selected','timelessTable'],
    components: {
        stundenplanRow,
        vorlesungsBox
    },
    methods: {
        onHoover(vId){
            this.$emit("box-hoover", vId);
        },
        onClick(vId){
            this.$emit("box-click", vId);
        }
    },
    emits:['box-hoover','box-click']
}
</script>

