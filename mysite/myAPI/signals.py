from django.dispatch import receiver
from django.db.models import signals
from .models import StudentOnProduct
from datetime import datetime


def redistribution_between_groups(students, groups_for_redistribution, min_student_on_product):
    print("перераспределение студентов по группам")
    count = 1
    for group in groups_for_redistribution:
        group.students.clear()
        group.students.add(*students[min_student_on_product*(count-1):min_student_on_product * count])
        group.save()
        count += 1


@receiver(signals.post_save, sender=StudentOnProduct)
def adding_to_group2(**kwargs):
    product = kwargs["instance"].product
    new_student = kwargs["instance"].student
    min_student_on_product = product.min_stud_in_group
    max_student_on_product = product.max_stud_in_group
    start_product = product.start_date_time
    groups = kwargs["instance"].product._prefetched_objects_cache["groups"]
    count_groups = len(groups)
    students = kwargs["instance"].product._prefetched_objects_cache["students"]
    count_students = len(students)
    if count_students + 1 > count_groups * max_student_on_product:
        print("Нет свободных групп")
    elif datetime.now() >= datetime.strptime(start_product, "%Y-%m-%d %H:%M"):
        print("курс уже стартовал")
        group_for_enrollment = None
        count_flag = max_student_on_product + 1

        for group in groups:
            count_students_in_group = len(group._prefetched_objects_cache["students"])
            if min_student_on_product <= count_students_in_group < max_student_on_product:
                if count_students_in_group < count_flag:
                    group_for_enrollment = group
                    count_flag = count_students_in_group
        if group_for_enrollment is not None:
            group_for_enrollment.students.add(new_student)
            group_for_enrollment.save()
            print("Новый студент зачислен в группу")
        else:
            print("нет подходящей группы для зачисления")
    elif (count_students + 1 > min_student_on_product and (count_students + 1) % min_student_on_product == 0 and
          (count_students + 1) // min_student_on_product <= count_groups):
        students = students[:]
        students.append(new_student)
        redistribution_between_groups(students,
                                      groups_for_redistribution=groups[:(count_students + 1)//min_student_on_product],
                                      min_student_on_product=min_student_on_product)

    elif datetime.now() < datetime.strptime(start_product, "%Y-%m-%d %H:%M"):
        print("курс не стартовал")
        group_for_enrollment = None
        count_flag = max_student_on_product + 1

        for group in groups:
            count_students_in_group = len(group._prefetched_objects_cache["students"])
            if min_student_on_product - 1 <= count_students_in_group < max_student_on_product:
                if count_students_in_group < count_flag:
                    group_for_enrollment = group
                    count_flag = count_students_in_group
        if group_for_enrollment is not None:
            group_for_enrollment.students.add(new_student)
            group_for_enrollment.save()
            print("Новый студент зачислен в группу")
        else:
            for group in groups:
                count_students_in_group = len(group._prefetched_objects_cache["students"])
                if count_students_in_group < max_student_on_product:
                    group.students.add(new_student)
                    group.save()
                    print("Новый студент зачислен в группу (студентов в ней меньше необходимого)")
                    break

