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
                <option v-for="opt in vorlesungsListe" :key="opt.id" :value="opt.id">{{ opt.id }}: {{ opt.name }}
                </option>
              </select>
              <div class="btn-group" role="group" aria-label="Basic example">
                <button type="button" class="btn btn-primary" @click="activateVorlesung(selected)">add</button>
                <button type="button" class="btn btn-primary" @click="removeVorlesung(selected)">del</button>
                <button type="button" class="btn btn-primary" @click="showVorlesung(selected)">show</button>
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
              @navMenuInput="activeVorlesungen = $event; setVorlesungen()" />
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
              <input class="form-check-input" type="checkbox" @change="setVorlesungen"
                :id="'cb_' + opt.id"
                :value="opt.id" v-model="activeVorlesungen">
              <label class="form-check-label" for="flexCheckDefault">
                {{ opt.id }}: {{ opt.name }}
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
    </div>

    <timeTable ref="timeTable" />

    <div id="stats" class="text-muted py-5">
      <div class="row" v-for="li in dataInfo" :key="li.name">
        <div class="col-5 text-start">
          <b>{{ li.name }} </b> data from {{ li.parsed }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import usersData from "../assets/data.json";
import navmenu from './navmenu/NavMenu.vue';
import timeTable from './newTimetable/TimeTable.vue';

export default {
  name: "Stundenplanner",
  data: function () {
    return {
      vorlesungsListe: usersData['data'],
      activeVorlesungen: [],
      selected: "",
      delModalVid: "",
      isDelModalVisible: false,
      dataInfo: usersData['input_files']
    }
  },
  computed: {
    console: () => console,
  },
  components: {
    navmenu, timeTable
  },
  methods: {
    // #######################
    // Dropdown Methods
    // #######################
    activateVorlesung(vId) {
      this.addVorlesung(vId);
      this.showVorlesung(vId);
    },
    removeVorlesung(vId) {
      this.$refs.timeTable.delVorlesung(vId)
    },
    showVorlesung(vId) {
      this.onHoover(vId);
    },


    // #######################
    // NavigationTree Methods
    // #######################

    // checkbox in navigation Tree
    activateNavCheckbox(vId, value) {
      alert(vId, value)
      if (value) {
        this.activateVorlesung(vId)
      } else {
        this.$refs.timeTable.delVorlesung(vId)
      }
    },

    // #######################
    // TimeTable Methods
    // #######################

    addVorlesung(vId) {
      let res = undefined;
      this.vorlesungsListe.forEach(vorl => { if (vorl.id == vId) res = vorl })
      if (res) {
        this.$refs.timeTable.addLecture(vId, res)
      }
    },
    onHoover(vId) {
      this.$refs.timeTable.onHover(vId)
    },


    // #######################
    // other Methods
    // #######################

    // build timetable
    setVorlesungen() {
      this.activeVorlesungen.forEach(vID => this.addVorlesung(vID));
    },

  },
  mounted: function () {
    if (window.location.search != "") {
      let searchParams = decodeURIComponent(window.location.search.substr(1).split('=')[1])
      searchParams.split(',').forEach(vl => this.addVorlesung(vl))
      this.onHoover("")
    }
  }
}
</script>