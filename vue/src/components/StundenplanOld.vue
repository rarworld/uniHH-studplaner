<template>
  <div id="stundenplanerApp">
    <div class="accordion" id="accordionFlushExample">

      <div class="accordion-item">
        <h2 class="accordion-header" id="headingOne">
          <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne"
            aria-expanded="true" aria-controls="collapseOne">
            DropDown der Vorlesungen
          </button>
        </h2>
        <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne"
          data-bs-parent="#accordionFlushExample">
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
          <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
            data-bs-target="#accordion-Nav-body" aria-expanded="false" aria-controls="accordion-Nav-body">
            Navigation Vorlesungen
          </button>
        </h2>
        <div id="accordion-Nav-body" class="accordion-collapse collapse" aria-labelledby="accordion-Nav-header"
          data-bs-parent="#accordionFlushExample">
          <div class="accordion-body">
            <navmenu :activeVorlesungen="activeVorlesungen"
              @navMenuInput="activeVorlesungen = $event;setVorlesungen()" />
          </div>
        </div>
      </div>

      <div class="accordion-item" v-if="false">
        <h2 class="accordion-header" id="flush-headingOne">
          <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
            data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
            Liste der Vorlesungen
          </button>
        </h2>
        <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne"
          data-bs-parent="#accordionFlushExample">
          <div class="accordion-body">
            <div v-for="opt in vorlesungsListe" :key="opt.id" class="form-check">
              <input class="form-check-input" type="checkbox" @change="setVorlesungen" :id="'cb_'+opt.id"
                :value="opt.id" v-model="activeVorlesungen">
              <label class="form-check-label" for="flexCheckDefault">
                {{opt.id}}: {{opt.name}}
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="accordion-item">
        <h2 class="accordion-header" id="textAreaHeader">
          <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
            data-bs-target="#textArea-collapse" aria-expanded="false" aria-controls="textArea-collapse">
            Eingabefeld Vorlesungen
          </button>
        </h2>
        <div id="textArea-collapse" class="accordion-collapse collapse" aria-labelledby="textAreaHeader"
          data-bs-parent="#accordionFlushExample">
          <div class="accordion-body">
            <form method="GET">
              <div class="row">
                <div class="col-10">
                  <input name="activList" class="form-control" v-model="activeVorlesungen"
                    placeholder="[VorlesugsId,…]" />
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

    <tableTimeTable @box-hoover="onHoover" @box-click="showModal" :studTable="studTable" :hoover="hoover"
      :selected="selected" :timelessTable="timelessTable" ref="tableTimeTable" />

    <timeTable ref="timeTable" />

    <delModal v-show="isDelModalVisible" :vId="delModalVid" @delModal="delVorlesung" @modalCancel="hideModal" />

    <div id="stats" class="text-muted py-5">
      <div class="row" v-for="li in dataInfo" :key="li.name">
        <div class="col-5 text-start">
          <b>{{li.name}} </b> data from {{li.parsed}}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import usersData from "../assets/data.json";
import navmenu from './navmenu/NavMenu.vue';
import delModal from './DelModal.vue';
import tableTimeTable from './timetable/TableTimeTable.vue';
import timeTable from './newTimetable/TimeTable.vue';

function createDay(number, dayName) {
  let data = []
  for (let i = 0; i < number; i++) {
    data.push({
      "hour": i,
      "vl": [],
      "width": 0,
      "height": 1,
      "blank": false,
      "master": false,
      "slave": false
    })
  }
  return {
    name: dayName,
    width: 0,
    hours: data
  }
}

function createDataArray() {
  const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
  let startHour = 8;
  const hours = [...Array(12).keys()].map((index) => {
    return {
      "id": index,
      "name": (index + startHour) + ":00 - " + (index + startHour + 1) + ":00"
    }
  })

  return {
    hours: hours,
    days: days.map(d => createDay(hours.length, d))
  };
}

Array.prototype.max = function () {
  return Math.max.apply(null, this);
};

function calcHeightAndSlaves(day, maxHour) {
  let masterCandidateHour = undefined
  let runnerSize = 0
  let runHour
  let i = 0;
  while (i < maxHour) {
    if (runnerSize == 0) {
      masterCandidateHour = undefined
    }
    runHour = day.hours[i]
    runHour.width = runHour.vl.length
    if (runHour.vl.length > 0) {
      runHour.height = runHour.vl.map(vl => vl.size).max()

      if (masterCandidateHour == undefined) {
        masterCandidateHour = runHour
        runnerSize = masterCandidateHour.height
        if (runnerSize > 1) {
          masterCandidateHour.master = true
        }
      } else {
        if (runHour.height > runnerSize) {
          masterCandidateHour.height += runHour.height - runnerSize
          runnerSize = runHour.height - 1
        }
        runHour.slave = true
      }
    } else {
      if (masterCandidateHour != undefined && runnerSize > 0) {
        runHour.slave = true
      }
    }
    day.width = day.hours.map(hour => hour.width).max()
    runnerSize--
    i++;
  }
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
  computed: {
    console: () => console,
  },
  components: {
    navmenu, delModal, tableTimeTable, timeTable
  },
  methods: {
    addToTable(element) {
      if (!element['time'] || element['time'].length == 0) {
        let tt = {
          'id': element['id'],
          'base': element['base'],
          'name': element['name'],
          'dozent': element['dozent'],
          'size': 1,
          'hs': "",
          'time': ""
        }
        this.timelessTable.push(tt)
      }
      if (element['time'] && element['time'].length > 0) {
        element["time"].forEach(slotTmp => {
          let slot = slotTmp['slot']
          let tt = {
            'id': element['id'],
            'base': element['base'],
            'name': element['name'],
            'dozent': element['dozent'],
            'hs': slotTmp['hs'],
            'size': slot['size'],
            'time': slotTmp['start'] + " - " + slotTmp['end']
          }
          let wantedDay = this.studTable.days[slot['day']]
          let startHour = slot['hour']
          wantedDay.hours[startHour].vl.push(tt)

          if (tt.size > 1) {
            for (let i = 1; i < tt.size; i++) {
              wantedDay.hours[startHour + i].vl.push({
                'id': "blank",
                'base': "",
                'name': "",
                'dozent': "",
                'hs': "",
                'time': ""
              })
            }
          }

          calcHeightAndSlaves(wantedDay, this.studTable.hours.length)
        })
      }
    },
    addVorlesung(vId) {
      let res = undefined;
      this.vorlesungsListe.forEach(vorl => { if (vorl.id == vId) res = vorl })
      if (res) {
        this.addToTable(res)
      }
    },
    addLecture(vId) {
      let res = undefined;
      this.vorlesungsListe.forEach(vorl => { if (vorl.id == vId) res = vorl })
      if (res ) {
        this.$refs.timeTable.addLecture(vId,res)
      }
    },
    delVorlesung(vId) {
      if (this.activeVorlesungen.includes(vId)) {
        this.activeVorlesungen.forEach((vorl, i) => {
          if (vId == vorl) {
            this.activeVorlesungen.splice(i, 1);
          }
        })
        this.timelessTable.forEach((vorl, i) => {
          if (vId == vorl['id']) {
            this.timelessTable.splice(i, 1);
          }
        })
      }
      this.setVorlesungen();
      this.hideModal()
    },
    // add Button under the Dropdown
    activateVorlesung(vId) {
      if (!this.activeVorlesungen.includes(vId)) {
        this.activeVorlesungen.push(vId)
      }
      this.setVorlesungen();
      this.onHoover(vId);
    },
    onHoover(vId) {
      this.hoover = vId;
    },
    // build timetable
    setVorlesungen() {
      this.studTable = createDataArray();
      this.timelessTable = []
      this.activeVorlesungen.forEach(vID => this.addVorlesung(vID));
    },
    // checkbox in navigation Tree
    activateNavCheckbox(vId, value) {
      if (value) {
        this.activateVorlesung(vId)
      } else {
        this.delVorlesung(vId)
      }
    },
    // dbl-click on lecture in timetable
    showModal(vId) {
      this.delModalVid = vId
      this.isDelModalVisible = true
      this.addLecture(vId)
    },
    // cancel modal
    hideModal() {
      this.delModalVid = ""
      this.isDelModalVisible = false
    }
  },
  created: function () {
    if (window.location.search != "") {
      let searchParams = decodeURIComponent(window.location.search.substr(1).split('=')[1])
      this.activeVorlesungen = searchParams.split(',')
      this.setVorlesungen()
      this.hoover = ""
    }
  }
}
</script>