<script setup lang="ts">
import { ref } from 'vue'
import Navbar from './components/Navbar.vue'
import AIAssistantDrawer from './components/AIAssistantDrawer.vue'

const isAIOpen = ref(false)

const toggleAIAssistant = () => {
  isAIOpen.value = !isAIOpen.value
}
</script>

<template>
  <div class="min-h-screen bg-[#090d16] text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
    <!-- Sticky Glass Navbar -->
    <Navbar @toggle-ai="toggleAIAssistant" />

    <!-- Main View Router Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500 no-print">
      <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
        <span>© 2026 Lesson Scheduling & Optimization System. All rights reserved.</span>
        <span class="flex items-center gap-2 text-indigo-400 font-medium">
          Vue 3 + Vite + TypeScript + Gemini AI Powered
        </span>
      </div>
    </footer>

    <!-- Floating AI Drawer Component -->
    <AIAssistantDrawer :is-open="isAIOpen" @close="isAIOpen = false" />
  </div>
</template>
