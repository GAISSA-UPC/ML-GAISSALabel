import {createI18n} from 'vue-i18n'

const i18n = createI18n({
    locale: 'en',
    messages: {
        en: {}
    },
    missing: (locale, key) => { // For missing translations, return the key itself
        return key
    }
})

export {
    i18n,
}
