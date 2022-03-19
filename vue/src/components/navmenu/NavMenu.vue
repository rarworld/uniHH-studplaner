<template>
  <div>
    <navsubmenu v-for="(sub,index) in navListe" :key="'0_'+index" :level="'_0'+index" 
      :submenu="sub" @navSubMenuInput="$emit('navMenuInput',$event)" :activeVorlesungen="activeVorlesungen">

    </navsubmenu>
  </div>
</template>

<script>
import navData from "../../assets/nav.json";
import navsubmenu from "./NavSubMenu.vue";

export default {
    name: "navMenu",
    props: ['activeVorlesungen'],
    components: {
        navsubmenu
    },
    data() {
      return {
        navListe: navData
      }
    },
    emits:['navMenuInput']
}
</script>

