<template>
  <AdminLayout>
    <div class="container-fluid py-4">

      <div class="d-flex justify-content-between align-items-center mb-4">

        <h2 class="gothic-heading mb-0">
          📚 Notes for
          <span class="text-primary">
            "{{ subjectName }} / {{ chapterName }}"
          </span>
        </h2>

        <button class="btn btn-dark" @click="showAddNote = true">
          ➕ Upload Note
        </button>

      </div>

      <div class="card shadow-sm">
        <div class="table-responsive">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>Title</th>
                <th>Visibility</th>
                <th>Date</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="n in notes" :key="n.id">
                <td class="fw-bold">{{ n.title }}</td>

                <td>
                  <span :class="['badge', n.visibility === 'public' ? 'bg-success' : 'bg-secondary']">
                    {{ n.visibility }}
                  </span>
                </td>

                <td>{{ formatDate(n.created_at) }}</td>

                <td class="text-center">

                  <button class="btn btn-outline-primary btn-sm me-2" @click="openNote(n)">
                    View
                  </button>

                  <button class="btn btn-outline-warning btn-sm me-2" @click="openEdit(n)">
                    Edit
                  </button>

                  <button class="btn btn-outline-danger btn-sm" @click="deleteNote(n.id)">
                    Delete
                  </button>

                </td>
              </tr>

              <tr v-if="notes.length === 0">
                <td colspan="4" class="text-center py-4 text-muted">
                  No notes found for this chapter.
                </td>
              </tr>

            </tbody>
          </table>
        </div>
      </div>

      <!-- View Modal -->
      <div v-if="activeNote" class="custom-modal-overlay" @click.self="activeNote = null">
        <div class="custom-modal-content">
          <div class="modal-header">
            <h3>{{ activeNote.title }}</h3>
            <button type="button" class="btn-close" @click="activeNote = null"></button>
          </div>
          <div class="modal-body py-3">
            <p style="white-space: pre-wrap;">{{ activeNote.content }}</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="activeNote = null">Close</button>
          </div>
        </div>
      </div>

      <!-- Add Modal -->
      <div v-if="showAddNote" class="custom-modal-overlay" @click.self="closeAddModal">
        <div class="custom-modal-content">

          <div class="modal-header">
            <h3>Add New Note</h3>
            <button type="button" class="btn-close" @click="closeAddModal"></button>
          </div>

          <div class="modal-body">

            <div class="mb-3">
              <label class="form-label">Title</label>
              <input v-model="noteForm.title" class="form-control" placeholder="Enter note title">
            </div>

            <div class="mb-3">
              <label class="form-label">Content / Link</label>
              <textarea v-model="noteForm.content" rows="4" class="form-control" placeholder="Enter note content"></textarea>
            </div>

            <div class="mb-3">
              <label class="form-label">Visibility</label>
              <select v-model="noteForm.visibility" class="form-select">
                <option value="public">Public</option>
                <option value="private">Private</option>
              </select>
            </div>

          </div>

          <div class="modal-footer d-flex gap-2">
            <button class="btn btn-primary" @click="submitNote" :disabled="!noteForm.title.trim()">Save</button>
            <button class="btn btn-light" @click="closeAddModal">Cancel</button>
          </div>

        </div>
      </div>

      <!-- Edit Modal -->
      <div v-if="editNote" class="custom-modal-overlay" @click.self="editNote = null">
        <div class="custom-modal-content">

          <div class="modal-header">
            <h3>Edit Note</h3>
            <button type="button" class="btn-close" @click="editNote = null"></button>
          </div>

          <div class="modal-body">

            <div class="mb-3">
              <label class="form-label">Title</label>
              <input v-model="editForm.title" class="form-control">
            </div>

            <div class="mb-3">
              <label class="form-label">Content</label>
              <textarea v-model="editForm.content" rows="4" class="form-control"></textarea>
            </div>

            <div class="mb-3">
              <label class="form-label">Visibility</label>
              <select v-model="editForm.visibility" class="form-select">
                <option value="public">Public</option>
                <option value="private">Private</option>
              </select>
            </div>

          </div>

          <div class="modal-footer d-flex gap-2">
            <button class="btn btn-primary" @click="submitEditNote" :disabled="!editForm.title.trim()">Update</button>
            <button class="btn btn-light" @click="editNote = null">Cancel</button>
          </div>

        </div>
      </div>

    </div>
  </AdminLayout>
</template>

<script>
import AdminLayout from "@/layouts/AdminLayout.vue";
import axios from "@/axios";

export default {
  components: { AdminLayout },

  data() {
    return {
      subjectId: null,
      chapterId: null,

      subjectName: "Loading…",
      chapterName: "Loading…",

      notes: [],

      activeNote: null,
      showAddNote: false,
      editNote: null,

      noteForm: { title: "", content: "", visibility: "public" },
      editForm: { id: null, title: "", content: "", visibility: "public" }
    };
  },

  async created() {

    // read IDs from params
    this.subjectId = this.$route.params.subjectId;
    this.chapterId = this.$route.params.chapterId;

    await this.fetchNames();
    await this.loadNotes();
  },

  methods: {

    async fetchNames() {
      try {

        // get subject name
        const subjectRes = await axios.get(`/admin/subject/${this.subjectId}`);
        this.subjectName = subjectRes.data.name;

        // get chapter name
        const chapterRes = await axios.get(
          `/admin/subject/${this.subjectId}/chapters/${this.chapterId}`
        );
        this.chapterName = chapterRes.data.name;

      } catch (err) {
        this.subjectName = "Subject";
        this.chapterName = "Chapter";
        console.error("Could not load names", err);
      }
    },

    formatDate(d) {
      return d ? new Date(d).toLocaleDateString() : "";
    },

    async loadNotes() {
      try {
        const res = await axios.get(
          `/admin/subject/${this.subjectId}/chapter/${this.chapterId}/notes`
        );
        this.notes = res.data;
      } catch (err) {
        console.error("Failed to load notes:", err);
      }
    },

    openNote(n) {
      this.activeNote = n;
    },

    closeAddModal() {
      this.showAddNote = false;
      this.noteForm = { title: "", content: "", visibility: "public" };
    },

    async submitNote() {
      if (!this.noteForm.title.trim()) return alert("Please enter a title");

      try {
        await axios.post(
          `/admin/subject/${this.subjectId}/chapter/${this.chapterId}/notes`,
          {
            title: this.noteForm.title,
            content: this.noteForm.content,
            visibility: this.noteForm.visibility
          }
        );
        this.closeAddModal();
        await this.loadNotes();
      } catch (err) {
        console.error("Failed to add note:", err);
        alert("Failed to add note. Please try again.");
      }
    },

    openEdit(n) {
      this.editNote = n;
      this.editForm = {
        id: n.id,
        title: n.title,
        content: n.content,
        visibility: n.visibility
      };
    },

    async submitEditNote() {
      if (!this.editForm.title.trim()) return alert("Please enter a title");

      try {
        await axios.put(`/admin/notes/${this.editForm.id}`, {
          title: this.editForm.title,
          content: this.editForm.content,
          visibility: this.editForm.visibility
        });

        this.editNote = null;
        await this.loadNotes();

      } catch (err) {
        console.error("Failed to update note:", err);
        alert("Failed to update note. Please try again.");
      }
    },

    async deleteNote(id) {
      if (!confirm("Delete this note permanently?")) return;

      try {
        await axios.delete(`/admin/notes/${id}`);
        await this.loadNotes();
      } catch (err) {
        console.error("Failed to delete note:", err);
        alert("Failed to delete note. Please try again.");
      }
    }
  }
};
</script>

<style scoped>
.custom-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}
.custom-modal-content {
  background: white;
  padding: 1.8rem;
  border-radius: 10px;
  width: 500px;
  max-width: 95%;
  max-height: 90vh;
  overflow-y: auto;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid #dee2e6;
}
.modal-footer {
  padding-top: 1rem;
  border-top: 1px solid #dee2e6;
}
</style>
