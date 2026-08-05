<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { Users, Plus, Trash2, Edit2, Phone, Mail, Calendar, CheckCircle2 } from 'lucide-vue-next'
import { TeacherService, type Teacher } from '../services/api'

const { t } = useI18n()

const teachers = ref<Teacher[]>([])
const isModalOpen = ref(false)
const editingTeacher = ref<Teacher | null>(null)

const formData = ref<Teacher>({
  name: '',
  branch: '',
  academic_title: 'Prof. Dr.',
  off_day: 'Pazartesi',
  phone: '',
  email: ''
})

const days = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']

const fetchTeachers = async () => {
  try {
    teachers.value = await TeacherService.getAll()
  } catch (err) {
    console.error('Error fetching teachers:', err)
  }
}

const openModal = (teacher?: Teacher) => {
  if (teacher) {
    editingTeacher.value = teacher
    formData.value = { ...teacher }
  } else {
    editingTeacher.value = null
    formData.value = {
      name: '',
      branch: '',
      academic_title: 'Prof. Dr.',
      off_day: 'Pazartesi',
      phone: '',
      email: ''
    }
  }
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

const saveTeacher = async () => {
  if (!formData.value.name) return
  try {
    if (editingTeacher.value && editingTeacher.value.id) {
      await TeacherService.update(editingTeacher.value.id, formData.value)
    } else {
      await TeacherService.create(formData.value)
    }
    await fetchTeachers()
    closeModal()
  } catch (err) {
    console.error('Save teacher error:', err)
  }
}

const deleteTeacher = async (id?: number) => {
  if (!id || !confirm(t('actions.confirm'))) return
  try {
    await TeacherService.delete(id)
    await fetchTeachers()
  } catch (err) {
    console.error('Delete teacher error:', err)
  }
}

onMounted(() => {
  fetchTeachers()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="glass-panel p-6 rounded-2xl flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold font-heading text-slate-100 flex items-center gap-3">
          <Users class="w-7 h-7 text-indigo-400" />
          {{ t('teachers.title') }}
        </h1>
        <p class="text-xs text-slate-400 mt-1">Öğretmen profilleri, unvanları ve izin günleri</p>
      </div>

      <button 
        @click="openModal()"
        class="gradient-btn flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 hover:scale-105 transition-all"
      >
        <Plus class="w-4 h-4" />
        <span>{{ t('actions.add') }}</span>
      </button>
    </div>

    <!-- Teachers Table -->
    <div class="glass-panel rounded-2xl overflow-hidden border border-slate-800 shadow-xl">
      <table class="w-full text-left border-collapse text-sm">
        <thead>
          <tr class="bg-slate-900/90 text-slate-400 text-xs uppercase tracking-wider border-b border-slate-800">
            <th class="py-4 px-6">{{ t('teachers.name') }}</th>
            <th class="py-4 px-6">{{ t('teachers.titleBranch') }}</th>
            <th class="py-4 px-6">{{ t('teachers.offDay') }}</th>
            <th class="py-4 px-6">{{ t('teachers.phone') }} / {{ t('teachers.email') }}</th>
            <th class="py-4 px-6 text-right">{{ t('teachers.actions') }}</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800/60">
          <tr v-for="teacher in teachers" :key="teacher.id" class="hover:bg-slate-900/40 transition-colors">
            <td class="py-4 px-6 font-semibold text-slate-100">
              {{ teacher.name }}
            </td>
            <td class="py-4 px-6 text-indigo-300 font-medium">
              {{ teacher.academic_title }} {{ teacher.branch ? `(${teacher.branch})` : '' }}
            </td>
            <td class="py-4 px-6">
              <span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
                {{ teacher.off_day || '-' }}
              </span>
            </td>
            <td class="py-4 px-6 text-xs text-slate-400 space-y-1">
              <div v-if="teacher.phone" class="flex items-center gap-1.5">
                <Phone class="w-3 h-3 text-slate-500" />
                <span>{{ teacher.phone }}</span>
              </div>
              <div v-if="teacher.email" class="flex items-center gap-1.5">
                <Mail class="w-3 h-3 text-slate-500" />
                <span>{{ teacher.email }}</span>
              </div>
            </td>
            <td class="py-4 px-6 text-right space-x-2">
              <button @click="openModal(teacher)" class="p-2 text-slate-400 hover:text-indigo-400 hover:bg-slate-800 rounded-lg transition-colors">
                <Edit2 class="w-4 h-4" />
              </button>
              <button @click="deleteTeacher(teacher.id)" class="p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg transition-colors">
                <Trash2 class="w-4 h-4" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Form -->
    <div v-if="isModalOpen" class="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="glass-panel w-full max-w-md rounded-2xl p-6 space-y-4 border border-slate-800">
        <h3 class="text-lg font-bold font-heading text-slate-100">
          {{ editingTeacher ? t('actions.edit') : t('actions.add') }} {{ t('teachers.name') }}
        </h3>

        <div class="space-y-3">
          <div>
            <label class="text-xs font-medium text-slate-400 block mb-1">{{ t('teachers.name') }}</label>
            <input v-model="formData.name" type="text" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>

          <div>
            <label class="text-xs font-medium text-slate-400 block mb-1">Branş / Bölüm</label>
            <input v-model="formData.branch" type="text" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>

          <div>
            <label class="text-xs font-medium text-slate-400 block mb-1">{{ t('teachers.offDay') }}</label>
            <select v-model="formData.off_day" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none">
              <option v-for="d in days" :key="d" :value="d">{{ d }}</option>
            </select>
          </div>
        </div>

        <div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
          <button @click="closeModal()" class="px-4 py-2 rounded-xl text-sm font-semibold text-slate-400 hover:text-white bg-slate-800">
            {{ t('actions.cancel') }}
          </button>
          <button @click="saveTeacher()" class="gradient-btn px-5 py-2 rounded-xl text-sm font-semibold text-white">
            {{ t('actions.save') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
