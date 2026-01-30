<template>
  <AdminLayout>
    <div class="admin-container p-4">
      <header class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
        <div>
          <nav aria-label="breadcrumb">
            <ol class="breadcrumb mb-1 small">
              <li class="breadcrumb-item text-muted">Subjects</li>
              <li class="breadcrumb-item active text-primary fw-semibold">{{ subjectName }}</li>
            </ol>
          </nav>
          <h2 class="gothic-heading mb-0 text-dark">📘 Chapter Management</h2>
        </div>
        <button class="btn btn-dark d-flex align-items-center gap-2 shadow-sm px-4" @click="prepareCreate">
          <i class="bi bi-plus-lg"></i> Create Chapter
        </button>
      </header>

      <div v-if="loading" class="d-flex flex-column align-items-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="mt-3 text-muted">Fetching chapters...</p>
      </div>

      <div v-else>
        <div v-if="chapters.length > 0" class="card shadow-sm border-0 rounded-3">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light text-uppercase small fw-bold text-muted">
                <tr>
                  <th class="ps-4 py-3">Chapter Name</th>
                  <th class="py-3">Description</th>
                  <th class="py-3 text-center">Resources</th>
                  <th class="text-end pe-4 py-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="chapter in chapters" :key="chapter.id" class="transition-row">
                  <td class="ps-4">
                    <div class="fw-bold text-dark">{{ chapter.name }}</div>
                  </td>
                  <td class="text-muted small w-25">
                    {{ chapter.description || 'No description provided.' }}
                  </td>
                  <td class="text-center">
                    <div class="d-flex justify-content-center gap-2">
                      <span class="badge rounded-pill bg-info-subtle text-info border border-info-subtle px-3">
                        🧪 {{ chapter.quiz_count }} Quizzes
                      </span>
                      <span class="badge rounded-pill bg-warning-subtle text-dark border border-warning-subtle px-3">
                        📝 {{ chapter.note_count }} Notes
                      </span>
                    </div>
                  </td>
                  <td class="text-end pe-4">
                    <div class="btn-group shadow-sm">
                      <button class="btn btn-sm btn-outline-success px-3" @click="goToNotes(chapter)">
                        <i class="bi bi-journal-text me-1"></i> Notes
                      </button>
                      <button class="btn btn-sm btn-outline-primary" title="Edit" @click="prepareEdit(chapter)">
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button class="btn btn-sm btn-outline-danger" title="Delete" @click="deleteChapter(chapter.id)">
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-else class="empty-state text-center py-5 bg-white rounded-3 shadow-sm border border-dashed">
          <div class="mb-3 display-4 text-muted opacity-25">📚</div>
          <h4>No chapters yet</h4>
          <p class="text-muted">Break down "{{ subjectName }}" into organized chapters.</p>
        </div>
      </div>

      <Transition name="modal-fade">
        <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
          <div class="modal-container shadow-lg border-0">
            <div class="modal-header bg-dark text-white p-3">
              <h5 class="mb-0">{{ isEditing ? '✏️ Edit Chapter' : '➕ New Chapter' }}</h5>
              <button type="button" class="btn-close btn-close-white shadow-none" @click="closeModal"></button>
            </div>
            
            <div class="modal-body p-4">
              <div class="row g-4">
                <div class="col-12">
                  <label class="form-label small text-uppercase fw-bold text-muted mb-1">Chapter Name</label>
                  <input 
                    v-model="chapterForm.name" 
                    class="form-control form-control-lg shadow-none" 
                    :class="{'is-invalid': errors.name}"
                    placeholder="e.g., Photosynthesis"
                  >
                  <div class="invalid-feedback">{{ errors.name }}</div>
                </div>

                <div class="col-12">
                  <label class="form-label small text-uppercase fw-bold text-muted mb-1">Description (Optional)</label>
                  <textarea 
                    v-model="chapterForm.description" 
                    class="form-control shadow-none" 
                    rows="4" 
                    placeholder="What will students learn in this chapter?"
                  ></textarea>
                </div>
              </div>
            </div>

            <div class="modal-footer border-top-0 p-4 pt-0">
              <button class="btn btn-light px-4 border" @click="closeModal">Cancel</button>
              <button class="btn btn-primary px-4 fw-bold shadow-sm" @click="submitChapter" :disabled="submitting">
                <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
                {{ isEditing ? 'Update Chapter' : 'Create Chapter' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
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
      chapters: [],
      subjectName: "Loading...",
      loading: false,
      submitting: false,
      showModal: false,
      isEditing: false,
      errors: {},
      chapterForm: {
        id: null,
        name: "",
        description: ""
      }
    };
  },

  async mounted() {
    await this.loadChapters();
  },

  methods: {
    async loadChapters() {
      const subjectId = this.$route.params.id;
      this.loading = true;
      try {
        // Optimally load subject name and chapters
        const [subjRes, chapRes] = await Promise.all([
          axios.get("/admin/subject"),
          axios.get(`/admin/subject/${subjectId}/chapters`)
        ]);

        const subject = subjRes.data.find(s => s.id == subjectId);
        this.subjectName = subject?.name || "Subject";
        this.chapters = chapRes.data;
      } catch (error) {
        this.$toast?.error("Failed to load data");
      } finally {
        this.loading = false;
      }
    },

    goToNotes(chapter) {
      this.$router.push({
        name: "AdminNotes",
        params: { chapterId: chapter.id, chapterName: chapter.name, subjectId: this.$route.params.id }
      });
    },

    prepareCreate() {
      this.isEditing = false;
      this.chapterForm = { id: null, name: "", description: "" };
      this.showModal = true;
    },

    prepareEdit(chapter) {
      this.isEditing = true;
      this.chapterForm = { ...chapter };
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.errors = {};
    },

    async submitChapter() {
      this.errors = {};
      if (!this.chapterForm.name.trim()) {
        this.errors.name = "Chapter name is required.";
        return;
      }

      this.submitting = true;
      try {
        const subjectId = this.$route.params.id;
        const payload = { 
          name: this.chapterForm.name, 
          description: this.chapterForm.description,
          subject_id: subjectId 
        };

        if (this.isEditing) {
          await axios.put(`/admin/chapter/${this.chapterForm.id}`, payload);
          this.$toast?.success("Chapter updated");
        } else {
          await axios.post(`/admin/chapter`, payload);
          this.$toast?.success("Chapter created");
        }

        this.closeModal();
        await this.loadChapters();
      } catch (error) {
        this.$toast?.error("Operation failed");
      } finally {
        this.submitting = false;
      }
    },

    async deleteChapter(id) {
      if (!confirm("Are you sure? This will remove all associated quizzes and notes.")) return;
      try {
        await axios.delete(`/admin/chapter/${id}`);
        this.$toast?.success("Chapter deleted");
        await this.loadChapters();
      } catch (error) {
        this.$toast?.error("Delete failed");
      }
    }
  }
};
</script>

<style scoped>
.admin-container {
  max-width: 1100px;
  margin: 0 auto;
}

.gothic-heading {
  font-family: "Playfair Display", serif;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.transition-row {
  transition: all 0.2s ease;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-container {
  background: white;
  border-radius: 16px;
  width: 95%;
  max-width: 450px;
  overflow: hidden;
}

.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

.border-dashed {
  border-style: dashed !important;
  background-color: #fcfcfc;
}
</style>