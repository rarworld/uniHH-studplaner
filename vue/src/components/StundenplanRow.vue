<template>
    <div class="row" :id="'tableRow_'+row.id">
        <div class="col-2 border fs-4">{{ row.timeRange }}</div>
        <div v-for="(day,i) in row.data" class="col-2 border" :id="'col_'+row.id+'_'+i" :key="row.id+'_'+i">
            <vorlesungsBox v-for="(vorl, index) in row.data[i]" :key="index" :data="vorl" @box-hoover="onHoover" :hover="hover"></vorlesungsBox>
        </div>
    </div>
</template>

<script>
import vorlesungsBox from "./VorlesungsBox.vue";

export default {
    name: "stundenplanRow",
    props: ['row', 'hover'],
    components: {
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
