import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import trainingForm from '@/views/trainingForm.vue'
import TrainingPreSaved from '@/views/TrainingPreSaved.vue'
import InferenceForm from '@/views/InferenceForm.vue'
import InferencePreSaved from '@/views/InferencePreSaved.vue'
import TrainingLabelInfo from "@/views/TrainingLabelInfo.vue";
import InferenceLabelInfo from "@/views/InferenceLabelInfo.vue";

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
      component: trainingForm
    },
    {
      path: '/trainingPre',
      name: 'training pre saved',
      component: TrainingPreSaved
    },
    {
      path: '/inferenceForm',
      name: 'inference form',
      component: InferenceForm
    },
    {
      path: '/InferencePre',
      name: 'inference pre saved',
      component: InferencePreSaved
    },
    {
      path: '/models/:id_model/trainings/:id_training',
      name: 'Label info for training',
      component: TrainingLabelInfo
    },
    {
      path: '/models/:id_model/inferences/:id_inference',
      name: 'Label info for inference',
      component: InferenceLabelInfo
    },
  ]
})

export default router
