<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { 
  Calendar, 
  Users, 
  School, 
  Building2, 
  BookOpen, 
  Clock, 
  FileSpreadsheet, 
  Sparkles, 
  Globe 
} from 'lucide-vue-next'

const { locale, t } = useI18n()
const route = useRoute()
const emit = defineEmits(['toggle-ai'])

const toggleLanguage = () => {
  locale.value = locale.value === 'tr' ? 'en' : 'tr'
  localStorage.setItem('user_language', locale.value)
}

const navItems = [
  { name: 'nav.dashboard', path: '/', icon: Calendar },
  { name: 'nav.teachers', path: '/teachers', icon: Users },
  { name: 'nav.classes', path: '/classes', icon: School },
  { name: 'nav.classrooms', path: '/classrooms', icon: Building2 },
  { name: 'nav.courses', path: '/courses', icon: BookOpen },
  { name: 'nav.timeslots', path: '/timeslots', icon: Clock },
  { name: 'nav.requirements', path: '/requirements', icon: FileSpreadsheet },
]
</script>

<template>
  <header class="sticky top-0 z-40 bg-slate-900/80 backdrop-blur-md border-b border-slate-800/80 no-print">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        
        <!-- Logo & Branding -->
        <router-link to="/" class="flex items-center gap-3 group">
          <div class="w-10 h-10 rounded-xl gradient-btn flex items-center justify-center text-white font-bold shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition-transform">
            <Calendar class="w-6 h-6" />
          </div>
          <div>
            <span class="text-lg font-bold font-heading gradient-text tracking-wide block leading-tight">
              OptiSchedule AI
            </span>
            <span class="text-xs text-slate-400 font-medium">
              {{ t('app.subtitle') }}
            </span>
          </div>
        </router-link>

        <!-- Navigation Links -->
        <nav class="hidden lg:flex items-center gap-1">
          <router-link 
            v-for="item in navItems" 
            :key="item.path"
            :to="item.path"
            :class="[
              'flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all',
              route.path === item.path 
                ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/30' 
                : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
            ]"
          >
            <component :is="item.icon" class="w-4 h-4" />
            <span>{{ t(item.name) }}</span>
          </router-link>
        </nav>

        <!-- Controls: Language Switcher & AI Launcher -->
        <div class="flex items-center gap-3">
          
          <!-- i18n Language Toggle -->
          <button 
            @click="toggleLanguage"
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/80 text-xs font-semibold text-slate-200 hover:bg-slate-700 transition-colors"
            :title="locale === 'tr' ? 'Switch to English' : 'Türkçe\'ye Geç'"
          >
            <Globe class="w-3.5 h-3.5 text-indigo-400" />
            <span>{{ locale.toUpperCase() }}</span>
          </button>

          <!-- AI Assistant Trigger Button -->
          <button 
            @click="emit('toggle-ai')"
            class="gradient-btn flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold text-white shadow-lg shadow-indigo-500/20 hover:scale-105 active:scale-95 transition-all"
          >
            <Sparkles class="w-4 h-4 animate-pulse text-amber-300" />
            <span>{{ t('nav.aiAssistant') }}</span>
          </button>

        </div>

      </div>
    </div>
  </header>
</template>
