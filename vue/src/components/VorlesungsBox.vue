<template>
    <div :class="['smallText', 'card','vorl_'+data.id, {'border-primary': isHoover}, {'text-primary': isHoover}]" 
            @mouseover="$emit('box-hoover',data.id)" @mouseleave="$emit('box-hoover','')">
        <div class="card-body">
            <div class="card-title"><strong>{{ data.name }}</strong></div>
            <div class="card-subtitle mb-2 text-muted">{{ data.id}}</div>
            <div v-if="data.dozent.length > 0" class="text-truncate"><strong>Dozent:</strong> {{ data.dozent }}</div>
            <div v-if="data.hs.length > 0"><strong>HS:</strong> {{ data.hs }}</div>
        </div>
    </div>
</template>

<script>
export default {
    name: "vorlesungsBox",
    props: ['data','hover'],
    emits: ['box-hoover'],
    data() {
        console.log(this.hover == this.data.id)
        return {
            isHoover: this.hover == this.data.id
        }
    },
    watch: {
        hover(val){
           this.isHoover= val == this.data.id 
        }
    }
}
</script>

<style scoped>
    .smallText {
        text-align: left !important;
        font-size: 0.7rem !important;
    }
</style>
