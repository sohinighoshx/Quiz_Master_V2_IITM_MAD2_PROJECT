<template>
  <AdminLayout>
    <div class="summary-container">
      <h1 class="mb-4">📊 Admin Statistics Summary</h1>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p>Loading statistics...</p>
      </div>

      <div v-else>
        <!-- Detailed Statistics Table -->
        <div class="card mb-4">
          <div class="card-header bg-primary text-white">
            <h2>📈 Detailed Statistics</h2>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-striped table-hover">
                <thead>
                  <tr>
                    <th>Subject</th>
                    <th>Chapters</th>
                    <th>Total Quizzes</th>
                    <th>Total Attempts</th>
                    <th>Top Score</th>
                    <th>Average Accuracy</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="stat in detailedStats" :key="stat.subject">
                    <td>{{ stat.subject }}</td>
                    <td>{{ stat.chapters }}</td>
                    <td>{{ stat.quizzes }}</td>
                    <td>{{ stat.attempts }}</td>
                    <td>{{ stat.top_score }}</td>
                    <td>{{ stat.average_accuracy }}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Charts Row -->
        <div class="row">
          <!-- Top Scores Chart -->
          <div class="col-md-6 mb-4">
            <div class="card h-100">
              <div class="card-header bg-success text-white">
                <h2>🏆 Subject-wise Top Scores</h2>
              </div>
              <div class="card-body">
                <div class="chart-container">
                  <canvas ref="topScoresChart"></canvas>
                </div>
                <ul class="list-group mt-3">
                  <li
                    v-for="(score, index) in topScores"
                    :key="index"
                    class="list-group-item"
                  >
                    {{ index + 1 }}. {{ score }} points
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- User Attempts Chart -->
          <div class="col-md-6 mb-4">
            <div class="card h-100">
              <div class="card-header bg-info text-white">
                <h2>👥 Subject-wise User Attempts</h2>
              </div>
              <div class="card-body">
                <div class="chart-container">
                  <canvas ref="attemptsChart"></canvas>
                </div>
                <ul class="list-group mt-3">
                  <li
                    v-for="attempt in userAttempts"
                    :key="attempt.subject"
                    class="list-group-item d-flex justify-content-between"
                  >
                    <span>{{ attempt.subject }}</span>
                    <span class="badge bg-primary rounded-pill">{{ attempt.attempts }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- 📊 Subject-wise Accuracy Line Chart -->
        <div class="row">
          <div class="col-12 mb-4">
            <div class="card h-100">
              <div class="card-header bg-warning text-dark">
                <h2>📊 Subject-wise Accuracy</h2>
              </div>
              <div class="card-body">
                <div class="chart-container">
                  <canvas ref="accuracyChart"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>


<script>
import AdminLayout from '@/layouts/AdminLayout.vue'
import axios from 'axios'
import { Chart, registerables } from 'chart.js'

export default {
  name: 'AdminSummary',
  components: { AdminLayout },
  data() {
    return {
      loading: true,
      detailedStats: [],
      topScores: [],
      userAttempts: [],
      topScoresChartInstance: null,
      attemptsChartInstance: null,
      accuracyChartInstance: null
    }
  },
  async mounted() {
    Chart.register(...registerables)
    await this.fetchSummaryData()
    this.$nextTick(() => {
      this.renderCharts()
    })
  },
  methods: {
    async fetchSummaryData() {
      try {
        const token = localStorage.getItem('token')
        const response = await axios.get('/admin/summary', {
          headers: { Authorization: `Bearer ${token}` }
        })

        this.detailedStats = response.data.detailed_stats
        this.topScores = response.data.top_scores
        this.userAttempts = response.data.user_attempts
      } catch (error) {
        console.error('Error fetching summary data:', error)
        alert('Failed to load summary data')
      } finally {
        this.loading = false
      }
    },

    renderCharts() {
      // Destroy existing charts if they exist
      if (this.topScoresChartInstance) this.topScoresChartInstance.destroy()
      if (this.attemptsChartInstance) this.attemptsChartInstance.destroy()
      if (this.accuracyChartInstance) this.accuracyChartInstance.destroy()

      // Top Scores Bar Chart
      const topScoresCtx = this.$refs.topScoresChart?.getContext('2d')
      if (topScoresCtx) {
        this.topScoresChartInstance = new Chart(topScoresCtx, {
          type: 'bar',
          data: {
            labels: this.topScores.map((_, i) => `#${i + 1}`),
            datasets: [{
              label: 'Top Scores',
              data: this.topScores,
              backgroundColor: 'rgba(75, 192, 192, 0.6)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'Score'
                }
              }
            }
          }
        })
      }

      // User Attempts Pie Chart
      const attemptsCtx = this.$refs.attemptsChart?.getContext('2d')
      if (attemptsCtx) {
        this.attemptsChartInstance = new Chart(attemptsCtx, {
          type: 'pie',
          data: {
            labels: this.userAttempts.map(a => a.subject),
            datasets: [{
              label: 'Attempts',
              data: this.userAttempts.map(a => a.attempts),
              backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(255, 159, 64, 0.6)'
              ],
              borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'right'
              }
            }
          }
        })
      }

      // Subject-wise Accuracy Line Chart
      const accuracyCtx = this.$refs.accuracyChart?.getContext('2d')
      if (accuracyCtx) {
        const labels = this.detailedStats.map(s => s.subject)
        const accuracyData = this.detailedStats.map(s => s.average_accuracy)

        this.accuracyChartInstance = new Chart(accuracyCtx, {
          type: 'line',
          data: {
            labels,
            datasets: [{
              label: 'Average Accuracy (%)',
              data: accuracyData,
              fill: false,
              borderColor: 'rgba(255, 193, 7, 0.9)',
              backgroundColor: 'rgba(255, 193, 7, 0.6)',
              tension: 0.3,
              pointRadius: 5,
              pointHoverRadius: 8
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true,
                max: 100,
                title: {
                  display: true,
                  text: 'Accuracy (%)'
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Subjects'
                }
              }
            }
          }
        })
      }
    }
  }
}
</script>



<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&display=swap');

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
}

.sidebar nav a {
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

/* Main Content */
.content {
  flex-grow: 1;
  padding: 2rem;
  background: #ffffff;
  overflow-y: auto;
  transition: all 0.3s ease;
}

/* Table Styling */
table {
  font-family: 'Playfair Display', serif;
  font-size: 0.95rem;
}

.table th {
  background-color: #1e1e1e;
  color: white;
  font-weight: 600;
}

.table td {
  background-color: #fefefe;
  color: #333;
}

.card {
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  border: none;
  font-family: 'Playfair Display', serif;
}

.card-header {
  font-size: 1.2rem;
  font-weight: 600;
  padding: 1rem 1.5rem;
  border-radius: 12px 12px 0 0;
}

.card-body {
  padding: 1.5rem;
}

.chart-container {
  position: relative;
  height: 280px;
  width: 100%;
}

.list-group-item {
  font-family: 'Playfair Display', serif;
  font-size: 0.95rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.badge {
  font-size: 0.85rem;
  background-color: #1e1e1e;
}
</style>
