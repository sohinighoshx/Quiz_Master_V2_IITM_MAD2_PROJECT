<template>
  <Transition name="modal">
    <div class="modal-backdrop" @click.self="$emit('close')">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ note.title }}</h5>
          <button class="btn-close" @click="$emit('close')">×</button>
        </div>
        <div class="modal-body">
          <p class="note-content">{{ note.content }}</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="$emit('close')">Close</button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  name: "NoteModal",
  props: {
    note: {
      type: Object,
      required: true
    }
  },
  emits: ["close"]
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 20px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  color: #333;
  margin: 0;
  font-weight: 600;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #999;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  color: #333;
}

.modal-body {
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}

.note-content {
  white-space: pre-wrap;
  line-height: 1.8;
  color: #444;
  font-size: 1.1rem;
}

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid #eee;
  text-align: right;
}

/* Animation */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-content {
  transform: scale(0.95);
}

.modal-leave-to .modal-content {
  transform: scale(0.95);
}
</style>