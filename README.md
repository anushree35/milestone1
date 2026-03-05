# Project Milestone #1
-----------------------

### **How to Run the Program**

To see the system in action with the provided university data, run the main demonstration script:

1. First you need to make sure that `university_data.csv` and `course_catalog.csv` are in the same directory as the source files.


2. Then run the following command in your terminal:
```bash
python main.py

```



The script will load the data and output course rosters, student GPAs, course grade stats, and the university-wide GPA trends .

---

### **How to Run the Tests**

#### **1. Test the Student Class Functionality**

To run the unit tests specifically for the `Student` class:

```bash
python test_student.py

```

This tests create objects for creation, enrollment, and GPA calculations .

#### **2. Testing Course and University Functionality**

To run the tests for the `Course` and `University` classes:

```bash
python test_course_university.py

```

This makes that courses track students correctly, stops any duplicate entries, and makes sure that the data is collected accurately .

---

### **Project Structure**

* 
**`student.py`**: Defines the `Student` class and GPA logic.


* 
**`course.py`**: Defines the `Course` class and roster management.


* 
**`university.py`**: The central manager for all students and courses.


* 
**`loader.py`**: Handles CSV data ingestion.


* 
**`stats.py`**: Helper functions for calculating mean, median, and mode.


* 
**`main.py`**: The primary demonstration script.





