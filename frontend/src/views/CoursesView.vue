<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { BookOpen, Plus, Trash2, Edit2, FlaskConical } from 'lucide-vue-next'
import { CourseService, type Course } from '../services/api'

const { t } = useI18n()

const courses = ref<Course[]>([])
const isModalOpen = ref(false)
const editingCourse = ref<Course | null>(null)

const formData = ref<Course>({
  code: '',
  name: '',
  is_lab_required: false
})

const fetchCourses = async () => {
  try {
    courses.value = await CourseService.getAll()
  } catch (err) {
    console.error('Error fetching courses:', err)
  }
}

const openModal = (course?: Course) => {
  if (course) {
    editingCourse.value = course
    formData.value = { ...course }
  } else {
    editingCourse.value = null
    formData.value = { code: '', name: '', is_lab_required: false }
  }
  isModalOpen.value = true
}

const closeModal = () => { isModalOpen.value = false }

const saveCourse = async () => {
  if (!formData.value.name) return
  try {
    if (editingCourse.value?.id) {
      await CourseService.update(editingCourse.value.id, formData.value)
    } else {
      await CourseService.create(formData.value)
    }
    await fetchCourses()
    closeModal()
  } catch (err) {
    console.error('Save course error:', err)
  }
}

const deleteCourse = async (id?: number) => {
  if (!id || !confirm(t('actions.confirm'))) return
  try {
    await CourseService.delete(id)
    await fetchCourses()
  } catch (err) {
    console.error('Delete course error:', err)
  }
}

onMounted(() => { fetchCourses() })
</script>

<template>
  <div class="space-y-6">
    <div class="glass-panel p-6 rounded-2xl flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold font-heading text-slate-100 flex items-center gap-3">
          <BookOpen class="w-7 h-7 text-indigo-400" />
          {{ t('courses.title') }}
        </h1>
        <p class="text-xs text-slate-400 mt-1">Müfredat dersleri ve laboratuvar kısıtları</p>
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
            <th class="py-4 px-6">{{ t('courses.code') }}</th>
            <th class="py-4 px-6">{{ t('courses.name') }}</th>
            <th class="py-4 px-6">{{ t('courses.isLabRequired') }}</th>
            <th class="py-4 px-6 text-right">{{ t('teachers.actions') }}</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800/60">
          <tr v-for="c in courses" :key="c.id" class="hover:bg-slate-900/40 transition-colors">
            <td class="py-4 px-6 font-mono text-indigo-400 font-bold">{{ c.code || 'DERS-' + c.id }}</td>
            <td class="py-4 px-6 font-semibold text-slate-100">{{ c.name }}</td>
            <td class="py-4 px-6">
              <span v-if="c.is_lab_required" class="px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/30 flex items-center gap-1.5 w-max">
                <FlaskConical class="w-3.5 h-3.5" /> {{ t('timetable.labRequired') }}
              </span>
              <span v-else class="text-xs text-slate-500">Standart Sınıf</span>
            </td>
            <td class="py-4 px-6 text-right space-x-2">
              <button @click="openModal(c)" class="p-2 text-slate-400 hover:text-indigo-400 hover:bg-slate-800 rounded-lg"><Edit2 class="w-4 h-4" /></button>
              <button @click="deleteCourse(c.id)" class="p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg"><Trash2 class="w-4 h-4" /></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="glass-panel w-full max-w-md rounded-2xl p-6 space-y-4 border border-slate-800">
        <h3 class="text-lg font-bold text-slate-100">{{ editingCourse ? t('actions.edit') : t('actions.add') }} {{ t('courses.name') }}</h3>
        <div class="space-y-3">
          <div>
            <label class="text-xs text-slate-400 block mb-1">{{ t('courses.code') }}</label>
            <input v-model="formData.code" type="text" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200" />
          </div>
          <div>
            <label class="text-xs text-slate-400 block mb-1">{{ t('courses.name') }}</label>
            <input v-model="formData.name" type="text" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200" />
          </div>
          <div class="flex items-center gap-2 pt-2">
            <input v-model="formData.is_lab_required" type="checkbox" id="is_lab_required" class="rounded bg-slate-950 border-slate-800 text-indigo-600" />
            <label for="is_lab_required" class="text-xs text-slate-300">{{ t('courses.isLabRequired') }}</label>
          </div>
        </div>
        <div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
          <button @click="closeModal()" class="px-4 py-2 rounded-xl text-slate-400 bg-slate-800">{{ t('actions.cancel') }}</button>
          <button @click="saveCourse()" class="gradient-btn px-5 py-2 rounded-xl text-white">{{ t('actions.save') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>
