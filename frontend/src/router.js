import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import EnergyLabel from '@/components/EnergyLabel.vue'
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
      path: '/trainingForm',
      name: 'training form',
      component: TrainingPreSaved
    },
    {
      path: '/trainingPre',
      name: 'training pre saved',
      component: TrainingPreSaved
    },
  ]
})

export default router
