import { createRouter, createWebHistory } from 'vue-router'

// Core routes
const HomeView = () => import('@/views/HomeView.vue')
const AboutView = () => import('@/views/AboutView.vue')

// Training routes
const TrainingForm = () => import('@/tools/gaissalabel/views/TrainingForm.vue')
const TrainingPreSaved = () => import('@/tools/gaissalabel/views/TrainingPreSaved.vue')
const TrainingFile = () => import('@/tools/gaissalabel/views/TrainingFile.vue')
const TrainingLabelInfo = () => import('@/tools/gaissalabel/views/TrainingLabelInfo.vue')

// Inference routes
const InferenceForm = () => import('@/tools/gaissalabel/views/InferenceForm.vue')
const InferencePreSaved = () => import('@/tools/gaissalabel/views/InferencePreSaved.vue')
const InferenceFile = () => import('@/tools/gaissalabel/views/InferenceFile.vue')
const InferenceDeploy = () => import('@/tools/gaissalabel/views/InferenceDeploy.vue')
const InferenceLabelInfo = () => import('@/tools/gaissalabel/views/InferenceLabelInfo.vue')

// GAISSA ROI Analyzer routes
const GAISSAROIAnalyzerAnalysis = () => import("@/tools/gaissaroianalyzer/views/GAISSAROIAnalyzerAnalysis.vue")
const GAISSAROIAnalyzerNewForm = () => import("@/tools/gaissaroianalyzer/views/GAISSAROIAnalyzerNewForm.vue")
const GAISSAROIAnalyzerCalculationRepository = () => import("@/tools/gaissaroianalyzer/views/GAISSAROIAnalyzerCalculationRepository.vue")
const GAISSAROIAnalyzerResearchRepository = () => import("@/tools/gaissaroianalyzer/views/GAISSAROIAnalyzerResearchRepository.vue")

// Admin routes
const AdminMetriquesInfo = () => import('@/tools/gaissalabel/views/AdminMetriquesInfo.vue')
const AdminMetrica = () => import('@/tools/gaissalabel/views/AdminMetrica.vue')
const AdminInformacio = () => import('@/tools/gaissalabel/views/AdminInformacio.vue')
const AdminEines = () => import('@/tools/gaissalabel/views/AdminEines.vue')
const AdminEina = () => import('@/tools/gaissalabel/views/AdminEina.vue')
const AdminSincro = () => import('@/tools/gaissalabel/views/AdminSincro.vue')
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
      path: '/gaissa-roi-analyzer/calculation-repository',
      name: 'GAISSA ROI Analyzer Calculation Repository',
      component: GAISSAROIAnalyzerCalculationRepository,
    },
    {
      path: '/gaissa-roi-analyzer/research-repository',
      name: 'GAISSA ROI Analyzer Research Repository',
      component: GAISSAROIAnalyzerResearchRepository,
    },
    {
      path: '/gaissa-roi-analyzer/gaissa-roi-analysis/:id_experiment',
      name: "GAISSA ROI Analyzer Analysis",
      component: GAISSAROIAnalyzerAnalysis,
    },
    {
      path: '/gaissa-roi-analyzer/new-form',
      name: 'GAISSA ROI Analyzer New Form',
      component: GAISSAROIAnalyzerNewForm,
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
