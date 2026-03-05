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
