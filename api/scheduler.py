from .models import Schedule
def is_teacher_available(teacher, time_slot, current_schedule):
    if teacher.off_day == time_slot.day:
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
        return not classroom.is_lab
    
def is_consecutive_limit_ok (school_class, course ,time_slot, current_schedule):
    day = time_slot.day
    same_day_hours = [assignment.time_slot.hour for assignment in current_schedule
                      if assignment.school_class_id == school_class.id 
                      and assignment.course_id == course.id
                      and assignment.time_slot.day == day]
    
    if len(same_day_hours) >= 4:
        return False
    return True

#Backtracing function to generate the schedule


def solve(assignment_list,pending_course, classrooms,time_slots):
    
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
            
            new_assignment = Schedule (
                
                school_class=school_class,
                course=course,
                teacher=teacher,
                classroom=classroom,
                time_slot=time_slot
            )
            assignment_list.append(new_assignment)

            result = solve(assignment_list, pending_course[1:], classrooms, time_slots)

            if result is not None:
                return result
            assignment_list.pop()
    return None 

def generate_schedule(raw_requirements, classrooms, time_slots):
    
    unpacked_pending_courses = []    
    for req in raw_requirements:
        
        for _ in range(req.weekly_hours):
            unpacked_pending_courses.append(req)
        
    return solve([], unpacked_pending_courses, classrooms, time_slots)

    





        
