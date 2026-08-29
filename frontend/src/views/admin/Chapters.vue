<template>
  <AdminLayout>
    <div>
      <h2 class="gothic-heading">📘 Chapters under "{{ subjectName }}"</h2>

      <table class="table table-bordered shadow-sm">
        <thead class="thead-dark">
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Quizzes</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="chapter in chapters" :key="chapter.id">
            <td>{{ chapter.name }}</td>
            <td>{{ chapter.description }}</td>
            <td>{{ chapter.quiz_count }}</td>
            <td>
              <button class="btn btn-sm btn-outline-primary" @click="openEditChapter(chapter)">Edit</button>
              <button class="btn btn-sm btn-outline-danger ms-2" @click="deleteChapter(chapter.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="text-end mt-4">
        <button class="btn btn-dark" @click="showAddChapterForm = true">➕ Create Chapter</button>
      </div>

      <!-- Modal: Add Chapter -->
      <div v-if="showAddChapterForm" class="modal-overlay">
        <div class="modal-form">
          <h2>Add Chapter</h2>
          <input v-model="chapterForm.name" placeholder="Chapter Name" />
          <textarea v-model="chapterForm.description" placeholder="Description"></textarea>
          <div class="modal-actions">
            <button @click="submitAddChapter">Create</button>
            <button class="cancel" @click="closeModals">Cancel</button>
          </div>
        </div>
      </div>

      <!-- Modal: Edit Chapter -->
      <div v-if="editChapterForm" class="modal-overlay">
        <div class="modal-form">
          <h2>Edit Chapter</h2>
          <input v-model="chapterForm.name" placeholder="Chapter Name" />
          <textarea v-model="chapterForm.description" placeholder="Description"></textarea>
          <div class="modal-actions">
            <button @click="submitEditChapter">Update</button>
            <button class="cancel" @click="closeModals">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script>
import AdminLayout from '@/layouts/AdminLayout.vue'
import axios from '@/axios'

export default {
  components: { AdminLayout },
  data() {
    return {
      chapters: [],
      subjectName: '',
      showAddChapterForm: false,
      editChapterForm: false,
      chapterForm: {
        id: null,
        name: '',
        description: ''
      }
    }
  },
  async mounted() {
    await this.loadChapters()
  },
  methods: {
    async loadChapters() {
      const subjectId = this.$route.params.id
      const token = localStorage.getItem('token')
      try {
        const subjRes = await axios.get('/admin/subject', {
          headers: { Authorization: `Bearer ${token}` }
        })
        const subject = subjRes.data.find(s => s.id == subjectId)
        this.subjectName = subject?.name || 'Unknown'

        const res = await axios.get(`/admin/subject/${subjectId}/chapters`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.chapters = res.data
      } catch (e) {
        console.error('Failed to load chapters', e)
      }
    },
    openEditChapter(chapter) {
      this.editChapterForm = true
      this.chapterForm = { ...chapter }
    },
    async submitEditChapter() {
      const token = localStorage.getItem('token')
      await axios.put(`/admin/chapter/${this.chapterForm.id}`, {
        name: this.chapterForm.name,
        description: this.chapterForm.description
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.closeModals()
      await this.loadChapters()
    },
    async deleteChapter(id) {
      if (!confirm('Are you sure?')) return
      const token = localStorage.getItem('token')
      await axios.delete(`/admin/chapter/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      await this.loadChapters()
    },
    async submitAddChapter() {
      const token = localStorage.getItem('token')
      await axios.post(`/admin/chapter`, {
        subject_id: this.$route.params.id,
        name: this.chapterForm.name,
        description: this.chapterForm.description
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.closeModals()
      await this.loadChapters()
    },
    closeModals() {
      this.showAddChapterForm = false
      this.editChapterForm = false
      this.chapterForm = { id: null, name: '', description: '' }
    }
  }
}
</script>

<style scoped>
.gothic-heading {
  font-family: 'Playfair Display', serif;
  font-size: 1.6rem;
  margin-bottom: 1.5rem;
  color: #222;
}

.table th {
  background-color: #2c2c2c;
  color: #f0f0f0;
  font-family: 'Playfair Display', serif;
}

.table td {
  font-family: 'Roboto', sans-serif;
}

.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal-form {
  background: #fff;
  padding: 2rem;
  border-radius: 16px;
  width: 400px;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  font-family: 'Playfair Display', serif;
}

.modal-form input,
.modal-form textarea {
  padding: 0.6rem;
  border-radius: 10px;
  border: 1px solid #aaa;
  background: #fafafa;
  font-size: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
}
.modal-actions .cancel {
  background: #eee;
  padding: 0.4rem 1rem;
  border-radius: 10px;
  font-weight: bold;
}
</style>
