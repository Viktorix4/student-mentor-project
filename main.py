class Student:
    """Класс для представления студента."""

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        """Выставляет оценку лектору за лекцию."""
        if (isinstance(lecturer, Lecturer)
                and course in lecturer.courses_attached
                and course in self.courses_in_progress
                and 1 <= grade <= 10):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def _average_grade(self):
        """Возвращает среднюю оценку за домашние задания."""
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0.0

    def __str__(self):
        """Строковое представление студента."""
        avg_grade = self._average_grade()
        courses_in_progress = ', '.join(self.courses_in_progress) or 'Нет'
        finished_courses = ', '.join(self.finished_courses) or 'Нет'
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {avg_grade}\n'
                f'Курсы в процессе изучения: {courses_in_progress}\n'
                f'Завершенные курсы: {finished_courses}')

    def __lt__(self, other):
        """Сравнение студентов по средней оценке (меньше)."""
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __eq__(self, other):
        """Сравнение студентов на равенство средней оценки."""
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() == other._average_grade()


class Mentor:
    """Родительский класс для преподавателей."""

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    """Класс лектора — наследуется от Mentor."""

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _average_grade(self):
        """Возвращает среднюю оценку за лекции."""
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0.0

    def __str__(self):
        """Строковое представление лектора."""
        avg_grade = self._average_grade()
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {avg_grade}')

    def __lt__(self, other):
        """Сравнение лекторов по средней оценке (меньше)."""
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __eq__(self, other):
        """Сравнение лекторов на равенство средней оценки."""
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() == other._average_grade()


class Reviewer(Mentor):
    """Класс эксперта, проверяющего домашние задания."""

    def rate_hw(self, student, course, grade):
        """Выставляет студенту оценку за домашнее задание."""
        if (isinstance(student, Student)
                and course in self.courses_attached
                and course in student.courses_in_progress
                and 1 <= grade <= 10):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        """Строковое представление проверяющего."""
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}')


# === ФУНКЦИИ ДЛЯ ЗАДАНИЯ №4 ===

def average_grade_students(students, course):
    """Средняя оценка за домашние задания по курсу среди студентов."""
    all_grades = []
    for student in students:
        if isinstance(student, Student) and course in student.grades:
            all_grades.extend(student.grades[course])
    if not all_grades:
        return 0.0
    return round(sum(all_grades) / len(all_grades), 1)


def average_grade_lecturers(lecturers, course):
    """Средняя оценка за лекции по курсу среди лекторов."""
    all_grades = []
    for lecturer in lecturers:
        if isinstance(lecturer, Lecturer) and course in lecturer.grades:
            all_grades.extend(lecturer.grades[course])
    if not all_grades:
        return 0.0
    return round(sum(all_grades) / len(all_grades), 1)


# === ПОЛЕВЫЕ ИСПЫТАНИЯ ===

if __name__ == '__main__':
    # --- Создание экземпляров ---

    # Студенты
    student1 = Student('Алиса', 'Селезнёва', 'женский')
    student1.courses_in_progress += ['Python', 'Git']
    student1.finished_courses += ['Введение в программирование']

    student2 = Student('Владимир', 'Путин', 'мужской')
    student2.courses_in_progress += ['Python', 'C++']
    student2.finished_courses += ['Алгоритмы']

    # Лекторы
    lecturer1 = Lecturer('Анна', 'Петрова')
    lecturer1.courses_attached += ['Python', 'Git']

    lecturer2 = Lecturer('Сергей', 'Сидоров')
    lecturer2.courses_attached += ['Python', 'C++']

    # Проверяющие
    reviewer1 = Reviewer('Иван', 'Иванов')
    reviewer1.courses_attached += ['Python']

    reviewer2 = Reviewer('Мария', 'Козлова')
    reviewer2.courses_attached += ['Git', 'C++']

    # --- Выставление оценок ---

    # Проверяющие оценивают студентов
    reviewer1.rate_hw(student1, 'Python', 10)
    reviewer1.rate_hw(student1, 'Python', 9)
    reviewer1.rate_hw(student2, 'Python', 8)

    reviewer2.rate_hw(student1, 'Git', 10)
    reviewer2.rate_hw(student2, 'C++', 7)

    # Студенты оценивают лекторов
    student1.rate_lecture(lecturer1, 'Python', 10)
    student1.rate_lecture(lecturer1, 'Git', 9)
    student2.rate_lecture(lecturer1, 'Python', 8)  # ошибка: student2 не учится на Git
    student2.rate_lecture(lecturer2, 'Python', 9)
    student2.rate_lecture(lecturer2, 'C++', 7)

    # --- Вывод через __str__ ---
    print("=== ПРОВЕРЯЮЩИЕ ===")
    print(reviewer1)
    print()
    print(reviewer2)
    print("\n=== ЛЕКТОРЫ ===")
    print(lecturer1)
    print()
    print(lecturer2)
    print("\n=== СТУДЕНТЫ ===")
    print(student1)
    print()
    print(student2)

    # --- Сравнение ---
    print("\n=== СРАВНЕНИЕ ===")
    print(f"Студент {student1.name} < {student2.name}? {student1 < student2}")
    print(f"Лектор {lecturer1.name} > {lecturer2.name}? {lecturer1 > lecturer2}")

    # --- Функции по курсам ---
    print("\n=== СРЕДНИЕ ОЦЕНКИ ПО КУРСАМ ===")
    students_list = [student1, student2]
    lecturers_list = [lecturer1, lecturer2]

    print(f"Средняя оценка студентов по курсу 'Python': "
          f"{average_grade_students(students_list, 'Python')}")
    print(f"Средняя оценка студентов по курсу 'Git': "
          f"{average_grade_students(students_list, 'Git')}")
    print(f"Средняя оценка лекторов по курсу 'Python': "
          f"{average_grade_lecturers(lecturers_list, 'Python')}")
    print(f"Средняя оценка лекторов по курсу 'C++': "
          f"{average_grade_lecturers(lecturers_list, 'C++')}")
    print(f"Средняя оценка лекторов по курсу 'Java' (нет оценок): "
          f"{average_grade_lecturers(lecturers_list, 'Java')}")