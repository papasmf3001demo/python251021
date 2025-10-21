# 상속02.py

class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        #f-string문법을 사용 
        print(f"ID: {self.id}, Name: {self.name}")


class Manager(Person):
    def __init__(self, id, name, title):
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        super().printInfo()
        print(f"Title: {self.title}")


class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        super().printInfo()
        print(f"Skill: {self.skill}")


# 인스턴스 10개 생성 및 출력
people = [
    Person(1, "Alice"),
    Manager(2, "Bob", "General Manager"),
    Employee(3, "Charlie", "Python"),
    Manager(4, "Diana", "Project Manager"),
    Employee(5, "Eve", "Java"),
    Person(6, "Frank"),
    Employee(7, "Grace", "C++"),
    Manager(8, "Heidi", "HR Manager"),
    Person(9, "Ivan"),
    Employee(10, "Judy", "Go"),
]

for p in people:
    p.printInfo()
    print("-" * 30)