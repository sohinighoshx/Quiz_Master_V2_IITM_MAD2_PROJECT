<template>
  <AdminLayout>
    <div class="container py-4">
      <h2 class="text-center mb-4">📋 Manage Quizzes</h2>

      <div class="d-flex align-items-center mb-3">
        <select v-model="selectedQuizId" class="form-select me-2 w-50">
          <option disabled value="">Select a Quiz</option>
          <option v-for="quiz in allQuizzes" :key="quiz.id" :value="quiz.id">
            {{ quiz.title }}
          </option>
        </select>
        <button class="btn btn-dark" @click="openAddQuizForm()">+ Add Quiz</button>
      </div>

      <!-- Quiz Cards -->
      <div v-for="quiz in allQuizzes" :key="quiz.id" class="card mb-3">
        <div class="card-body">
          <h5 class="card-title">Title: {{ quiz.title }}</h5>
          <p>
            <strong>Subject:</strong> {{ quiz.subject_name }}<br />
            <strong>Chapter:</strong> {{ quiz.chapter_name }}<br />
            <strong>Date:</strong> {{ quiz.date_of_quiz }}<br />
            <strong>Time:</strong> {{ quiz.time_duration }}<br />
            <strong>No. of Questions:</strong> {{ quiz.question_count }}
          </p>

          <div class="mb-2">
            <button class="btn btn-primary btn-sm me-2" @click="openEditQuizForm(quiz)">Edit</button>
            <button class="btn btn-danger btn-sm" @click="deleteQuiz(quiz.id)">Delete</button>
          </div>

          <button class="btn btn-secondary btn-sm mb-2" @click="toggleQuestions(quiz)">
            {{ quiz.showQuestions ? 'Hide Questions' : 'Show Questions' }}
          </button>

          <div v-if="quiz.showQuestions">
            <ul class="list-group mb-2">
              <li v-for="q in quiz.questions" :key="q.id" class="list-group-item d-flex justify-content-between align-items-center">
                {{ q.question_statement }}
                <div>
                  <button class="btn btn-sm btn-warning me-1" @click="openEditQuestionForm(q)">Edit</button>
                  <button class="btn btn-sm btn-danger" @click="deleteQuestion(q.id)">Delete</button>
                </div>
              </li>
            </ul>
            <button class="btn btn-success btn-sm" @click="openAddQuestionForm(quiz.id)">Add Question</button>
          </div>
        </div>
      </div>

      <!-- Floating Quiz Form -->
      <div v-if="showQuizForm" class="modal-backdrop" @click.self="closeQuizForm">
        <div class="modal-card bg-white p-4 rounded shadow">
          <h5 class="mb-3">{{ editingQuiz ? '✏️ Edit Quiz' : '📝 Add New Quiz' }}</h5>
          <form @submit.prevent="submitQuizForm">
            <!-- Subject Dropdown -->
            <select v-model="selectedSubjectId" @change="fetchChapters" class="form-select mb-2" required>
              <option disabled value="">Select Subject</option>
              <option v-for="s in allSubjects" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>

            <!-- Chapter Dropdown -->
            <select v-model="selectedChapterId" class="form-select mb-2" required>
              <option disabled value="">Select Chapter</option>
              <option v-for="c in filteredChapters" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>

            <input v-model="quizForm.title" class="form-control mb-2" placeholder="Title" required />
            <input v-model="quizForm.date_of_quiz" class="form-control mb-2" placeholder="Date (YYYY-MM-DD)" required />
            <input v-model="quizForm.time_duration" class="form-control mb-2" placeholder="Time Duration" required />
            <textarea v-model="quizForm.remarks" class="form-control mb-2" placeholder="Remarks"></textarea>

            <button class="btn btn-success w-100">{{ editingQuiz ? 'Update' : 'Save' }}</button>
          </form>
        </div>
      </div>

      <!-- Floating Question Form -->
      <div v-if="showQuestionForm" class="modal-backdrop" @click.self="closeQuestionForm">
        <div class="modal-card bg-white p-4 rounded shadow">
          <h5 class="mb-3">Add Question</h5>
          <form @submit.prevent="submitQuestionForm">
            <textarea v-model="questionForm.question_statement" class="form-control mb-2" placeholder="Question" required />
            <input v-model="questionForm.option1" class="form-control mb-2" placeholder="Option 1" required />
            <input v-model="questionForm.option2" class="form-control mb-2" placeholder="Option 2" required />
            <input v-model="questionForm.option3" class="form-control mb-2" placeholder="Option 3" required />
            <input v-model="questionForm.option4" class="form-control mb-2" placeholder="Option 4" required />
            <input v-model="questionForm.correct_option" class="form-control mb-2" placeholder="Correct Option (1-4)" required />
            <button class="btn btn-success w-100">Save Question</button>
          </form>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script>
import AdminLayout from '@/layouts/AdminLayout.vue'

export default {
  components: { AdminLayout },

  data() {
    return {
      allQuizzes: [],
      allSubjects: [],
      filteredChapters: [],
      selectedQuizId: '',
      selectedSubjectId: '',
      selectedChapterId: '',

      chapters: [],
      subjectName: '',
      showAddChapterForm: false,
      editChapterForm: false,

      showQuizForm: false,
      editingQuiz: null,
      quizForm: {
        title: '',
        date_of_quiz: '',
        time_duration: '',
        remarks: '',
        chapter_id: null
      },

      showQuestionForm: false,
      editingQuestionId: null, // ✅ added for edit functionality
      questionForm: {
        quiz_id: null,
        question_statement: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: ''
      },

      chapterForm: {
        id: null,
        name: '',
        description: ''
      }
    }
  },

  methods: {
    async fetchQuizzes() {
      const res = await fetch('/admin/quizzes', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await res.json();
      this.allQuizzes = data.map(q => ({ ...q, showQuestions: false, questions: [] }));
    },

    async fetchSubjects() {
      const res = await fetch('/admin/subject', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      this.allSubjects = await res.json();
    },

    async fetchChapters() {
      const res = await fetch(`/admin/subject/${this.selectedSubjectId}/chapters`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      this.filteredChapters = await res.json();
    },

    async toggleQuestions(quiz) {
      if (!quiz.showQuestions) {
        const res = await fetch(`/admin/quiz/${quiz.id}/questions`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        quiz.questions = await res.json();
      }
      quiz.showQuestions = !quiz.showQuestions;
    },

    openAddQuizForm() {
      this.editingQuiz = null;
      this.quizForm = {
        title: '',
        date_of_quiz: '',
        time_duration: '',
        remarks: '',
        chapter_id: null
      };
      this.selectedSubjectId = '';
      this.selectedChapterId = '';
      this.filteredChapters = [];
      this.showQuizForm = true;
    },

    openEditQuizForm(quiz) {
      this.editingQuiz = quiz;
      this.quizForm = {
        title: quiz.title,
        date_of_quiz: quiz.date_of_quiz,
        time_duration: quiz.time_duration,
        remarks: quiz.remarks
      };
      this.selectedSubjectId = this.allSubjects.find(s => s.name === quiz.subject_name)?.id || '';
      this.fetchChapters().then(() => {
        const ch = this.filteredChapters.find(c => c.name === quiz.chapter_name);
        this.selectedChapterId = ch?.id || '';
        this.showQuizForm = true;
      });
    },

    async submitQuizForm() {
      const body = {
        ...this.quizForm,
        chapter_id: this.selectedChapterId
      };

      const url = this.editingQuiz ? `/admin/quiz/${this.editingQuiz.id}` : '/admin/quiz';
      const method = this.editingQuiz ? 'PUT' : 'POST';

      await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(body)
      });

      this.fetchQuizzes();
      this.closeQuizForm();
    },

    closeQuizForm() {
      this.showQuizForm = false;
    },

    async deleteQuiz(id) {
      await fetch(`/admin/quiz/${id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      this.fetchQuizzes();
    },

    openAddQuestionForm(quizId) {
      this.editingQuestionId = null;
      this.questionForm = {
        quiz_id: quizId,
        question_statement: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: ''
      };
      this.showQuestionForm = true;
    },

    openEditQuestionForm(question) {
      this.questionForm = {
        quiz_id: question.quiz_id,
        question_statement: question.question_statement,
        option1: question.option1,
        option2: question.option2,
        option3: question.option3,
        option4: question.option4,
        correct_option: question.correct_option
      };
      this.editingQuestionId = question.id;
      this.showQuestionForm = true;
    },

    async submitQuestionForm() {
      const isEditing = !!this.editingQuestionId;
      const url = isEditing
        ? `/admin/question/${this.editingQuestionId}`
        : '/admin/question';
      const method = isEditing ? 'PUT' : 'POST';

      await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(this.questionForm)
      });

      this.fetchQuizzes();
      this.closeQuestionForm();
    },

    async deleteQuestion(id) {
      await fetch(`/admin/question/${id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      this.fetchQuizzes();
    },

    closeQuestionForm() {
      this.showQuestionForm = false;
      this.editingQuestionId = null;
    }
  },

  mounted() {
    this.fetchQuizzes();
    this.fetchSubjects();
  }
};
</script>

<style scoped>
.card {
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-card {
  width: 100%;
  max-width: 500px;
}
</style>
