import random
import string


class Person:
    lastName = ""
    firstName = ""
    patronymic = ""
    position = 0
    project = ""
    expire = ""
    future = ""
    nickname = ""
    fired = False


def get_random_person():
    person = Person()
    person.lastName = random_word(7)
    person.firstName = random_word(6)
    person.patronymic = random_word(5)
    person.position = random.randint(0, 3)
    person.project = random_word(9)
    person.expire = str(round(2*random.random(), 1))
    person.future = random_word(10)
    person.nickname = random_word(5)
    return person


def random_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def compare_persons(person_a, person_b):
    if (person_a.lastName == person_b.lastName) & (person_a.firstName == person_b.firstName):
        return True
    return False

