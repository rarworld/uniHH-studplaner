<template>

  <div class="modalVue modal" tabindex="-1" role="dialog" ref="delModal" id="delModal">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Delete Vorlesung {{ vId }}</h5>
          <button type="button" class="close" aria-label="Close" @click="$emit('modalCancel')">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <p>Sicher das die Vorlesung <strong>{{ vId }}</strong> aus dem Plan entfernt werden soll?</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('modalCancel')">Cancel</button>
          <button type="button" class="btn btn-primary" @click="$emit('delModal',vId)">Delete</button>
        </div>
      </div>
    </div>
  </div> 
  
</template>

<script>

export default {
    name: "delModal",
    props: ['vId', 'delMethod'],
    emits: ['modalCancel', 'delModal']
}
</script>
<style>
  .modalVue.modal{
    display: inline;
  }
</style>

