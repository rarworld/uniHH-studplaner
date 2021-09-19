<template>
  <div class="accordion" :id="level">
    <div class="accordion-item">
      <h2 class="accordion-header" :id="level+'-heading'">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" :data-bs-target="'#'+level+'-collapseOne'" aria-expanded="false" :aria-controls="level+'-collapseOne'">
          {{ submenu.name }}
        </button>
      </h2>
      <div :id="level+'-collapseOne'" class="accordion-collapse collapsed collapse" :aria-labelledby="level+'-heading'">
        <div class="accordion-body">
          <navsubmenu v-for="(sub, index) in submenu.submenu" :key="level+'_'+index" :level="level+'_'+index" 
              :submenu="sub" @nav-cb="onNavCbChange" :activeVorlesungen="activeVorlesungen"></navSubmenu>
          <navEntry v-for="(entry, index) in submenu.entries" 
              :key="level+'_e_'+index" :level="level+'_e_'+index" 
              :data="entry" @nav-cb="onNavCbChange" :activeVorlesungen="activeVorlesungen">
          </navEntry>
        </div>
      </div>
    </div>
  </div>

  
</template>

<script>
import navEntry from "./NavEntry.vue";

export default {
    name: "navsubmenu",
    props: ['level','submenu','onNavChange','activeVorlesungen'],
    components: {
        navEntry
    },
    methods: {
        onNavCbChange(vId, value){
          this.$emit("nav-cb", vId, value);
        }
    },
    emits:['nav-cb']
}
</script>

