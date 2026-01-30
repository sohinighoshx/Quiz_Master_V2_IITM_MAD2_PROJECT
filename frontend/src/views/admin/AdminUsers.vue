<template>
  <AdminLayout>
    <div class="admin-users p-4">
      <h2 class="text-center mb-4">👥 User Management</h2>

      <input
        type="text"
        v-model="searchQuery"
        class="form-control mb-3 search-input"
        placeholder="Search users by name or email"
      />

      <div class="table-responsive">
        <table class="table table-bordered table-hover table-striped text-center">
          <thead class="table-dark">
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>DOB</th>
              <th>Qualification</th>
              <th>Quizzes Attempted</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.id">
              <td>{{ user.full_name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.dob }}</td>
              <td>{{ user.qualification }}</td>
              <td>{{ user.quizzes_attempted }}</td>
              <td>
                <button class="btn btn-primary btn-sm me-1" @click="viewUser(user.id)">View</button>
                <button class="btn btn-warning btn-sm me-1" @click="openEditUser(user)">Edit</button>
                <button class="btn btn-danger btn-sm" @click="deleteUser(user.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- VIEW USER MODAL -->
      <div v-if="showViewModal" class="modal-overlay">
        <div class="modal-content">
          <h4>User Profile</h4>
          <p><strong>Name:</strong> {{ viewUserData.full_name }}</p>
          <p><strong>Email:</strong> {{ viewUserData.email }}</p>
          <p><strong>DOB:</strong> {{ viewUserData.dob }}</p>
          <p><strong>Qualification:</strong> {{ viewUserData.qualification }}</p>
          <button class="btn btn-secondary" @click="showViewModal = false">Close</button>
        </div>
      </div>

      <!-- EDIT USER MODAL -->
      <div v-if="showEditModal" class="modal-overlay">
        <div class="modal-content">
          <h4>Edit User</h4>
          <input v-model="editUserData.full_name" class="form-control mb-2" placeholder="Full Name" />
          <input v-model="editUserData.email" class="form-control mb-2" placeholder="Email" />
          <input v-model="editUserData.dob" class="form-control mb-2" placeholder="DOB" />
          <input v-model="editUserData.qualification" class="form-control mb-3" placeholder="Qualification" />
          <div class="d-flex justify-content-between">
            <button class="btn btn-primary" @click="updateUser">Save</button>
            <button class="btn btn-secondary" @click="showEditModal = false">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script>
import axios from 'axios'
import AdminLayout from '@/layouts/AdminLayout.vue'

export default {
  name: "AdminUsers",
  components: { AdminLayout },
  data() {
    return {
      users: [],
      searchQuery: '',
      showViewModal: false,
      showEditModal: false,
      viewUserData: {},
      editUserData: {}
    }
  },
  computed: {
    filteredUsers() {
      const q = this.searchQuery.toLowerCase()
      return this.users.filter(
        u =>
          u.full_name.toLowerCase().includes(q) ||
          u.email.toLowerCase().includes(q)
      )
    }
  },
  methods: {
    async fetchUsers() {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.get('/admin/users', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.users = res.data
      } catch (err) {
        console.error("Failed to fetch users", err)
      }
    },
    async viewUser(id) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.get(`/admin/user/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.viewUserData = res.data
        this.showViewModal = true
      } catch (err) {
        console.error("View failed", err)
      }
    },
    openEditUser(user) {
      this.editUserData = { ...user }
      this.showEditModal = true
    },
    async updateUser() {
      try {
        const token = localStorage.getItem('token')
        await axios.put(`/admin/user/${this.editUserData.id}`, this.editUserData, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.showEditModal = false
        this.fetchUsers()
      } catch (err) {
        console.error("Update failed", err)
      }
    },
    async deleteUser(id) {
      if (!confirm("Are you sure you want to delete this user?")) return
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`/admin/user/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.fetchUsers()
      } catch (err) {
        console.error("Delete failed", err)
      }
    }
  },
  mounted() {
    this.fetchUsers()
  }
}
</script>

<style scoped>
.admin-users {
  font-family: 'Playfair Display', serif;
  background: #fdfbff;
  min-height: 100vh;
}

.search-input {
  max-width: 400px;
  margin: 0 auto;
  border-radius: 10px;
  padding: 0.5rem;
  font-weight: 500;
}

/* MODAL STYLES */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(10, 10, 10, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 400px;
  font-family: 'Playfair Display', serif;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
}

.modal-content h4 {
  margin-bottom: 1rem;
}
</style>
