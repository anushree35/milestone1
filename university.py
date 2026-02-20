class University:
  def __init__(self):
              self.students = {}
              self.courses = {}

  def  add_course(self, course_code, credits) -> None:
    if course_code not in self.courses:
      self.courses[course_code] = Course(course_code, credits)
      return self.courses[course_code]

  def add_student(self, student_id, name) -> None:
    if student_id not in self.students:
      self.students[student_id] = Student(student_id, name)
      return self.students[student_id]

  def  get_student(self, student_id) -> None:
      return self.students(student_id)

  def  get_course(self, course_code) -> None:
      return self.courses(course_code)

  def get_course_enrollment(self, course_code):
    return self.get_course(course_code).get_student_count()

  def get_students_in_course(self, course_code):
    return self.get_course(course_code).students
