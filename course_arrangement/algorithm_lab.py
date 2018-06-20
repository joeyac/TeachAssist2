from django.conf import settings
from django.core.cache import cache
from pulp.pulp import *

from course_arrangement.models import *
from utils.constants import AlgorithmStatus


class Solver(object):
    def __init__(self, debug=settings.DEBUG):
        self.debug = debug

        self.prob = None
        self.L = None  # 课时数
        self.W = None
        self.D = None
        self.T = None
        self.R = None  # 教室数量

        self.LECTURE_IDS = {}
        self.LECTURE_IDS_REVERSE = {}
        self.LECTURE_IDS_LAB = []
        self.CLASSROOM_IDS = {}
        self.CLASSROOM_IDS_REVERSE = {}

        self.S = {}
        self.Q = {}
        self.P1 = {}
        self.P2 = {}
        self.P3 = {}
        self.P4 = {}

        self.LS = {}
        self.LP = {}
        self.LC = {}
        self.SW_L = {}
        self.EW_L = {}
        self.X_vars = None
        self.Y_vars = None

    def load_data(self, week=4, day=5, time_slot=5):
        self.prob = LpProblem("arrange course", LpMaximize)
        self.L = Course.objects.all().aggregate(sum=Sum('slots_per_week'))['sum']  # 课时数
        self.W = week
        self.D = day
        self.T = time_slot
        self.R = ClassRoom.objects.all().count()  # 教室数量
        self.map_ids()
        self.add_lecture_parameters()
        self.add_set_constants()
        l_seq = [i for i in range(self.L)]
        w_seq = [i for i in range(self.W)]
        d_seq = [i for i in range(self.D)]
        t_seq = [i for i in range(self.T)]
        r_seq = [i for i in range(self.R + 1)]

        self.X_vars = LpVariable.dicts("X", (l_seq, w_seq, d_seq, t_seq, r_seq), 0, 1, LpBinary)
        self.Y_vars = LpVariable.dicts("Y", (l_seq, d_seq, t_seq, r_seq), 0, 1, LpBinary)

        self.add_objective_func()
        self.add_subject_func()

    def status(self):
        return LpStatus[self.prob.status]

    def pr(self):
        if not self.debug:
            return
        for l in range(self.L):
            for d in range(self.D):
                for t in range(self.T):
                    for i in range(self.R + 1):
                        if value(self.Y_vars[l][d][t][i]) == 1:
                            print("Y[{}][{}][{}][{}]={}".format(l, d, t, i, value(self.Y_vars[l][d][t][i])))

    def run(self):
        self.prob.solve()
        if self.debug:
            print("Status:", self.status())
        if self.status() == "Optimal":
            self.pr()
        return self.status() == "Optimal"

    def run_another_optimal(self):
        if LpStatus[self.prob.status] != "Optimal":
            if self.debug:
                print("can not found optimal solution anymore")
            return False
        self.prob += lpSum([self.Y_vars[l][d][t][i]
                            for l in range(self.L)
                            for d in range(self.D)
                            for t in range(self.T)
                            for i in range(self.R + 1)
                            if value(self.Y_vars[l][d][t][i]) == 1
                            ]) <= self.L - 1

        courses = list(Course.objects.all().values('id', 'slots_per_week'))
        for course in courses:
            index_list = []
            for slot in range(course['slots_per_week']):
                index_list.append(self.LECTURE_IDS[(course['id'], slot)])
            self.prob += lpSum([self.Y_vars[l][d][t][i]
                                for l in index_list
                                for d in range(self.D)
                                for t in range(self.T)
                                for i in range(self.R + 1)
                                if value(self.Y_vars[l][d][t][i]) == 1
                                ]) <= course['slots_per_week'] - 1

        return self.run()

    def write_to_database(self):
        # 这一步会将数据库中已有的排课方案清空
        Assignment.objects.all().delete()
        if LpStatus[self.prob.status] == "Optimal":
            cnt = 0
            for l in range(self.L):
                for d in range(self.D):
                    for t in range(self.T):
                        for i in range(self.R + 1):
                            if value(self.Y_vars[l][d][t][i]) == 1:
                                course = Course.objects.get(id=self.LECTURE_IDS_REVERSE[l][0])
                                classroom = ClassRoom.objects.get(
                                    id=self.CLASSROOM_IDS_REVERSE[i]) if l not in self.LECTURE_IDS_LAB else None

                                Assignment.objects.create(course=course,
                                                          classroom=classroom,
                                                          day=d,
                                                          slot=t)
                                cnt = cnt + 1

            return "optimal solution found, create {} assignment(s).".format(cnt)
        else:
            return "status: {}, no optimal solution can be found".format(LpStatus[self.prob.status])

    def map_ids(self):
        classrooms = list(ClassRoom.objects.all().values('id'))
        index = 0
        for cls in classrooms:
            self.CLASSROOM_IDS[cls['id']] = index
            self.CLASSROOM_IDS_REVERSE[index] = cls['id']
            index = index + 1

        courses = list(Course.objects.all().values('id', 'slots_per_week', 'is_lab'))
        index = 0
        for course in courses:
            for slot in range(course['slots_per_week']):
                self.LECTURE_IDS[(course['id'], slot)] = index
                self.LECTURE_IDS_REVERSE[index] = (course['id'], slot)
                if course['is_lab']:
                    self.LECTURE_IDS_LAB.append(index)
                index = index + 1

    def add_lecture_parameters(self):
        classrooms = list(ClassRoom.objects.all().values('id', 'capacity', 'floor', 'college'))
        for course in Course.objects.all():
            self.S[course.id] = course.max_slots_per_day
            dp = course.day_preference
            sp = course.slot_preference

            for slot in range(course.slots_per_week):
                index = self.LECTURE_IDS[(course.id, slot)]

                for preference in course.floor_preference.all():
                    floor = preference.refer_to.floor
                    for classroom in ClassRoom.objects.all().filter(floor=floor):
                        self.P3[(index, self.CLASSROOM_IDS[classroom.id])] = preference.value

                for preference in course.college_preference.all():
                    college = preference.refer_to.college
                    for classroom in ClassRoom.objects.all().filter(college=college):
                        self.P4[(index, self.CLASSROOM_IDS[classroom.id])] = preference.value

                self.Q[index] = {}
                for cls in classrooms:
                    cid = self.CLASSROOM_IDS[cls['id']]
                    if course.is_lab:
                        self.Q[index][cid] = 0
                        self.Q[index][self.R] = 1
                    else:
                        self.Q[index][cid] = 1 if cls['capacity'] >= course.capacity else 0
                        self.Q[index][self.R] = 0

                self.P1[index] = {}
                for d in range(self.D):
                    self.P1[index][d] = dp[d]

                self.P2[index] = {}
                for t in range(self.T):
                    self.P2[index][t] = sp[t]

    def add_set_constants(self):
        # 班级的课时集合
        for cls in Class.objects.all():
            self.LS[cls.id] = []
            for course in cls.course_set.all():
                self.LS[cls.id].extend(
                    [self.LECTURE_IDS[(course.id, slot)] for slot in range(course.slots_per_week)]
                )

        # 老师的课时集合
        for teacher in User.objects.all().filter(user_type=UserType.TEACHER):
            self.LP[teacher.id] = []
            for course in teacher.course_set.all():
                self.LP[teacher.id].extend(
                    [self.LECTURE_IDS[(course.id, slot)] for slot in range(course.slots_per_week)]
                )

        # 课程的课时集合
        for course in Course.objects.all():
            self.LC[course.id] = [self.LECTURE_IDS[(course.id, slot)] for slot in range(course.slots_per_week)]

        # 某个课时的起始周, 結束周
        for course in Course.objects.all():
            cid = course.id
            sw = course.start_week
            ew = course.end_week
            for slot in range(course.slots_per_week):
                sid = self.LECTURE_IDS[(cid, slot)]
                self.SW_L[sid] = sw
                self.EW_L[sid] = ew

    def get_objective_value(self):
        data = 0
        for l in range(self.L):
            for w in range(self.W):
                for d in range(self.D):
                    for t in range(self.T):
                        for i in range(self.R + 1):
                            data += value(self.X_vars[l][w][d][t][i]) * (self.P1[l][d] + self.P2[l][t])

        for l, i in self.P3:
            for w in range(self.W):
                for d in range(self.D):
                    for t in range(self.T):
                        data += value(self.X_vars[l][w][d][t][i]) * self.P3[(l, i)]

        for l, i in self.P4:
            for w in range(self.W):
                for d in range(self.D):
                    for t in range(self.T):
                        data += value(self.X_vars[l][w][d][t][i]) * self.P4[(l, i)]
        return data

    def add_objective_func(self):
        self.prob += lpSum([
            self.X_vars[l][w][d][t][i] * self.P1[l][d]
            for l in range(self.L)
            for w in range(self.W)
            for d in range(self.D)
            for t in range(self.T)
            for i in range(self.R + 1)
        ]) + lpSum([
            self.X_vars[l][w][d][t][i] * self.P2[l][t]
            for l in range(self.L)
            for w in range(self.W)
            for d in range(self.D)
            for t in range(self.T)
            for i in range(self.R + 1)
        ]) + lpSum([
            self.X_vars[l][w][d][t][i] * self.P3[(l, i)]
            for l, i in self.P3
            for w in range(self.W)
            for d in range(self.D)
            for t in range(self.T)
        ]) + lpSum([
            self.X_vars[l][w][d][t][i] * self.P4[(l, i)]
            for l, i in self.P4
            for w in range(self.W)
            for d in range(self.D)
            for t in range(self.T)
        ])

    def add_subject_func(self):
        # 注意考虑针对实验课的虚拟教室的处理
        self.R = self.R + 1

        # 保证同一个课时在不同周分配到相同的时槽和教室
        for l in range(self.L):
            sw = min(self.SW_L[l], self.W)
            ew = min(self.EW_L[l], self.W)
            for w in range(sw - 1, ew):
                for d in range(self.D):
                    for t in range(self.T):
                        for i in range(self.R):
                            self.prob += self.X_vars[l][w][d][t][i] == self.Y_vars[l][d][t][i]

        # 一个课时分配到一个具体的时槽和教室
        for l in range(self.L):
            self.prob += lpSum([
                self.Y_vars[l][d][t][i]
                for d in range(self.D)
                for t in range(self.T)
                for i in range(self.R)
            ]) == 1

        # 每个时槽最多分配一个具体的课程和教室
        for w in range(self.W):
            for d in range(self.D):
                for t in range(self.T):
                    for i in range(self.R - 1):
                        self.prob += lpSum([
                            self.X_vars[l][w][d][t][i]
                            for l in range(self.L)
                        ]) <= 1

        # 每个老师在一个时槽最多一个课时
        for tid in self.LP:
            for w in range(self.W):
                for d in range(self.D):
                    for t in range(self.T):
                        self.prob += lpSum([
                            self.X_vars[l][w][d][t][i]
                            for l in self.LP[tid]
                            for i in range(self.R)
                        ]) <= 1

        # 每个班级在一个时槽最多一个课时
        for cid in self.LS:
            for w in range(self.W):
                for d in range(self.D):
                    for t in range(self.T):
                        self.prob += lpSum([
                            self.X_vars[l][w][d][t][i]
                            for l in self.LS[cid]
                            for i in range(self.R)
                        ]) <= 1

        # 每个课时只能安排到能放下的教室中
        # 新建一个虚拟教室，完成实验课需求
        for l in range(self.L):
            for w in range(self.W):
                for d in range(self.D):
                    for t in range(self.T):
                        for i in range(self.R):
                            self.prob += self.X_vars[l][w][d][t][i] <= self.Q[l][i]

        # 每个教室在一个时槽最多一个课时
        # 注意实验课虚拟教室可能会分配多个不同课时

        for w in range(self.W):
            for d in range(self.D):
                for t in range(self.T):
                    for i in range(self.R - 1):
                        self.prob += lpSum([
                            self.X_vars[l][w][d][t][i]
                            for l in range(self.L)
                        ]) <= 1

        # 每门课程每天最大课时限制

        for course_id in self.LC:
            for w in range(self.W):
                for d in range(self.D):
                    self.prob += lpSum([
                        self.X_vars[l][w][d][t][i]
                        for l in self.LC[course_id]
                        for t in range(self.T)
                        for i in range(self.R)
                    ]) <= self.S[course_id]

        self.R = self.R - 1


solver = Solver()
cache.set('ALGO_STATUS', AlgorithmStatus.NEW)
