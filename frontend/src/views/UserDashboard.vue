<template>
  <div class="dashboard-wrapper">
    <Sidebar @toggle="handleSidebarToggle" class="sidebar-element" />

    <div :class="['content-area', { 'sidebar-collapsed': isSidebarCollapsed }]">
      <div class="container py-5">
        
        <header class="dashboard-header text-center mb-5">
          <h1 class="display-5 text-white fw-bold tracking-tight">
            Welcome back, <span class="text-accent">Scholar</span> 👋
          </h1>
          <p class="lead text-white-50">
            You've completed <span class="fw-bold text-white">85%</span> of your weekly goal. Keep going!
          </p>
        </header>

        <div class="row g-4">
          <div
            v-for="card in cards"
            :key="card.title"
            class="col-xl-4 col-md-6"
          >
            <div class="glass-card h-100" :class="{ 'logout-card': card.action === 'logout' }">
              <div class="card-content">
                <div class="icon-box mb-4">
                  <span class="icon-display">{{ card.icon }}</span>
                </div>

                <div class="text-section">
                  <h4 class="card-title text-white mb-2">{{ card.title }}</h4>
                  <p class="card-description text-white-50 small">
                    {{ card.text }}
                  </p>
                </div>

                <div class="action-section mt-4">
                  <button
                    v-if="card.action === 'logout'"
                    @click="logout"
                    class="btn-glass btn-logout w-100"
                  >
                    Logout System
                  </button>

                  <router-link
                    v-else
                    :to="card.link"
                    class="btn-glass btn-action w-100"
                  >
                    Enter Module
                  </router-link>
                </div>
              </div>
              <div class="card-glow"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue';

export default {
  name: "UserDashboard",
  components: { Sidebar },
  data() {
    return {
      isSidebarCollapsed: false,
      cards: [
        { title: "Settings", text: "Configure your workspace, themes, and audio.", link: "/user/settings", icon: "⚙️" },
        { title: "Library", text: "Access curated study materials and chapter notes.", link: "/user/read-notes", icon: "📚" },
        { title: "Challenge", text: "Test your knowledge with adaptive AI quizzes.", link: "/user/quizzes", icon: "🧠" },
        { title: "Insights", text: "Detailed breakdown of your academic journey.", link: "/user/history", icon: "📖" },
        { title: "Analytics", text: "Real-time performance metrics and charts.", link: "/user/progress", icon: "📊" },
        { title: "Sign Out", text: "Securely terminate your active session.", action: "logout", icon: "🚪" }
      ]
    };
  },
  methods: {
    handleSidebarToggle(collapsed) {
      this.isSidebarCollapsed = collapsed;
    },
    logout() {
      localStorage.clear();
      this.$router.push("/");
    }
  }
};
</script>

<style scoped>
/* Layout Structure */
.dashboard-wrapper {
  display: flex;
  min-height: 100vh;
  background: radial-gradient(circle at top left, #1e1e2f, #11111d);
  overflow-x: hidden;
}

.content-area {
  flex: 1;
  margin-left: 260px; /* Adjust to your sidebar default width */
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.content-area.sidebar-collapsed {
  margin-left: 80px;
}

/* Glassmorphism Cards */
.glass-card {
  position: relative;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 2rem;
  overflow: hidden;
  transition: all 0.3s ease;
  z-index: 1;
}

.glass-card:hover {
  transform: translateY(-10px);
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

/* Icon Styling */
.icon-box {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  transition: transform 0.3s ease;
}

.glass-card:hover .icon-box {
  transform: scale(1.1) rotate(5deg);
  background: rgba(0, 174, 255, 0.2);
}

/* Buttons */
.btn-glass {
  padding: 12px;
  border-radius: 12px;
  border: none;
  font-weight: 600;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.btn-action {
  background: #ffffff;
  color: #11111d;
}

.btn-action:hover {
  background: #00aeff;
  color: white;
  box-shadow: 0 0 15px rgba(0, 174, 255, 0.5);
}

.btn-logout {
  background: rgba(255, 68, 68, 0.1);
  border: 1px solid rgba(255, 68, 68, 0.3);
  color: #ff4444;
}

.btn-logout:hover {
  background: #ff4444;
  color: white;
}

/* Accent Colors */
.text-accent {
  background: linear-gradient(to right, #00aeff, #ff009d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Card Glow Effect */
.card-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(0, 174, 255, 0.05) 0%, transparent 70%);
  pointer-events: none;
  z-index: -1;
}

.tracking-tight {
  letter-spacing: -1px;
}
</style>