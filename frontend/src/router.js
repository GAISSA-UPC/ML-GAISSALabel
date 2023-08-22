import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import EnergyLabel from '@/views/EnergyLabel.vue'
import TrainingPreSaved from '@/views/TrainingPreSaved.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/prova',
      name: 'prova',
      component: EnergyLabel
    },
    {
      path: '/trainingPre',
      name: 'training pre saved',
      component: TrainingPreSaved
    },
  ]
})

export default router
