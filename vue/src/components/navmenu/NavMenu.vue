<template>
  <navsubmenu v-for="(sub,index) in navListe" :key="'0_'+index" :level="'_0'+index" 
      :submenu="sub" @nav-cb="onNavCbChange" :activeVorlesungen="activeVorlesungen">

  </navsubmenu>
</template>

<script>
import navData from "../../assets/nav.json";
import navsubmenu from "./NavSubMenu.vue";

export default {
    name: "navMenu",
    props: ['onNavChange','activeVorlesungen'],
    components: {
        navsubmenu
    },
    data() {
      return {
        navListe: navData
      }
    },
    methods: {
        onNavCbChange(vId, value){
          this.$emit("nav-cb", vId, value);
        }
    },
    emits:['nav-cb']
}
</script>

