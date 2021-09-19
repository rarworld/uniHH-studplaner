<template>
    <div :class="'card vorl_'+data.id" style="width: 14rem;" @mouseover="$emit('box-hoover',data.id)" >
        <div class="card-body" :class="{'hoverClass': hover == data.id}">
            <h6 class="card-title"><strong>{{ data.id}}</strong> {{ data.name }}</h6>
            <div class="card-text fs-6">
                <div>{{ data.dozent }}</div>
                <div>{{ data.hs }}</div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "vorlesungsBox",
    props: ['data','hover'],
    emits: ['box-hoover']
}
</script>

<style scoped>
    .hoverClass {
        background-color: blue;
    }
</style>
