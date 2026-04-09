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

## Data Files (provided, don't need to modify)
- `course_catalog_CSE10_with_capacity.csv` -- 10 CSE courses with capacity
- `enrollments_CSE10.csv` -- enrollment records for those courses

---

## Submission Checklist
- [ ] All Python source files complete
- [ ] `test_milestone2.py` passing (38 tests)
- [ ] `milestone2_report.txt` complete
- [ ] `demo_milestone2.py` working end-to-end
