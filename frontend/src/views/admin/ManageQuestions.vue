<template>
  <div class="container py-4">
    <h3>Create Question</h3>
    <form @submit.prevent="addQuestion">
      <select v-model="quiz_id" class="form-select mb-2">
        <option disabled value="">Select Quiz</option>
        <option v-for="q in quizzes" :value="q.id">Quiz {{ q.id }}</option>
      </select>
      <textarea v-model="question_statement" class="form-control mb-2" placeholder="Question"></textarea>
      <input v-model="option1" class="form-control mb-1" placeholder="Option 1" />
      <input v-model="option2" class="form-control mb-1" placeholder="Option 2" />
      <input v-model="option3" class="form-control mb-1" placeholder="Option 3" />
      <input v-model="option4" class="form-control mb-1" placeholder="Option 4" />
      <input v-model="correct_option" class="form-control mb-2" placeholder="Correct Option (e.g. option1)" />
      <button class="btn btn-warning">Add Question</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      quiz_id: '', question_statement: '', option1: '', option2: '', option3: '', option4: '', correct_option: '', quizzes: []
    }
  },
  async mounted() {
    const res = await axios.get('/api/quizzes')
    this.quizzes = res.data
  },
  methods: {
    async addQuestion() {
      const token = localStorage.getItem('token')
      await axios.post('/admin/question', {
        quiz_id: this.quiz_id, question_statement: this.question_statement,
        option1: this.option1, option2: this.option2, option3: this.option3,
        option4: this.option4, correct_option: this.correct_option
      }, { headers: { Authorization: `Bearer ${token}` }})
      alert('Question added!')
    }
  }
}
</script>

