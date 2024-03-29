import '@/assets/base.css'
import '@/assets/common.scss'

import { createApp } from 'vue'
import elementplus from 'element-plus'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import App from './App.vue'
import router from './router'
import store from './store'
import {i18n} from './i18n.js'

import '@fortawesome/fontawesome-free/css/all.css';
import { library } from '@fortawesome/fontawesome-svg-core';
import { far } from '@fortawesome/free-regular-svg-icons';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { fab } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Font Awesome: Llibreria d'icones, importem tots els gratuits.
library.add(far);
library.add(fas);
library.add(fab);

const app = createApp(App)

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

// ElementPlus i Vuetify: Llibreries amb components per facilitar disseny de les templates
app.use(elementplus)

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
