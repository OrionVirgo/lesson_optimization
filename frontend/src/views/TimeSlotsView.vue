<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { Clock, Plus, Trash2, Edit2 } from 'lucide-vue-next'
import { TimeSlotService, type TimeSlot } from '../services/api'

const { t } = useI18n()

const timeSlots = ref<TimeSlot[]>([])
const isModalOpen = ref(false)
const editingSlot = ref<TimeSlot | null>(null)

const formData = ref<TimeSlot>({
  day: 'Pazartesi',
  hour: 1,
  time_range_str: '09:00 - 09:45'
})

const days = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']

const fetchSlots = async () => {
  try {
    timeSlots.value = await TimeSlotService.getAll()
  } catch (err) {
    console.error('Error fetching time slots:', err)
  }
}

const openModal = (ts?: TimeSlot) => {
  if (ts) {
    editingSlot.value = ts
    formData.value = { ...ts }
  } else {
    editingSlot.value = null
    formData.value = { day: 'Pazartesi', hour: 1, time_range_str: '09:00 - 09:45' }
  }
  isModalOpen.value = true
}

const closeModal = () => { isModalOpen.value = false }

const saveSlot = async () => {
  try {
    if (editingSlot.value?.id) {
      await TimeSlotService.update(editingSlot.value.id, formData.value)
    } else {
      await TimeSlotService.create(formData.value)
    }
    await fetchSlots()
    closeModal()
  } catch (err) {
    console.error('Save slot error:', err)
  }
}

const deleteSlot = async (id?: number) => {
  if (!id || !confirm(t('actions.confirm'))) return
  try {
    await TimeSlotService.delete(id)
    await fetchSlots()
  } catch (err) {
    console.error('Delete slot error:', err)
  }
}

onMounted(() => { fetchSlots() })
</script>

<template>
  <div class="space-y-6">
    <div class="glass-panel p-6 rounded-2xl flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold font-heading text-slate-100 flex items-center gap-3">
          <Clock class="w-7 h-7 text-indigo-400" />
          {{ t('timeslots.title') }}
        </h1>
        <p class="text-xs text-slate-400 mt-1">Haftalık ders gün ve saat dilimleri</p>
      </div>

      <button @click="openModal()" class="gradient-btn flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold text-white hover:scale-105 transition-all">
        <Plus class="w-4 h-4" />
        <span>{{ t('actions.add') }}</span>
      </button>
    </div>

    <div class="glass-panel rounded-2xl overflow-hidden border border-slate-800 shadow-xl">
      <table class="w-full text-left border-collapse text-sm">
        <thead>
          <tr class="bg-slate-900/90 text-slate-400 text-xs uppercase border-b border-slate-800">
            <th class="py-4 px-6">{{ t('timeslots.day') }}</th>
            <th class="py-4 px-6">{{ t('timeslots.hour') }}</th>
            <th class="py-4 px-6">{{ t('timeslots.timeRange') }}</th>
            <th class="py-4 px-6 text-right">{{ t('teachers.actions') }}</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800/60">
          <tr v-for="ts in timeSlots" :key="ts.id" class="hover:bg-slate-900/40 transition-colors">
            <td class="py-4 px-6 font-semibold text-slate-100">{{ ts.day }}</td>
            <td class="py-4 px-6 font-mono text-indigo-300">{{ ts.hour }}. Ders Saati</td>
            <td class="py-4 px-6 text-slate-400 font-mono text-xs">{{ ts.time_range_str || `${8 + ts.hour}:00 - ${8 + ts.hour}:45` }}</td>
            <td class="py-4 px-6 text-right space-x-2">
              <button @click="openModal(ts)" class="p-2 text-slate-400 hover:text-indigo-400 hover:bg-slate-800 rounded-lg"><Edit2 class="w-4 h-4" /></button>
              <button @click="deleteSlot(ts.id)" class="p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg"><Trash2 class="w-4 h-4" /></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="glass-panel w-full max-w-md rounded-2xl p-6 space-y-4 border border-slate-800">
        <h3 class="text-lg font-bold text-slate-100">{{ editingSlot ? t('actions.edit') : t('actions.add') }} {{ t('timeslots.title') }}</h3>
        <div class="space-y-3">
          <div>
            <label class="text-xs text-slate-400 block mb-1">{{ t('timeslots.day') }}</label>
            <select v-model="formData.day" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200">
              <option v-for="d in days" :key="d" :value="d">{{ d }}</option>
            </select>
          </div>
          <div>
            <label class="text-xs text-slate-400 block mb-1">{{ t('timeslots.hour') }}</label>
            <input v-model.number="formData.hour" type="number" min="1" max="10" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200" />
          </div>
        </div>
        <div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
          <button @click="closeModal()" class="px-4 py-2 rounded-xl text-slate-400 bg-slate-800">{{ t('actions.cancel') }}</button>
          <button @click="saveSlot()" class="gradient-btn px-5 py-2 rounded-xl text-white">{{ t('actions.save') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>
