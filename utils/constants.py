class Choices:
    @classmethod
    def choices(cls):
        d = cls.__dict__
        return [d[item] for item in d.keys() if not item.startswith("__")]

    @classmethod
    def model_choices(cls):
        d = cls.__dict__
        return [(d[item], d[item]) for item in d.keys() if not item.startswith("__")]


class UserType(Choices):
    TEACHER = 'teacher'
    STUDENT = 'student'
    SECRETARY = 'secretary'



