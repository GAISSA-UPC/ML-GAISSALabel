import { createRouter, createWebHistory } from 'vue-router'
import store from './store'

// Core routes
const GAISSAToolsHome = () => import('@/views/GAISSAToolsHome.vue')
const AboutView = () => import('@/views/AboutView.vue')

// GAISSALabel tool routes
const GAISSALabelHome = () => import('@/tools/gaissalabel/views/HomeView.vue')

// GAISSALabel Training routes
const TrainingForm = () => import('@/tools/gaissalabel/views/TrainingForm.vue')
const TrainingPreSaved = () => import('@/tools/gaissalabel/views/TrainingPreSaved.vue')
const TrainingFile = () => import('@/tools/gaissalabel/views/TrainingFile.vue')
const TrainingLabelInfo = () => import('@/tools/gaissalabel/views/TrainingLabelInfo.vue')

// GAISSALabel Inference routes
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
const GAISSAROIAnalyzerComparison = () => import("@/tools/gaissaroianalyzer/views/GAISSAROIAnalyzerComparison.vue")

// Admin routes
const AdminMetriquesInfo = () => import('@/tools/gaissalabel/views/AdminMetriquesInfo.vue')
const AdminMetrica = () => import('@/tools/gaissalabel/views/AdminMetrica.vue')
const AdminInformacio = () => import('@/tools/gaissalabel/views/AdminInformacio.vue')
const AdminEines = () => import('@/tools/gaissalabel/views/AdminEines.vue')
const AdminEina = () => import('@/tools/gaissalabel/views/AdminEina.vue')
const AdminSincro = () => import('@/tools/gaissalabel/views/AdminSincro.vue')
const AdminTools = () => import('@/tools/admin/views/AdminTools.vue')
const AdminLogin = () => import('@/views/AdminLogin.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: GAISSAToolsHome
    },
    {
      path: '/gaissalabel',
      name: 'gaissalabel-home',
      component: GAISSALabelHome,
      meta: { tool: 'gaissalabel' }
    },{
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/trainingForm',
      name: 'training form',
      component: TrainingForm,
      meta: { tool: 'gaissalabel' }
    },
    {
      path: '/trainingPre',
      name: 'training pre saved',
      component: TrainingPreSaved,
      meta: { tool: 'gaissalabel' }
    },
    {
      path: '/trainingFile',
      name: 'training file',
      component: TrainingFile,
      meta: { tool: 'gaissalabel' }
    },
    {
      path: '/inferenceForm',
      name: 'inference form',
      component: InferenceForm,
      meta: { tool: 'gaissalabel' }
    },
    {
      path: '/InferencePre',
      name: 'inference pre saved',
      component: InferencePreSaved,
      meta: { tool: 'gaissalabel' }
    },
    {
      path: '/InferenceFile',
      name: 'inference file',
      component: InferenceFile,
      meta: { tool: 'gaissalabel' }
    },
    {
      path: '/InferenceDeploy',
      name: 'inference deploy',
      component: InferenceDeploy,
      meta: { tool: 'gaissalabel' }
    },
    {
      path: '/models/:id_model/trainings/:id_training',
      name: 'Label info for training',
      component: TrainingLabelInfo,
      meta: { tool: 'gaissalabel' }
    },
    {
      path: '/models/:id_model/inferences/:id_inference',
      name: 'Label info for inference',
      component: InferenceLabelInfo,
      meta: { tool: 'gaissalabel' }
    },
    {
      path: '/gaissa-roi-analyzer/calculation-repository',
      name: 'GAISSA ROI Analyzer Calculation Repository',
      component: GAISSAROIAnalyzerCalculationRepository,
      meta: { tool: 'gaissaroianalyzer' }
    },
    {
      path: '/gaissa-roi-analyzer/research-repository',
      name: 'GAISSA ROI Analyzer Research Repository',
      component: GAISSAROIAnalyzerResearchRepository,
      meta: { tool: 'gaissaroianalyzer' }
    },
    {
      path: '/gaissa-roi-analyzer/gaissa-roi-analysis/:id_experiment',
      name: "GAISSA ROI Analyzer Analysis",
      component: GAISSAROIAnalyzerAnalysis,
      meta: { tool: 'gaissaroianalyzer' }
    },
    {
      path: '/gaissa-roi-analyzer/new-form',
      name: 'GAISSA ROI Analyzer New Form',
      component: GAISSAROIAnalyzerNewForm,
      meta: { tool: 'gaissaroianalyzer' }
    },
    {
      path: '/gaissa-roi-analyzer/comparison',
      name: 'GAISSA ROI Analyzer Comparison',
      component: GAISSAROIAnalyzerComparison,
      meta: { tool: 'gaissaroianalyzer' }
    },
    {
      path: '/admin/metriquesinfo',
      name: 'Admin mètriques i informacions',
      component: AdminMetriquesInfo,
      meta: { requiresAuth: true, tool: 'gaissalabel' }
    },
    {
      path: '/admin/metriques/:id_metrica',
      name: 'Admin mètrica edit',
      component: AdminMetrica,
      meta: { requiresAuth: true, tool: 'gaissalabel' }
    },
    {
      path: '/admin/metriques',
      name: 'Admin mètrica new',
      component: AdminMetrica,
      meta: { requiresAuth: true, tool: 'gaissalabel' }
    },
    {
      path: '/admin/informacions/:id_informacio',
      name: 'Admin informació edit',
      component: AdminInformacio,
      meta: { requiresAuth: true, tool: 'gaissalabel' }
    },
    {
      path: '/admin/informacions',
      name: 'Admin informació new',
      component: AdminInformacio,
      meta: { requiresAuth: true, tool: 'gaissalabel' }
    },
    {
      path: '/admin/listeines',
      name: 'Admin eines',
      component: AdminEines,
      meta: { requiresAuth: true, tool: 'gaissalabel' }
    },
    {
      path: '/admin/eines/:id_eina',
      name: 'Admin eina edit',
      component: AdminEina,
      meta: { requiresAuth: true, tool: 'gaissalabel' }
    },
    {
      path: '/admin/eines',
      name: 'Admin eina new',
      component: AdminEina,
      meta: { requiresAuth: true, tool: 'gaissalabel' }
    },
    {
      path: '/admin/sincronitzacio',
      name: 'Admin sincronitzacio',
      component: AdminSincro,
      meta: { requiresAuth: true, tool: 'gaissalabel' }
    },
    {
      path: '/admin/tools',
      name: 'Admin tools',
      component: AdminTools,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/login',
      name: 'Admin login',
      component: AdminLogin
    },
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters['auth/isLogged'];

  // Check authentication for routes that require it
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'Admin login' });
      return;
    }
  }

  // Check tool enablement status
  if (to.matched.some((record) => record.meta.tool === 'gaissalabel')) {
    if (!store.getters['configuration/isGAISSALabelEnabled']) {
      next({ name: 'home' });
      return;
    }
  }

  if (to.matched.some((record) => record.meta.tool === 'gaissaroianalyzer')) {
    if (!store.getters['configuration/isGAISSAROIAnalyzerEnabled']) {
      next({ name: 'home' });
      return;
    }
  }

  next();
});

export default router
