from django.test import TestCase
from course_arrangement.algorithm_lab import Solver
from course_arrangement.models import *


class ArrangeTest(TestCase):
    def setUp(self):
        room1 = ClassRoom.objects.create(college='机电楼', floor=4, identifier='02', capacity=120)
        room2 = ClassRoom.objects.create(college='逸夫楼', floor=2, identifier='03', capacity=70)

        user1 = User.objects.create(username='41416060', user_type=UserType.TEACHER, real_name='刘老师')
        user1.set_password('123456')
        user1.save()
        user2 = User.objects.create(username='41416068', user_type=UserType.TEACHER, real_name='李老师')
        user2.set_password('123456')
        user2.save()

        college_prefer = ClassRoomCollegeChoice.objects.create(refer_to=room1, value=RequireDegree.SOFT_ACCEPT_5)

        floor_prefer = ClassRoomFloorChoice.objects.create(refer_to=room2, value=RequireDegree.SOFT_ACCEPT_5)

        class1 = Class.objects.create(name='信安15', capacity=100)
        class2 = Class.objects.create(name='计科1501', capacity=33)
        class3 = Class.objects.create(name='计科1504', capacity=40)

        course1 = Course.objects.create(name='c++', teacher=user2, start_week=3, end_week=4, slots_per_week=2,
                                        max_slots_per_day=1)
        course1.time_slot1 = RequireDegree.SOFT_ACCEPT_5
        course1.time_slot2 = RequireDegree.SOFT_ACCEPT_5
        course1.classes.add(class2)
        course1.classes.add(class3)

        course2 = Course.objects.create(name='java', teacher=user1, start_week=1, end_week=4, slots_per_week=3,
                                        max_slots_per_day=1)
        course2.classes.add(class1)

        course3 = Course.objects.create(name='模式识别', teacher=user2, start_week=1, end_week=2, slots_per_week=3,
                                        max_slots_per_day=1)
        course3.classes.add(class3)
        course3.floor_preference.add(floor_prefer)

        course4 = Course.objects.create(name='计算机组成原理课程设计', teacher=user2, start_week=3, end_week=4, slots_per_week=1,
                                        max_slots_per_day=1, is_lab=True)
        course4.classes.add(class1)
        course4.classes.add(class2)
        course4.classes.add(class3)

        self.solver = Solver()
        self.solver.load_data()

    def test_arrange(self):
        self.solver.run()
        self.solver.write_to_database()
        for item in Assignment.objects.all():
            print(item)
