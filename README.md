Ownership split (who codes what)
Anushree owns: core system

Files Anushree edits:

course.py

university.py

(optional) loader.py part for courses

tests/test_course_university.py (or separate test files)

What Anushree needs to implement

Course

Fields:

course_code (string)

credits (int)

students (list of Student objects)

Methods:

add_student(student)

must prevent duplicates

best method: compare by student.student_id

get_student_count() → int

University

Fields:

students dict: student_id -> Student

courses dict: course_code -> Course

Methods:

add_course(course_code, credits)

prevent duplicate courses

add_student(student_id, name)

prevent duplicate students

get_course(course_code) (safe lookup, error if missing)

get_student(student_id) (safe lookup, error if missing)

get_course_enrollment(course_code) → number of students

get_students_in_course(course_code) → list of Student

Validation rules (Anushree owns these)

reject empty student names

reject empty/invalid IDs

prevent duplicates

handle “course not found” / “student not found” cleanly

Prudhvi owns: student + GPA + stats

Files Prudhvi edits:

student.py

stats.py

(optional) loader.py part for students/enrollments

tests/test_student_stats.py (or separate test files)

What Prudhvi needs to implement

Student

Fields:

student_id

name

courses mapping
Recommend: course_code -> grade (grade can be None if not set yet)

Methods:

enroll(course, grade=None)

must set student’s record

must also call course.add_student(self) (handshake rule)

update_grade(course, grade)

validate grade is allowed

error if student not enrolled

calculate_gpa(course_lookup)

weighted by credits

ignore None grades

Optional helpers (only if required by PDF):

get_courses()

get_course_info()

stats.py

mean, median, mode

stats for:

a single course’s grades

all student GPAs (mean/median)

(Exactly which stats you need depends on what the milestone PDF asks, but this is the usual set.)

Shared / integration work (do last, one person edits at a time)
loader.py (if required)

Split responsibilities but avoid both editing the same file at once.

Anushree writes: load_course_catalog(csv_path, uni)

Prudhvi writes: load_students(csv_path, uni)

main.py

Only for:

creating University()

calling loaders

running the required queries and printing results

Best move: pick one person to own main.py to avoid conflicts.

Big warning since you’re not using branches

Because you’re on main, you cannot both edit the same file at the same time. If you do, one person will overwrite the other or you’ll get merge conflicts.

Simple rule that prevents 99% of problems:

Anushree edits only course.py, university.py (and maybe a course loader)

Prudhvi edits only student.py, stats.py (and maybe a student loader)

Only one person edits main.py / loader.py at any given time

Before pushing changes:

refresh the GitHub page (web editor) or git pull (local)

then commit + push

Minimal checklist to finish Milestone 1

Anushree finishes Course + University

Prudhvi finishes Student + GPA + stats

Agree on the “handshake” behavior:

Student.enroll() always calls Course.add_student()

Course.add_student() blocks duplicates by student_id

Add loader.py if CSV loading is required

Make main.py demonstrate required queries

Write tests for each file owner’s code

Run tests once at the end (pytest or whatever you’re using)
