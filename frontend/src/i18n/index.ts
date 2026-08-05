import { createI18n } from 'vue-i18n'
import tr from './tr'
import en from './en'

const i18n = createI18n({
  legacy: false, // Use Vue 3 Composition API
  locale: localStorage.getItem('user_language') || 'tr',
  fallbackLocale: 'en',
  messages: {
    tr,
    en
  }
})

export default i18n
