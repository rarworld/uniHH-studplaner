<template>
    <tr>
        <th scope="row">{{ row.timeRange }}</th>
        <th scope="col" :id="'col_'+row.id+'_0'"><vorlesungsBox v-for="(vorl, index) in row.data[0]" :key="index" :data="vorl" @tata="onHoover"></vorlesungsBox></th>
        <th scope="col" :id="'col_'+row.id+'_1'"><vorlesungsBox v-for="(vorl, index) in row.data[1]" :key="index" :data="vorl"></vorlesungsBox></th>
        <th scope="col" :id="'col_'+row.id+'_2'"><vorlesungsBox v-for="(vorl, index) in row.data[2]" :key="index" :data="vorl"></vorlesungsBox></th>
        <th scope="col" :id="'col_'+row.id+'_3'"><vorlesungsBox v-for="(vorl, index) in row.data[3]" :key="index" :data="vorl"></vorlesungsBox></th>
        <th scope="col" :id="'col_'+row.id+'_4'"><vorlesungsBox v-for="(vorl, index) in row.data[4]" :key="index" :data="vorl"></vorlesungsBox></th>
    </tr>
</template>

<script>
import vorlesungsBox from "./VorlesungsBox.vue";

export default {
    name: "stundenplanRow",
    props: ['row'],
    components: {
        vorlesungsBox
    },
    methods: {
        onHoover(vId){
            console.log("StundenplanRow "+vId);
            this.$emit("toto", vId);
        }
    },
    emits:['toto']
}
</script>
