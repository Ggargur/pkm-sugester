<template>
  <div class="modal fade" id="alertModal" tabindex="-1" aria-labelledby="alertModalLabel" aria-hidden="true"
    ref="modal">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content bg-dark text-white border-secondary">
        <div class="modal-header bg-warning text-dark">
          <h5 class="modal-title" id="alertModalLabel">
            <i class="fas fa-exclamation-triangle me-2"></i>Atenção
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
        </div>
        <div class="modal-body" v-html="message"></div>
        <div class="modal-footer">
          <button type="button" class="btn btn-outline-warning" data-bs-dismiss="modal">
            OK
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';

export default {
  data() {
    return {
      message: '',
      modalInstance: null,
    };
  },
  mounted() {
    const modalElement = this.$refs.modal;
    this.modalInstance = new Modal(modalElement);
  },
  methods: {
    show(msg) {
      this.message = msg;
      this.modalInstance.show();
    },
  },
};
</script>