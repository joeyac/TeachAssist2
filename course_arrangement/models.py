from django.db import models
from django.db.models import Sum
from account.models import User
from django.core.exceptions import ValidationError
from utils.constants import UserType, RequireDegree
from utils.shortcuts import compress_week_arrays
from django.utils.translation import gettext_lazy as _


def validate_teacher(value):
    if not User.objects.filter(id=value, user_type=UserType.TEACHER).exists():
        raise ValidationError(
            _('User %(value)s is not a teacher'),
            params={'value': value},
        )


def validate_week(value):
    lv = 1
    rv = 16
    if value < lv or value > rv:
        raise ValidationError(
            _('week %(value)s validate failed, week range[%(lv)s,%(rv)s]'),
            params={'value': value,
                    'lv': lv,
                    'rv': rv},
        )


class ClassRoom(models.Model):
    capacity = models.IntegerField()
    college = models.CharField(max_length=255)
    floor = models.IntegerField()
    identifier = models.CharField(max_length=10)

    def __str__(self):
        return "{}{}{}".format(self.college, self.floor, self.identifier)


class Class(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()

    def __str__(self):
        return "{}({}人)".format(self.name, self.capacity)


class ClassRoomFloorChoice(models.Model):
    refer_to = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    value = models.IntegerField(choices=RequireDegree.model_choices(), default=RequireDegree.SOFT_MEDIOCRE,
                                help_text="preference certain floor")

    @property
    def floor(self):
        return self.refer_to.floor

    def __str__(self):
        return "{}层".format(self.floor)

    def clean(self):
        if ClassRoomCollegeChoice.objects.all().filter(refer_to__college=self.floor, value=self.value).exists():
            raise ValidationError('objects(college={},value={}) existed.'.format(self.floor, self.value))


class ClassRoomCollegeChoice(models.Model):
    refer_to = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    value = models.IntegerField(choices=RequireDegree.model_choices(), default=RequireDegree.SOFT_MEDIOCRE,
                                help_text="preference certain college")

    @property
    def college(self):
        return self.refer_to.college

    def __str__(self):
        return "{}".format(self.college)

    def clean(self):
        if ClassRoomCollegeChoice.objects.all().filter(refer_to__college=self.college, value=self.value).exists():
            raise ValidationError('objects(college={},value={}) existed.'.format(self.college, self.value))


class Course(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(User, validators=[validate_teacher], on_delete=models.CASCADE)
    classes = models.ManyToManyField(Class)

    # 1 <= start_week <= end_week <= 16
    start_week = models.IntegerField(validators=[validate_week])
    end_week = models.IntegerField(validators=[validate_week])

    # 每周几节课时
    slots_per_week = models.IntegerField(default=1)

    # 每天默认最多两节课
    max_slots_per_day = models.IntegerField(default=2, help_text='max time slots every day')

    # 为了拓展可以使用postgres的ArrayField，实际上不太需要
    # from django.contrib.postgres.fields import ArrayField, JSONField
    # day = ArrayField(models.IntegerField(choices=RequireDegree.model_choices(), default=RequireDegree.SOFT_MEDIOCRE,
    #                                      help_text="preference of Day"))

    day1 = models.IntegerField(choices=RequireDegree.model_choices(), default=RequireDegree.SOFT_MEDIOCRE,
                               help_text="preference of Monday")
    day2 = models.IntegerField(choices=RequireDegree.model_choices(), default=RequireDegree.SOFT_MEDIOCRE,
                               help_text="preference of Tuesday")
    day3 = models.IntegerField(choices=RequireDegree.model_choices(), default=RequireDegree.SOFT_MEDIOCRE,
                               help_text="preference of Wednesday")
    day4 = models.IntegerField(choices=RequireDegree.model_choices(), default=RequireDegree.SOFT_MEDIOCRE,
                               help_text="preference of Thursday")
    day5 = models.IntegerField(choices=RequireDegree.model_choices(), default=RequireDegree.SOFT_MEDIOCRE,
                               help_text="preference of Friday")

    time_slot1 = models.IntegerField(choices=RequireDegree.model_choices(), default=RequireDegree.SOFT_MEDIOCRE,
                                     help_text='preference of time slot 1')
    time_slot2 = models.IntegerField(choices=RequireDegree.model_choices(), default=RequireDegree.SOFT_MEDIOCRE,
                                     help_text='preference of time slot 2')
    time_slot3 = models.IntegerField(choices=RequireDegree.model_choices(), default=RequireDegree.SOFT_MEDIOCRE,
                                     help_text='preference of time slot 3')
    time_slot4 = models.IntegerField(choices=RequireDegree.model_choices(), default=RequireDegree.SOFT_MEDIOCRE,
                                     help_text='preference of time slot 4')
    time_slot5 = models.IntegerField(choices=RequireDegree.model_choices(), default=RequireDegree.SOFT_MEDIOCRE,
                                     help_text='preference of time slot 5')

    floor_preference = models.ManyToManyField(ClassRoomFloorChoice, blank=True)

    college_preference = models.ManyToManyField(ClassRoomCollegeChoice, blank=True)

    is_lab = models.BooleanField(default=False)

    class Meta:
        ordering = ['is_lab']

    def clean(self):
        if self.start_week > self.end_week:
            raise ValidationError(_('start week must less or equal than end week.'))

    @property
    def day_preference(self):
        return [self.day1, self.day2, self.day3, self.day4, self.day5]

    @property
    def slot_preference(self):
        return [self.time_slot1, self.time_slot2, self.time_slot3, self.time_slot4, self.time_slot5]

    @property
    def capacity(self):
        return self.classes.aggregate(Sum('capacity'))['capacity__sum']

    @property
    def full_name(self):
        if self.is_lab:
            return "{}(实验)".format(self.name)
        else:
            return "{}".format(self.name)

    @property
    def week_str(self):
        arr = [i for i in range(self.start_week, self.end_week + 1)]
        return compress_week_arrays(arr) + '周'

    @property
    def teacher_name(self):
        return "{}".format(self.teacher)

    @property
    def class_name(self):
        if self.classes:
            return ','.join([cls.name for cls in self.classes.all()])
        else:
            return '无'

    def __str__(self):
        return "{}-{}-{}".format(self.full_name, self.teacher.real_name, self.week_str)


class Assignment(models.Model):

    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.IntegerField()
    slot = models.IntegerField()

    @property
    def teacher_name(self):
        return "{}".format(self.course.teacher)

    @property
    def course_name(self):
        return "{}".format(self.course.name)

    @property
    def classroom_name(self):
        if self.classroom:
            return "{}".format(self.classroom)
        else:
            return "地点未知"

    def __str__(self):
        return "{}-{}".format(self.course, self.classroom_name)
