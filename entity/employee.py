class Employee:
    def __init__(self, employee_id=None, name=None, department=None, email=None, password=None):
        self.__employee_id = employee_id
        self.__name = name
        self.__department = department
        self.__email = email
        self.__password = password

    # Getters
    @property
    def employee_id(self):
        return self.__employee_id

    @property
    def name(self):
        return self.__name

    @property
    def department(self):
        return self.__department

    @property
    def email(self):
        return self.__email

    @property
    def password(self):
        return self.__password

    # Setters
    @employee_id.setter
    def employee_id(self, value):
        self.__employee_id = value

    @name.setter
    def name(self, value):
        self.__name = value

    @department.setter
    def department(self, value):
        self.__department = value

    @email.setter
    def email(self, value):
        self.__email = value

    @password.setter
    def password(self, value):
        self.__password = value