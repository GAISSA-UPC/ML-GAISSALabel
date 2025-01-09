import { createRouter, createWebHistory } from 'vue-router'

// Core routes
const HomeView = () => import('@/views/HomeView.vue')
const AboutView = () => import('@/views/AboutView.vue')

// Training routes
const TrainingForm = () => import('@/views/TrainingForm.vue')
const TrainingPreSaved = () => import('@/views/TrainingPreSaved.vue')
const TrainingFile = () => import('@/views/TrainingFile.vue')
const TrainingLabelInfo = () => import('@/views/TrainingLabelInfo.vue')

// Inference routes
const InferenceForm = () => import('@/views/InferenceForm.vue')
const InferencePreSaved = () => import('@/views/InferencePreSaved.vue')
const InferenceFile = () => import('@/views/InferenceFile.vue')
const InferenceDeploy = () => import('@/views/InferenceDeploy.vue')
const InferenceLabelInfo = () => import('@/views/InferenceLabelInfo.vue')

// ROI Inference Analysis routes
const ROIInferencePreSaved = () => import('@/views/ROIInferencePreSaved.vue')
const ROIInferenceAnalysis = () => import("@/views/ROIInferenceAnalysis.vue")

// Admin routes
const AdminMetriquesInfo = () => import('@/views/AdminMetriquesInfo.vue')
const AdminMetrica = () => import('@/views/AdminMetrica.vue')
const AdminInformacio = () => import('@/views/AdminInformacio.vue')
const AdminEines = () => import('@/views/AdminEines.vue')
const AdminEina = () => import('@/views/AdminEina.vue')
const AdminSincro = () => import('@/views/AdminSincro.vue')
const AdminLogin = () => import('@/views/AdminLogin.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },{
      path: '/about',
      name: 'about',
      component: AboutView
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
      path: '/roi-inference-pre',
      name: 'ROI Inference PreSaved Consult',
      component: ROIInferencePreSaved,
    },
    {
      path: "/roi-inference-analysis/:id_model/:optimization_technique/:technique_param/:id_experiment",
      name: "ROI Inference Analysis",
      component: ROIInferenceAnalysis,
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
