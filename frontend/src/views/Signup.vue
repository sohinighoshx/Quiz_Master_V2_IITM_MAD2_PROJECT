<template>
  <div class="signup-wrapper">
    <div class="signup-card">
      <h2 class="title">Create Your Account ✨</h2>
      <p class="subtitle">Join Quiz Master and start your learning journey!</p>

      <form @submit.prevent="register" autocomplete="off">
        <div class="mb-3">
          <input
            type="text"
            v-model="full_name"
            class="form-control"
            placeholder="Full Name"
            required
            autocomplete="off"
          />
        </div>

        <div class="mb-3">
          <input
            type="email"
            v-model="email"
            class="form-control"
            placeholder="Email"
            required
            autocomplete="new-email"
          />
        </div>

        <div class="mb-3">
          <input
            type="password"
            v-model="password"
            class="form-control"
            placeholder="Password"
            required
            autocomplete="new-password"
          />
        </div>

        <div class="mb-3">
          <input
            type="text"
            v-model="qualification"
            class="form-control"
            placeholder="Qualification"
            required
            autocomplete="off"
          />
        </div>

        <div class="mb-3">
          <input
            type="date"
            v-model="dob"
            class="form-control"
            :max="today"
            required
          />
        </div>

        <button type="submit" class="btn btn-purple w-100">Sign Up</button>
      </form>

      <!-- Link to login -->
      <p class="mt-3 login-text">
        Already have an account?
        <router-link to="/login" class="login-link">Log In</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      full_name: '',
      email: '',
      password: '',
      qualification: '',
      dob: '',
      today: new Date().toISOString().split('T')[0] // 📅 today's date
    }
  },
  methods: {
    async register() {
      try {
        const res = await axios.post('http://localhost:5001/signup', {
          full_name: this.full_name,
          email: this.email,
          password: this.password,
          qualification: this.qualification,
          dob: this.dob
        })
        alert('Signup successful ✅')
        this.$router.push('/login')
      } catch (err) {
        console.error(err.response?.data || err.message)
        alert('Signup failed ❌')
      }
    }
  }
}
</script>

<style scoped>
.signup-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #e0c3fc, #8ec5fc);
}

.signup-card {
  background: rgba(255, 255, 255, 0.85);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
  backdrop-filter: blur(10px);
}

.title {
  font-weight: bold;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  color: #4b0082;
}

.subtitle {
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.btn-purple {
  background-color: #9b59b6;
  color: white;
  font-weight: bold;
  border: none;
}

.btn-purple:hover {
  background-color: #8e44ad;
}

.login-text {
  margin-top: 1.2rem;
  font-size: 0.9rem;
  color: #555;
}

.login-link {
  color: #7b2cbf;
  font-weight: bold;
  margin-left: 5px;
  text-decoration: underline;
}
</style>
