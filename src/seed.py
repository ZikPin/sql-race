from faker import Faker


class Entity:
    fk: Faker

    def __init__(self):
        self.fk = Faker()

    def print_attributes(self):
        attributes = self.__annotations__
        result_entry = []

        for attribute in attributes.keys():
            if attribute == "name":
                result_entry.append(self.fk.name())
            elif attribute == "email":
                result_entry.append(self.fk.email())

        return tuple(result_entry)


class Student(Entity):
    name: str
    email: str
    enrollment_date: str
    birth_date: str
    department_id: int


class Room(Entity):
    has_projector: bool
    capacity: int
    building: str


class Department(Entity):
    name: str
    faculty: str
    office_location: int # room_id


class Professor(Entity):
    hire_date: str
    email: str
    name: str
    

entity = Student()
print(entity.fk.__doc__)