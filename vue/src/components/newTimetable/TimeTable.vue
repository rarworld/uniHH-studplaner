<template>
  <div>
    <schedule :timeTable="timeTable" :hover="hover" @box-hover="onHover" @box-click="showModal" />
    <timeLessTable :hover="hover" :lectureList="timelessTable" @box-hover="onHover" @box-click="showModal"  />
    <delModal v-show="isDelModalVisible" :vId="delModalVid" @delModal="delVorlesung" @modalCancel="hideModal" />
  </div>
</template>

<script>

import schedule from "./schedule/Schedule.vue";
import timeLessTable from "./TimelessTable.vue";
import delModal from "./DelModal.vue";

function createDay(number, dayName) {
  let data = []
  for (let i = 0; i < number; i++) {
    data.push({
      "hour": i,
      "vl": [],
      "blanks": 0,
      "maxWidth": 1
    })
  }
  return {
    name: dayName,
    hours: data,
    width: 1
  }
}

function createDataArray() {
  const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
  let startHour = 8;
  const hours = [...Array(12).keys()].map((index) => {
    return {
      "id": index,
      "name": (index + startHour) + ":00 - " + (index + startHour + 1) + ":00",
      "width": 1
    }
  })

  return {
    hours: hours,
    days: days.map(d => createDay(hours.length, d))
  };

}

function createLection(dbElement, timeSlot) {
  let lectiom = {
    'id': dbElement['id'],
    'base': dbElement['base'],
    'name': dbElement['name'],
    'dozent': dbElement['dozent'],
    'hs': undefined,
    'size': undefined,
    'time': undefined
  }
  if (timeSlot != undefined) {
    lectiom['hs'] = timeSlot['hs']
    lectiom['size'] = timeSlot.slot['size']
    lectiom['time'] = timeSlot['start'] + " - " + timeSlot['end']
  }

  return lectiom
}

function setBlankHours(day, size, startHour, maxHour) {
  for (let i = startHour + 1; i < startHour + size && i < maxHour; i++) {
    let tmpHour = day.hours[i]
    tmpHour.blanks++
    tmpHour.maxWidth = tmpHour.vl.length + tmpHour.blanks
  }
}

Array.prototype.max = function () {
  return Math.max.apply(null, this);
};

function calcMaxWidthOfDay(day, maxHour) {
  day.hours.forEach(hour => {
    hour.blanks = 0
    hour.maxWidth = 1
  })

  day.hours.forEach((hour) => {
    hour.maxWidth = hour.vl.length + hour.blanks
    hour.vl.forEach(vl => {
      setBlankHours(day, vl.size, hour.hour, maxHour)
    })
  })
  day.width = day.hours.map(hour => hour.maxWidth).max()
}

export default {
  name: "timeTable",
  props: [],
  components: {
    schedule, timeLessTable, delModal
  },
  data: function () {
    return {
      hover: undefined,
      timeTable: createDataArray(),
      timelessTable: [],
      activeVorlesungen: [],
      isDelModalVisible: false,
      delModalVid: ""
    }
  },
  methods: {
    onHover(vId) {
      this.hover = vId;
    },
    // dbl-click on lecture in timetable
    showModal(vId) {
      this.delModalVid = vId
      this.isDelModalVisible = true
    },
    // cancel modal
    hideModal() {
      this.delModalVid = ""
      this.isDelModalVisible = false
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
      this.syncTable();
      this.hideModal()
    },
    addToTable(element) {
      if (!element['time'] || element['time'].length == 0) {
        this.timelessTable.push(createLection(element, undefined))
      }
      if (element['time'] && element['time'].length > 0) {
        element["time"].forEach(slotTmp => {
          let slot = slotTmp['slot']
          let lection = createLection(element, slotTmp)
          let tmpDay = this.timeTable.days[slot['day']]
          tmpDay.hours[slot['hour']].vl.push(lection)
          calcMaxWidthOfDay(tmpDay, this.timeTable.hours.length)
        })
      }
    },
    hasLecture(vId) {
      return this.activeVorlesungen.includes(vId)
    },
    addLecture(vId, element) {
      if (!this.hasLecture(vId)) {
        this.activeVorlesungen.push(vId)
        this.addToTable(element)
      }
    },
    syncTable() {
      this.timeTable.days.forEach(day =>{
        day.hours.forEach(hour =>{
          hour.vl = hour.vl.filter( lecture => this.activeVorlesungen.includes(lecture.id))
        })
        calcMaxWidthOfDay(day, this.timeTable.hours.length)
      })
    },

  },
  emits: []
}
</script>

