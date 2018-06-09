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


ERROR_RESPONSE_STRING = {"error": "err", "data": "msg"}.__str__()
SUCCESS_RESPONSE_STRING = {"error": None, "data": "data"}.__str__()
