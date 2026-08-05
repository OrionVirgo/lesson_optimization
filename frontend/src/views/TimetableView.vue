<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { 
  Calendar, 
  Sparkles, 
  Printer, 
  Filter, 
  CheckCircle2, 
  AlertCircle, 
  BookOpen, 
  User, 
  Building2 
} from 'lucide-vue-next'
import { 
  ScheduleService, 
  ClassService, 
  TeacherService, 
  TimeSlotService,
  type ScheduleEntry, 
  type SchoolClass, 
  type Teacher, 
  type TimeSlot 
} from '../services/api'

const { t } = useI18n()

const schedules = ref<ScheduleEntry[]>([])
const classes = ref<SchoolClass[]>([])
const teachers = ref<Teacher[]>([])
const timeSlots = ref<TimeSlot[]>([])

const selectedClassId = ref<number | string>('')
const selectedTeacherId = ref<number | string>('')

const isGenerating = ref(false)
const notification = ref<{ type: 'success' | 'error'; message: string } | null>(null)

const days = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']
const hours = [1, 2, 3, 4, 5, 6, 7, 8]

const fetchData = async () => {
  try {
    const [sData, cData, tData, tsData] = await Promise.all([
      ScheduleService.getAll(),
      ClassService.getAll(),
      TeacherService.getAll(),
      TimeSlotService.getAll()
    ])
    schedules.value = sData
    classes.value = cData
    teachers.value = tData
    timeSlots.value = tsData
  } catch (err) {
    console.error('Data fetch error:', err)
  }
}

const generateSchedule = async () => {
  isGenerating.value = true
  notification.value = null
  try {
    const res = await ScheduleService.generate()
    notification.value = {
      type: 'success',
      message: `${t('timetable.generatedSuccess')} (${res.count} ders saati atandı).`
    }
    await fetchData()
  } catch (err: any) {
    notification.value = {
      type: 'error',
      message: err.response?.data?.error || t('timetable.generatedError')
    }
  } finally {
    isGenerating.value = false
  }
}

const printSchedule = () => {
  window.print()
}

// Compute filtered matrix entries
const filteredSchedules = computed(() => {
  return schedules.value.filter(s => {
    const scId = typeof s.school_class === 'object' ? s.school_class.id : s.school_class
    const tId = typeof s.teacher === 'object' ? s.teacher.id : s.teacher

    if (selectedClassId.value && scId !== Number(selectedClassId.value)) return false
    if (selectedTeacherId.value && tId !== Number(selectedTeacherId.value)) return false
    return true
  })
})

const getSlotContent = (day: string, hour: number) => {
  return filteredSchedules.value.filter(s => {
    let sDay = ''
    let sHour = 0

    if (typeof s.time_slot === 'object' && s.time_slot !== null) {
      sDay = s.time_slot.day
      sHour = s.time_slot.hour
    } else {
      sDay = s.day || ''
      sHour = s.hour || 0
    }
    return sDay.toLowerCase() === day.toLowerCase() && sHour === hour
  })
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="space-y-6">
    
    <!-- Top Action Banner -->
    <div class="glass-panel p-6 rounded-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold font-heading text-slate-100 flex items-center gap-3">
          <Calendar class="w-7 h-7 text-indigo-400" />
          {{ t('timetable.title') }}
        </h1>
        <p class="text-sm text-slate-400 mt-1">
          {{ t('app.subtitle') }}
        </p>
      </div>

      <div class="flex items-center gap-3 w-full md:w-auto no-print">
        <button 
          @click="generateSchedule"
          :disabled="isGenerating"
          class="gradient-btn flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 hover:scale-105 active:scale-95 disabled:opacity-50 transition-all"
        >
          <Sparkles :class="['w-4 h-4 text-amber-300', isGenerating ? 'animate-spin' : '']" />
          <span>{{ isGenerating ? t('actions.generating') : t('actions.generateSchedule') }}</span>
        </button>

        <button 
          @click="printSchedule"
          class="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-sm font-semibold text-slate-200 hover:bg-slate-700 transition-colors"
        >
          <Printer class="w-4 h-4 text-slate-400" />
          <span>{{ t('actions.print') }}</span>
        </button>
      </div>
    </div>

    <!-- Notification Alert -->
    <div 
      v-if="notification"
      :class="[
        'p-4 rounded-xl flex items-center gap-3 text-sm font-medium border animate-fade-in no-print',
        notification.type === 'success' 
          ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' 
          : 'bg-rose-500/10 border-rose-500/30 text-rose-400'
      ]"
    >
      <CheckCircle2 v-if="notification.type === 'success'" class="w-5 h-5 shrink-0" />
      <AlertCircle v-else class="w-5 h-5 shrink-0" />
      <span>{{ notification.message }}</span>
    </div>

    <!-- Filters Bar -->
    <div class="glass-panel p-4 rounded-xl flex flex-wrap items-center gap-4 no-print">
      <div class="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
        <Filter class="w-4 h-4 text-indigo-400" />
        <span>{{ t('actions.filter') }}:</span>
      </div>

      <!-- Class Filter -->
      <div class="flex items-center gap-2">
        <label class="text-xs text-slate-300 font-medium">{{ t('timetable.selectClass') }}</label>
        <select 
          v-model="selectedClassId"
          class="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:border-indigo-500 focus:outline-none"
        >
          <option value="">{{ t('timetable.allClasses') }}</option>
          <option v-for="c in classes" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>

      <!-- Teacher Filter -->
      <div class="flex items-center gap-2">
        <label class="text-xs text-slate-300 font-medium">{{ t('timetable.selectTeacher') }}</label>
        <select 
          v-model="selectedTeacherId"
          class="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:border-indigo-500 focus:outline-none"
        >
          <option value="">{{ t('timetable.allTeachers') }}</option>
          <option v-for="tItem in teachers" :key="tItem.id" :value="tItem.id">{{ tItem.name }}</option>
        </select>
      </div>
    </div>

    <!-- Timetable Matrix Table -->
    <div class="glass-panel rounded-2xl overflow-hidden shadow-xl border border-slate-800">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-900/90 text-slate-400 text-xs uppercase tracking-wider border-b border-slate-800">
              <th class="py-4 px-4 font-bold text-center w-24 border-r border-slate-800">Saat / Ders</th>
              <th v-for="day in days" :key="day" class="py-4 px-4 font-bold text-center border-r border-slate-800 last:border-r-0">
                {{ day }}
              </th>
            </tr>
          </thead>

          <tbody class="divide-y divide-slate-800/60 text-xs">
            <tr v-for="h in hours" :key="h" class="hover:bg-slate-900/40 transition-colors">
              
              <!-- Hour Column Header -->
              <td class="py-4 px-3 text-center font-bold text-indigo-400 bg-slate-900/50 border-r border-slate-800">
                <div class="text-sm">{{ h }}. Ders</div>
                <div class="text-[10px] text-slate-500 font-mono mt-0.5">
                  {{ 8 + h }}:00 - {{ 8 + h }}:45
                </div>
              </td>

              <!-- Day Columns -->
              <td v-for="day in days" :key="day" class="p-2 border-r border-slate-800/80 last:border-r-0 align-top min-w-[160px] h-24">
                <div class="h-full space-y-2">
                  <div 
                    v-for="entry in getSlotContent(day, h)" 
                    :key="entry.id"
                    class="p-2.5 rounded-xl bg-slate-800/90 border border-indigo-500/30 hover:border-indigo-500/60 shadow-md transition-all space-y-1"
                  >
                    <!-- Course Name & Lab Badge -->
                    <div class="flex items-center justify-between font-bold text-slate-100 text-xs">
                      <span class="flex items-center gap-1.5 text-indigo-300">
                        <BookOpen class="w-3.5 h-3.5 shrink-0" />
                        {{ typeof entry.course === 'object' ? entry.course.name : entry.course_name }}
                      </span>
                    </div>

                    <!-- Teacher Name -->
                    <div class="text-[11px] text-slate-300 flex items-center gap-1">
                      <User class="w-3 h-3 text-purple-400 shrink-0" />
                      <span>{{ typeof entry.teacher === 'object' ? entry.teacher.name : entry.teacher_name }}</span>
                    </div>

                    <!-- Classroom & Class Info -->
                    <div class="flex items-center justify-between text-[10px] text-slate-400 pt-1 border-t border-slate-700/50">
                      <span class="flex items-center gap-1 font-semibold text-emerald-400">
                        <Building2 class="w-3 h-3 shrink-0" />
                        {{ typeof entry.classroom === 'object' ? entry.classroom.name : entry.classroom_name }}
                      </span>
                      <span class="px-1.5 py-0.5 rounded bg-slate-900 text-slate-300 font-mono">
                        {{ typeof entry.school_class === 'object' ? entry.school_class.name : entry.school_class_name }}
                      </span>
                    </div>
                  </div>

                  <!-- Empty Slot Indicator -->
                  <div 
                    v-if="getSlotContent(day, h).length === 0" 
                    class="h-full flex items-center justify-center text-slate-600 text-[11px] font-medium border border-dashed border-slate-800/60 rounded-xl p-2"
                  >
                    {{ t('timetable.emptySlot') }}
                  </div>
                </div>
              </td>

            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>
