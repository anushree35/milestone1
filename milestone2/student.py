class Student:

    GRADE_POINTS = {
        'A' : 4.0, 'A-' : 3.7,
        'B+': 3.3, 'B' : 3.0, 'B-' : 2.7,
        'C+': 2.3, 'C' : 2.0, 'C-' : 1.7,
        'D' : 1.0,
        'F' : 0.0
    }

    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.courses = {}

    def enroll(self, course, grade):
        if grade not in Student.GRADE_POINTS:
            raise ValueError(f"Invalid grade '{grade}' for course {course.course_code}")
        self.courses[course] = grade
        course.add_student(self)

    def update_grade(self, course, grade):
        if course in self.courses:
            self.courses[course] = grade

    def calculate_gpa(self):
        total_points = 0
        total_credits = 0
        for course, grade in self.courses.items():
            credits = course.credits          
            grade_points = Student.GRADE_POINTS.get(grade, 0)
            total_points += grade_points * credits
            total_credits += credits
        if total_credits == 0:
            return 0.0
        return total_points / total_credits

    def get_courses(self):
        return list(self.courses.keys())

    def get_course_info(self):
        info = []
        for course, grade in self.courses.items():
            info.append({
                "course_code": course.course_code,
                "credits": course.credits,
                "grade": grade
            })
        return info

    def __repr__(self):
        return f"Student(id={self.student_id}, name={self.name})"
