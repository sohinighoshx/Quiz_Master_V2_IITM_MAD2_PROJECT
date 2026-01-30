<template>
  <div class="user-layout">
    <Sidebar @toggle="handleSidebarToggle" />

    <div :class="['main-content', { collapsed: isSidebarCollapsed }]">
  <div class="quiz-attempt-container container-fluid py-4">
    <!-- Gradient Header -->
    <div class="quiz-header">
      <h3 class="quiz-title">🧠 Attempt Quiz</h3>
      <div class="quiz-meta">
        <span v-if="quizDetails" class="badge subject-badge">
          {{ quizDetails.subject_name }} / {{ quizDetails.chapter_name }}
        </span>
      </div>
    </div>

    <div class="quiz-content">
      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner-grow text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p>Loading quiz questions...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <div class="error-icon">⚠️</div>
        <h4>Failed to load quiz</h4>
        <p>{{ error }}</p>
        <button class="btn back-btn" @click="$router.push('/user/quizzes')">
          Back to Quizzes
        </button>
      </div>

      <!-- Quiz Content -->
      <div v-else>
        <!-- Quiz Status Bar -->
        <div class="status-bar">
          <div class="status-item timer" :class="{ 'time-warning': timeLeft <= 60 }">
            <i class="fas fa-clock"></i>
            <span>{{ formattedTime }}</span>
          </div>
          <div class="status-item progress">
            <i class="fas fa-check-circle"></i>
            <span>{{ Object.keys(userAnswers).length }}/{{ totalQuestions }}</span>
          </div>
          <div class="status-item score-preview" v-if="!submitted">
            <i class="fas fa-star"></i>
            <span>Score: {{ calculatedScore }}</span>
          </div>
        </div>

        <!-- Questions -->
        <form @submit.prevent="submitQuiz">
          <div
            v-for="(q, index) in questions"
            :key="q.id"
            class="question-card"
            :class="{ 'answered': userAnswers[q.id], 'current': currentQuestion === index }"
          >
            <div class="question-header">
              <span class="question-number">Q{{ index + 1 }}</span>
              <span class="question-status" v-if="userAnswers[q.id]">
                <i class="fas fa-check-circle"></i> Answered
              </span>
            </div>
            <p class="question-text">{{ q.question_statement }}</p>

            <div class="options-grid">
              <div 
                class="option-card"
                v-for="(val, key) in q.options" 
                :key="key"
                :class="{ 'selected': userAnswers[q.id] === key.replace('option', '') }"
              >
                <input
                  type="radio"
                  :id="`q_${q.id}_${key}`"
                  :name="`q_${q.id}`"
                  :value="key.replace('option', '')"
                  v-model="userAnswers[q.id]"
                  :disabled="submitted"
                  required
                />
                <label :for="`q_${q.id}_${key}`">
                  <span class="option-letter">{{ key.replace('option', '') }}</span>
                  <span class="option-text">{{ val }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="action-buttons">
            <button 
              v-if="!submitted" 
              type="submit" 
              class="submit-btn"
              :disabled="!allQuestionsAnswered"
              :class="{ 'pulse': allQuestionsAnswered }"
            >
              <i class="fas fa-paper-plane"></i>
              <span v-if="allQuestionsAnswered">Submit Quiz</span>
              <span v-else>Complete all questions to submit</span>
            </button>

            <div v-if="submitted" class="results-summary">
              <div class="result-card" :class="scoreAlertClass">
                <div class="result-header">
                  <i class="fas fa-award"></i>
                  <h4>Quiz Results</h4>
                </div>
                <div class="result-stats">
                  <div class="stat-item">
                    <span class="stat-label">Correct Answers</span>
                    <span class="stat-value">{{ correctCount }}/{{ totalQuestions }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Percentage</span>
                    <span class="stat-value">{{ scorePercentage }}%</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Performance</span>
                    <span class="stat-value">
                      <span v-if="scorePercentage >= 80">Excellent! 🎉</span>
                      <span v-else-if="scorePercentage >= 50">Good effort! 👍</span>
                      <span v-else>Keep practicing! 💪</span>
                    </span>
                  </div>
                </div>
              </div>
              <button 
                type="button" 
                class="back-btn"
                @click="$router.push('/user/quizzes')"
              >
                <i class="fas fa-arrow-left"></i> Back to Quizzes
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
  </div>
</div>
</template>

<script>
import axios from "@/axios";
import Sidebar from "@/components/Sidebar.vue";

export default {
  name: "QuizAttempt",
  components: {
    Sidebar
  },
  data() {
    return {
      questions: [],
      userAnswers: {},
      totalQuestions: 0,
      correctCount: 0,
      submitted: false,
      loading: true,
      timeLeft: 0,
      timer: null,
      quizDetails: null,
      error: null,
      currentQuestion: 0,
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
          title: "📥 Export Report",
          text: "Export your quiz history and performance.",
          link: "/user/export",
          btnClass: "btn-info"
        },
        {
          title: "📊 My Progress",
          text: "Track your progress with charts and stats.",
          link: "/user/progress",
          btnClass: "btn-warning"
        }
      ]
    };
  },
  computed: {
    formattedTime() {
      const m = Math.floor(this.timeLeft / 60).toString().padStart(2, "0");
      const s = (this.timeLeft % 60).toString().padStart(2, "0");
      return `${m}:${s}`;
    },
    calculatedScore() {
      return this.submitted ? this.correctCount : "-";
    },
    allQuestionsAnswered() {
      return Object.keys(this.userAnswers).length === this.totalQuestions;
    },
    scorePercentage() {
      return Math.round((this.correctCount / this.totalQuestions) * 100);
    },
    scoreAlertClass() {
      if (this.scorePercentage >= 80) return 'excellent';
      if (this.scorePercentage >= 50) return 'good';
      return 'poor';
    }
  },
  async mounted() {
    await this.loadQuizData();
    this.startTimer();
    this.setupScrollListener();
  },
  beforeUnmount() {
    clearInterval(this.timer);
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    async loadQuizData() {
      const token = localStorage.getItem("token");
      const quizId = this.$route.params.id;

      try {
        const [questionsRes, quizzesRes] = await Promise.all([
          axios.get(`/user/quiz/${quizId}`, {
            headers: { Authorization: `Bearer ${token}` }
          }),
          axios.get(`/user/all_quizzes`, {
            headers: { Authorization: `Bearer ${token}` }
          })
        ]);

        this.questions = questionsRes.data;
        this.totalQuestions = this.questions.length;
        this.quizDetails = quizzesRes.data.find(q => q.id == quizId);
        this.timeLeft = (parseInt(this.quizDetails?.time_duration) || 10) * 60;
        this.loading = false;
      } catch (err) {
        console.error("Quiz loading error:", err);
        this.error = err.response?.data?.message || "Network error";
        this.loading = false;
      }
    },
    startTimer() {
      this.timer = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft--;
          if (this.timeLeft === 60) {
            this.$notify({
              type: 'warning',
              title: 'Time Warning',
              text: 'Only 1 minute remaining!'
            });
          }
        } else {
          this.autoSubmitQuiz();
        }
      }, 1000);
    },
    setupScrollListener() {
      window.addEventListener('scroll', this.handleScroll);
    },
    handleScroll() {
      const questions = document.querySelectorAll('.question-card');
      questions.forEach((q, index) => {
        const rect = q.getBoundingClientRect();
        if (rect.top <= 100 && rect.bottom >= 100) {
          this.currentQuestion = index;
        }
      });
    },
    async autoSubmitQuiz() {
      if (this.submitted) return;

      this.$notify({
        type: 'warning',
        title: 'Time Expired',
        text: 'Your quiz has been automatically submitted'
      });

      await this.submitQuiz();
    },
    async submitQuiz() {
      if (this.submitted) return;

      clearInterval(this.timer);
      this.submitted = true;

      const token = localStorage.getItem("token");
      const quizId = this.$route.params.id;

      try {
        const payload = this.questions.reduce((acc, q) => {
          if (this.userAnswers[q.id]) {
            acc[q.id.toString()] = this.userAnswers[q.id];
          }
          return acc;
        }, {});

        const res = await axios.post(
          `/user/submit_quiz/${quizId}`,
          payload,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        this.correctCount = res.data.total_scored;

        setTimeout(() => {
          const results = document.querySelector('.results-summary');
          if (results) results.scrollIntoView({ behavior: 'smooth' });
        }, 300);

      } catch (err) {
        console.error("Submission error:", err);
        this.$notify({
          type: 'error',
          title: 'Submission Failed',
          text: err.response?.data?.message || 'Please try again'
        });
      }
    }
  }
};
</script>


<style scoped>
.quiz-attempt-container {
  max-width: 800px;
  margin: 0 auto;
  background-color: #f8f9fa;
  min-height: 100vh;
}

.quiz-header {
  background: linear-gradient(to right, #6a11cb, #2575fc);
  color: white;
  padding: 1.5rem;
  text-align: center;
  border-radius: 0 0 20px 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.quiz-title {
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.subject-badge {
  background-color: rgba(255, 255, 255, 0.2);
  font-size: 0.9rem;
  padding: 5px 10px;
  border-radius: 20px;
}

.quiz-content {
  padding: 2rem;
}

.loading-state {
  text-align: center;
  padding: 3rem;
  color: #6a11cb;
}

.spinner-grow {
  width: 3rem;
  height: 3rem;
  margin-bottom: 1rem;
}

.error-state {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.status-bar {
  display: flex;
  justify-content: space-between;
  background: white;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 8px;
}

.timer {
  background-color: #f0f7ff;
  color: #2575fc;
}

.time-warning {
  background-color: #fff0f0;
  color: #ff6b6b;
  animation: pulse 1s infinite;
}

.progress {
  background-color: #f0fff4;
  color: #2bb673;
}

.score-preview {
  background-color: #fff8f0;
  color: #ff9500;
}

.question-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border-left: 4px solid transparent;
}

.question-card.answered {
  border-left-color: #2bb673;
  background-color: #f8fff9;
}

.question-card.current {
  box-shadow: 0 0 0 3px rgba(106, 17, 203, 0.2);
}

.question-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.question-number {
  font-weight: 700;
  color: #6a11cb;
  font-size: 1.1rem;
}

.question-status {
  color: #2bb673;
  font-size: 0.9rem;
}

.question-text {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.options-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.option-card {
  position: relative;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s ease;
  cursor: pointer;
}

.option-card:hover {
  border-color: #6a11cb;
  background-color: #f9f5ff;
}

.option-card.selected {
  border-color: #6a11cb;
  background-color: #f0e6ff;
}

.option-card input {
  position: absolute;
  opacity: 0;
}

.option-card label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.option-letter {
  width: 28px;
  height: 28px;
  background-color: #6a11cb;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.option-text {
  flex: 1;
}

.action-buttons {
  margin-top: 2rem;
  text-align: center;
}

.submit-btn {
  background: linear-gradient(to right, #6a11cb, #2575fc);
  color: white;
  border: none;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 15px rgba(106, 17, 203, 0.3);
}

.submit-btn:disabled {
  background: #e0e0e0;
  color: #999;
  box-shadow: none;
  cursor: not-allowed;
}

.submit-btn.pulse {
  animation: pulse 2s infinite;
}

.back-btn {
  background: white;
  color: #6a11cb;
  border: 2px solid #6a11cb;
  padding: 0.8rem 1.5rem;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 1rem;
}

.back-btn:hover {
  background: #f5f0ff;
}

.results-summary {
  margin-top: 2rem;
}

.result-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.result-card.excellent {
  border-top: 4px solid #2bb673;
}

.result-card.good {
  border-top: 4px solid #ff9500;
}

.result-card.poor {
  border-top: 4px solid #ff6b6b;
}

.result-header {
  margin-bottom: 1.5rem;
}

.result-header i {
  font-size: 2.5rem;
  color: #6a11cb;
  margin-bottom: 1rem;
}

.result-header h4 {
  font-weight: 700;
  color: #333;
}

.result-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.stat-item {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
}

.stat-label {
  display: block;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-weight: 700;
  font-size: 1.2rem;
  color: #6a11cb;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

@media (max-width: 768px) {
  .options-grid {
    grid-template-columns: 1fr;
  }
  
  .result-stats {
    grid-template-columns: 1fr;
  }
  
  .status-bar {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .status-item {
    justify-content: center;
  }
}
</style>