<template>
    <div :class="'card vorl_'+data.id" style="width: 18rem;">
        <div class="card-body">
            <h6 class="card-title">{{ data.name }}</h6>
            <div @mouseover="$emit('tata',data.id)" class="card-text fs-6">
                <div>{{ data.prof }}</div>
                <div>{{ data.time }}</div>
                <button @click="$emit('tata',data.id)">blub</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "vorlesungsBox",
    props: ['data'],
    emits: ['tata']
}
</script>
