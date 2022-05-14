def info(function):
    def wrapper(self, extra):
        print("================")
        function(self, extra)
        print("================")
    return wrapper



class Student:
    count = 0

    def __init__(self, firstname, lastname, index, specialization):
        self.firstname = firstname
        self.lastname = lastname
        self.index = index
        self.specialization = specialization
        Student.count += 1

    def __del__(self):
        Student.count -= 1

    def __str__(self):
        return F"{self.firstname} {self.lastname} {self.index}: {self.specialization}"

    def __gt__(self, student):
        return (self.firstname + self.lastname) > (student.firstname + student.lastname)

    def __ge__(self, student):
        return (self.firstname + self.lastname) >= (student.firstname + student.lastname)

    def __lt__(self, student):
        return (self.firstname + self.lastname) < (student.firstname + student.lastname)

    def __le__(self, student):
        return (self.firstname + self.lastname) <= (student.firstname + student.lastname)

    def __eq__(self, student):
        return (self.firstname + self.lastname) == (student.firstname + student.lastname)

    @info
    def __call__(self, extra):
        print(extra)



class StudentIT(Student):
    def __init__(self, firstname, lastname, index):
        super().__init__(firstname, lastname, index, "IT")

    def __del__(self):
        super().__del__()


def main():
    print("Z1")
    student1 = Student("Michał", "Miętkiewski", 20000, "IT")
    print(student1)
    print()

    print("Z4")
    student2 = StudentIT("Piotr", "Kiryczuk", 19998)
    print(student2)
    print()

    print("Z2")
    print(student1 > student2)
    print(student1 >= student2)
    print(student1 < student2)
    print(student1 <= student2)
    print(student1 == student2)
    print()

    print("Z3")
    print(F"Count: {Student.count}")
    print()

    print("Z5")
    student1("Hello World!")
    print()



if __name__ == "__main__":
    main()
