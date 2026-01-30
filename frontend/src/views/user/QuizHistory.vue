<template>
  <div class="user-layout">
    <Sidebar @toggle="handleSidebarToggle" />

    <div :class="['main-content', { collapsed: isSidebarCollapsed }]">
      <div class="quiz-history container py-4">
        <!-- 🔹 Header -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="mb-0">📖 Quiz History</h2>
        </div>

        <!-- 🔹 History Loading Spinner -->
        <div v-if="loading" class="text-center">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <!-- 🔹 No History -->
        <div v-else-if="history.length === 0" class="text-center">
          <p>No quiz attempts found.</p>
        </div>

        <!-- 🔹 History Cards -->
        <div v-else>
          <div v-for="(attempt, index) in history" :key="index" class="card mb-4 shadow-sm">
            <div class="card-body">
              <h5 class="card-title">{{ attempt.quiz_title }}</h5>
              <div class="row">
                <div class="col-md-6">
                  <p class="mb-1"><strong>Subject:</strong> {{ attempt.subject_name }}</p>
                  <p class="mb-1"><strong>Chapter:</strong> {{ attempt.chapter_name }}</p>
                </div>
                <div class="col-md-6">
                  <p class="mb-1"><strong>Date:</strong> {{ formatDate(attempt.timestamp) }}</p>
                  <p class="mb-1"><strong>Questions:</strong> {{ attempt.total }}</p>
                </div>
              </div>
              <hr>
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <span class="display-6">{{ attempt.score }}/{{ attempt.total }}</span>
                  <span class="ms-2" :class="scoreClass(attempt.score, attempt.total)">
                    {{ scorePercentage(attempt.score, attempt.total) }}%
                  </span>
                </div>
                <div v-if="getFeedback(attempt.score, attempt.total)" class="feedback-badge">
                  {{ getFeedback(attempt.score, attempt.total) }}
                </div>
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
import axios from 'axios';

export default {
  name: 'QuizHistory',
  components: {
    Sidebar
  },
  data() {
    return {
      history: [],
      loading: true,
      isSidebarCollapsed: false
    };
  },
  mounted() {
    this.fetchQuizHistory();
  },
  methods: {
    handleSidebarToggle(val) {
      this.isSidebarCollapsed = val;
    },
    async fetchQuizHistory() {
      try {
        const response = await axios.get('/user/progress_summary', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.history = response.data.map(item => ({
          quiz_title: item.quiz_title,
          subject_name: item.subject_name,
          chapter_name: item.chapter_name,
          timestamp: item.timestamp,
          score: item.score,
          total: item.total
        }));
      } catch (error) {
        console.error('Error fetching quiz history:', error);
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    scorePercentage(score, total) {
      return Math.round((score / total) * 100);
    },
    scoreClass(score, total) {
      const percentage = (score / total) * 100;
      if (percentage >= 80) return 'text-success';
      if (percentage >= 60) return 'text-primary';
      if (percentage >= 40) return 'text-warning';
      return 'text-danger';
    },
    getFeedback(score, total) {
      const percentage = (score / total) * 100;
      if (percentage >= 80) return 'Excellent! Keep it up! 💤';
      if (percentage >= 60) return 'Good effort! Try to improve. 😊';
      if (percentage >= 40) return 'Needs improvement. Don\'t give up! 💤';
      return 'Keep practicing! You can do better!';
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
  flex-grow: 1;
  transition: margin-left 0.3s ease;
  margin-left: 250px;
}

.main-content.collapsed {
  margin-left: 80px;
}

.quiz-history {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.card {
  border-radius: 15px;
  border: none;
}

.card-title {
  color: #6a11cb;
  font-weight: bold;
}

.feedback-badge {
  background: linear-gradient(to right, #6a11cb, #2575fc);
  color: white;
  padding: 5px 15px;
  border-radius: 20px;
  font-weight: bold;
}

.display-6 {
  font-size: 2rem;
  font-weight: bold;
}

.text-success {
  color: #28a745 !important;
}

.text-primary {
  color: #007bff !important;
}

.text-warning {
  color: #ffc107 !important;
}

.text-danger {
  color: #dc3545 !important;
}
</style>
