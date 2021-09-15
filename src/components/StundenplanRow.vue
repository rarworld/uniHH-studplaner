<template>
    <tr>
        <th scope="row">{{ row.timeRange }}</th>
        <th v-for="(day,i) in row.data" scope="col" :id="'col_'+row.id+'_'+i" :key="row.id+'_'+i">
            <vorlesungsBox v-for="(vorl, index) in row.data[i]" :key="index" :data="vorl" @box-hoover="onHoover" :hover="hover"></vorlesungsBox>
        </th>
    </tr>
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
            this.$emit("box-selected", vId);
        }
    },
    emits:['box-selected']
}
</script>
