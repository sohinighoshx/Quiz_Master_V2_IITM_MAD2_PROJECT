<template>
  <div class="container py-4">
    <h3 class="mb-4 text-center">📚 Manage Subjects & Chapters</h3>

    <!-- Subject Form -->
    <form @submit.prevent="addSubject" class="mb-4 shadow-sm p-4 rounded bg-white">
      <input v-model="name" ref="nameInput" class="form-control mb-3" placeholder="Enter Subject Name" required />
      <textarea v-model="description" class="form-control mb-3" placeholder="Enter Subject Description" required />
      <button class="btn btn-purple w-100">
        {{ editMode ? 'Update Subject' : 'Add Subject' }}
      </button>
    </form>

    <!-- Loading -->
    <div v-if="loading" class="text-center mt-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2">Loading subjects...</p>
    </div>

    <!-- Subjects -->
    <div v-else>
      <h5 class="mb-3">Available Subjects</h5>
      <div class="row">
        <div v-for="subject in subjects" :key="subject.id" class="col-md-6 mb-4">
          <div class="shadow-sm subject-card text-dark">
            <h5 class="mb-1">{{ subject.name }}</h5>
            <p class="text-muted mb-3 small">{{ subject.description }}</p>

            <div class="d-flex justify-content-end mb-2">
              <button class="btn btn-sm btn-outline-primary me-2" @click="startEdit(subject)">✏️ Edit</button>
              <button class="btn btn-sm btn-outline-danger" @click="deleteSubject(subject.id)">🗑️ Delete</button>
            </div>

            <!-- Toggle Chapters -->
            <button class="btn btn-sm btn-purple w-100 mb-2" @click="toggleChapters(subject.id)">
              {{ showChapters[subject.id] ? 'Hide Chapters' : 'Show Chapters' }}
            </button>

            <!-- Chapter Form + List -->
            <div v-if="showChapters[subject.id]">
              <!-- Add/Edit Chapter Form -->
              <form @submit.prevent="saveChapter(subject.id)" class="mb-3 p-3 bg-light rounded">
                <h6 class="mb-3">{{ newChapter[subject.id].editId ? 'Edit Chapter' : 'Add New Chapter' }}</h6>
                <div class="mb-2">
                  <label class="form-label">Chapter Name</label>
                  <input v-model="newChapter[subject.id].name" class="form-control" placeholder="Enter chapter name" required />
                </div>
                <div class="mb-3">
                  <label class="form-label">Chapter Description</label>
                  <textarea v-model="newChapter[subject.id].description" class="form-control" placeholder="Enter chapter description" rows="3" required></textarea>
                </div>
                <button class="btn btn-sm btn-purple w-100">
                  {{ newChapter[subject.id].editId ? 'Update Chapter' : 'Add Chapter' }}
                </button>
                <button v-if="newChapter[subject.id].editId" 
                        class="btn btn-sm btn-outline-secondary w-100 mt-2" 
                        @click.prevent="cancelEdit(subject.id)">
                  Cancel
                </button>
              </form>

              <!-- Chapter List -->
              <div v-if="chapters[subject.id]?.length" class="mt-3">
                <h6 class="mb-3">Chapters:</h6>
                <div
                  v-for="(chapter, index) in chapters[subject.id]"
                  :key="chapter.id"
                  class="p-3 mb-3 bg-white rounded border shadow-sm"
                >
                  <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                      <h6 class="mb-1">
                        <span class="badge bg-secondary me-2">{{ index + 1 }}</span>
                        {{ chapter.name }}
                      </h6>
                      <p class="mb-0 text-muted small">{{ chapter.description }}</p>
                    </div>
                    <div class="btn-group">
                      <button class="btn btn-sm btn-outline-primary" @click="editChapter(subject.id, chapter)">✏️ Edit</button>
                      <button class="btn btn-sm btn-outline-danger" @click="deleteChapter(subject.id, chapter.id)">🗑️ Delete</button>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center p-3 bg-light rounded">
                <p class="text-muted mb-0">No chapters added yet</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios'

export default {
  data() {
    return {
      name: '',
      description: '',
      subjects: [],
      chapters: {},
      loading: false,
      editMode: false,
      editingId: null,
      showChapters: {},
      newChapter: {} // Maps subject.id => { name, description, editId }
    }
  },
  async mounted() {
    await this.loadSubjects()
  },
  methods: {
    // === SUBJECTS ===
    async loadSubjects() {
      try {
        this.loading = true
        const token = localStorage.getItem('token')
        const res = await axios.get('/admin/subject', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.subjects = res.data

        for (const s of res.data) {
          this.showChapters[s.id] = false
          this.newChapter[s.id] = { name: '', description: '', editId: null }
          await this.loadChapters(s.id)
        }
      } catch (err) {
        alert('❌ Failed to load subjects')
      } finally {
        this.loading = false
      }
    },
    async addSubject() {
      const token = localStorage.getItem('token')
      const payload = {
        name: this.name.trim(),
        description: this.description.trim()
      }

      try {
        if (this.editMode) {
          await axios.put(`/admin/subject/${this.editingId}`, payload, {
            headers: { Authorization: `Bearer ${token}` }
          })
          alert('✅ Subject updated')
        } else {
          await axios.post('/admin/subject', payload, {
            headers: { Authorization: `Bearer ${token}` }
          })
          alert('✅ Subject added')
        }

        this.name = ''
        this.description = ''
        this.editMode = false
        this.editingId = null
        await this.loadSubjects()
        this.$nextTick(() => this.$refs.nameInput?.focus?.())
      } catch (err) {
        alert('❌ Failed to save subject')
      }
    },
    startEdit(subject) {
      this.name = subject.name
      this.description = subject.description
      this.editingId = subject.id
      this.editMode = true
    },
    async deleteSubject(id) {
      if (!confirm('Are you sure?')) return
      const token = localStorage.getItem('token')
      await axios.delete(`/admin/subject/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      await this.loadSubjects()
    },
    toggleChapters(subjectId) {
      this.showChapters[subjectId] = !this.showChapters[subjectId]
    },

    // === CHAPTERS ===
    async loadChapters(subjectId) {
      const token = localStorage.getItem('token')
      try {
        const res = await axios.get(`/admin/search/chapters?q=`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.chapters[subjectId] = res.data.filter(ch => ch.subject_id === subjectId)
      } catch (err) {
        console.error('❌ Error loading chapters', err)
      }
    },
    async saveChapter(subjectId) {
      const token = localStorage.getItem('token')
      const ch = this.newChapter[subjectId]

      if (!ch.name || !ch.description) {
        return alert('Both chapter name and description are required.')
      }

      try {
        if (ch.editId) {
          await axios.put(`/admin/chapter/${ch.editId}`, {
            name: ch.name,
            description: ch.description
          }, {
            headers: { Authorization: `Bearer ${token}` }
          })
          alert('✅ Chapter updated!')
        } else {
          await axios.post('/admin/chapter', {
            subject_id: subjectId,
            name: ch.name,
            description: ch.description
          }, {
            headers: { Authorization: `Bearer ${token}` }
          })
          alert('✅ Chapter added!')
        }

        this.newChapter[subjectId] = { name: '', description: '', editId: null }
        await this.loadChapters(subjectId)
      } catch (err) {
        alert('❌ Failed to save chapter')
      }
    },
    editChapter(subjectId, chapter) {
      this.newChapter[subjectId] = {
        name: chapter.name,
        description: chapter.description,
        editId: chapter.id
      }
      // Scroll to the form
      this.$nextTick(() => {
        const card = this.$el.querySelector(`.card[data-subject-id="${subjectId}"]`)
        if (card) {
          const form = card.querySelector('form')
          form?.scrollIntoView({ behavior: 'smooth' })
        }
      })
    },
    cancelEdit(subjectId) {
      this.newChapter[subjectId] = { name: '', description: '', editId: null }
    },
    async deleteChapter(subjectId, chapterId) {
      const token = localStorage.getItem('token')
      if (!confirm('Delete this chapter?')) return

      try {
        await axios.delete(`/admin/chapter/${chapterId}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        await this.loadChapters(subjectId)
      } catch (err) {
        alert('❌ Failed to delete chapter')
      }
    }
  }
}
</script>

<style scoped>
.container {
  background: linear-gradient(to right, #f2e4ff, #e6d9ff);
  border-radius: 12px;
  min-height: 100vh;
}

.btn-purple {
  background-color: #7b2cbf;
  color: white;
  font-weight: bold;
  border: none;
}

.btn-purple:hover {
  background-color: #6829a8;
}

.bg-light-purple {
  background-color: #fff !important; /* changed to pure white */
  border-radius: 12px;
  padding: 16px;
}


.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
}

.chapter-item {
  transition: all 0.2s;
}

.chapter-item:hover {
  background-color: #f8f9fa;
}
.subject-card {
  background-color: #ffffff;
  border-radius: 16px; /* smooth, soft corners like your dashboard */
  padding: 16px;
  min-height: 150px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}


.form-label {
  font-weight: 500;
  color: #495057;
}
</style>