import sys
sys.path.insert(0, '..')
import unittest
from student import Student
from course import Course

class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student("STU00008", "Prudhvi")
        self.course1 = Course("CSE2050", 3)
        self.course2 = Course("MATH2010", 4)
    
    def test_student_creation(self):
        self.assertEqual(self.student.student_id, "STU00008")
        self.assertEqual(self.student.name, "Prudhvi")
        self.assertEqual(self.student.courses, {})

    def test_enroll(self):
        self.student.enroll(self.course1, 'F')
        self.assertIn(self.course1, self.student.courses)
        self.assertEqual(self.student.courses[self.course1], 'F')
        self.assertIn(self.student, self.course1.students)

    def test_calculate_gpa(self):
        self.student.enroll(self.course1, 'B')
        self.student.enroll(self.course2, 'A')
        gpa = self.student.calculate_gpa()
        self.assertAlmostEqual(gpa, (3.0*3 + 4.0*4) / 7)

    def test_get_courses(self):
        self.student.enroll(self.course1, 'C')
        courses = self.student.get_courses()
        self.assertIn(self.course1, courses)

    def test_get_course_info(self):
        self.student.enroll(self.course1, 'C')
        info = self.student.get_course_info()
        self.assertEqual(len(info), 1)
        self.assertEqual(info[0]['course_code'], "CSE2050")
        self.assertEqual(info[0]['credits'], 3)
        self.assertEqual(info[0]['grade'], 'C')

if __name__ == '__main__':
    unittest.main()
