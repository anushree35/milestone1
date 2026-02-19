class Course: 
  def __init__(self, course_code: str, credits: int):
      self.course_code = course_code
      self.credits = credits
      self.students = []

  def add_student(self, student) -> None:
      for s in self.students:
          if getattr(s, "student_id", None) == getattr(student, "student_id", None):
                return
      self.students.append(student)

  def get_student_count(self) -> int:
      return len(self.students)
