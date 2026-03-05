import sys
sys.path.insert(0, '..')

from course import Course
from student import Student
from university import University

# testing Course class - Anushree
def test_course_creation():
    c = Course("CSE2050", 3)
    assert c.course_code == "CSE2050"
    assert c.credits == 3
    assert c.students == []

def test_add_student():
    c = Course("CSE2050", 3)
    s = Student("STU00001", "Anushree")
    c.add_student(s)
    assert c.get_student_count() == 1

def test_duplicate_students():
    # adding same student twice, count should still be 1
    c = Course("CSE2050", 3)
    s = Student("STU00001", "Anushree")
    c.add_student(s)
    c.add_student(s)
    assert c.get_student_count() == 1

def test_student_count():
    c = Course("CSE2050", 3)
    s1 = Student("STU00001", "Anushree")
    s2 = Student("STU00002", "Prudhvi")
    c.add_student(s1)
    c.add_student(s2)
    assert c.get_student_count() == 2

# testing University class - Anushree
def test_university_creation():
    uni = University()
    assert uni.students == {}
    assert uni.courses == {}

def test_add_course():
    uni = University()
    uni.add_course("CSE2050", 3)
    assert "CSE2050" in uni.courses

def test_duplicate_course():
    # shouldnt add the same course twice
    uni = University()
    uni.add_course("CSE2050", 3)
    uni.add_course("CSE2050", 3)
    assert len(uni.courses) == 1

def test_add_student():
    uni = University()
    uni.add_student("STU00001", "Anushree")
    assert "STU00001" in uni.students

def test_duplicate_student():
    uni = University()
    uni.add_student("STU00001", "Anushree")
    uni.add_student("STU00001", "Anushree")
    assert len(uni.students) == 1

def test_get_student():
    uni = University()
    uni.add_student("STU00001", "Anushree")
    s = uni.get_student("STU00001")
    assert s.name == "Anushree"

def test_get_nonexistent_student():
    # should return None if student doesnt exist
    uni = University()
    assert uni.get_student("STU99999") is None

def test_get_course():
    uni = University()
    uni.add_course("CSE2050", 3)
    c = uni.get_course("CSE2050")
    assert c.course_code == "CSE2050"

def test_get_nonexistent_course():
    uni = University()
    assert uni.get_course("FAKE999") is None
