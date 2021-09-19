<template>

  <div class="container table">
    <div class="row bg-secondary bg-gradient" id="timetableHead">
      <div class="col-2 border">#</div>
      <div class="col-2 border">Montag</div>
      <div class="col-2 border">Dienstag</div>
      <div class="col-2 border">Mittwoch</div>
      <div class="col-2 border">Donnerstag</div>
      <div class="col-2 border">Freitag</div>
    </div>
    <stundenplan-row 
        v-for="row in studTable" 
        v-bind:key="row.id"
        v-bind:row="row"
        :hover="hoover"
        @box-hoover="onHoover">
    </stundenplan-row>
  </div>

  <div class="container table border">
    <div class="row bg-secondary bg-gradient" id="timelessHead">
      <div class="col">
        Timeless
      </div>
    </div>
    <div class="row row-cols-auto" id="timelessRow">
      <div class="col" v-for="(vorl,i) in timelessTable" scope="col" :id="'col_TL_'+i" :key="vorl.id">
        <vorlesungsBox :data="vorl" @box-hoover="onHoover" :hover="hoover"></vorlesungsBox>
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
        }
    },
    emits:['box-hoover']
}
</script>

