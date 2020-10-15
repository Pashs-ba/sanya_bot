class User:
    def __init__(self, id: int, name, surname, nickname):
        self.id = id
        self.nickname = nickname
        self.name = name
        self.surname = surname
        self.to_print = {'id': self.id,
                         'name': self.name,
                         'surname': self.surname,
                         'nickname': self.nickname}

    def __str__(self):
        return str(self.to_print)

    def get_data(self):
        return self.to_print


class Admin(User):
    pass


class Student(User):
    def __init__(self, id: int, name, surname, nickname):
        super().__init__(id, name, surname, nickname)
        self.lesson = 0
        self.group = []
        self.to_print.update({'Number of lesson': self.lesson,
                              'Groups': self.group})
