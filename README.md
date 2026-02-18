Here’s a clean way to split Milestone 1 so both people have real ownership, minimal merge pain, and you still hit every requirement in the PDF. 

## Split by “modules” (best for avoiding conflicts)

### Anushree: **Course + University (core manager)**

Owns:

* `Course` class

  * fields: `course_code`, `credits`, `students` list
  * methods: `add_student()`, `get_student_count()` 
* `University` class

  * fields: `students` dict, `courses` dict
  * methods: `add_course()`, `add_student()`, `get_student()`, `get_course()`,
    `get_course_enrollment()`, `get_students_in_course()` 
* Validation helpers that logically belong to “system-level rules”

  * reject invalid IDs / empty names, prevent duplicates, safe lookups 

Deliverables Person A writes:

* `course.py` (Course)
* `university.py` (University)
* Unit tests for Course + University test cases listed 

---

### Prudhvi: **Student + GPA + stats**

Owns:

* `Student` class

  * fields: `student_id`, `name`, `courses` dict mapping `Course -> grade`
  * methods: `enroll()`, `update_grade()`, `calculate_gpa()`, `get_courses()`, `get_course_info()` 
* Grade validation + grade-point mapping (GPA logic must be weighted by credits) 
* “Stats” functions for:

  * mean/median/mode for a course (based on grades or GPA-equivalent per course, depending on how your TA expects it)
  * mean/median of all student GPAs 

Deliverables Person B writes:

* `student.py` (Student)
* `stats.py` (course + university stats helper functions)
* Unit tests for Student test cases listed 

---

## Shared (pair-program or assign “driver”)

### CSV loading + demo script

The PDF requires loading both CSVs into a `University` object and supporting specific queries. 

A good split:

* Person A writes: `load_course_catalog(csv_path, university)` (creates courses)
* Person B writes: `load_students(csv_path, university)` (creates students + enrollments)
* Then you merge into `main.py` that demonstrates required queries.

---

## File structure (simple and Gradescope-friendly)

* `course.py`
* `student.py`
* `university.py`
* `stats.py`
* `loader.py`
* `main.py` (runs the demo queries)
* `test_project.py` (all tests in one place is fine)
* `README.md`

---

## Super important “handshake rules” to agree on early

To prevent bugs where enrollments don’t match both sides:

* `Student.enroll(course, grade)` should also call `course.add_student(self)` (so both objects reflect the relationship). 
* Decide whether `Course.students` prevents duplicates by:

  * checking `if student not in self.students`, or
  * checking by `student.student_id` (more reliable)

---

If you want, paste your current repo/file layout (or just what files you already created), and I’ll map this split onto exactly what you have so you don’t redo work.
