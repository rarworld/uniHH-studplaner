<template>
    <div id="stundenplanerApp">
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
          <h2 class="accordion-header" id="accordion-Nav-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#accordion-Nav-body" aria-expanded="false" aria-controls="accordion-Nav-body">
              Navigation Vorlesungen
            </button>
          </h2>
          <div id="accordion-Nav-body" class="accordion-collapse collapse" aria-labelledby="accordion-Nav-header" data-bs-parent="#accordionFlushExample">
            <div class="accordion-body">
              <navmenu :activeVorlesungen="activeVorlesungen" @navMenuInput="activeVorlesungen = $event;setVorlesungen()" />
            </div>
          </div>
        </div>

        <div class="accordion-item" v-if="false">
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
              Eingabefeld Vorlesungen
            </button>
          </h2>
          <div id="textArea-collapse" class="accordion-collapse collapse" aria-labelledby="textAreaHeader" data-bs-parent="#accordionFlushExample">
            <div class="accordion-body">
              <form method="GET">
                <div class="row">
                  <div class="col-10">
                    <input name="activList" class="form-control" v-model="activeVorlesungen" placeholder="[VorlesugsId,…]" />
                  </div>
                  <div class="col-auto">
                    <button type="submit" class="btn btn-primary mb-3">Laden</button>
                  </div>
                </div>
              </form>
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
        @box-click="showModal"
        :studTable="studTable"
        :hoover="hoover"
        :selected="selected"
        :timelessTable="timelessTable" />
      
      <delModal 
        v-show="isDelModalVisible"
        :vId="delModalVid"
        @delModal="delVorlesung"
        @modalCancel="hideModal" />
      
      <div id="stats" class="text-muted py-5">
        <div class="row" v-for="li in dataInfo" :key="li.name" >
          <div class="col-5 text-start">
            <b>{{li.name}} </b> data from {{li.parsed}}
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import usersData from "../assets/data.json";
import timetable from './timetable/Timetable.vue';
import navmenu from './navmenu/NavMenu.vue';
import delModal from './DelModal.vue';

function createEmptyBlock() {
  return {
    rowspan:1,
    visible:true,
    vl:[]
  }
}

function createEmptyDataBlock() {
  let data=[]
  for (let i = 0; i < 5; i++) {
    data.push(createEmptyBlock())
  }
  return data
}

function createDataArray() {
  return [
          { id: 0, data: createEmptyDataBlock(), timeRange: "08:00-10:00" },
          { id: 1, data: createEmptyDataBlock(), timeRange: "10:00-12:00" },
          { id: 2, data: createEmptyDataBlock(), timeRange: "12:00-14:00" },
          { id: 3, data: createEmptyDataBlock(), timeRange: "14:00-16:00" },
          { id: 4, data: createEmptyDataBlock(), timeRange: "16:00-18:00" },
          { id: 5, data: createEmptyDataBlock(), timeRange: "18:00-20:00" }
      ];
}

export default {
    name: "Stundenplanner",
    data: function () {
        return {
            vorlesungsListe: usersData['data'],
            studTable: createDataArray(),
            hoover: "",
            selected: "",
            activeVorlesungen: [],
            timelessTable: [],
            delModalVid: "",
            isDelModalVisible: false,
            dataInfo: usersData['input_files']
        }
      },
    components: {
        timetable, navmenu, delModal
    },
    methods: {
        addToTable(element) {
          if(!element['time'] || element['time'].length == 0){
            let tt = {
              'id': element['id'],
              'base': element['base'],
              'name': element['name'],
              'dozent': element['dozent'],
              'hs': "",
              'time': ""
            }
            this.timelessTable.push(tt)
          }
          if(element['time'] && element['time'].length > 0){
            element["time"].forEach(slotTmp => {
              let slot = slotTmp['slot']
              let tt = {
                'id': element['id'],
                'base': element['base'],
                'name': element['name'],
                'dozent': element['dozent'],
                'hs': slotTmp['hs'],
                'time': slotTmp['start']+" - "+slotTmp['end']
              }
              this.studTable[slot['hour']]['data'][slot['day']]['vl'].push(tt);
            })
          }
        },
        addVorlesung(vId){
          let res = undefined;
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
          this.hideModal()
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
        },
        activateNavCheckbox(vId,value){
          if(value){
            this.activateVorlesung(vId)
          }else{
            this.delVorlesung(vId)
          }
        },
        showModal(vId){
          this.delModalVid = vId
          this.isDelModalVisible=true
        },
        hideModal(){
          this.delModalVid = ""
          this.isDelModalVisible=false
        }
    },
    created: function(){
      if( window.location.search != ""){
        let searchParams = decodeURIComponent(window.location.search.substr(1).split('=')[1])
        this.activeVorlesungen=searchParams.split(',')
        this.activeVorlesungen.forEach(vID => this.addVorlesung(vID))
        this.hoover=""
      }
    }
}
</script>