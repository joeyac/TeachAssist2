class Choices:
    @classmethod
    def choices(cls):
        d = cls.__dict__
        ret = [d[item] for item in d.keys() if not item.startswith("__")]
        ret.sort(reverse=True)
        return ret

    @classmethod
    def model_choices(cls):
        d = cls.__dict__
        ret = [(d[item], item) for item in d.keys() if not item.startswith("__")]
        ret.sort(reverse=True)
        return ret


class UserType(Choices):
    STUDENT = 'student'
    TEACHER = 'teacher'
    SECRETARY = 'secretary'


class AlgorithmStatus(Choices):
    NEW = 'new'
    IDLE = 'idle'
    RUNNING = 'running'


class RequireDegree(Choices):
    HARD_ACCEPT = 10

    SOFT_ACCEPT_5 = 5
    SOFT_ACCEPT_4 = 4
    SOFT_ACCEPT_3 = 3
    SOFT_ACCEPT_2 = 2
    SOFT_ACCEPT_1 = 1

    SOFT_MEDIOCRE = 0

    SOFT_REJECT_1 = -1
    SOFT_REJECT_2 = -2
    SOFT_REJECT_3 = -3
    SOFT_REJECT_4 = -4
    SOFT_REJECT_5 = -5

    HARD_REJECT = -10


class FileType(Choices):
    DOC = 'docx/doc'
    EXCEL = 'excel'
    ALL = 'all'
    RAR = 'rar'


class ProStage(Choices):
    INIT = 'initial'
    MID = 'midterm'
    FIN = 'final'
    END = 'end'
    POSTPONE = 'postpone'


class ProType(Choices):
    SRTP = 'srtp'
    EDUCATION = 'education'
    GRADUATION = 'graduation'


class ProState(Choices):
    UNCONFIRMED = 'unconfirmed'
    APPLY_PASSED = 'apply_passed'
    MIDTERM_CHECKING = 'midterm_checking'
    MIDTERM_PASSED = 'midterm_passed'
    FINAL_CHEKING = 'final_checking'
    POSTPONE_UNCONFIRMED = 'postpone_unconfirmed'
    POSTPONED = 'postponed'
    DONE = 'done'
    TERMINATED = 'terminated'
    TERMINATE_UNCONFIRMED = 'terminate_unconfirmed'


class OperationCode(Choices):
    UPDATE = '000'
    UPLOAD_INT = '100'
    UPLOAD_MID = '101'
    UPLOAD_TER = '102'
    UPLOAD_POS = '103'
    UPLOAD_FIN = '104'
    CREATION_PASS = '201'
    MID_PASS = '202'
    FIN_PASS = '203'
    REJECT = '204'


class ProLevel(Choices):
    COLLEGE = u'院级'
    MUNICIPALPROMOTED = u'市级推荐级'
    NATIONALPROMOTED = u'国家推荐级'


ERROR_RESPONSE_STRING = {"error": "err", "data": "msg"}.__str__()
SUCCESS_RESPONSE_STRING = {"error": None, "data": "data"}.__str__()
