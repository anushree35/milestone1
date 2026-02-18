# Milestone 1 Plan + Ownership Split (with CSV loading)

This project builds a small university system with three core pieces: **Course**, **Student**, and **University**, plus basic stats and **CSV loading using `csv.DictReader`**.

## CSV loading requirement (what we’re doing)

We will load data from CSVs using:

* `csv.DictReader(f)` so each row is a **dictionary**
* Access fields by header name, like `row["course_code"]`
* Convert types when needed, like `int(row["credits"])`

**Expected course catalog CSV headers (typical):**

* `course_code`
* `credits`

**Expected student/enrollment CSV headers (typical):**

* `student_id`
* `name`
* `course_code`
* `grade` (may be blank → treat as `None`)

If the class CSV headers are different, we will update `loader.py` to match the exact header names.

---

## Ownership split (who codes what)

### Anushree owns: core system

**Files Anushree edits:**

* `course.py`
* `university.py`
* (optional) `loader.py` part for courses
* `tests/test_course_university.py` (or separate test files)

### What Anushree needs to implement

#### `Course`

**Fields**

* `course_code` (string)
* `credits` (int)
* `students` (list of `Student` objects)

**Methods**

* `add_student(student)`

  * must prevent duplicates
  * best method: compare by `student.student_id`
* `get_student_count()` → int

#### `University`

**Fields**

* `students` dict: `student_id -> Student`
* `courses` dict: `course_code -> Course`

**Methods**

* `add_course(course_code, credits)`

  * prevent duplicate courses
* `add_student(student_id, name)`

  * prevent duplicate students
* `get_course(course_code)` (safe lookup, error if missing)
* `get_student(student_id)` (safe lookup, error if missing)
* `get_course_enrollment(course_code)` → number of students
* `get_students_in_course(course_code)` → list of `Student`

#### Validation rules (Anushree owns these)

* reject empty student names
* reject empty/invalid IDs
* prevent duplicates
* handle “course not found” / “student not found” cleanly

---

### Prudhvi owns: student + GPA + stats

**Files Prudhvi edits:**

* `student.py`
* `stats.py`
* (optional) `loader.py` part for students/enrollments
* `tests/test_student_stats.py` (or separate test files)

### What Prudhvi needs to implement

#### `Student`

**Fields**

* `student_id`
* `name`
* `courses` mapping
  Recommend: `course_code -> grade` (grade can be `None` if not set yet)

**Methods**

* `enroll(course, grade=None)`

  * must set student’s record
  * must also call `course.add_student(self)` (handshake rule)
* `update_grade(course, grade)`

  * validate grade is allowed
  * error if student not enrolled
* `calculate_gpa(course_lookup)`

  * weighted by credits
  * ignore `None` grades

**Optional helpers (only if required by PDF)**

* `get_courses()`
* `get_course_info()`

#### `stats.py`

* `mean`, `median`, `mode`
* stats for:

  * a single course’s grades
  * all student GPAs (mean/median)

(Exact stats depend on the PDF, but this is the standard set.)

---

## Shared / integration work (do last, one person edits at a time)

### `loader.py` (if required)

Split responsibilities but avoid both editing the same file at once:

* Anushree writes: `load_course_catalog(csv_path, uni)`

  * uses `csv.DictReader`
  * reads `course_code`, `credits`
  * calls `uni.add_course(...)`

* Prudhvi writes: `load_students(csv_path, uni)`

  * uses `csv.DictReader`
  * reads `student_id`, `name`, `course_code`, `grade`
  * calls `uni.add_student(...)`, then `student.enroll(course, grade)`

### `main.py`

Only for:

* creating `University()`
* calling loaders
* running the required queries and printing results

Best move: pick **one person** to own `main.py` to avoid conflicts.

---

## Big warning (no branches)

Because we’re working directly on `main`, we **cannot both edit the same file at the same time**. If we do, someone will overwrite the other person’s work or we’ll hit merge conflicts.

**Simple rule that prevents problems**

* Anushree edits only `course.py`, `university.py` (and maybe course loader)
* Prudhvi edits only `student.py`, `stats.py` (and maybe student loader)
* Only one person edits `main.py` / `loader.py` at any given time

Before pushing changes:

* refresh GitHub (web editor) or `git pull` (local)
* then commit + push

---

## Minimal checklist to finish Milestone 1

* Anushree finishes `Course` + `University`
* Prudhvi finishes `Student` + GPA + stats
* Agree on handshake behavior:

  * `Student.enroll()` always calls `Course.add_student()`
  * `Course.add_student()` blocks duplicates by `student_id`
* Add `loader.py` (CSV loading with `csv.DictReader`) if required
* Make `main.py` demonstrate required queries
* Write tests for each file owner’s code
* Run tests once at the end (pytest or course runner)
