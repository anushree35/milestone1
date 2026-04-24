# Milestone 3 -- University/Course/Student System with HashMap & Prerequisites

CSE 2050 | Spring 2026 | Group Project

## Overview

Milestone 3 extends the Milestone 2 system with:
- A HashMap (separate chaining + rehashing at 80% load factor) to store prerequisite data
- Prerequisite verification before student enrollment
- Merge Sort and Quick Sort to replace quadratic sorting algorithms
- Full unit test suite and complexity report

---

## File Responsibilities

### Prudhvi
| File | Description |
|---|---|
| `hashmap.py` | HashMap class -- `put`, `get`, `__contains__`, `_hash`, `_rehash`, separate chaining, load factor check |
| `sorting.py` | `merge_sort()` and `quick_sort()` -- support sort by name, id, and date; replace insertion/selection sort |
| `test_milestone3.py` (partial) | Unit tests for HashMap (collision handling, rehashing) and both sorting algorithms |

### Anushree
| File | Description |
|---|---|
| `course.py` | Updated Course class -- adds `prerequisite` HashMap field, loads `cse_prerequisites.csv`, updates `request_enroll()` to check prerequisites before enrolling/waitlisting |
| `student.py` | Updated Student class -- adds `courses_taken` field and `complete_course()` method for prerequisite tracking |
| `university.py` | Updated University -- wires prerequisite loading into existing data loading pipeline |
| `test_milestone3.py` (partial) | Unit tests for enrollment with and without prerequisites met |
| `milestone3_report.txt` | Big-O complexity report for HashMap put/get and both sorting algorithms, with Merge vs Quick sort comparison |
| `demo_milestone3.py` | Demo script showing full Milestone 3 workflow including all previous milestone demos |

---

## How to Run

### Load data and run demo
```bash
cd milestone3
python3 demo_milestone3.py
```

### Run tests
```bash
cd milestone3
python3 -m unittest test_milestone3 -v
```

---

## Data Files (provided, don't need to modify)
- `cse_prerequisites.csv` -- prerequisite requirements for each CSE course
- `course_catalog_CSE10_with_capacity.csv` -- carry over from Milestone 2
- `enrollments_CSE10.csv` -- carry over from Milestone 2

---

## Submission Checklist
- [ ] All Python source files complete
- [ ] `test_milestone3.py` passing
- [ ] `milestone3_report.txt` complete
- [ ] `demo_milestone3.py` working end-to-end
