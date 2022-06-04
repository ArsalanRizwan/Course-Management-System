
class Course:
    __Id = None
    __CourseName = None
    __CreditHours = None

    def get_Id(self):
        return self.__Id

    def get_course_name(self):
        return self.__CourseName

    def get_credit_hours(self):
        return self.__CreditHours

    def set_Id(self,id):
        self.__Id = id

    def set_course_name(self, nm):
        self.__CourseName = nm

    def set_credit_hours(self,hrs):
        self.__CreditHours = hrs

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)

        return cls.instance