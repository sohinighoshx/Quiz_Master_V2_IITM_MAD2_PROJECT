<template>
  <div class="admin-dashboard">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ collapsed: isSidebarCollapsed }">
      <h2>QuizMaster</h2>
      <nav>
        <router-link to="/admin">🏠 Home</router-link>
        <router-link to="/admin/users">👥 Users</router-link>
        <router-link to="/admin/summary">📊 Summary</router-link>
        <router-link to="/admin/quizzes">📝 Quizzes</router-link>

        <router-link to="/">🚪 Logout</router-link>

      </nav>
      <button class="collapse-btn" @click="isSidebarCollapsed = !isSidebarCollapsed">
        {{ isSidebarCollapsed ? '🎡' : '🎡' }}
      </button>
    </aside>

    <!-- Main Content -->
    <main class="content">
      <header>
        <h1>Admin Dashboard</h1>
        <input
          v-model="searchQuery"
          @input="fetchSubjects"
          placeholder="Search subjects..."
          class="search-bar"
        />
      </header>

      <div class="subjects-container" :class="{ collapsed: isSidebarCollapsed }">
        <div
          v-for="subject in subjects"
          :key="subject.id"
          class="subject-card"
        >
          <h3>{{ subject.name }}</h3>
          <p>{{ subject.description }}</p>
          <div class="card-actions">
            <button @click="$router.push(`/admin/subject/${subject.id}/chapters`)" class="link">Show Details</button>
            <button class="edit" @click="openEditForm(subject)">Edit</button>
            <button class="delete" @click="deleteSubject(subject.id)">Delete</button>
          </div>
        </div>
      </div>

      <div class="add-subject">
        <button class="add-btn" @click="showAddForm = true">+ ADD SUBJECT</button>
      </div>

      <!-- Modal for Add/Edit Subject -->
      <div class="modal-overlay" v-if="showAddForm || editForm">
        <div class="modal-form">
          <h2>{{ editForm ? 'Edit Subject' : 'Add Subject' }}</h2>
          <input v-model="form.name" placeholder="Subject Name" />
          <textarea v-model="form.description" placeholder="Description"></textarea>
          <div class="modal-actions">
            <button @click="submitForm">{{ editForm ? 'Update' : 'Create' }}</button>
            <button class="cancel" @click="closeModal">Cancel</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      subjects: [],
      searchQuery: '',
      showAddForm: false,
      editForm: false,
      form: {
        id: null,
        name: '',
        description: ''
      },
      isSidebarCollapsed: false
    }
  },
  methods: {
    async fetchSubjects() {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.get('/admin/subject', {
          headers: { Authorization: `Bearer ${token}` },
          params: { q: this.searchQuery }
        })
        this.subjects = res.data
      } catch (err) {
        console.error('Error fetching subjects:', err)
      }
    },
    async deleteSubject(id) {
      if (!confirm('Are you sure you want to delete this subject?')) return
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`/admin/subject/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        await this.fetchSubjects()
      } catch (err) {
        console.error('Delete failed:', err)
      }
    },
    openEditForm(subject) {
      this.editForm = true
      this.form = { ...subject }
    },
    closeModal() {
      this.editForm = false
      this.showAddForm = false
      this.form = { id: null, name: '', description: '' }
    },
    async submitForm() {
      const token = localStorage.getItem('token')
      const headers = { Authorization: `Bearer ${token}` }

      try {
        if (this.editForm) {
          await axios.put(`/admin/subject/${this.form.id}`, this.form, { headers })
        } else {
          await axios.post('/admin/subject', this.form, { headers })
        }
        this.fetchSubjects()
        this.closeModal()
      } catch (err) {
        console.error('Save failed:', err)
      }
    },
    viewDetails(id) {
      this.$router.push({ name: 'SubjectDetails', params: { id } })
    }
  },
  mounted() {
    this.fetchSubjects()
  }
}
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Roboto:wght@400;500&display=swap');

.admin-dashboard {
  display: flex;
  height: 100vh;
  font-family: 'Playfair Display', serif;
  background-color: #fdfdfd;
  color: #1a1a1a;
}

/* Sidebar */
.sidebar {
  width: 220px;
  background-color: #1e1e1e;
  color: white;
  padding: 2rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  transition: width 0.3s ease;
  box-shadow: 4px 0 12px rgba(0, 0, 0, 0.2);
}

.sidebar h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.8rem;
  text-align: center;
  color: #ffffff;
  letter-spacing: 0.5px;
}

.sidebar nav a {
  font-family: 'Playfair Display', serif;
  display: block;
  color: #ccc;
  margin: 0.8rem 0;
  text-decoration: none;
  font-size: 1rem;
  transition: color 0.3s;
}

.sidebar nav a:hover {
  color: #fff;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar.collapsed nav a,
.sidebar.collapsed h2 {
  display: none;
}

.collapse-btn {
  background: none;
  border: none;
  color: #999;
  font-size: 1.5rem;
  cursor: pointer;
  margin-top: auto;
  align-self: center;
}

/* Main content */
.content {
  flex-grow: 1;
  padding: 2rem;
  background: #ffffff;
  overflow-y: auto;
  transition: all 0.3s ease;
}

header h1 {
  font-family: 'Playfair Display', serif;
  font-size: 2.2rem;
  margin-bottom: 0.5rem;
  color: #1a1a1a;
}

header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
}

.search-bar {
  padding: 0.6rem 1rem;
  border-radius: 10px;
  border: 2px solid #333;
  background-color: #fafafa;
  color: #1a1a1a;
  width: 260px;
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  font-weight: 500;
}

/* Subjects Layout */
.subjects-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
  transition: grid-template-columns 0.3s ease;
}

/* Subject Cards */
.subject-card {
  background: #f8f8f8;
  border: 1px solid #ccc;
  padding: 1.2rem;
  border-radius: 16px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
  font-family: 'Playfair Display', serif;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.subject-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

/* Card Actions */
.card-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
  gap: 0.5rem;
}

.card-actions button {
  background: none;
  padding: 0.3rem 0.6rem;
  border-radius: 8px;
  font-size: 0.85rem;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  border: 1px solid #555;
  color: #1a1a1a;
  font-family: 'Playfair Display', serif;
}

.card-actions .edit {
  border-color: #2e7d32;
  color: #2e7d32;
}

.card-actions .edit:hover {
  background-color: #e8f5e9;
}

.card-actions .delete {
  border-color: #c62828;
  color: #c62828;
}

.card-actions .delete:hover {
  background-color: #ffebee;
}

/* Add Subject Button */
.add-subject {
  margin-top: 2rem;
  text-align: right;
}

.add-btn {
  background: #1e1e1e;
  color: white;
  padding: 0.6rem 1.2rem;
  border-radius: 20px;
  border: none;
  font-family: 'Playfair Display', serif;
  font-weight: bold;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: background 0.3s;
}

.add-btn:hover {
  background: #333;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(20, 20, 20, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-form {
  background: #ffffff;
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
  background-color: #fafafa;
  border: 1.5px solid #aaa;
  font-family: 'Playfair Display', serif;
  color: #333;
  font-size: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
}

.modal-actions .cancel {
  background: #eee;
  color: #222;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  border: none;
  font-weight: bold;
  font-family: 'Playfair Display', serif;
  transition: background 0.3s ease;
}

.modal-actions .cancel:hover {
  background: #ddd;
}
</style>
