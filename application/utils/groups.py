# -*- coding:utf-8 -*-

import datetime

from django.db.models import Q
from django.contrib.auth.models import User

from application.utils.passes import get_color_classes
from application.models import Groups, Students, Passes, Lessons, GroupList
from application.utils.date_api import get_count_of_weekdays_per_interval, get_week_days_names
from application.utils.passes import ORG_PASS_HTML_CLASS


def get_groups_list(user):

    u"""
    Получить список групп для конкретного пользоваетля
    """

    if not isinstance(user, User):
        return None

    return [
        {'id': g.id, 'name': g.name, 'days': ' '.join(g.days)}
        for g in Groups.objects.filter(
            Q(teacher_leader=user) | Q(teacher_follower=user)
        )
    ]


def get_group_detail(group_id, date_from, date_to):

    u"""
    Получить детальную информацию о группе
    """

    group = Groups.objects.get(pk=group_id)

    dates_count = get_count_of_weekdays_per_interval(
        group.days,
        date_from,
        date_to
    )

    students = [
        {
            'person': s,
            'calendar': get_student_calendar(s, group, date_from, dates_count, '%d.%m.%Y')
        } for s in get_group_students_list(group)
    ]

    return {
        'id': group.id,
        'name': group.name,
        'days': group.days,
        'start_date': group.start_date,
        'students': students,
        'calendar': map(lambda d: d.strftime('%d.%m.%Y'), group.get_calendar(date_from=date_from, count=dates_count))
    }


def get_group_students_list(group):

    u"""
    Получить список учеников из группы
    """

    if not isinstance(group, Groups):
        raise TypeError('Expected Groups instance!')

    return Students.objects.filter(
        pk__in=GroupList.objects.filter(group=group).values('student_id')
    )


def get_teacher_students_list(teacher):

    u"""
    Получить список учеников конкретного преподавателя
    """

    if not isinstance(teacher, User):
        raise TypeError('Expected User instance!')

    res = []

    for group in Groups.objects.filter(Q(teacher_leader=teacher) | Q(teacher_follower=teacher)):

        res += filter(
            lambda elem: elem not in res,
            get_group_students_list(group)
        )

    return res


def get_student_calendar(student, group, from_date, lessons_count, form=None):

    u"""
    Получить календарь занятий для конкретного ученика и конкретной ргуппы
    """

    html_color_classes = {
        key: val for val, key in get_color_classes()
    }

    group_calendar = group.get_calendar(date_from=from_date, count=lessons_count)
    lessons = iter(Lessons.objects.filter(student=student, group=group, date__gte=from_date).order_by('date'))
    statuses = {Lessons.STATUSES[key]: Lessons.STATUSES_RUS[key] for key in Lessons.STATUSES.iterkeys()}

    calendar = []

    try:
        c_lesson = lessons.next()

    except StopIteration:
        return [
            {
                'date': d if not form else d.strftime(form),
                'sign': ''
            } for d in group_calendar
        ]

    no_lessons = False

    for c_date in group_calendar:

        buf = {
            'date': c_date if not form else c_date.strftime(form)
        }

        if no_lessons or c_lesson.date > c_date.date():
            buf['pass'] = False
            buf['color'] = None
            buf['sign'] = ''

        else:
            buf['pass'] = True
            buf['sign'] = statuses[c_lesson.status] if c_lesson.status != Lessons.STATUSES['non_precessed'] and c_lesson.date == c_date.date() else ''
            buf['color'] = html_color_classes[c_lesson.group_pass.color] if not student.org else ORG_PASS_HTML_CLASS

            try:
                c_lesson = lessons.next()

            except StopIteration:
                no_lessons = True

        calendar.append(buf)

    return calendar