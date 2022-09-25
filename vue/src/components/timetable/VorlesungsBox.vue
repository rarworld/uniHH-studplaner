<template>
    <div :class="['smallText', 'card','vorl_'+data.id, {'border-primary': isHoover}, {'text-primary': isHoover},{'border-info': isSubHoover}, {'text-info': isSubHoover}]" 
            @mouseover="$emit('box-hoover',data.id)" @mouseleave="$emit('box-hoover','')" @dblclick="test(data.id)">
        <div class="card-body">
            <div class="card-title"><strong>{{ data.name }}</strong></div>
            <div class="card-subtitle mb-2 text-muted">{{ data.id}}</div>
            <div v-if="data.dozent.length > 0" class="text-truncate"><strong>Dozent:</strong> {{ shorter(data.dozent,10) }}</div>
            <div v-if="data.hs.length > 0"><strong>HS:</strong> {{ data.hs }}</div>
            <div v-if="data.time.length > 0"><strong>Zeit:</strong> {{ data.time }}</div>
        </div>
    </div>
</template>

<script>
export default {
    name: "vorlesungsBox",
    props: ['data','hover'],
    emits: ['box-hoover','box-click'],
    data() {
        return {
            isHoover: this.hover == this.data.id,
            isSubHoover: this.hover == this.data.base
        }
    },
    watch: {
        hover(val){
           this.isHoover= val == this.data.id 
           this.isSubHoover= !this.isHoover && val.includes(this.data.base)
        }
    },
    methods:{
        test(value){
            this.$emit('box-click',value)
        },
        shorter(content, length=50){
            return content.length > length ? content.slice(0, length) + "..." : content;
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
