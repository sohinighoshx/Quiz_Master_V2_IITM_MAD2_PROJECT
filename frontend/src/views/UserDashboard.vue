<template>
  <div class="user-layout">
    <Sidebar @toggle="handleSidebarToggle" />

    <div :class="['main-content', { collapsed: isSidebarCollapsed }]">
      <div class="user-dashboard container-fluid py-4">
        <h2 class="text-center mb-4 text-white">🎓 User Dashboard</h2>

        <div class="row g-4 justify-content-center">
          <div class="col-md-5" v-for="card in cards" :key="card.title">
            <div class="card bg-light-purple h-100 text-center shadow p-3" style="border-radius: 20px;">
              <div class="card-body">
                <h5 class="card-title">{{ card.title }}</h5>
                <p class="card-text">{{ card.text }}</p>

                <!-- 🔁 Conditional: Logout button vs Router Link -->
                <button
                  v-if="card.action === 'logout'"
                  @click="logout"
                  :class="['btn', card.btnClass]"
                >
                  Logout
                </button>
                <router-link
                  v-else
                  :to="card.link"
                  :class="['btn', card.btnClass]"
                >
                  Go
                </router-link>
              </div>
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
  components: {
    Sidebar
  },
  data() {
    return {
      isSidebarCollapsed: false,
      cards: [
        {
          title: "📚 Browse Quizzes",
          text: "Choose a subject and chapter to start a quiz.",
          link: "/user/quizzes",
          btnClass: "btn-primary"
        },
        {
          title: "📖 Quiz History",
          text: "View your previous scores and quiz attempts.",
          link: "/user/history",
          btnClass: "btn-success"
        },
        {
          title: "📊 My Progress",
          text: "Track your progress with charts and stats.",
          link: "/user/progress",
          btnClass: "btn-warning"
        },
        {
          title: "🚪 Logout",
          text: "Click here to logout and return to the home page.",
          link: null,
          btnClass: "btn-danger",
          action: "logout"
        }
      ]
    };
  },
  methods: {
    handleSidebarToggle(collapsed) {
      this.isSidebarCollapsed = collapsed;
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.user-layout {
  display: flex;
  min-height: 100vh;
}

.main-content {
  margin-left: 250px;
  width: calc(100% - 250px);
  background: linear-gradient(to right, #d5aaff, #c6c1ff);
  transition: all 0.3s ease;
}

.main-content.collapsed {
  margin-left: 80px;
  width: calc(100% - 80px);
}

.user-dashboard {
  min-height: 100vh;
}

.card {
  transition: 0.3s ease-in-out;
}
.card:hover {
  transform: scale(1.03);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.bg-light-purple {
  background-color: rgba(245, 235, 255, 0.85);
  border: none;
}
</style>
