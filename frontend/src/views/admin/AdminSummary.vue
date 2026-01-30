<template>
  <AdminLayout>
    <div class="summary-container">
      <!-- Header with refresh and export -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 class="mb-2">
            <i class="bi bi-graph-up me-2"></i>Admin Statistics Dashboard
          </h1>
          <p class="text-muted mb-0">
            Last updated: {{ lastUpdated || 'Loading...' }}
            <span v-if="!loading" class="badge bg-primary ms-2">
              {{ totalSubjects }} subjects, {{ totalUsers || '' }} users
            </span>
          </p>
        </div>
        <div>
          <button 
            @click="refreshData" 
            :disabled="loading"
            class="btn btn-outline-primary me-2"
            title="Refresh data"
          >
            <i class="bi bi-arrow-clockwise" :class="{ 'spin': loading }"></i>
            Refresh
          </button>
          <button 
            @click="exportToCSV" 
            :disabled="loading || !detailedStats.length"
            class="btn btn-outline-success"
          >
            <i class="bi bi-download me-1"></i>Export CSV
          </button>
        </div>
      </div>

      <!-- Stats Overview Cards -->
      <div v-if="!loading" class="row mb-4">
        <div class="col-xl-3 col-md-6 mb-3">
          <div class="card stat-card border-start border-primary border-4">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="text-muted mb-1">Total Quizzes</h6>
                  <h3 class="mb-0">{{ totalQuizzes }}</h3>
                </div>
                <div class="icon-circle bg-primary-light">
                  <i class="bi bi-question-circle text-primary"></i>
                </div>
              </div>
              <small class="text-success" v-if="trends.quizzes > 0">
                <i class="bi bi-arrow-up"></i> {{ trends.quizzes }}% from last period
              </small>
            </div>
          </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-3">
          <div class="card stat-card border-start border-success border-4">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="text-muted mb-1">Total Attempts</h6>
                  <h3 class="mb-0">{{ totalAttempts.toLocaleString() }}</h3>
                </div>
                <div class="icon-circle bg-success-light">
                  <i class="bi bi-check-circle text-success"></i>
                </div>
              </div>
              <small class="text-success" v-if="trends.attempts > 0">
                <i class="bi bi-arrow-up"></i> {{ trends.attempts }}%
              </small>
            </div>
          </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-3">
          <div class="card stat-card border-start border-info border-4">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="text-muted mb-1">Total Notes</h6>
                  <h3 class="mb-0">{{ totalNotes.toLocaleString() }}</h3>
                </div>
                <div class="icon-circle bg-info-light">
                  <i class="bi bi-journal-text text-info"></i>
                </div>
              </div>
              <small class="text-success" v-if="trends.notes > 0">
                <i class="bi bi-arrow-up"></i> {{ trends.notes }}%
              </small>
            </div>
          </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-3">
          <div class="card stat-card border-start border-warning border-4">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="text-muted mb-1">Avg. Accuracy</h6>
                  <h3 class="mb-0">{{ averageAccuracy }}%</h3>
                </div>
                <div class="icon-circle bg-warning-light">
                  <i class="bi bi-bar-chart text-warning"></i>
                </div>
              </div>
              <small :class="trends.accuracy >= 0 ? 'text-success' : 'text-danger'">
                <i :class="trends.accuracy >= 0 ? 'bi bi-arrow-up' : 'bi bi-arrow-down'"></i>
                {{ Math.abs(trends.accuracy) }}%
              </small>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-grow text-primary" style="width: 3rem; height: 3rem;" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3">Fetching latest statistics...</p>
        <div class="progress mt-3" style="height: 4px; max-width: 300px; margin: 0 auto;">
          <div 
            class="progress-bar progress-bar-striped progress-bar-animated" 
            role="progressbar" 
            :style="{ width: loadingProgress + '%' }"
          ></div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="alert alert-danger d-flex align-items-center" role="alert">
        <i class="bi bi-exclamation-triangle-fill me-3 fs-4"></i>
        <div>
          <h5 class="alert-heading mb-1">Failed to Load Data</h5>
          <p class="mb-0">{{ error }}</p>
          <button @click="fetchSummaryData" class="btn btn-sm btn-outline-danger mt-2">
            Try Again
          </button>
        </div>
      </div>

      <!-- Main Content -->
      <div v-else>
        <!-- Detailed Statistics Table -->
        <div class="card shadow-sm mb-4">
          <div class="card-header bg-white border-bottom d-flex justify-content-between align-items-center">
            <h5 class="mb-0">
              <i class="bi bi-table me-2"></i>Detailed Statistics
            </h5>
            <div class="input-group input-group-sm" style="width: 250px;">
              <span class="input-group-text">
                <i class="bi bi-search"></i>
              </span>
              <input 
                type="text" 
                v-model="searchQuery" 
                class="form-control" 
                placeholder="Search subjects..."
              >
            </div>
          </div>
          
          <div class="card-body p-0">
            <div class="table-responsive">
              <table class="table table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th @click="sortTable('subject')" class="cursor-pointer">
                      Subject
                      <i v-if="sortBy === 'subject'" class="bi" :class="sortDesc ? 'bi-sort-down' : 'bi-sort-up'"></i>
                    </th>
                    <th @click="sortTable('chapters')" class="cursor-pointer text-center">
                      Chapters
                      <i v-if="sortBy === 'chapters'" class="bi" :class="sortDesc ? 'bi-sort-down' : 'bi-sort-up'"></i>
                    </th>
                    <th @click="sortTable('quizzes')" class="cursor-pointer text-center">
                      Quizzes
                      <i v-if="sortBy === 'quizzes'" class="bi" :class="sortDesc ? 'bi-sort-down' : 'bi-sort-up'"></i>
                    </th>
                    <th @click="sortTable('notes')" class="cursor-pointer text-center">
                      <i class="bi bi-journal-text me-1"></i>Notes
                      <i v-if="sortBy === 'notes'" class="bi" :class="sortDesc ? 'bi-sort-down' : 'bi-sort-up'"></i>
                    </th>
                    <th @click="sortTable('attempts')" class="cursor-pointer text-center">
                      Attempts
                      <i v-if="sortBy === 'attempts'" class="bi" :class="sortDesc ? 'bi-sort-down' : 'bi-sort-up'"></i>
                    </th>
                    <th @click="sortTable('top_score')" class="cursor-pointer text-center">
                      Top Score
                      <i v-if="sortBy === 'top_score'" class="bi" :class="sortDesc ? 'bi-sort-down' : 'bi-sort-up'"></i>
                    </th>
                    <th @click="sortTable('average_accuracy')" class="cursor-pointer text-center">
                      Accuracy
                      <i v-if="sortBy === 'average_accuracy'" class="bi" :class="sortDesc ? 'bi-sort-down' : 'bi-sort-up'"></i>
                    </th>
                    <th class="text-center">Actions</th>
                  </tr>
                </thead>

                <tbody>
                  <tr v-for="stat in filteredStats" :key="stat.subject">
                    <td>
                      <div class="d-flex align-items-center">
                        <div class="subject-icon me-2">
                          <i class="bi bi-book"></i>
                        </div>
                        <div>
                          <strong>{{ stat.subject }}</strong>
                          <div class="text-muted small">
                            {{ stat.chapters }} chapter{{ stat.chapters !== 1 ? 's' : '' }}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td class="text-center">
                      <span class="badge bg-primary rounded-pill">{{ stat.chapters }}</span>
                    </td>
                    <td class="text-center">
                      <span class="badge bg-info rounded-pill">{{ stat.quizzes }}</span>
                    </td>
                    <td class="text-center">
                      <span class="badge bg-secondary rounded-pill">{{ stat.notes }}</span>
                    </td>
                    <td class="text-center">
                      <div class="d-flex flex-column align-items-center">
                        <span class="fw-bold">{{ stat.attempts.toLocaleString() }}</span>
                        <small class="text-muted">
                          {{ Math.round((stat.attempts / totalAttempts) * 100) || 0 }}%
                        </small>
                      </div>
                    </td>
                    <td class="text-center">
                      <span class="badge bg-success rounded-pill px-3 py-2 fs-6">
                        {{ stat.top_score }}%
                      </span>
                    </td>
                    <td class="text-center">
                      <div class="progress" style="height: 6px; width: 80px; margin: 0 auto;">
                        <div 
                          class="progress-bar" 
                          :class="getAccuracyClass(stat.average_accuracy)"
                          role="progressbar" 
                          :style="{ width: stat.average_accuracy + '%' }"
                        ></div>
                      </div>
                      <small class="fw-bold mt-1 d-block">
                        {{ stat.average_accuracy }}%
                      </small>
                    </td>
                    <td class="text-center">
                      <button 
                        @click="viewSubjectDetails(stat.subject)"
                        class="btn btn-sm btn-outline-primary"
                        title="View Details"
                      >
                        <i class="bi bi-eye"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
              
              <!-- Empty State -->
              <div v-if="!filteredStats.length" class="text-center py-5">
                <i class="bi bi-search display-6 text-muted mb-3"></i>
                <p class="text-muted">No subjects found matching "{{ searchQuery }}"</p>
              </div>
            </div>
          </div>

          <div class="card-footer bg-white border-top d-flex justify-content-between align-items-center">
            <div class="text-muted small">
              Showing {{ filteredStats.length }} of {{ detailedStats.length }} subjects
            </div>
            <div class="d-flex align-items-center">
              <label class="me-2 small text-muted">Rows per page:</label>
              <select v-model="rowsPerPage" class="form-select form-select-sm" style="width: auto;">
                <option>5</option>
                <option>10</option>
                <option>25</option>
                <option>50</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Charts Section -->
        <div class="row">
          <!-- Top Scores Chart -->
          <div class="col-xl-6 mb-4">
            <div class="card shadow-sm h-100">
              <div class="card-header bg-white border-bottom d-flex justify-content-between align-items-center">
                <h5 class="mb-0">
                  <i class="bi bi-trophy me-2 text-warning"></i>Top Scores Distribution
                </h5>
                <select v-model="chartPeriod" class="form-select form-select-sm" style="width: auto;">
                  <option value="week">This Week</option>
                  <option value="month">This Month</option>
                  <option value="quarter">This Quarter</option>
                  <option value="year">This Year</option>
                </select>
              </div>
              <div class="card-body">
                <div class="chart-container">
                  <canvas ref="topScoresChart"></canvas>
                </div>
                <div class="mt-3 d-flex justify-content-center">
                  <div class="d-flex align-items-center me-4">
                    <span class="legend-dot bg-primary"></span>
                    <small class="ms-2 text-muted">Scores</small>
                  </div>
                  <div class="d-flex align-items-center">
                    <span class="legend-dot bg-success"></span>
                    <small class="ms-2 text-muted">Average: {{ averageTopScore }}%</small>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- User Attempts Chart -->
          <div class="col-xl-6 mb-4">
            <div class="card shadow-sm h-100">
              <div class="card-header bg-white border-bottom">
                <h5 class="mb-0">
                  <i class="bi bi-people me-2 text-info"></i>Subject-wise User Attempts
                </h5>
              </div>
              <div class="card-body">
                <div class="chart-container">
                  <canvas ref="attemptsChart"></canvas>
                </div>
                <div class="mt-3 text-center">
                  <small class="text-muted">
                    Total attempts across all subjects: <strong>{{ totalAttempts.toLocaleString() }}</strong>
                  </small>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Second Row Charts -->
        <div class="row">
          <!-- Notes Distribution -->
          <div class="col-xl-6 mb-4">
            <div class="card shadow-sm h-100">
              <div class="card-header bg-white border-bottom">
                <h5 class="mb-0">
                  <i class="bi bi-journal-text me-2 text-secondary"></i>Notes Distribution by Subject
                </h5>
              </div>
              <div class="card-body">
                <div class="chart-container">
                  <canvas ref="notesChart"></canvas>
                </div>
                <div class="mt-3 text-center">
                  <small class="text-muted">
                    Most notes in: <strong>{{ subjectWithMostNotes }}</strong>
                    ({{ maxNotes }} notes)
                  </small>
                </div>
              </div>
            </div>
          </div>

          <!-- Accuracy Trends -->
          <div class="col-xl-6 mb-4">
            <div class="card shadow-sm h-100">
              <div class="card-header bg-white border-bottom d-flex justify-content-between align-items-center">
                <h5 class="mb-0">
                  <i class="bi bi-bar-chart me-2 text-warning"></i>Accuracy Trends
                </h5>
                <button @click="toggleChartType" class="btn btn-sm btn-outline-secondary">
                  Switch to {{ currentChartType === 'line' ? 'Bar' : 'Line' }}
                </button>
              </div>
              <div class="card-body">
                <div class="chart-container">
                  <canvas ref="accuracyChart"></canvas>
                </div>
                <div class="mt-3 text-center">
                  <small class="text-muted">
                    Overall average: <strong>{{ averageAccuracy }}%</strong>
                    <span :class="trends.accuracy >= 0 ? 'text-success' : 'text-danger'" class="ms-2">
                      <i :class="trends.accuracy >= 0 ? 'bi bi-arrow-up' : 'bi bi-arrow-down'"></i>
                      {{ Math.abs(trends.accuracy) }}%
                    </span>
                  </small>
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
import ChartDataLabels from 'chartjs-plugin-datalabels'

export default {
  name: 'AdminSummary',
  components: { AdminLayout },

  data() {
    return {
      loading: true,
      loadingProgress: 0,
      error: null,
      lastUpdated: null,
      
      detailedStats: [],
      topScores: [],
      userAttempts: [],
      
      // UI Controls
      searchQuery: '',
      sortBy: 'subject',
      sortDesc: false,
      rowsPerPage: 10,
      chartPeriod: 'month',
      currentChartType: 'line',
      
      // Chart instances
      topScoresChartInstance: null,
      attemptsChartInstance: null,
      notesChartInstance: null,
      accuracyChartInstance: null,
      
      // Mock trends (replace with actual API data)
      trends: {
        quizzes: 12,
        attempts: 8,
        notes: 15,
        accuracy: 3
      }
    }
  },

  computed: {
    filteredStats() {
      let filtered = this.detailedStats.filter(stat => 
        stat.subject.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
      
      // Sorting
      filtered.sort((a, b) => {
        let valA = a[this.sortBy]
        let valB = b[this.sortBy]
        
        // Handle numeric vs string sorting
        if (typeof valA === 'number') {
          return this.sortDesc ? valB - valA : valA - valB
        } else {
          return this.sortDesc 
            ? valB.localeCompare(valA)
            : valA.localeCompare(valB)
        }
      })
      
      // Pagination
      return filtered.slice(0, this.rowsPerPage)
    },
    
    totalSubjects() {
      return this.detailedStats.length
    },
    
    totalQuizzes() {
      return this.detailedStats.reduce((sum, stat) => sum + stat.quizzes, 0)
    },
    
    totalAttempts() {
      return this.detailedStats.reduce((sum, stat) => sum + stat.attempts, 0)
    },
    
    totalNotes() {
      return this.detailedStats.reduce((sum, stat) => sum + stat.notes, 0)
    },
    
    averageAccuracy() {
      if (!this.detailedStats.length) return 0
      const total = this.detailedStats.reduce((sum, stat) => sum + stat.average_accuracy, 0)
      return (total / this.detailedStats.length).toFixed(1)
    },
    
    averageTopScore() {
      if (!this.topScores.length) return 0
      const total = this.topScores.reduce((sum, score) => sum + score, 0)
      return (total / this.topScores.length).toFixed(1)
    },
    
    subjectWithMostNotes() {
      if (!this.detailedStats.length) return 'N/A'
      const maxStat = this.detailedStats.reduce((max, stat) => 
        stat.notes > max.notes ? stat : max
      )
      return maxStat.subject
    },
    
    maxNotes() {
      if (!this.detailedStats.length) return 0
      return Math.max(...this.detailedStats.map(stat => stat.notes))
    },
    
    totalUsers() {
      // This should come from your API
      return 1500 // Mock data
    }
  },

  async mounted() {
    Chart.register(...registerables, ChartDataLabels)
    await this.fetchSummaryData()
    this.$nextTick(() => this.renderCharts())
  },

  methods: {
    async fetchSummaryData() {
      this.loading = true
      this.error = null
      this.loadingProgress = 0
      
      try {
        const token = localStorage.getItem('token')
        
        // Simulate progress for better UX
        const progressInterval = setInterval(() => {
          if (this.loadingProgress < 90) {
            this.loadingProgress += 10
          }
        }, 200)

        const res = await axios.get('/admin/summary', {
          headers: { Authorization: `Bearer ${token}` },
          params: { period: this.chartPeriod }
        })

        clearInterval(progressInterval)
        this.loadingProgress = 100

        this.detailedStats = res.data.detailed_stats || []
        this.topScores = res.data.top_scores || []
        this.userAttempts = res.data.user_attempts || []
        this.lastUpdated = new Date().toLocaleString()
        
        // Update charts when data changes
        this.$nextTick(() => this.renderCharts())
        
      } catch (err) {
        console.error('Failed to fetch summary:', err)
        this.error = err.response?.data?.message || 'Failed to load statistics. Please try again.'
      } finally {
        this.loading = false
        setTimeout(() => { this.loadingProgress = 0 }, 300)
      }
    },

    renderCharts() {
      // Cleanup old charts
      [this.topScoresChartInstance, this.attemptsChartInstance, 
       this.notesChartInstance, this.accuracyChartInstance].forEach(chart => {
        chart?.destroy()
      })

      // Chart colors
      const colors = {
        primary: '#4e73df',
        success: '#1cc88a',
        info: '#36b9cc',
        warning: '#f6c23e',
        danger: '#e74a3b',
        secondary: '#858796',
        light: '#f8f9fc'
      }

      // 1. Top Scores Chart (Horizontal Bar)
      const tsCtx = this.$refs.topScoresChart?.getContext('2d')
      if (tsCtx && this.topScores.length) {
        this.topScoresChartInstance = new Chart(tsCtx, {
          type: 'bar',
          data: {
            labels: this.topScores.map((_, i) => `Score ${i + 1}`),
            datasets: [{
              label: 'Score (%)',
              data: this.topScores,
              backgroundColor: this.topScores.map(score => 
                score >= 90 ? colors.success : 
                score >= 70 ? colors.primary : 
                score >= 50 ? colors.warning : colors.danger
              ),
              borderColor: colors.light,
              borderWidth: 1,
              borderRadius: 4,
            }]
          },
          options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: {
                callbacks: {
                  label: (context) => `Score: ${context.raw}%`
                }
              },
              datalabels: {
                anchor: 'end',
                align: 'right',
                color: colors.light,
                formatter: (value) => `${value}%`
              }
            },
            scales: {
              x: {
                beginAtZero: true,
                max: 100,
                grid: { display: false },
                ticks: { callback: (value) => `${value}%` }
              },
              y: { grid: { display: false } }
            }
          }
        })
      }

      // 2. Attempts Chart (Doughnut)
      const atCtx = this.$refs.attemptsChart?.getContext('2d')
      if (atCtx && this.userAttempts.length) {
        const backgroundColors = [
          colors.primary, colors.success, colors.info, 
          colors.warning, colors.danger, colors.secondary
        ]
        
        this.attemptsChartInstance = new Chart(atCtx, {
          type: 'doughnut',
          data: {
            labels: this.userAttempts.map(x => x.subject),
            datasets: [{
              data: this.userAttempts.map(x => x.attempts),
              backgroundColor: backgroundColors,
              borderColor: colors.light,
              borderWidth: 2,
              hoverOffset: 15
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
              legend: {
                position: 'right',
                labels: {
                  padding: 20,
                  usePointStyle: true,
                  pointStyle: 'circle'
                }
              },
              tooltip: {
                callbacks: {
                  label: (context) => {
                    const total = this.userAttempts.reduce((sum, x) => sum + x.attempts, 0)
                    const percentage = ((context.raw / total) * 100).toFixed(1)
                    return `${context.label}: ${context.raw} attempts (${percentage}%)`
                  }
                }
              }
            }
          }
        })
      }

      // 3. Notes Chart (Bar)
      const ntCtx = this.$refs.notesChart?.getContext('2d')
      if (ntCtx && this.detailedStats.length) {
        this.notesChartInstance = new Chart(ntCtx, {
          type: 'bar',
          data: {
            labels: this.detailedStats.map(s => s.subject),
            datasets: [{
              label: 'Notes Count',
              data: this.detailedStats.map(s => s.notes),
              backgroundColor: colors.secondary,
              borderColor: colors.secondary,
              borderWidth: 1,
              borderRadius: 4,
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: {
                callbacks: {
                  afterLabel: (context) => {
                    const total = this.totalNotes
                    const percentage = ((context.raw / total) * 100).toFixed(1)
                    return `Share: ${percentage}%`
                  }
                }
              }
            },
            scales: {
              x: { grid: { display: false } },
              y: { 
                beginAtZero: true,
                ticks: { 
                  callback: function(value) { return Number.isInteger(value) ? value : null }
                }
              }
            }
          }
        })
      }

      // 4. Accuracy Chart (Line/Bar)
      const acCtx = this.$refs.accuracyChart?.getContext('2d')
      if (acCtx && this.detailedStats.length) {
        const accuracyData = this.detailedStats.map(s => s.average_accuracy)
        
        this.accuracyChartInstance = new Chart(acCtx, {
          type: this.currentChartType,
          data: {
            labels: this.detailedStats.map(s => s.subject),
            datasets: [{
              label: 'Accuracy (%)',
              data: accuracyData,
              backgroundColor: this.currentChartType === 'bar' 
                ? accuracyData.map(acc => 
                    acc >= 80 ? colors.success : 
                    acc >= 60 ? colors.warning : colors.danger
                  )
                : colors.primary,
              borderColor: colors.primary,
              borderWidth: 2,
              fill: this.currentChartType === 'line',
              tension: this.currentChartType === 'line' ? 0.4 : 0,
              pointBackgroundColor: colors.primary,
              pointBorderColor: colors.light,
              pointBorderWidth: 2,
              pointRadius: 6,
              pointHoverRadius: 8
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              tooltip: {
                callbacks: {
                  label: (context) => `${context.raw}% accuracy`
                }
              }
            },
            scales: {
              y: {
                beginAtZero: false,
                min: Math.min(...accuracyData) - 10,
                max: 100,
                ticks: { callback: (value) => `${value}%` }
              }
            }
          }
        })
      }
    },

    sortTable(column) {
      if (this.sortBy === column) {
        this.sortDesc = !this.sortDesc
      } else {
        this.sortBy = column
        this.sortDesc = false
      }
    },

    getAccuracyClass(accuracy) {
      if (accuracy >= 80) return 'bg-success'
      if (accuracy >= 60) return 'bg-warning'
      return 'bg-danger'
    },

    viewSubjectDetails(subject) {
      // Navigate to subject detail page
      this.$router.push(`/admin/subjects/${encodeURIComponent(subject)}`)
    },

    refreshData() {
      this.fetchSummaryData()
    },

    toggleChartType() {
      this.currentChartType = this.currentChartType === 'line' ? 'bar' : 'line'
      this.renderCharts()
    },

    exportToCSV() {
      const headers = ['Subject', 'Chapters', 'Quizzes', 'Notes', 'Attempts', 'Top Score', 'Average Accuracy']
      const csvContent = [
        headers.join(','),
        ...this.detailedStats.map(stat => 
          [
            `"${stat.subject}"`,
            stat.chapters,
            stat.quizzes,
            stat.notes,
            stat.attempts,
            stat.top_score,
            stat.average_accuracy
          ].join(',')
        )
      ].join('\n')

      const blob = new Blob([csvContent], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `admin-statistics-${new Date().toISOString().split('T')[0]}.csv`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    }
  },

  watch: {
    chartPeriod() {
      this.fetchSummaryData()
    },
    rowsPerPage() {
      // Trigger recomputation of filtered stats
      this.$forceUpdate()
    }
  }
}
</script>

<style scoped>
.summary-container {
  max-width: 1400px;
  margin: auto;
  padding: 20px;
}

.chart-container {
  width: 100%;
  height: 300px;
  position: relative;
}

.stat-card {
  transition: transform 0.2s;
  height: 100%;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 .5rem 1rem rgba(0,0,0,.15);
}

.icon-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-primary-light { background-color: rgba(78, 115, 223, 0.1); }
.bg-success-light { background-color: rgba(28, 200, 138, 0.1); }
.bg-info-light { background-color: rgba(54, 185, 204, 0.1); }
.bg-warning-light { background-color: rgba(246, 194, 62, 0.1); }

.cursor-pointer {
  cursor: pointer;
}

.cursor-pointer:hover {
  background-color: rgba(0,0,0,0.02);
}

.subject-icon {
  width: 36px;
  height: 36px;
  background-color: #f8f9fc;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

/* Loading spinner animation */
.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Progress bar animation */
.progress-bar-animated {
  animation: progress-bar-stripes 1s linear infinite;
}

@keyframes progress-bar-stripes {
  0% { background-position: 1rem 0; }
  100% { background-position: 0 0; }
}

/* Table row hover effect */
.table-hover tbody tr {
  transition: all 0.2s;
}

.table-hover tbody tr:hover {
  background-color: rgba(78, 115, 223, 0.05);
  transform: scale(1.002);
}

/* Card shadow enhancement */
.card {
  box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.1);
  border: 1px solid #e3e6f0;
}

.card-header {
  border-bottom: 1px solid #e3e6f0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .summary-container {
    padding: 10px;
  }
  
  .chart-container {
    height: 250px;
  }
  
  .d-flex.justify-content-between.align-items-center {
    flex-direction: column;
    align-items: flex-start !important;
  }
  
  .d-flex.justify-content-between.align-items-center > div:last-child {
    margin-top: 10px;
  }
}
</style>