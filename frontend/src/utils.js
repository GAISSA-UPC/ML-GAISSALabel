import {i18n} from '@/i18n'

function formatData(dataString) {
    if (dataString) {
        const data = new Date(dataString)
        const format = {
            day: 'numeric',
            month: 'long',
            year: 'numeric',
            hour: 'numeric',
            minute: 'numeric'
        }
        return data.toLocaleString(i18n.locale, format)
    }
    else {
        return i18n.global.t("Sense data assignada")
    }
}

export {formatData}