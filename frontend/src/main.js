import '@/assets/base.css'
import '@/assets/common.scss'

import { createApp } from 'vue'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'


import App from './App.vue'
import router from './router'
import store from './store'
import {i18n} from './i18n.js'

// Font Awesome: Llibreria d'icones, importem els tipus de icones que farem servir
import { library } from '@fortawesome/fontawesome-svg-core';
import { faBars, faHome, faTag, faDumbbell, faBullseye, faChartLine, faPeopleGroup, faCloudArrowUp, faPlus,
    faIdCardClip, faUser, faCircleInfo, faCalendarDays, faPenToSquare, faTrash, faCloud, faArrowRight,
    faLeaf, faSeedling, faDownLong, faEquals, faUpLong, faFilePdf, faLightbulb, faBrain, faRocket, 
    faScrewdriverWrench, faChartBar,
 } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Font Awesome: Llibreria d'icones, importem els tipus de icones que farem servir
library.add(
    faBars, faHome, faTag, faDumbbell, faBullseye, faChartLine, faPeopleGroup, faCloudArrowUp, faPlus,
    faIdCardClip, faUser, faCircleInfo, faCalendarDays, faPenToSquare, faTrash, faCloud, faArrowRight,
    faLeaf, faSeedling, faDownLong, faEquals, faUpLong, faFilePdf, faLightbulb, faBrain, faRocket, 
    faScrewdriverWrench, faChartBar
);

const app = createApp(App)

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
