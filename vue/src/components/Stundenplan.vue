<template>
    <div>
      <div class="accordion" id="accordionFlushExample">

        <div class="accordion-item">
          <h2 class="accordion-header" id="headingOne">
            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
              DropDown der Vorlesungen
            </button>
          </h2>
          <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionFlushExample">
            <div class="accordion-body">

              <div id="v-model-select" class="demo">
                <select v-model="selected" class="form-select">
                  <option disabled value="">Please select one</option>
                  <option v-for="opt in vorlesungsListe" :key="opt.id" :value="opt.id">{{opt.id}}: {{opt.name}}</option>
                </select>
                <div class="btn-group" role="group" aria-label="Basic example">
                  <button type="button" class="btn btn-primary" @click="activateVorlesung(selected)">add</button>
                  <button type="button" class="btn btn-primary" @click="delVorlesung(selected)">del</button>
                  <button type="button" class="btn btn-primary" @click="onHoover(selected)">show</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="accordion-item">
          <h2 class="accordion-header" id="flush-headingOne">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
              Liste der Vorlesungen
            </button>
          </h2>
          <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#accordionFlushExample">
            <div class="accordion-body">
              <div v-for="opt in vorlesungsListe" :key="opt.id"  class="form-check">
                <input class="form-check-input" type="checkbox" @change="setVorlesungen"
                    :id="'cb_'+opt.id" :value="opt.id" v-model="activeVorlesungen" >
                <label class="form-check-label" for="flexCheckDefault">
                  {{opt.id}}: {{opt.name}}
                </label>
              </div>
            </div>
          </div>
        </div>

        <div class="accordion-item">
          <h2 class="accordion-header" id="textAreaHeader">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#textArea-collapse" aria-expanded="false" aria-controls="textArea-collapse">
              TextArea Vorlesungen
            </button>
          </h2>
          <div id="textArea-collapse" class="accordion-collapse collapse" aria-labelledby="textAreaHeader" data-bs-parent="#accordionFlushExample">
            <div class="accordion-body">
              <form method="GET">
              <input name="activList" class="form-control" v-model="activeVorlesungen" placeholder="[VorlesugsId,…]" />
              </form>
            </div>
          </div>
        </div>
      </div>

      <div>
        <br />
        <span>Aktive Vorlesungen: {{ activeVorlesungen }}</span>
      </div>
    </div>

    <timetable 
      @box-hoover="onHoover"
      :studTable="studTable"
      :hoover="hoover"
      :selected="selected"
      :timelessTable="timelessTable" />
          
</template>

<script>
import usersData from "../assets/data.json";
import timetable from './Timetable.vue';

function createDataArray() {
  return [
          { id: 0, data:[ [], [], [], [], [] ], timeRange: "08:00-10:00" },
          { id: 1, data:[ [], [], [], [], [] ], timeRange: "10:00-12:00" },
          { id: 2, data:[ [], [], [], [], [] ], timeRange: "12:00-14:00" },
          { id: 3, data:[ [], [], [], [], [] ], timeRange: "14:00-16:00" },
          { id: 4, data:[ [], [], [], [], [] ], timeRange: "16:00-18:00" },
          { id: 5, data:[ [], [], [], [], [] ], timeRange: "18:00-20:00" }
      ];
}

export default {
    name: "Stundenplanner",
    data: function () {
        return {
            vorlesungsListe: usersData,
            studTable: createDataArray(),
            hoover: "",
            selected: "",
            activeVorlesungen: [],
            timelessTable: []
        }
      },
    components: {
        timetable
    },
    methods: {
        addToTable(element) {
          if(!element['time'] || element['time'].length == 0){
            var tt = {
              'id': element['id'],
              'name': element['name'],
              'dozent': element['dozent'],
              'hs': ""
            }
            this.timelessTable.push(tt)
          }
          if(element['time'] && element['time'].length > 0){
            element["time"].forEach(slotTmp => {
              var slot = slotTmp['slot']
              var tt = {
                'id': element['id'],
                'name': element['name'],
                'dozent': element['dozent'],
                'hs': slotTmp['hs']
              }
              this.studTable[slot[0]]['data'][slot[1]].push(tt);
            })
          }
        },
        addVorlesung(vId){
          var res = undefined;
          this.vorlesungsListe.forEach(vorl => {if(vorl.id == vId) res=vorl })
          if(res){
            this.addToTable(res)
          }
        },
        delVorlesung(vId){
          if(this.activeVorlesungen.includes(vId)){
            this.activeVorlesungen.forEach((vorl, i) => {
                if(vId == vorl){
                  this.activeVorlesungen.splice(i, 1);
                }
              })
            this.timelessTable.forEach((vorl, i) => {
                if(vId == vorl['id']){
                  this.timelessTable.splice(i, 1);
                }
              })
          }
          this.setVorlesungen();
        },
        activateVorlesung(vId){
          if(!this.activeVorlesungen.includes(vId)){
            this.activeVorlesungen.push(vId)
          }
          this.setVorlesungen();
          this.onHoover(vId);
        },
        onHoover(vId){
            this.hoover= vId;
        },
        setVorlesungen(){
          this.studTable= createDataArray();
          this.timelessTable=[]
          this.activeVorlesungen.forEach(vID => this.addVorlesung(vID));
        }
    },
    created: function(){
      console.log(window.location.search)
      if( window.location.search != ""){
        var searchParams = decodeURIComponent(window.location.search.substr(1).split('=')[1])
        this.activeVorlesungen=searchParams.split(',')
        this.activeVorlesungen.forEach(vID => this.addVorlesung(vID))
        this.hoover=""
      }
    }
}
</script>