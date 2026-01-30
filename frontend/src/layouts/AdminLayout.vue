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
      <slot />
    </main>
  </div>
</template>

<script>
export default {
  name: "AdminLayout",
  data() {
    return {
      isSidebarCollapsed: false
    }
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

.content {
  flex-grow: 1;
  padding: 2rem;
  background: #ffffff;
  overflow-y: auto;
}
</style>
