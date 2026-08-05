<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { Sparkles, X, Send, Bot, User, AlertCircle, HelpCircle } from 'lucide-vue-next'
import { AIChatService } from '../services/api'

const props = defineProps<{ isOpen: boolean }>()
const emit = defineEmits(['close'])

const { t } = useI18n()

interface ChatMessage {
  role: 'user' | 'model'
  text: string
}

const userPrompt = ref('')
const isLoading = ref(false)
const messages = ref<ChatMessage[]>([
  {
    role: 'model',
    text: 'Merhaba! Ben Ders Programı Yapay Zeka Asistanınız. Derslik kapasiteleri, öğretmen izin günleri, çakışma nedenleri veya boş zaman dilimleri hakkında bana her türlü soruyu sorabilirsiniz.'
  }
])

const chatContainer = ref<HTMLElement | null>(null)

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

const sendMessage = async (textToSend?: string) => {
  const query = textToSend || userPrompt.value.trim()
  if (!query || isLoading.value) return

  messages.value.push({ role: 'user', text: query })
  if (!textToSend) userPrompt.value = ''
  isLoading.value = true
  scrollToBottom()

  try {
    const history = messages.value.slice(0, -1)
    const data = await AIChatService.sendMessage(query, history)
    messages.value.push({
      role: 'model',
      text: data.response || 'Bir yanıt alınamadı.'
    })
  } catch (err: any) {
    messages.value.push({
      role: 'model',
      text: '⚠️ Yapay zeka yanıt verirken bir bağlantı hatası oluştu.'
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

const sendQuickQuestion = (key: string) => {
  const qText = t(`ai.${key}`)
  sendMessage(qText)
}

watch(() => props.isOpen, (newVal) => {
  if (newVal) scrollToBottom()
})
</script>

<template>
  <!-- Backdrop -->
  <div 
    v-if="isOpen" 
    @click="emit('close')"
    class="fixed inset-0 bg-slate-950/60 backdrop-blur-sm z-50 transition-opacity no-print"
  ></div>

  <!-- Drawer Panel -->
  <div 
    :class="[
      'fixed right-0 top-0 bottom-0 w-full sm:w-[480px] bg-slate-900 border-l border-slate-800 shadow-2xl z-50 flex flex-col transition-transform duration-300 ease-in-out no-print',
      isOpen ? 'translate-x-0' : 'translate-x-full'
    ]"
  >
    <!-- Header -->
    <div class="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/90">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl gradient-btn flex items-center justify-center text-white shadow-lg shadow-indigo-500/20">
          <Sparkles class="w-5 h-5 text-amber-300 animate-pulse" />
        </div>
        <div>
          <h3 class="font-bold font-heading text-slate-100 flex items-center gap-2">
            {{ t('ai.title') }}
            <span class="text-[10px] px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 font-mono uppercase">
              Gemini 2.0
            </span>
          </h3>
          <p class="text-xs text-slate-400">Tool Calling & Conflict Analyzer</p>
        </div>
      </div>

      <button 
        @click="emit('close')"
        class="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
      >
        <X class="w-5 h-5" />
      </button>
    </div>

    <!-- Quick Prompts Section -->
    <div class="px-6 py-3 border-b border-slate-800/60 bg-slate-950/40">
      <p class="text-xs text-slate-400 mb-2 flex items-center gap-1 font-medium">
        <HelpCircle class="w-3.5 h-3.5 text-indigo-400" />
        {{ t('ai.quickQuestions') }}
      </p>
      <div class="flex flex-wrap gap-2">
        <button 
          @click="sendQuickQuestion('q1')"
          class="text-xs px-2.5 py-1 rounded-lg bg-slate-800/80 border border-slate-700/80 text-slate-300 hover:text-white hover:border-indigo-500/50 transition-all text-left"
        >
          ⚡ {{ t('ai.q1') }}
        </button>
        <button 
          @click="sendQuickQuestion('q2')"
          class="text-xs px-2.5 py-1 rounded-lg bg-slate-800/80 border border-slate-700/80 text-slate-300 hover:text-white hover:border-indigo-500/50 transition-all text-left"
        >
          🏢 {{ t('ai.q2') }}
        </button>
        <button 
          @click="sendQuickQuestion('q3')"
          class="text-xs px-2.5 py-1 rounded-lg bg-slate-800/80 border border-slate-700/80 text-slate-300 hover:text-white hover:border-indigo-500/50 transition-all text-left"
        >
          📊 {{ t('ai.q3') }}
        </button>
      </div>
    </div>

    <!-- Chat Messages Stream -->
    <div ref="chatContainer" class="flex-1 p-6 overflow-y-auto space-y-4">
      <div 
        v-for="(msg, idx) in messages" 
        :key="idx"
        :class="[
          'flex gap-3 text-sm animate-fade-in',
          msg.role === 'user' ? 'justify-end' : 'justify-start'
        ]"
      >
        <div v-if="msg.role === 'model'" class="w-8 h-8 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center shrink-0 text-indigo-400">
          <Bot class="w-4 h-4" />
        </div>

        <div 
          :class="[
            'max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap',
            msg.role === 'user' 
              ? 'gradient-btn text-white shadow-md rounded-br-none' 
              : 'bg-slate-800/90 border border-slate-700/70 text-slate-200 shadow-md rounded-bl-none'
          ]"
        >
          {{ msg.text }}
        </div>

        <div v-if="msg.role === 'user'" class="w-8 h-8 rounded-lg bg-purple-600/20 border border-purple-500/30 flex items-center justify-center shrink-0 text-purple-400">
          <User class="w-4 h-4" />
        </div>
      </div>

      <!-- Loading Indicator -->
      <div v-if="isLoading" class="flex gap-3 text-sm animate-pulse">
        <div class="w-8 h-8 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
          <Bot class="w-4 h-4" />
        </div>
        <div class="bg-slate-800/80 border border-slate-700 px-4 py-3 rounded-2xl text-slate-400 text-xs flex items-center gap-2">
          <Sparkles class="w-4 h-4 text-amber-400 animate-spin" />
          <span>{{ t('ai.sending') }}</span>
        </div>
      </div>
    </div>

    <!-- Input Form -->
    <div class="p-4 border-t border-slate-800 bg-slate-900">
      <form @submit.prevent="sendMessage()" class="flex items-center gap-2">
        <input 
          v-model="userPrompt"
          type="text"
          :placeholder="t('ai.placeholder')"
          :disabled="isLoading"
          class="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
        />
        <button 
          type="submit"
          :disabled="isLoading || !userPrompt.trim()"
          class="gradient-btn p-2.5 rounded-xl text-white disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          <Send class="w-4 h-4" />
        </button>
      </form>
    </div>

  </div>
</template>
