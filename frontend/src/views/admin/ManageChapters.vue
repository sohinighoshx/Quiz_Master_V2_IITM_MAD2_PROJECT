<!-- ✅ ManageChapters.vue -->
<template>
  <div class="container py-4">
    <h3 class="mb-4">Manage Chapters</h3>
    <form @submit.prevent="addChapter">
      <select v-model="subject_id" class="form-select mb-2">
        <option disabled value="">Select Subject</option>
        <option v-for="s in subjects" :value="s.id">{{ s.name }}</option>
      </select>
      <input v-model="name" class="form-control mb-2" placeholder="Chapter Name" />
      <textarea v-model="description" class="form-control mb-2" placeholder="Description"></textarea>
      <button class="btn btn-primary">Add Chapter</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return { subject_id: '', name: '', description: '', subjects: [] }
  },
  async mounted() {
    const res = await axios.get('/api/subjects')
    this.subjects = res.data
  },
  methods: {
    async addChapter() {
      const token = localStorage.getItem('token')
      await axios.post('/admin/chapter', {
        subject_id: this.subject_id, name: this.name, description: this.description
      }, { headers: { Authorization: `Bearer ${token}` }})
      this.name = this.description = this.subject_id = ''
    }
  }
}
</script>