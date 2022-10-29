<template>
    <div :class="['lectureBox', 'smallText', 'vorl_' + data.id, { 'border-primary': isHover }, { 'text-primary': isHover }, { 'border-info': isSubHover }, { 'text-info': isSubHover }]"
        @mouseover="onMouseOver(data.id)" @mouseleave="onMouseLeave()" @dblclick="boxClick(data.id)">
        <p class="card-title"><strong>{{ data.name }}</strong></p>
        <p class="card-subtitle mb-2 text-muted">{{ data.id }}</p>
        <p v-if="data.dozent.length > 0" class="text-truncate"><strong>Dozent:</strong> {{ shorter(data.dozent, 10) }}
        </p>
        <p v-if="data.hs && data.hs.length > 0"><strong>HS:</strong> {{ data.hs }}</p>
        <p v-if="data.time && data.time.length > 0"><strong>Zeit:</strong> {{ data.time }}</p>
        <p><strong>Blöcke:</strong> {{ data.size }}</p>
    </div>
</template>

<script>
export default {
    name: "vorlesungsBox",
    props: ['data', 'hover'],
    emits: ['box-hover', 'box-click'],
    data() {
        return {
            isHover: this.hover == this.data.id,
            isSubHover: this.hover == this.data.base
        }
    },
    watch: {
        hover(val) {
            this.isHover = val == this.data.id
            this.isSubHover = !this.isHover && val.includes(this.data.base)
        }
    },
    methods: {
        onMouseOver(value) {
            this.$emit('box-hover', value)
        },
        onMouseLeave() {
            this.$emit('box-hover', "")
        },
        boxClick(value) {
            this.$emit('box-click', value)
        },
        shorter(content, length = 50) {
            return content.length > length ? content.slice(0, length) + "..." : content;
        }
    }
}
</script>

<style>
.smallText {
    text-align: left !important;
    font-size: 0.7rem !important;
}

.lectureBox {
    padding: 10px;
    background: rgb(241, 241, 241);
    height: 100%;
    border-color: grey;
    border-width: 1px;
    border-style: solid;
}
</style>
