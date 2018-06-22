import sys

from django.test import TestCase, Client

from course_arrangement.algorithm_lab import Solver
from course_arrangement.views import *


class ArrangeTest(TestCase):
    def setUp(self):
        room1 = ClassRoom.objects.create(college='机电楼', floor=4, identifier='02', capacity=120)
        room1.save()
        room2 = ClassRoom.objects.create(college='逸夫楼', floor=2, identifier='03', capacity=70)
        room2.save()

        user1 = User.objects.create(username='41416060', user_type=UserType.TEACHER, real_name='刘老师')
        user1.set_password('123456')
        user1.save()
        user2 = User.objects.create(username='41416068', user_type=UserType.TEACHER, real_name='李老师')
        user2.set_password('123456')
        user2.save()

        college_prefer = ClassRoomCollegeChoice.objects.create(refer_to=room1, value=RequireDegree.SOFT_ACCEPT_5)
        college_prefer.save()

        floor_prefer = ClassRoomFloorChoice.objects.create(refer_to=room2, value=RequireDegree.SOFT_ACCEPT_5)
        floor_prefer.save()

        class1 = Class.objects.create(name='信安15', capacity=100)
        class2 = Class.objects.create(name='计科1501', capacity=33)
        class3 = Class.objects.create(name='计科1504', capacity=40)
        class1.save()
        class2.save()
        class3.save()

        course1 = Course.objects.create(name='c++', teacher=user2, start_week=3, end_week=4, slots_per_week=2,
                                        max_slots_per_day=1)
        course1.time_slot1 = RequireDegree.SOFT_ACCEPT_5
        course1.classes.add(class2)
        course1.classes.add(class3)
        course1.save()

        course2 = Course.objects.create(name='java', teacher=user1, start_week=1, end_week=4, slots_per_week=3,
                                        max_slots_per_day=1)
        course2.classes.add(class1)
        course2.save()

        course3 = Course.objects.create(name='模式识别', teacher=user2, start_week=1, end_week=2, slots_per_week=3,
                                        max_slots_per_day=1)
        course3.classes.add(class3)
        course3.floor_preference.add(floor_prefer)
        course3.time_slot3 = RequireDegree.SOFT_ACCEPT_1
        course3.time_slot4 = RequireDegree.SOFT_ACCEPT_2
        course3.save()

        course4 = Course.objects.create(name='计算机组成原理课程设计', teacher=user2, start_week=3, end_week=4, slots_per_week=1,
                                        max_slots_per_day=1, is_lab=True)
        course4.classes.add(class1)
        course4.classes.add(class2)
        course4.classes.add(class3)
        course4.save()

        self.solver = Solver()
        self.solver.load_data()
        self.c = Client()

        days = ['周一', '周二', '周三', '周四', '周五']
        self.solver.run()
        self.solver.write_to_database()
        for item in Assignment.objects.all():
            print('{}({} 第{}节)'.format(item, days[item.day], item.slot))
        print('------------\n')

    def send(self, url, data):
        return self.c.post(url, data)

    @staticmethod
    def output(data):
        for c in data:
            days = ['周一', '周二', '周三', '周四', '周五']
            print(
                "{} {} ({},{}) {} 第{}节: ".format(c['course']['full_name'], c['course']['teacher'], c['classroom_name'],
                                                 c['course']['week_str'], days[c['day']], c['slot'] + 1), end='')
            course = Course.objects.get(id=c['course']['id'])
            for cls in course.classes.all():
                print(cls, end=' ')
            print()
        print('===========\n')

    def test_time_table_teacher(self):
        print(sys._getframe().f_code.co_name)
        response = self.send('/course/timetable/teacher/', {'tid': 2})
        self.output(response.json()['data'])

    def test_time_table_room(self):
        print(sys._getframe().f_code.co_name)
        response = self.send('/course/timetable/classroom/', {'rid': 1})
        self.output(response.json()['data'])

    def test_time_table_class(self):
        print(sys._getframe().f_code.co_name)
        response = self.send('/course/timetable/class/', {'cid': 1})
        self.output(response.json()['data'])
