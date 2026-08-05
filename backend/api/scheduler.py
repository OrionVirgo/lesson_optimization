import time
from .models import Schedule

def is_teacher_available(teacher, time_slot, current_schedule):
    if teacher.off_day and teacher.off_day.lower() == time_slot.day.lower():
        return False

    for assignment in current_schedule:
        if assignment.teacher_id == teacher.id and assignment.time_slot_id == time_slot.id:
            return False

    return True


def are_class_and_classroom_available(school_class, classroom, time_slot, current_schedule):
    for assignment in current_schedule:
        if assignment.school_class_id == school_class.id and assignment.time_slot_id == time_slot.id:
            return False

        if assignment.classroom_id == classroom.id and assignment.time_slot_id == time_slot.id:
            return False

    return True


def is_classroom_suitable_for_course(classroom, course):
    if course.is_lab_required:
        return classroom.is_lab
    else:
        return True


def is_consecutive_limit_ok(school_class, course, time_slot, current_schedule):
    day = time_slot.day
    same_day_hours = [
        assignment.time_slot.hour for assignment in current_schedule
        if assignment.school_class_id == school_class.id 
        and assignment.course_id == course.id
        and assignment.time_slot.day == day
    ]
    
    if len(same_day_hours) >= 4:
        return False
    return True


def solve(assignment_list, pending_course, classrooms, time_slots, start_time, max_seconds=5.0):
    # Timeout guard to prevent backend locks
    if time.time() - start_time > max_seconds:
        return None

    if not pending_course:
        return assignment_list
    
    current_requirement = pending_course[0]
    school_class = current_requirement.school_class
    course = current_requirement.course
    teacher = current_requirement.teacher

    for time_slot in time_slots:
        if not is_teacher_available(teacher, time_slot, assignment_list):
            continue

        for classroom in classrooms:
            if not is_classroom_suitable_for_course(classroom, course):
                continue

            if not are_class_and_classroom_available(school_class, classroom, time_slot, assignment_list):
                continue

            if not is_consecutive_limit_ok(school_class, course, time_slot, assignment_list):
                continue
            
            new_assignment = Schedule(
                school_class=school_class,
                course=course,
                teacher=teacher,
                classroom=classroom,
                time_slot=time_slot
            )
            assignment_list.append(new_assignment)

            result = solve(assignment_list, pending_course[1:], classrooms, time_slots, start_time, max_seconds)

            if result is not None:
                return result
            assignment_list.pop()
    return None 


def generate_schedule(raw_requirements, classrooms, time_slots):
    # MRV (Minimum Remaining Values) sort: process lab-required and teacher-constrained courses first
    sorted_reqs = sorted(
        raw_requirements,
        key=lambda r: (0 if r.course.is_lab_required else 1, 0 if r.teacher.off_day else 1, -r.weekly_hours)
    )

    unpacked_pending_courses = []    
    for req in sorted_reqs:
        for _ in range(req.weekly_hours):
            unpacked_pending_courses.append(req)
        
    start_time = time.time()
    return solve([], unpacked_pending_courses, classrooms, time_slots, start_time, max_seconds=5.0)

