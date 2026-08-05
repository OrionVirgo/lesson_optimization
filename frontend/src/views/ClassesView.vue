<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { School, Plus, Trash2, Edit2 } from 'lucide-vue-next'
import { ClassService, type SchoolClass } from '../services/api'

const { t } = useI18n()

const classes = ref<SchoolClass[]>([])
const isModalOpen = ref(false)
const editingClass = ref<SchoolClass | null>(null)

const formData = ref<SchoolClass>({
  name: '',
  grade_level: 1,
  student_count: 30
})

const fetchClasses = async () => {
  try {
    classes.value = await ClassService.getAll()
  } catch (err) {
    console.error('Error fetching classes:', err)
  }
}

const openModal = (cls?: SchoolClass) => {
  if (cls) {
    editingClass.value = cls
    formData.value = { ...cls }
  } else {
    editingClass.value = null
    formData.value = { name: '', grade_level: 1, student_count: 30 }
  }
  isModalOpen.value = true
}

const closeModal = () => { isModalOpen.value = false }

const saveClass = async () => {
  if (!formData.value.name) return
  try {
    if (editingClass.value?.id) {
      await ClassService.update(editingClass.value.id, formData.value)
    } else {
      await ClassService.create(formData.value)
    }
    await fetchClasses()
    closeModal()
  } catch (err) {
    console.error('Save class error:', err)
  }
}

const deleteClass = async (id?: number) => {
  if (!id || !confirm(t('actions.confirm'))) return
  try {
    await ClassService.delete(id)
    await fetchClasses()
  } catch (err) {
    console.error('Delete class error:', err)
  }
}

onMounted(() => { fetchClasses() })
</script>

<template>
  <div class="space-y-6">
    <div class="glass-panel p-6 rounded-2xl flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold font-heading text-slate-100 flex items-center gap-3">
          <School class="w-7 h-7 text-indigo-400" />
          {{ t('classes.title') }}
        </h1>
        <p class="text-xs text-slate-400 mt-1">Okul şubeleri ve öğrenci kapasiteleri</p>
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
            <th class="py-4 px-6">{{ t('classes.name') }}</th>
            <th class="py-4 px-6">{{ t('classes.gradeLevel') }}</th>
            <th class="py-4 px-6">{{ t('classes.studentCount') }}</th>
            <th class="py-4 px-6 text-right">{{ t('teachers.actions') }}</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800/60">
          <tr v-for="cls in classes" :key="cls.id" class="hover:bg-slate-900/40 transition-colors">
            <td class="py-4 px-6 font-semibold text-slate-100">{{ cls.name }}</td>
            <td class="py-4 px-6 text-indigo-300 font-mono">{{ cls.grade_level }}. Sınıf</td>
            <td class="py-4 px-6 text-slate-300">{{ cls.student_count || 0 }} Öğrenci</td>
            <td class="py-4 px-6 text-right space-x-2">
              <button @click="openModal(cls)" class="p-2 text-slate-400 hover:text-indigo-400 hover:bg-slate-800 rounded-lg"><Edit2 class="w-4 h-4" /></button>
              <button @click="deleteClass(cls.id)" class="p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg"><Trash2 class="w-4 h-4" /></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="glass-panel w-full max-w-md rounded-2xl p-6 space-y-4 border border-slate-800">
        <h3 class="text-lg font-bold text-slate-100">{{ editingClass ? t('actions.edit') : t('actions.add') }} {{ t('classes.name') }}</h3>
        <div class="space-y-3">
          <div>
            <label class="text-xs text-slate-400 block mb-1">{{ t('classes.name') }}</label>
            <input v-model="formData.name" type="text" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200" />
          </div>
          <div>
            <label class="text-xs text-slate-400 block mb-1">{{ t('classes.gradeLevel') }}</label>
            <input v-model.number="formData.grade_level" type="number" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200" />
          </div>
        </div>
        <div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
          <button @click="closeModal()" class="px-4 py-2 rounded-xl text-slate-400 bg-slate-800">{{ t('actions.cancel') }}</button>
          <button @click="saveClass()" class="gradient-btn px-5 py-2 rounded-xl text-white">{{ t('actions.save') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>
