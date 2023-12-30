import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import TrainingForm from '@/views/TrainingForm.vue'
import TrainingPreSaved from '@/views/TrainingPreSaved.vue'
import TrainingFile from '@/views/TrainingFile.vue'
import InferenceForm from '@/views/InferenceForm.vue'
import InferencePreSaved from '@/views/InferencePreSaved.vue'
import InferenceFile from '@/views/InferenceFile.vue'
import InferenceDeploy from '@/views/InferenceDeploy.vue'
import TrainingLabelInfo from "@/views/TrainingLabelInfo.vue"
import InferenceLabelInfo from "@/views/InferenceLabelInfo.vue"
import AdminMetriquesInfo from "@/views/AdminMetriquesInfo.vue"
import AdminMetrica from "@/views/AdminMetrica.vue"
import AdminInformacio from "@/views/AdminInformacio.vue"
import AdminEines from "@/views/AdminEines.vue"
import AdminEina from "@/views/AdminEina.vue"
import AdminSincro from "@/views/AdminSincro.vue"
import AdminLogin from "@/views/AdminLogin.vue"

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
      component: TrainingForm
    },
    {
      path: '/trainingPre',
      name: 'training pre saved',
      component: TrainingPreSaved
    },
    {
      path: '/trainingFile',
      name: 'training file',
      component: TrainingFile
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
      path: '/InferenceFile',
      name: 'inference file',
      component: InferenceFile
    },
    {
      path: '/InferenceDeploy',
      name: 'inference deploy',
      component: InferenceDeploy
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
    {
      path: '/admin/metriquesinfo',
      name: 'Admin mètriques i informacions',
      component: AdminMetriquesInfo,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/metriques/:id_metrica',
      name: 'Admin mètrica edit',
      component: AdminMetrica,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/metriques',
      name: 'Admin mètrica new',
      component: AdminMetrica,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/informacions/:id_informacio',
      name: 'Admin informació edit',
      component: AdminInformacio,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/informacions',
      name: 'Admin informació new',
      component: AdminInformacio,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/listeines',
      name: 'Admin eines',
      component: AdminEines,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/eines/:id_eina',
      name: 'Admin eina edit',
      component: AdminEina,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/eines',
      name: 'Admin eina new',
      component: AdminEina,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/sincronitzacio',
      name: 'Admin sincronitzacio',
      component: AdminSincro,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/login',
      name: 'Admin login',
      component: AdminLogin
    },
  ]
})

export default router
