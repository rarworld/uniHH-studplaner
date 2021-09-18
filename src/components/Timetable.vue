<template>
  <table class="table table-striped table-hover table-bordered">
    <thead>
      <tr>
        <th scope="col">#</th>
        <th scope="col">Montag</th>
        <th scope="col">Dienstag</th>
        <th scope="col">Mittwoch</th>
        <th scope="col">Donnerstag</th>
        <th scope="col">Freitag</th>
      </tr>
    </thead>
    <tbody>          
      <stundenplan-row 
        v-for="row in studTable" 
        v-bind:key="row.id"
        v-bind:row="row"
        :hover="hoover"
        @box-selected="onHoover">
      </stundenplan-row>
    </tbody>
  </table> 

  <div class="container">
    <div class="card">
      <div class="card-header">
        Timeless
      </div>
    
      <div class="card-body row row-cols-auto">
        <div class="col" v-for="(vorl,i) in timelessTable" scope="col" :id="'col_TL_'+i" :key="vorl.id">
          <vorlesungsBox :data="vorl" @box-hoover="onHoover" :hover="hoover"></vorlesungsBox>
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
        this.$emit("box-selected", vId);
      }
    }
}
</script>

