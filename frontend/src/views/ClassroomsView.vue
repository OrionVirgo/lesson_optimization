<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { Building2, Plus, Trash2, Edit2, FlaskConical } from 'lucide-vue-next'
import { ClassroomService, type Classroom } from '../services/api'

const { t } = useI18n()

const classrooms = ref<Classroom[]>([])
const isModalOpen = ref(false)
const editingClassroom = ref<Classroom | null>(null)

const formData = ref<Classroom>({
  name: '',
  building_wing: 'Ana Bina',
  capacity: 40,
  is_lab: false
})

const fetchClassrooms = async () => {
  try {
    classrooms.value = await ClassroomService.getAll()
  } catch (err) {
    console.error('Error fetching classrooms:', err)
  }
}

const openModal = (c?: Classroom) => {
  if (c) {
    editingClassroom.value = c
    formData.value = { ...c }
  } else {
    editingClassroom.value = null
    formData.value = { name: '', building_wing: 'Ana Bina', capacity: 40, is_lab: false }
  }
  isModalOpen.value = true
}

const closeModal = () => { isModalOpen.value = false }

const saveClassroom = async () => {
  if (!formData.value.name) return
  try {
    if (editingClassroom.value?.id) {
      await ClassroomService.update(editingClassroom.value.id, formData.value)
    } else {
      await ClassroomService.create(formData.value)
    }
    await fetchClassrooms()
    closeModal()
  } catch (err) {
    console.error('Save classroom error:', err)
  }
}

const deleteClassroom = async (id?: number) => {
  if (!id || !confirm(t('actions.confirm'))) return
  try {
    await ClassroomService.delete(id)
    await fetchClassrooms()
  } catch (err) {
    console.error('Delete classroom error:', err)
  }
}

onMounted(() => { fetchClassrooms() })
</script>

<template>
  <div class="space-y-6">
    <div class="glass-panel p-6 rounded-2xl flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold font-heading text-slate-100 flex items-center gap-3">
          <Building2 class="w-7 h-7 text-indigo-400" />
          {{ t('classrooms.title') }}
        </h1>
        <p class="text-xs text-slate-400 mt-1">Derslikler, amfiler ve laboratuvar tanımları</p>
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
            <th class="py-4 px-6">{{ t('classrooms.name') }}</th>
            <th class="py-4 px-6">{{ t('classrooms.building') }}</th>
            <th class="py-4 px-6">{{ t('classrooms.capacity') }}</th>
            <th class="py-4 px-6">{{ t('classrooms.isLab') }}</th>
            <th class="py-4 px-6 text-right">{{ t('teachers.actions') }}</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800/60">
          <tr v-for="c in classrooms" :key="c.id" class="hover:bg-slate-900/40 transition-colors">
            <td class="py-4 px-6 font-semibold text-slate-100">{{ c.name }}</td>
            <td class="py-4 px-6 text-slate-400">{{ c.building_wing || '-' }}</td>
            <td class="py-4 px-6 text-indigo-300 font-mono">{{ c.capacity || 30 }} Kişi</td>
            <td class="py-4 px-6">
              <span v-if="c.is_lab" class="px-2.5 py-1 rounded-full text-xs font-semibold bg-purple-500/10 text-purple-400 border border-purple-500/30 flex items-center gap-1.5 w-max">
                <FlaskConical class="w-3.5 h-3.5" /> Laboratuvar
              </span>
              <span v-else class="text-xs text-slate-500">Standart Derslik</span>
            </td>
            <td class="py-4 px-6 text-right space-x-2">
              <button @click="openModal(c)" class="p-2 text-slate-400 hover:text-indigo-400 hover:bg-slate-800 rounded-lg"><Edit2 class="w-4 h-4" /></button>
              <button @click="deleteClassroom(c.id)" class="p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg"><Trash2 class="w-4 h-4" /></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="glass-panel w-full max-w-md rounded-2xl p-6 space-y-4 border border-slate-800">
        <h3 class="text-lg font-bold text-slate-100">{{ editingClassroom ? t('actions.edit') : t('actions.add') }} {{ t('classrooms.name') }}</h3>
        <div class="space-y-3">
          <div>
            <label class="text-xs text-slate-400 block mb-1">{{ t('classrooms.name') }}</label>
            <input v-model="formData.name" type="text" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200" />
          </div>
          <div>
            <label class="text-xs text-slate-400 block mb-1">{{ t('classrooms.capacity') }}</label>
            <input v-model.number="formData.capacity" type="number" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200" />
          </div>
          <div class="flex items-center gap-2 pt-2">
            <input v-model="formData.is_lab" type="checkbox" id="is_lab" class="rounded bg-slate-950 border-slate-800 text-indigo-600" />
            <label for="is_lab" class="text-xs text-slate-300">{{ t('classrooms.isLab') }}</label>
          </div>
        </div>
        <div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
          <button @click="closeModal()" class="px-4 py-2 rounded-xl text-slate-400 bg-slate-800">{{ t('actions.cancel') }}</button>
          <button @click="saveClassroom()" class="gradient-btn px-5 py-2 rounded-xl text-white">{{ t('actions.save') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>
