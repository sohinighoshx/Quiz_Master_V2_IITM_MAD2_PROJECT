<template>
  <div class="login-wrapper">
    <div class="login-card">
      <h2 class="title">Welcome Back 👋</h2>
      <p class="subtitle">Login to your Quiz Master account</p>

      <form @submit.prevent="login" autocomplete="off">
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
        <button type="submit" class="btn btn-purple w-100">Login</button>
      </form>

      <p class="mt-3 signup-text">
        Don't have an account?
        <router-link to="/signup" class="signup-link">Sign Up</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    async login() {
      try {
        const res = await axios.post('http://localhost:5001/login', {
          email: this.email,
          password: this.password
        })
        localStorage.setItem('token', res.data.access_token)
        localStorage.setItem('role', res.data.role)
        this.$router.push(res.data.role === 'admin' ? '/admin' : '/user')
      } catch (err) {
        console.error(err.response?.data || err.message)
        alert('Login failed ❌')
      }
    }
  }
}
</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #e0c3fc, #8ec5fc);
}

.login-card {
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

.signup-text {
  margin-top: 1.2rem;
  font-size: 0.9rem;
  color: #555;
}

.signup-link {
  color: #7b2cbf;
  font-weight: bold;
  margin-left: 5px;
  text-decoration: underline;
}
</style>
