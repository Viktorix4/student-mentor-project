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


# --- Примеры использования (для проверки) ---
if __name__ == '__main__':
    # Студент
    student = Student('Ruoy', 'Eman', 'your_gender')
    student.courses_in_progress += ['Python', 'Git']
    student.finished_courses += ['Введение в программирование']

    # Лектор
    lecturer = Lecturer('Some', 'Buddy')
    lecturer.courses_attached += ['Python']
    student.rate_lecture(lecturer, 'Python', 10)
    student.rate_lecture(lecturer, 'Python', 9)

    # Проверяющий
    reviewer = Reviewer('Cool', 'Mentor')
    reviewer.courses_attached += ['Python']
    reviewer.rate_hw(student, 'Python', 10)
    reviewer.rate_hw(student, 'Python', 9)

    # Вывод через __str__
    print(reviewer)
    print()
    print(lecturer)
    print()
    print(student)
    print()

    # Сравнение
    student2 = Student('Jane', 'Doe', 'female')
    student2.courses_in_progress += ['Python']
    reviewer.rate_hw(student2, 'Python', 8)

    lecturer2 = Lecturer('Ivan', 'Ivanov')
    lecturer2.courses_attached += ['Python']
    student2.rate_lecture(lecturer2, 'Python', 7)

    print(f'Студент {student.name} < {student2.name}? {student < student2}')  # False
    print(f'Лектор {lecturer.name} > {lecturer2.name}? {lecturer > lecturer2}')  # True