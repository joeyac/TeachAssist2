class Choices:
    @classmethod
    def choices(cls):
        d = cls.__dict__
        return [d[item] for item in d.keys() if not item.startswith("__")]

    @classmethod
    def model_choices(cls):
        d = cls.__dict__
        return [(d[item], item) for item in d.keys() if not item.startswith("__")]


class UserType(Choices):
    STUDENT = 'student'
    TEACHER = 'teacher'
    SECRETARY = 'secretary'


class RequireDegree(Choices):
    MOST = 5
    SECOND = 4
    ACCEPT = 3
    MEDIOCRE = 2
    LEAST = 1
    REJECT = -10


class FileType(Choices):
    DOC = 'docx/doc'
    EXCEL = 'excel'
    ALL = 'all'
    RAR = 'rar'


class ProStage(Choices):
    INIT = 'initial'
    MID = 'midterm'
    FIN = 'final'


class ProType(Choices):
    SRTP = 'srtp'
    EDUCATION = 'education'
    GRADUATION = 'graduation'


class ProState(Choices):
    APPLYING = 'apllying'
    APPLY_PASSED = 'apply_passed'
    MIDTERM_CHECKING = 'midterm_checking'
    MIDTERM_PASSED = 'midterm_passed'
    FINAL_CHEKING = 'final_checking'
    POSTPONED = 'postponed'
    DONE = 'done'
    ABANDONED = 'abandoned'


class ProLevel(Choices):
    COLLEGE = u'院级'
    MUNICIPALPROMOTED = u'市级推荐级'
    NATIONALPROMOTED = u'国家推荐级'


ERROR_RESPONSE_STRING = {"error": "err", "data": "msg"}.__str__()
SUCCESS_RESPONSE_STRING = {"error": None, "data": "data"}.__str__()
