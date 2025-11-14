import { createRouter, createWebHistory } from 'vue-router'

// Lazy-load route components
const UploadResume = () => import('../components/UploadResume.vue')
const Recommendations = () => import('../components/Recommendations.vue')

const routes = [
  { path: '/', name: 'Home', component: UploadResume },
  { path: '/recommendations', name: 'Recommendations', component: Recommendations },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
