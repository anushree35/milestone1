# Project Milestone #1

### How to Run the Program

Make sure `university_data.csv` and `course_catalog.csv` are in the same folder as the source files, then run:

```bash
python main.py
```

This will load all the data and print out course rosters, student GPAs, grade stats, and university-wide GPA info.

---

### How to Run the Tests

To test the Student class:
```bash
python tests/test_student.py
```

To test the Course and University classes:
```bash
python tests/test_course_university.py
```

---

### Project Structure

- `student.py` — Student class, enrollment, GPA calculation (Prudhvi)
- `course.py` — Course class, student roster (Anushree)
- `university.py` — manages all students and courses (Anushree)
- `loader.py` — loads data from CSV files (Anushree & Prudhvi)
- `stats.py` — mean, median, mode functions (Prudhvi)
- `main.py` — runs the demo queries (Anushree & Prudhvi)


# Milestone 2 -- University/Course/Student System

CSE 2050 | Spring 2026 | Group Project

## Overview

Milestone 2 extends the Milestone 1 system with:
- Enrollment capacity and a linked-list waitlist (FIFO)
- Sorting the enrolled roster by name, ID, or date
- Recursive binary search for efficient drop operations
- Full unit test suite

---

## File Responsibilities

### Anushree
| File | Description |
|---|---|
| `course.py` | Updated Course class -- capacity, waitlist logic, sort_enrolled(), drop() using binary search |
| `university.py` | Updated University -- loads CSE10 catalog + enrollments, connects enroll/drop to Course |
| `test_milestone2.py` | Full unittest suite covering all Milestone 2 features |
| `milestone2_report.txt` | Big-O complexity report for queue, sorting, and binary search |

### Prudhvi
| File | Description |
|---|---|
| `linked_queue.py` | Node class + LinkedQueue ADT (enqueue, dequeue, is_empty, __len__) |
| `enrollment_record.py` | EnrollmentRecord class (student + enroll_date) |
| `sorting.py` | insertion_sort(), selection_sort(), recursive_binary_search() |
| `student.py` | Student class (carry over from M1, minimal changes) |
| `demo_milestone2.py` | Demo script showing full workflow |

---

## How to Run

### Load data and run demo
```bash
cd milestone2
python3 demo_milestone2.py
```

### Run tests
```bash
cd milestone2
python3 -m unittest test_milestone2 -v
```

---

## Data Files (provided, do not modify)
- `course_catalog_CSE10_with_capacity.csv` -- 10 CSE courses with capacity
- `enrollments_CSE10.csv` -- enrollment records for those courses

---

## Submission Checklist
- [ ] All Python source files complete
- [ ] `test_milestone2.py` passing (38 tests)
- [ ] `milestone2_report.txt` complete
- [ ] `demo_milestone2.py` working end-to-end
