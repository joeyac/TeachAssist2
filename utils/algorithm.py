from course_arrangement.models import *
from utils.constants import UserType
from django.db.models import Sum
import random
import math
import copy

T = User.objects.all().filter(user_type=UserType.TEACHER).count()  # teachers cnt
P = Period.objects.all().count()  # period cnt
D = T * P

TEACHER_LECTURE = {}
for t in User.objects.all().filter(user_type=UserType.TEACHER):
    tol_lecture = Course.objects.all().filter(teacher=t).aggregate(Sum('total_period_number'))
    TEACHER_LECTURE[t.id] = tol_lecture

COURSE_CAPACITY = {}
for c in Course.objects.all():
    COURSE_CAPACITY[c.id] = c.capacity


def reset_arrangement():
    for l in Lecture.objects.all():
        l.course = None
        l.save()


class Single(object):
    def __init__(self, pos, velocity, pid):
        self.pos = pos
        self.v = velocity
        self.pid = pid

    def update(self, pos_best, g_pos_best):
        K = 0.72984
        c1 = 2.05
        c2 = 2.05
        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)
        self.v = self.v + c1 * r1 * (pos_best - self.pos) + c2 * r2 * (g_pos_best - self.pos)

        self.v = self.v * K

        self.pos = self.pos + self.v


class Particle(object):
    def __init__(self,
                 pos_min, pos_max,
                 velocity_min, velocity_max):
        self.arr = []
        for _t in User.objects.all().filter(user_type=UserType.TEACHER):
            cur = []
            for p in Period.objects.all():
                _p = random.randint(pos_min, pos_max)
                _v = random.uniform(velocity_min, velocity_max)
                cur.append(Single(_p, _v, p.id))
            self.arr.append([cur, _t.id])
        self.best = []
        self.best_fitness = -math.inf

    def update(self, global_best):

        pass

    def fix_conflict(self):
        for cur, tid in self.arr:
            n = len(cur)
            if n < TEACHER_LECTURE[tid]:
                raise ValueError(
                    "periods({}) less than teacher({}) needs({}).".format(len(cur), tid, TEACHER_LECTURE[tid]))

            cur.sort(key=lambda item: item.pos, reverse=True)
            teacher = User.objects.get(id=tid)
            courses = Course.objects.filter(teacher=teacher)
            curp = 0
            lastp = TEACHER_LECTURE[tid]

            for course in courses:
                cnt = course.total_period_number
                choice = Lecture.objects.all().filter(classroom__capacity__gte=course.capacity)
                for i in range(cnt):
                    while True:
                        lecture = choice.filter(period__id=cur[curp].pid, course=None)
                        if lecture:
                            lecture = lecture[0]
                            lecture.course = course
                            lecture.save()
                            curp = curp + 1
                            lastp = TEACHER_LECTURE[tid]
                            break
                        else:
                            if lastp >= n:
                                raise ValueError("can not assign course({}).".format(course.id))
                            cur[curp], cur[lastp] = cur[lastp], cur[curp]
                            lastp = lastp + 1

    def cal_fitness(self):
        # teacher preference
        # classroom preference
        # Penalty
        # day preference
        # requirement preference

        fitness = 0
        # teacher preference
        # 老师在一天当中上多节课，一节课为0，两节课为-1，以此类推

        # classroom preference
        # 一门课程在一个教室上，为0，两个教室上，为-1，以此类推

        # penalty
        # 额外罚权

        # day preference
        # 一门课应该尽量分配到整个学期，

        # requirement preference
        # 如果对应的lecture确实被分配了任务，才需要加上对应的preference值
        reqs = Requirement.objects.all().filter(lecture__course__isnull=False)
        for req in reqs:
            fitness = fitness + req.favorite

        if fitness > self.best_fitness:
            self.best_fitness = fitness
            self.best = copy.deepcopy(self.arr)
        return fitness


class Swarm(object):
    def __init__(self, swarm_size,
                 pos_min, pos_max,
                 velocity_min, velocity_max,
                 iteration_max,
                 c1, c2,
                 r1, r2,
                 ):
        self.s = [[Particle(pos_min, pos_max, velocity_min, velocity_max), i] for i in range(swarm_size)]
        self.iteration_max = iteration_max
        self.c1 = c1
        self.c2 = c2
        self.r1 = r1
        self.r2 = r2
        self.global_best = []
        self.global_best_fitness = -math.inf

    def run(self):
        for item, i in self.s:
            try:
                item.fix_conflict()
                fitness = item.cal_fitness()
                if fitness > self.global_best_fitness:
                    self.global_best_fitness = fitness
                    self.global_best = copy.deepcopy(item.best)
            except ValueError as e:
                print('particle({}) warning: {}'.format(i, str(e)))


def execute(popSize=10,
            maxIterations=100,
            intertia_weight=0.5,
            c1=2.0,
            c2=2.0,
            w_fixed=True,
            ):
    return ''
