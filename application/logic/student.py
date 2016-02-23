# -*- coding:utf-8 -*-

from application.models import GroupList, Students
from application.utils.phones import check_phone

__all__ = (
	'add_student'
)

def add_student(group_id, first_name, last_name,  phone, e_mail=None, is_org=False, group_list_orm=GroupList):
    try:
        first_name = first_name.replace(' ', '')
        last_name = last_name.replace(' ', '')
        phone = check_phone(phone)
        e_mail = e_mail.replace(' ', '') if e_mail else None
        group_id = int(group_id)
        is_org = is_org == u'true'

        try:
            student = Students.objects.get(first_name=first_name, last_name=last_name, phone=phone)
            group_list = group_list_orm.objects.get(student=student, group_id=group_id)

        except Students.DoesNotExist:
            student = Students(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                e_mail=e_mail,
                org=is_org
            )

            student.save()

            group_list = None

        except group_list_orm.DoesNotExist:
            group_list = None

        if not group_list:
            group_list = group_list_orm(
                student=student,
                group_id=group_id
            )
            group_list.save()

        elif not group_list.active:
            group_list.active = True
            group_list.save()

        else:
            return None

        return student.__json__()

    except Exception:
    	from traceback import format_exc
        print format_exc()
        return None


def remove_student(group_id, students, group_list_orm):
	try:
		group_list_orm.objects.filter(group__id=group_id, student__id__in=students).select_related('student').update(active=False)
		return True
	except Exception:
		print format_exc()
		return False