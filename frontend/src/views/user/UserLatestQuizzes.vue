<template>
  <div class="user-layout">
    <Sidebar @toggle="handleSidebarToggle" class="sidebar" />

    <div :class="['main-content', { 'collapsed': isSidebarCollapsed }]">
      <div class="quiz-browser-container">
        <!-- Gradient Header -->
        <div class="header-gradient">
          <h3 class="quiz-title">🔥 Browse & Attempt Latest Quizzes</h3>
          <div class="quiz-meta">
            <span class="badge subject-badge">
              {{ selectedSubjectName || 'All Subjects' }}
            </span>
          </div>
        </div>

        <div class="quiz-content">
          <!-- 🎯 Colorful Dropdown Filters -->
          <div class="filters-row">
            <div class="filter-card">
              <label class="filter-label">📘 Select Subject</label>
              <select v-model="selectedSubjectId" @change="loadChapters" class="filter-select">
                <option value="">All Subjects</option>
                <option v-for="s in subjects" :key="s.id" :value="s.id">{{ s.name }}</option>
              </select>
            </div>
            <div class="filter-card">
              <label class="filter-label">📖 Select Chapter</label>
              <select v-model="selectedChapterId" @change="loadQuizzes" class="filter-select" :disabled="!chapters.length">
                <option value="">All Chapters</option>
                <option v-for="c in chapters" :key="c.id" :value="c.id">{{ c.name }}</option>
              </select>
            </div>
            <div class="filter-card">
              <label class="filter-label">📝 Select Quiz</label>
              <select v-model="selectedQuizId" class="filter-select" :disabled="!quizzes.length">
                <option value="">All Quizzes</option>
                <option v-for="q in allQuizzes" :key="q.id" :value="q.id">{{ q.title || `Quiz ${q.id}` }}</option>
              </select>
            </div>
          </div>

          <!-- ✅ Colorful Card Grid -->
          <div v-if="filteredQuizzes.length > 0" class="quizzes-grid">
            <div v-for="q in filteredQuizzes" :key="q.id" class="quiz-card" :style="{ borderTopColor: getSubjectColor(q.subject_name) }">
              <div class="quiz-card-body">
                <h5 class="quiz-title">{{ q.title || 'Untitled Quiz' }}</h5>
                <div class="quiz-meta">
                  <span class="badge subject-badge" :style="{ backgroundColor: getSubjectColor(q.subject_name) }">
                    {{ q.subject_name }}
                  </span>
                  <span class="badge chapter-badge">
                    {{ q.chapter_name }}
                  </span>
                </div>
                <div class="quiz-details">
                  <p><i class="fas fa-calendar-alt"></i> <strong>Date:</strong> {{ formatDate(q.date_of_quiz) }}</p>
                  <p><i class="fas fa-clock"></i> <strong>Duration:</strong> {{ q.time_duration }}</p>
                  <p><i class="fas fa-hourglass-end"></i> <strong>Deadline:</strong> {{ q.deadline }}</p>
                  <p v-if="q.remarks"><i class="fas fa-comment"></i> <strong>Remarks:</strong> {{ q.remarks }}</p>
                </div>
                <router-link class="start-quiz-btn" :to="`/user/quiz/${q.id}`">
                  <i class="fas fa-play"></i> Start Quiz
                </router-link>
              </div>
            </div>
          </div>

          <div v-else class="no-quizzes">
            <i class="fas fa-book-open"></i>
            <h4>No quizzes found matching your criteria</h4>
            <button class="btn-reset-filters" @click="resetFilters">
              <i class="fas fa-sync-alt"></i> Reset Filters
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios"
import Sidebar from '@/components/Sidebar.vue';

export default {
  name: "UserLatestQuizzes",
  components: {
    Sidebar
  },
  data() {
    return {
      isSidebarCollapsed: false,
      subjects: [],
      chapters: [],
      quizzes: [],
      allQuizzes: [],
      selectedSubjectId: "",
      selectedChapterId: "",
      selectedQuizId: ""
    }
  },
  computed: {
    filteredQuizzes() {
      if (this.selectedQuizId) {
        return this.quizzes.filter(q => q.id == this.selectedQuizId)
      }
      return this.quizzes
    },
    selectedSubjectName() {
      if (!this.selectedSubjectId) return null
      const subject = this.subjects.find(s => s.id == this.selectedSubjectId)
      return subject?.name || null
    }
  },
  async mounted() {
    await this.loadInitialData()
  },
  methods: {
    handleSidebarToggle() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed
    },
    async loadInitialData() {
      const token = localStorage.getItem("token")
      
      const [subjectsRes, quizzesRes] = await Promise.all([
        axios.get('/user/subjects', {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get('/user/all_quizzes', {
          headers: { Authorization: `Bearer ${token}` }
        })
      ])
      
      this.subjects = subjectsRes.data
      this.allQuizzes = quizzesRes.data
      this.quizzes = quizzesRes.data
    },
    async loadChapters() {
      this.selectedChapterId = ""
      this.selectedQuizId = ""
      
      if (!this.selectedSubjectId) {
        this.quizzes = this.allQuizzes
        this.chapters = []
        return
      }
      
      const token = localStorage.getItem("token")
      const res = await axios.get(`/user/chapters/${this.selectedSubjectId}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.chapters = res.data
      await this.loadQuizzes()
    },
    async loadQuizzes() {
      this.selectedQuizId = ""
      
      if (!this.selectedChapterId) {
        if (this.selectedSubjectId) {
          this.quizzes = this.allQuizzes.filter(q => 
            q.subject_id == this.selectedSubjectId
          )
        } else {
          this.quizzes = this.allQuizzes
        }
        return
      }
      
      const token = localStorage.getItem("token")
      const res = await axios.get(`/user/quizzes/${this.selectedChapterId}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.quizzes = res.data
    },
    resetFilters() {
      this.selectedSubjectId = ""
      this.selectedChapterId = ""
      this.selectedQuizId = ""
      this.quizzes = this.allQuizzes
      this.chapters = []
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        })
      } catch {
        return dateString
      }
    },
    getSubjectColor(subjectName) {
      const colors = {
        'Mathematics': '#6a11cb',
        'Physics': '#2575fc',
        'Chemistry': '#2bb673',
        'Biology': '#8e44ad',
        'Default': '#ff6b6b'
      }
      return colors[subjectName] || colors['Default']
    }
  }
}
</script>

<style scoped>
.user-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.sidebar {
  width: 250px;
  transition: width 0.3s ease;
  position: fixed;
  height: 100vh;
  z-index: 100;
}

.main-content {
  margin-left: 250px;
  transition: margin-left 0.3s ease;
  flex-grow: 1;
  min-height: 100vh;
}

.main-content.collapsed {
  margin-left: 80px; /* Adjust based on your collapsed sidebar width */
}

.quiz-browser-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.header-gradient {
  background: linear-gradient(to right, #6a11cb, #2575fc);
  color: white;
  padding: 2rem;
  border-radius: 0 0 20px 20px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.quiz-title {
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-align: center;
}

.subject-badge {
  background-color: rgba(255, 255, 255, 0.2);
  font-size: 0.9rem;
  padding: 5px 10px;
  border-radius: 20px;
  display: inline-block;
}

.quiz-content {
  padding: 0 1rem;
}

.filters-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.filter-card {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.filter-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #6a11cb;
}

.filter-select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s;
}

.filter-select:focus {
  border-color: #6a11cb;
  outline: none;
  box-shadow: 0 0 0 3px rgba(106, 17, 203, 0.2);
}

.quizzes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.quiz-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border-top: 4px solid #6a11cb;
}

.quiz-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.quiz-card-body {
  padding: 1.5rem;
}

.quiz-title {
  color: #343a40;
  font-weight: 700;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.quiz-meta {
  margin-bottom: 1rem;
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.badge {
  padding: 0.5rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.subject-badge {
  background-color: #6a11cb;
  color: white;
}

.chapter-badge {
  background-color: #e9ecef;
  color: #495057;
}

.quiz-details {
  margin-bottom: 1.5rem;
}

.quiz-details p {
  margin-bottom: 0.75rem;
  color: #6c757d;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.quiz-details i {
  width: 20px;
  text-align: center;
  color: #6a11cb;
}

.start-quiz-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: linear-gradient(to right, #6a11cb, #2575fc);
  color: white;
  padding: 0.75rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
  width: 100%;
  border: none;
  cursor: pointer;
}

.start-quiz-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(106, 17, 203, 0.3);
}

.no-quizzes {
  background: white;
  border-radius: 12px;
  padding: 3rem;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  margin: 2rem 0;
}

.no-quizzes i {
  font-size: 3rem;
  color: #6a11cb;
  margin-bottom: 1rem;
}

.no-quizzes h4 {
  margin-bottom: 1.5rem;
  color: #495057;
}

.btn-reset-filters {
  background: linear-gradient(to right, #6a11cb, #2575fc);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-reset-filters:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(106, 17, 203, 0.3);
}

@media (max-width: 992px) {
  .main-content {
    margin-left: 0;
    padding-left: 80px; /* Space for collapsed sidebar */
  }
  
  .main-content.collapsed {
    padding-left: 0;
  }
  
  .quizzes-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
}

@media (max-width: 768px) {
  .filters-row {
    grid-template-columns: 1fr;
  }
  
  .quizzes-grid {
    grid-template-columns: 1fr;
  }
  
  .header-gradient {
    padding: 1.5rem;
  }
}

@media (max-width: 576px) {
  .quiz-card-body {
    padding: 1rem;
  }
  
  .no-quizzes {
    padding: 2rem 1rem;
  }
}
</style>