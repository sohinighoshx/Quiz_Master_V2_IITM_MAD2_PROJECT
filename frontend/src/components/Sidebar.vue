<template>
  <div :class="['sidebar', { collapsed }]">
    <div class="sidebar-header d-flex justify-content-between align-items-center">
      <h3 v-if="!collapsed">User Menu</h3>
      <button @click="toggleSidebar" class="toggle-btn" :title="collapsed ? 'Expand' : 'Collapse'">
        🧠
      </button>
    </div>

    <ul class="sidebar-menu">
      <li>
        <router-link to="/user" class="sidebar-link">
          <i class="fas fa-home"></i>
          <span v-if="!collapsed">Dashboard</span>
        </router-link>
      </li>
      <li>
        <router-link to="/user/quizzes" class="sidebar-link">
          <i class="fas fa-book"></i>
          <span v-if="!collapsed">Browse Quizzes</span>
        </router-link>
      </li>
      <li>
        <router-link to="/user/history" class="sidebar-link">
          <i class="fas fa-history"></i>
          <span v-if="!collapsed">Quiz History</span>
        </router-link>
      </li>
      <li>
        <router-link to="/user/progress" class="sidebar-link">
          <i class="fas fa-chart-line"></i>
          <span v-if="!collapsed">My Progress</span>
        </router-link>
      </li>
      <li>
        <a @click="logout" class="sidebar-link" href="#">
          <i class="fas fa-sign-out-alt"></i>
          <span v-if="!collapsed">Logout</span>
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Sidebar',
  data() {
    return {
      collapsed: false
    }
  },
  methods: {
    toggleSidebar() {
      this.collapsed = !this.collapsed;
      this.$emit('toggle', this.collapsed); // Notify parent
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 250px;
  height: 100vh;
  background: linear-gradient(to bottom, #6a11cb, #2575fc);
  color: white;
  position: fixed;
  left: 0;
  top: 0;
  padding-top: 20px;
  transition: width 0.3s ease;
  z-index: 1000;
  overflow: hidden;
}

.sidebar.collapsed {
  width: 80px;
}

.sidebar-header {
  padding: 0 20px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toggle-btn {
  background: none;
  border: none;
  color: white;
  font-size: 22px;
  cursor: pointer;
  transition: transform 0.2s ease;
}
.toggle-btn:hover {
  transform: rotate(20deg);
}

.sidebar-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-menu li {
  margin-bottom: 5px;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s;
  font-size: 16px;
  white-space: nowrap;
}

.sidebar-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  padding-left: 25px;
}

.sidebar-link i {
  width: 20px;
  text-align: center;
}

.router-link-active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border-left: 4px solid white;
}
</style>
