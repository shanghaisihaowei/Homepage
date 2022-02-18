import { createI18n } from 'vue-i18n'
import messages from 'src/i18n'
import { Cookies } from 'quasar'

const i18n = new createI18n({
    messages,
    warnHtmlInMessage: 'off' // disable of the Detected HTML in message
})

export default ({ app, ssrContext }) => {
    const cookies = process.env.SERVER
        ? Cookies.parseSSR(ssrContext)
        : Cookies

    var lang = cookies.get('lang')
    if (lang) {
        lang = lang || 'en-US'
    } else {
        cookies.set('lang', 'zh-hans')
        lang = 'zh-hans'
    }
    i18n.global.locale = lang
    i18n.global.fallbackLocale = lang
    app.use(i18n)
}

export { i18n }
