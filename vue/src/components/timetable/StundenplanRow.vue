<template>
    <tr :id="'tableRow_'+row.id">
        <td class="col-md-2">{{ row.timeRange }}</td>
        <td v-for="(day,i) in row.data" :id="'col_'+row.id+'_'+i" :key="row.id+'_'+i" class="col-md-2" :rowspan=day.rowspan>
            <vorlesungsBox v-for="(vorl, index) in day.vl" :key="index" :data="vorl" @box-hoover="onHoover" :hover="hover" @box-click="onClick"></vorlesungsBox>
        </td>
    </tr>
</template>

<script>
import vorlesungsBox from "../timetable/VorlesungsBox.vue";

export default {
    name: "stundenplanRow",
    props: ['row', 'hover'],
    components: {
        vorlesungsBox
    },
    methods: {
        onHoover(vId){
            this.$emit("box-hoover", vId)
        },
        onClick(vId){
            this.$emit("box-click", vId)
        }
    },
    emits:['box-hoover','box-click']
}
</script>
