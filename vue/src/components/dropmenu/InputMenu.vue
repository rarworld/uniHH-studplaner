<template>
  <form method="GET">
    <div class="row">
      <div class="col-10">
        <input name="activList" class="form-control" :value="lectureList" placeholder="[VorlesugsId,…]" />
      </div>
      <div class="col-auto">
        <button type="submit" class="btn btn-primary mb-3">Laden</button>
      </div>
    </div>
  </form>
</template>

<script>

export default {
  name: "inputMenu",
  props: ['lectureList'],
  components: {},
  data() {
    return {
    }
  },
  methods: {
  },
  watch: {

  },
  emits: []
}
</script>

