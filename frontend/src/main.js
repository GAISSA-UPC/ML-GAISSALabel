import '@/assets/base.css'
import '@/assets/common.scss'

import { createApp } from 'vue'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

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
import { fas } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Font Awesome: Llibreria d'icones, importem els tipus de icones que farem servir
library.add(fas);

const app = createApp(App)

// Register Element Plus components
elcomponents.forEach(component => {
    app.component(component.name, component)
})  

router.beforeEach((to, from, next) => {
    const isAuthenticated = store.getters.isLogged;

    if (to.matched.some((record) => record.meta.requiresAuth)) {
        if (!isAuthenticated) {
            next({name: 'Admin login'}); // Redirect to login page if not authenticated
        } else {
            next();
        }
    } else {
        next();
    }
});

const vuetify = createVuetify({
    components,
    directives,
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
