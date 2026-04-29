import csv
import datetime
from student import Student
from course import Course, PrerequisiteError


class University:
    """
    Manages students and courses.
    Loads course catalog, enrollments, and prerequisite data.
    """

    def __init__(self, name="UConn"):
        self.name = name
        self.students = {}
        self.courses = {}

    def load_course_catalog(self, filepath):
        """Load courses from CSV: course_id, course_title, credits, department, capacity."""
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
        """Load students from CSV: student_id, name."""
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sid = row['student_id'].strip()
                name = row['name'].strip()
                self.students[sid] = Student(sid, name)

    def load_enrollments(self, filepath, default_date="2026-01-15"):
        """
        Load enrollments from CSV: student_id, course_id, ...
        Auto-creates students if not already loaded.
        Skips prerequisite check during bulk load (historical data).
        """
        enroll_date = datetime.date.fromisoformat(default_date)
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sid = row['student_id'].strip()
                cid = row['course_id'].strip()

                if sid not in self.students:
                    self.students[sid] = Student(sid, sid)

                if cid not in self.courses:
                    continue

                # Bypass prereq check during bulk historical load
                course = self.courses[cid]
                already = any(r.student.student_id == sid
                              for r in course.enrolled_roster)
                if not already:
                    if len(course.enrolled_roster) < course.capacity:
                        from enrollment_record import EnrollmentRecord
                        course.enrolled_roster.append(
                            EnrollmentRecord(self.students[sid], enroll_date)
                        )
                    else:
                        course.waitlist.enqueue(self.students[sid])

                # Mark as taken for prerequisite purposes
                self.students[sid].complete_course(cid)

    def load_prerequisites(self, filepath):
        """
        Load prerequisite data from CSV.
        Expected columns: course_id, prerequisite_id
        'NONE' or blank prerequisite_id means no prerequisite.
        """
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cid = row['course_id'].strip()
                prereq = row.get('prerequisite_id', row.get('prerequisite', '')).strip()
                if cid in self.courses:
                    self.courses[cid].set_prerequisite(prereq)

    def enroll_student(self, student_id, course_id, enroll_date=None):
        """Enroll a student -- checks prerequisites."""
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

    def print_course_summary(self, course_id):
        if course_id not in self.courses:
            print(f"Course {course_id} not found.")
            return
        c = self.courses[course_id]
        prereqs = [pid for pid, _ in c.prerequisite.items()] if c.has_prerequisite() else ['None']
        print(f"\n{c.course_id}: {c.title}")
        print(f"  Prerequisites: {', '.join(prereqs)}")
        print(f"  Enrolled: {c.enrollment_count()}/{c.capacity}  |  Waitlist: {c.waitlist_count()}")
        for rec in c.enrolled_roster:
            print(f"    {rec.student.student_id}  {rec.student.name}  {rec.enroll_date}")

    def __repr__(self):
        return f"University({self.name}, students={len(self.students)}, courses={len(self.courses)})"
