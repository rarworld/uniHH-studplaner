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
            @toto="onHoover">
        </stundenplan-row>
      </tbody>
    </table> 
</template>

<script>

import usersData from "./assets/data2.json";

var dataArray =[
    { id: 0, data:[ [], [], [], [], [], [] ], timeRange: "08:00-10:00" },
    { id: 1, data:[ [], [], [], [], [], [] ], timeRange: "10:00-12:00" },
    { id: 2, data:[ [], [], [], [], [], [] ], timeRange: "12:00-14:00" },
    { id: 3, data:[ [], [], [], [], [], [] ], timeRange: "14:00-16:00" },
    { id: 4, data:[ [], [], [], [], [], [] ], timeRange: "16:00-18:00" },
    { id: 5, data:[ [], [], [], [], [], [] ], timeRange: "18:00-20:00" }
];

import stundenplanRow from "./components/StundenplanRow.vue";

usersData.forEach(element => {
  element["slots"].forEach(slot => {
    dataArray[slot[1]]['data'][slot[0]].push(element);
  })
});

export default {
    name: "Stundenplanner",
    data: function () {
        return {
            studTable: dataArray
        }
      },
    components: {
        stundenplanRow
    },
    methods: {
        onHoover(vId){
            console.log(vId)
        }
    }
}
</script>