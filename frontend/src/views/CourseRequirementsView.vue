<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { FileSpreadsheet, Plus, Trash2, Edit2 } from 'lucide-vue-next'
import { 
  RequirementService, 
  ClassService, 
  CourseService, 
  TeacherService,
  type CourseRequirement, 
  type SchoolClass, 
  type Course, 
  type Teacher 
} from '../services/api'

const { t } = useI18n()

const requirements = ref<CourseRequirement[]>([])
const classes = ref<SchoolClass[]>([])
const courses = ref<Course[]>([])
const teachers = ref<Teacher[]>([])

const isModalOpen = ref(false)
const editingReq = ref<CourseRequirement | null>(null)

const formData = ref<CourseRequirement>({
  school_class: 0,
  course: 0,
  teacher: 0,
  weekly_hours: 2
})

const fetchData = async () => {
  try {
    const [rData, cData, crsData, tData] = await Promise.all([
      RequirementService.getAll(),
      ClassService.getAll(),
      CourseService.getAll(),
      TeacherService.getAll()
    ])
    requirements.value = rData
    classes.value = cData
    courses.value = crsData
    teachers.value = tData
  } catch (err) {
    console.error('Error fetching requirements:', err)
  }
}

const openModal = (req?: CourseRequirement) => {
  if (req) {
    editingReq.value = req
    formData.value = {
      school_class: typeof req.school_class === 'object' ? (req.school_class as any).id : req.school_class,
      course: typeof req.course === 'object' ? (req.course as any).id : req.course,
      teacher: typeof req.teacher === 'object' ? (req.teacher as any).id : req.teacher,
      weekly_hours: req.weekly_hours
    }
  } else {
    editingReq.value = null
    formData.value = {
      school_class: classes.value[0]?.id || 0,
      course: courses.value[0]?.id || 0,
      teacher: teachers.value[0]?.id || 0,
      weekly_hours: 2
    }
  }
  isModalOpen.value = true
}

const closeModal = () => { isModalOpen.value = false }

const saveRequirement = async () => {
  try {
    if (editingReq.value?.id) {
      await RequirementService.update(editingReq.value.id, formData.value)
    } else {
      await RequirementService.create(formData.value)
    }
    await fetchData()
    closeModal()
  } catch (err) {
    console.error('Save requirement error:', err)
  }
}

const deleteRequirement = async (id?: number) => {
  if (!id || !confirm(t('actions.confirm'))) return
  try {
    await RequirementService.delete(id)
    await fetchData()
  } catch (err) {
    console.error('Delete requirement error:', err)
  }
}

onMounted(() => { fetchData() })
</script>

<template>
  <div class="space-y-6">
    <div class="glass-panel p-6 rounded-2xl flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold font-heading text-slate-100 flex items-center gap-3">
          <FileSpreadsheet class="w-7 h-7 text-indigo-400" />
          {{ t('requirements.title') }}
        </h1>
        <p class="text-xs text-slate-400 mt-1">Sınıf, ders ve öğretmen atama kısıtlamaları</p>
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
            <th class="py-4 px-6">{{ t('requirements.schoolClass') }}</th>
            <th class="py-4 px-6">{{ t('requirements.course') }}</th>
            <th class="py-4 px-6">{{ t('requirements.teacher') }}</th>
            <th class="py-4 px-6">{{ t('requirements.weeklyHours') }}</th>
            <th class="py-4 px-6 text-right">{{ t('teachers.actions') }}</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800/60">
          <tr v-for="req in requirements" :key="req.id" class="hover:bg-slate-900/40 transition-colors">
            <td class="py-4 px-6 font-semibold text-slate-100">
              {{ typeof req.school_class === 'object' ? (req.school_class as any).name : (req.school_class_name || req.school_class) }}
            </td>
            <td class="py-4 px-6 text-indigo-300 font-medium">
              {{ typeof req.course === 'object' ? (req.course as any).name : (req.course_name || req.course) }}
            </td>
            <td class="py-4 px-6 text-purple-300">
              {{ typeof req.teacher === 'object' ? (req.teacher as any).name : (req.teacher_name || req.teacher) }}
            </td>
            <td class="py-4 px-6 font-mono text-emerald-400 font-bold">
              {{ req.weekly_hours }} Saat / Hafta
            </td>
            <td class="py-4 px-6 text-right space-x-2">
              <button @click="openModal(req)" class="p-2 text-slate-400 hover:text-indigo-400 hover:bg-slate-800 rounded-lg"><Edit2 class="w-4 h-4" /></button>
              <button @click="deleteRequirement(req.id)" class="p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg"><Trash2 class="w-4 h-4" /></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="glass-panel w-full max-w-md rounded-2xl p-6 space-y-4 border border-slate-800">
        <h3 class="text-lg font-bold text-slate-100">{{ editingReq ? t('actions.edit') : t('actions.add') }} {{ t('requirements.title') }}</h3>
        <div class="space-y-3">
          <div>
            <label class="text-xs text-slate-400 block mb-1">{{ t('requirements.schoolClass') }}</label>
            <select v-model="formData.school_class" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200">
              <option v-for="c in classes" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>

          <div>
            <label class="text-xs text-slate-400 block mb-1">{{ t('requirements.course') }}</label>
            <select v-model="formData.course" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200">
              <option v-for="crs in courses" :key="crs.id" :value="crs.id">{{ crs.name }}</option>
            </select>
          </div>

          <div>
            <label class="text-xs text-slate-400 block mb-1">{{ t('requirements.teacher') }}</label>
            <select v-model="formData.teacher" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200">
              <option v-for="tItem in teachers" :key="tItem.id" :value="tItem.id">{{ tItem.name }}</option>
            </select>
          </div>

          <div>
            <label class="text-xs text-slate-400 block mb-1">{{ t('requirements.weeklyHours') }}</label>
            <input v-model.number="formData.weekly_hours" type="number" min="1" max="15" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200" />
          </div>
        </div>

        <div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
          <button @click="closeModal()" class="px-4 py-2 rounded-xl text-slate-400 bg-slate-800">{{ t('actions.cancel') }}</button>
          <button @click="saveRequirement()" class="gradient-btn px-5 py-2 rounded-xl text-white">{{ t('actions.save') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>
