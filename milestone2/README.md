Milestone 3 -- University/Course/Student System
CSE 2050 | Spring 2026 | Anushree & Prudhvi
What We Built
For Milestone 3 we added prerequisite checking to the enrollment system, swapped out the quadratic sorting algorithms for merge sort and quick sort, and built a HashMap from scratch to store the prerequisite data.

Who Did What
Prudhvi

hashmap.py -- HashMap with separate chaining and rehashing at 80% load factor
sorting.py -- merge sort and quick sort, works for sorting by name, id, or date
test_milestone3.py -- tests for HashMap and sorting

Anushree

course.py -- added prerequisite field and updated enrollment to check prerequisites before adding to roster or waitlist
student.py -- added courses_taken tracking and complete_course() method
university.py -- added load_prerequisites() to wire in the CSV data
test_milestone3.py -- tests for prerequisite enrollment logic
milestone3_report.txt -- complexity analysis
demo_milestone3.py -- full demo script


How to Run
bashcd milestone3
python3 demo_milestone3.py
python3 -m unittest test_milestone3 -v

Data Files

cse_prerequisites.csv
course_catalog_CSE10_with_capacity.csv
enrollments_CSE10.csv
