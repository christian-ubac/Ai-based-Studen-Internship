import { createRouter, createWebHistory } from 'vue-router'

// Lazy-load route components
const Home = () => import('../components/Home.vue')
const UploadResume = () => import('../components/UploadResume.vue')
const Recommendations = () => import('../components/Recommendations.vue')

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/upload', name: 'Upload', component: UploadResume },
  { path: '/recommendations', name: 'Recommendations', component: Recommendations },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
