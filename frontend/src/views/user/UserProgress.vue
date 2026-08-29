<template>
  <div class="user-layout">
    <Sidebar @toggle="handleSidebarToggle" />

    <div :class="['main-content', { collapsed: isSidebarCollapsed }]">
      <div class="progress-container container py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="mb-0">📊 My Progress</h2>
        </div>

        <div v-if="loading" class="text-center">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <div v-else class="progress-content">
          <!-- Summary Cards -->
          <div class="row mb-4">
            <div class="col-md-6 mb-3">
              <div class="card summary-card h-100">
                <div class="card-body text-center">
                  <h5 class="card-title">Quizzes Attempted</h5>
                  <h2 class="display-4">{{ stats.total_quizzes_attempted || 0 }}</h2>
                </div>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <div class="card summary-card h-100">
                <div class="card-body text-center">
                  <h5 class="card-title">Questions Attempted</h5>
                  <h2 class="display-4">{{ stats.total_questions_attempted || 0 }}</h2>
                </div>
              </div>
            </div>
          </div>

          <!-- Subject Statistics -->
          <div class="card mb-4">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">Subject Statistics</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Subject</th>
                      <th>Quizzes Attempted</th>
                      <th>Questions Attempted</th>
                      <th>Accuracy</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="subject in stats.subjects" :key="subject.subject">
                      <td>{{ subject.subject }}</td>
                      <td>{{ subject.quizzes_attempted }}</td>
                      <td>{{ subject.questions_attempted }}</td>
                      <td>
                        <div class="progress">
                          <div class="progress-bar"
                            :class="getAccuracyClass(subject.accuracy)"
                            :style="{ width: subject.accuracy + '%' }">
                            {{ subject.accuracy }}%
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr v-if="!stats.subjects || stats.subjects.length === 0">
                      <td colspan="4" class="text-center text-muted">No subject data available</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Overall Accuracy -->
          <div class="card">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">Overall Performance</h5>
            </div>
            <div class="card-body text-center">
              <h3>Your Overall Accuracy</h3>
              <div class="d-flex justify-content-center">
                <div class="overall-accuracy-circle">
                  <h1 class="display-3">{{ stats.overall_accuracy || 0 }}%</h1>
                </div>
              </div>
              <div class="mt-3">
                <div v-if="stats.total_questions_attempted > 0" class="text-muted">
                  Based on {{ stats.total_questions_attempted }} questions across {{ stats.total_quizzes_attempted }} quizzes
                </div>
                <div v-else class="text-muted">
                  No quiz attempts yet
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
import axios from 'axios';
import Sidebar from '@/components/Sidebar.vue';

export default {
  name: 'UserProgress',
  components: { Sidebar },
  data() {
    return {
      stats: {
        total_quizzes_attempted: 0,
        total_questions_attempted: 0,
        overall_accuracy: 0,
        subjects: []
      },
      loading: true,
      isSidebarCollapsed: false
    };
  },
  mounted() {
    this.fetchProgressStats();
  },
  methods: {
    handleSidebarToggle(val) {
      this.isSidebarCollapsed = val;
    },
    async fetchProgressStats() {
      try {
        this.loading = true;
        const response = await axios.get('/user/progress_stats', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.stats = response.data || { 
          total_quizzes_attempted: 0,
          total_questions_attempted: 0,
          overall_accuracy: 0,
          subjects: [] 
        };
      } catch (error) {
        console.error('Error fetching progress stats:', error);
        this.stats = {
          total_quizzes_attempted: 0,
          total_questions_attempted: 0,
          overall_accuracy: 0,
          subjects: []
        };
      } finally {
        this.loading = false;
      }
    },
    getAccuracyClass(accuracy) {
      if (accuracy >= 80) return 'bg-success';
      if (accuracy >= 60) return 'bg-primary';
      if (accuracy >= 40) return 'bg-warning';
      return 'bg-danger';
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

.progress-container {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.summary-card {
  border-radius: 15px;
  background: linear-gradient(135deg, #d5aaff, #c6c1ff);
  color: white;
  transition: transform 0.3s ease;
}

.summary-card:hover {
  transform: translateY(-5px);
}

.overall-accuracy-circle {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.progress {
  height: 25px;
}

.progress-bar {
  font-weight: bold;
}

.card {
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-header {
  border-radius: 15px 15px 0 0 !important;
}

.table-responsive {
  overflow-x: auto;
}

.text-muted {
  color: #6c757d !important;
}
</style>