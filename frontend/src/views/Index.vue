<template>
  <div class="landing">
    <!-- Navigation -->
    <header class="top-nav">
      <div class="logo">QuizMaster</div>
      <nav class="nav-links">
        <a href="#features">Features</a>
        <router-link to="/login" class="btn-outline">Log In</router-link>
        <router-link to="/signup" class="btn-filled">Sign Up</router-link>
      </nav>
    </header>

    <!-- Hero -->
    <section class="hero">
      <p class="tagline">Beautiful Minds Don’t Guess — They Analyze🪽✨</p>
      <h1>Think Smart<br />Slay Hard</h1>
      <p class="subtext">
        Ace your exams with personalized quizzes, chapter-wise tracking, and smart analytics.
        Built for students, procrastinators, and overachievers alike.
      </p>
      <router-link to="/signup" class="btn-glow">Get Started</router-link>
    </section>

    <!-- Why Us -->
    <section class="why-us" id="features">
      <h2 class="section-title">Why Us?</h2>
      <p class="why-desc">
        I started QuizMaster because I struggled to stay consistent while preparing for exams. Creating this app
        helped me track my own progress with clarity and ease. It’s designed for students who want to stop cramming
        last-minute and instead build long-term learning success through structured practice and motivation.
      </p>

      <div class="feature-cards">
        <div class="card">
          <h3>📚 Chapter-based Quizzes</h3>
          <p>Break down big topics into small, manageable quizzes by subject and chapter.</p>
        </div>
        <div class="card">
          <h3>📊 Score Tracking</h3>
          <p>Keep track of what you’ve mastered and what needs revision — all in one dashboard.</p>
        </div>
        <div class="card">
          <h3>🎯 Personalized Learning</h3>
          <p>We adapt quizzes based on your strengths and weaknesses to boost your performance.</p>
        </div>
      </div>
    </section>

  </div>
</template>

<script>
export default {
  name: 'Index',
  data() {
    return {
      faqName: '',
      faqEmail: '',
      faqQuestion: ''
    }
  },
  methods: {
    submitFaq() {
      console.log("FAQ Submitted:", {
        name: this.faqName,
        email: this.faqEmail,
        question: this.faqQuestion
      })
      alert('Your question has been submitted! 💬')
      this.faqName = ''
      this.faqEmail = ''
      this.faqQuestion = ''
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro&display=swap');
.landing {
  background: url('/index.png') no-repeat center center fixed;
  background-size: cover;
  color: rgb(255, 255, 255);
  overflow-x: hidden;
  min-height: 100vh;
}

.top-nav {
  display: flex;
  justify-content: space-between;
  padding: 1.2rem 2rem;
  flex-wrap: wrap;
}

.nav-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-links a,
.nav-links router-link {
  color: white;
  text-decoration: none;
}

.btn-outline {
  border: 2px solid white;
  padding: 0.4rem 1rem;
  border-radius: 8px;
  background: transparent;
  font-weight: bold;
}

.btn-filled {
  background-color: #7b2cbf;
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 8px;
  font-weight: bold;
}

.hero {
  text-align: center;
  margin-top: 4rem;
  padding: 2rem;
}

.tagline {
  font-family: 'Crimson Pro', serif;
  background: rgba(0, 0, 0, 0.2);
  padding: 0.4rem 1rem;
  border-radius: 20px;
  display: inline-block;
  font-size: 1 rem;
}

.hero h1 {
  font-size: 3.5rem;
  font-weight: 900;
}

.subtext {
  font-size: 1rem;
  max-width: 600px;
  margin: 1rem auto 2rem;
}

.btn-glow {
  background-color: white;
  color: #7b2cbf;
  font-weight: bold;
  padding: 0.75rem 2rem;
  border-radius: 50px;
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
}

.btn-glow:hover {
  transform: scale(1.05);
  box-shadow: 0 0 25px rgba(255, 255, 255, 0.5);
}

/* Why Us + Features Section */
.why-us {
  padding: 3rem 2rem;
  background-color: rgba(255, 255, 255, 0.08);
  text-align: center;
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.why-desc {
  max-width: 700px;
  margin: 0 auto 2rem;
  font-size: 1rem;
}

.feature-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.card {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  transition: 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}

/* FAQ form */
.faqs {
  padding: 3rem 2rem;
  text-align: center;
  background-color: rgba(0, 0, 0, 0.1);
}

.faq-form {
  max-width: 500px;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-control {
  border: none;
  border-radius: 8px;
  padding: 0.8rem;
  font-size: 1rem;
  color: #333;
}

.form-control:focus {
  outline: none;
}

.btn-purple {
  background-color: #9b59b6;
  color: white;
  font-weight: bold;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 10px;
}

.btn-purple:hover {
  background-color: #8e44ad;
}
</style>
