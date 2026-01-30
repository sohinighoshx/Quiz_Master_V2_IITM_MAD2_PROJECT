import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/Index.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import UserDashboard from '../views/UserDashboard.vue'

// ✅ Admin child components
import ManageSubjects from '../views/admin/ManageSubjects.vue'
import ManageChapters from '../views/admin/ManageChapters.vue'
import ExportReport from '../views/admin/ExportReport.vue'

const routes = [
  { path: '/', component: Index },
  { path: '/login', component: Login },
  { path: '/signup', name: 'Signup', component: Signup },
  { path: '/admin', component: AdminDashboard },

  // ✅ Admin Routes
  { path: '/admin/subject', component: ManageSubjects },
  { path: '/admin/chapters', component: ManageChapters },
  { path: '/admin/quizzes',component: () => import('@/views/admin/ManageQuizzes.vue'),meta: { requiresAuth: true }},
  { path: '/admin/users', name: 'AdminUsers',component: () => import('@/views/admin/AdminUsers.vue')},
  { path: '/admin/export', component: ExportReport },
  { path: '/admin/summary', name: 'AdminSummary',component:()=> import('@/views/admin/AdminSummary.vue')},
  { path: '/admin/subject/:id/chapters',name: 'Chapters',component: () => import('@/views/admin/Chapters.vue')},
  { path: '/admin/subject/:subjectId/chapter/:chapterId/notes',name: 'AdminNotes',component: () => import('@/views/admin/AdminNotes.vue')},
  // ✅ User
  { path: '/user', component: UserDashboard },
  { path: "/user/quizzes", name: "UserLatestQuizzes", component: () => import('@/views/user/UserLatestQuizzes.vue')},
  { path: "/user/quiz/:id", name: "QuizAttempt", component: () => import("@/views/user/QuizAttempt.vue")},
  { path: "/user/history", name: "QuizHistory", component: () => import("@/views/user/QuizHistory.vue")},
  { path: "/user/progress", name: "UserProgress",component: () => import("@/views/user/UserProgress.vue")},
  {
  path: "/user/settings",
  name: "UserSettings",
  component: () => import("@/views/user/UserSettings.vue"),
},

{
  path: "/user/read-notes",
  name: "UserReadNotes",
  component: () => import("@/views/user/UserReadNotes.vue"),
}

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router