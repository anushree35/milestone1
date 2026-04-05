import csv
import datetime
from student import Student
from course import Course


class University:
    """
    Manages a collection of students and courses.

    Loads data from:
      - course catalog CSV (with capacity)
      - enrollments CSV
      - (optional) full university student CSV
    """

    def __init__(self, name="UConn"):
        self.name = name
        self.students = {}  # student_id -> Student
        self.courses = {}   # course_id -> Course

    # --- Loaders ---

    def load_course_catalog(self, filepath):
        """Load courses from a CSV with columns: course_id, course_title, credits, department, capacity."""
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                course_id = row['course_id'].strip()
                self.courses[course_id] = Course(
                    course_id=course_id,
                    title=row['course_title'].strip(),
                    credits=int(row['credits']),
                    department=row['department'].strip(),
                    capacity=int(row['capacity']),
                )

    def load_students(self, filepath):
        """Load students from the university_data CSV (columns: student_id, name, ...)."""
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sid = row['student_id'].strip()
                name = row['name'].strip()
                self.students[sid] = Student(sid, name)

    def load_enrollments(self, filepath, default_date="2026-01-15"):
        """
        Load enrollment records from the CSE10 enrollments CSV.
        Columns: student_id, course_id, term, grade, attempt

        Students not already loaded are created automatically.
        The CSV has no enroll_date column, so default_date is used.
        """
        enroll_date = datetime.date.fromisoformat(default_date)
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sid = row['student_id'].strip()
                cid = row['course_id'].strip()

                # Auto-create student if not already loaded
                if sid not in self.students:
                    self.students[sid] = Student(sid, sid)  # name defaults to ID

                if cid not in self.courses:
                    continue  # skip courses not in our catalog

                self.courses[cid].request_enroll(self.students[sid], enroll_date)

    # --- Operations ---

    def enroll_student(self, student_id, course_id, enroll_date=None):
        """Enroll a student in a course. Creates student if unknown."""
        if student_id not in self.students:
            raise KeyError(f"Student {student_id} not found.")
        if course_id not in self.courses:
            raise KeyError(f"Course {course_id} not found.")
        date = enroll_date or datetime.date.today()
        self.courses[course_id].request_enroll(self.students[student_id], date)

    def drop_student(self, student_id, course_id, enroll_date_for_replacement=None):
        """Drop a student from a course."""
        if course_id not in self.courses:
            raise KeyError(f"Course {course_id} not found.")
        self.courses[course_id].drop(student_id, enroll_date_for_replacement)

    def add_student(self, student_id, name):
        """Register a new student."""
        self.students[student_id] = Student(student_id, name)
        return self.students[student_id]

    # --- Reporting ---

    def print_course_summary(self, course_id):
        if course_id not in self.courses:
            print(f"Course {course_id} not found.")
            return
        c = self.courses[course_id]
        print(f"\n{c.course_id}: {c.title}")
        print(f"  Enrolled: {c.enrollment_count()}/{c.capacity}  |  Waitlist: {c.waitlist_count()}")
        for rec in c.enrolled_roster:
            print(f"    {rec.student.student_id}  {rec.student.name}  {rec.enroll_date}")

    def __repr__(self):
        return f"University({self.name}, students={len(self.students)}, courses={len(self.courses)})"
