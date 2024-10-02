class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def average_grade(self):
        total_grades = 0
        total_count = 0
        for grades in self.grades.values():
            total_grades += sum(grades)
            total_count += len(grades)
        return total_grades / total_count if total_count > 0 else 0

    def __str__(self):
        avg_grade = self.average_grade()
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {avg_grade:.1f}\n'
                f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
                f'Завершенные курсы: {", ".join(self.finished_courses)}')

    def __lt__(self, other):
        if isinstance(other, Student):
            return self.average_grade() < other.average_grade()
        return NotImplemented


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average_grade(self):
        total_grades = 0
        total_count = 0
        for grades in self.grades.values():
            total_grades += sum(grades)
            total_count += len(grades)
        return total_grades / total_count if total_count > 0 else 0

    def __str__(self):
        avg_grade = self.average_grade()
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {avg_grade:.1f}')

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            return self.average_grade() < other.average_grade()
        return NotImplemented


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.finished_courses:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


def average_student_grade(students, course):
    total_grades = 0
    total_count = 0
    for student in students:
        if course in student.grades:
            total_grades += sum(student.grades[course])
            total_count += len(student.grades[course])
    return total_grades / total_count if total_count > 0 else 0


def average_lecturer_grade(lecturers, course):
    total_grades = 0
    total_count = 0
    for lecturer in lecturers:
        if course in lecturer.grades:
            total_grades += sum(lecturer.grades[course])
            total_count += len(lecturer.grades[course])
    return total_grades / total_count if total_count > 0 else 0


# Создание экземпляров классов
student1 = Student('Ruoy', 'Eman', 'male')
student1.courses_in_progress += ['Python']
student1.finished_courses += ['Введение в программирование']

student2 = Student('Jane', 'Doe', 'female')
student2.courses_in_progress += ['Python']
student2.finished_courses += ['Введение в программирование']

reviewer1 = Reviewer('Some', 'Buddy')
reviewer1.courses_attached += ['Python']
reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student2, 'Python', 8)
reviewer1.rate_hw(student2, 'Python', 7)

reviewer2 = Reviewer('Thomas', 'Shelby')
reviewer2.courses_attached += ['Python']
reviewer2.rate_hw(student1, 'Python', 8)
reviewer2.rate_hw(student2, 'Python', 6)

lecturer1 = Lecturer('John', 'Doe')
lecturer1.courses_attached += ['Python']
student1.rate_lecturer(lecturer1, 'Python', 8)
student2.rate_lecturer(lecturer1, 'Python', 9)

lecturer2 = Lecturer('Alice', 'Smith')
lecturer2.courses_attached += ['Python']
student1.rate_lecturer(lecturer2, 'Python', 10)
student2.rate_lecturer(lecturer2, 'Python', 7)

# Вывод информации о студентах, лекторах и проверяющих
print(student1)
print(student2)
print(reviewer1)
print(reviewer2)
print(lecturer1)
print(lecturer2)

# Подсчет средней оценки за домашние задания по всем студентам в рамках курса
students = [student1, student2]
average_hw = average_student_grade(students, 'Python')
print(f'Средняя оценка за домашние задания по курсу Python: {average_hw:.1f}')

# Подсчет средней оценки за лекции всех лекторов в рамках курса
lecturers = [lecturer1, lecturer2]
average_lectures = average_lecturer_grade(lecturers, 'Python')
print(f'Средняя оценка за лекции по курсу Python: {average_lectures:.1f}')