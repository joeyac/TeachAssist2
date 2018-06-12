from django.db import models
from account.models import User
from utils.constants import RequireDegree


class ClassRoom(models.Model):
    college = models.CharField(max_length=255)
    floor = models.IntegerField()
    capacity = models.IntegerField()
    room_id = models.CharField(max_length=20)

    def __str__(self):
        return "{}: {}".format(self.college, self.room_id)


class Period(models.Model):
    # 代表周数，1<=week<=16
    week = models.IntegerField()
    # 代表工作日，1<=day<=5
    day = models.IntegerField()
    # 代表一天的时间段，1<=section<=5
    section = models.IntegerField()

    def __str__(self):
        return "week{} day{} section{}".format(self.week, self.day, self.section)

    class Meta:
        unique_together = ('week', 'day', 'section')


class Course(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    total_period_number = models.IntegerField()
    capacity = models.IntegerField()

    # 特殊课程对上课教室的特殊需求，比如实验课,这儿是硬性需求
    reject_class_room = models.ManyToManyField(ClassRoom, blank=True, default=None)

    def __str__(self):
        return "{}({})".format(self.name, self.teacher.get_full_name())


class Class(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    course = models.ManyToManyField(Course, blank=True, default=None)


class Lecture(models.Model):
    # one room-period -> one lecture

    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)

    # one lecture can belong to a course or none
    course = models.ForeignKey(Course, related_name='lectures', on_delete=models.SET_NULL, null=True, blank=True,
                               default=None)

    def __str__(self):
        return "{}-{}".format(self.classroom, self.period)

    class Meta:
        unique_together = ('classroom', 'period')


class Requirement(models.Model):
    # 5 represents the most favorite
    # 4 represents the second favorite
    # 3 represents acceptable favorite
    # 2 represents mediocre favorite
    # 1 represents the least favorite
    # -10 represents reject
    favorite = models.IntegerField(choices=RequireDegree.model_choices(), default=RequireDegree.MEDIOCRE)
    # every requirement should link to a lecture
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    # 所属老师
    # 不需要，每个lecture已经对应到了一个具体的teacher
    # teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.lecture.course.teacher.get_full_name(), self.lecture)
