import '@/assets/base.css'
import '@/assets/common.scss'

import { createApp } from 'vue'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'


import App from './App.vue'
import router from './router'
import store from './store'
import {i18n} from './i18n.js'

// ElementPlus Components 
import {
    // Layout
    ElContainer,
    ElHeader,
    ElAside,
    ElMain,
    
    // Form
    ElInput,
    ElFormItem,
    ElButton,
    ElUpload,
    ElSelect,
    ElOption,
    ElInputNumber,
    
    // Data
    ElDescriptions,
    ElDescriptionsItem,
    
    // Navigation
    ElMenu,
    ElMenuItem,
    ElSubMenu,
    
    // Feedback
    ElAlert,
    ElDialog,
    
    // Basic
    ElRow,
    ElCol,
    ElCard,
    ElImage,
    ElIcon,
    ElSlider,
    
    // Config Provider
    ElConfigProvider
} from 'element-plus'
  
const elcomponents = [
    ElContainer, ElHeader, ElAside, ElMain,
    ElInput, ElFormItem, ElButton, ElUpload, ElSelect, ElOption, ElInputNumber,
    ElDescriptions, ElDescriptionsItem,
    ElMenu, ElMenuItem, ElSubMenu,
    ElAlert, ElDialog,
    ElRow, ElCol, ElCard, ElImage, ElIcon, ElSlider,
    ElConfigProvider
]  

// Font Awesome: Llibreria d'icones, importem els tipus de icones que farem servir
import { library } from '@fortawesome/fontawesome-svg-core';
import { faBars, faHome, faTag, faDumbbell, faBullseye, faChartLine, faPeopleGroup, faCloudArrowUp, faPlus,
    faIdCardClip, faUser, faCircleInfo, faCalendarDays, faPenToSquare, faTrash, faCloud, faArrowRight,
    faLeaf, faSeedling, faDownLong, faEquals, faUpLong, faFilePdf, faLightbulb, faBrain, faRocket, faScrewdriverWrench
 } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Font Awesome: Llibreria d'icones, importem els tipus de icones que farem servir
library.add(
    faBars, faHome, faTag, faDumbbell, faBullseye, faChartLine, faPeopleGroup, faCloudArrowUp, faPlus,
    faIdCardClip, faUser, faCircleInfo, faCalendarDays, faPenToSquare, faTrash, faCloud, faArrowRight,
    faLeaf, faSeedling, faDownLong, faEquals, faUpLong, faFilePdf, faLightbulb, faBrain, faRocket, faScrewdriverWrench
);

const app = createApp(App)

// Register Element Plus components
elcomponents.forEach(component => {
    app.component(component.name, component)
})  

const vuetify = createVuetify({

})
app.use(vuetify)

// Router: Definició de les rutes de la single page application
app.use(router)

// Store: Variables que es conserven durant les vistes
app.use(store)

// i18n: Llibreria per traduir, fent servir $t('...') en les templates
app.use(i18n)

app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')
