"""
test_milestone3.py -- unittest suite for Milestone 3.
Covers: HashMap, prerequisite enrollment, merge sort, quick sort.
"""
import unittest
import datetime
from student import Student
from enrollment_record import EnrollmentRecord
from hashmap import HashMap
from course import Course, PrerequisiteError
from sorting import merge_sort, quick_sort


def make_student(n):
    return Student(f"STU{n:05d}", f"Student_{n}")

def make_course(capacity=5):
    return Course("CSE9999", "Test Course", 3, "CSE", capacity)

def make_record(n, date_str="2026-01-15"):
    return EnrollmentRecord(make_student(n), date_str)

def build_roster():
    data = [(5,"Zara","2026-03-01"),(2,"Alice","2026-01-20"),
            (4,"Mina","2026-02-15"),(1,"Bob","2026-01-10"),(3,"Charlie","2026-02-01")]
    return [EnrollmentRecord(Student(f"STU{n:05d}", name), date)
            for n, name, date in data]


# --- HashMap tests ---
class TestHashMap(unittest.TestCase):

    def test_put_and_get(self):
        hm = HashMap()
        hm.put("CSE1010", True)
        self.assertEqual(hm.get("CSE1010"), True)

    def test_get_missing_returns_none(self):
        hm = HashMap()
        self.assertIsNone(hm.get("MISSING"))

    def test_contains(self):
        hm = HashMap()
        hm.put("CSE2050", True)
        self.assertIn("CSE2050", hm)
        self.assertNotIn("CSE9999", hm)

    def test_update_existing_key(self):
        hm = HashMap()
        hm.put("key", "first")
        hm.put("key", "second")
        self.assertEqual(hm.get("key"), "second")
        self.assertEqual(len(hm), 1)

    def test_collision_handling(self):
        # Force collisions by using a tiny capacity
        hm = HashMap(capacity=2)
        hm.put("a", 1)
        hm.put("b", 2)
        hm.put("c", 3)
        self.assertEqual(hm.get("a"), 1)
        self.assertEqual(hm.get("b"), 2)
        self.assertEqual(hm.get("c"), 3)

    def test_rehash_triggered(self):
        hm = HashMap(capacity=5)
        # Adding 5 items pushes load factor to 1.0, rehash should have fired
        for i in range(5):
            hm.put(f"key{i}", i)
        # After rehash capacity should be doubled
        self.assertGreater(hm.capacity, 5)
        # All values preserved
        for i in range(5):
            self.assertEqual(hm.get(f"key{i}"), i)

    def test_rehash_preserves_all_keys(self):
        hm = HashMap(capacity=3)
        keys = ["x", "y", "z", "w"]
        for i, k in enumerate(keys):
            hm.put(k, i)
        for i, k in enumerate(keys):
            self.assertEqual(hm.get(k), i)

    def test_len(self):
        hm = HashMap()
        self.assertEqual(len(hm), 0)
        hm.put("a", 1)
        hm.put("b", 2)
        self.assertEqual(len(hm), 2)

    def test_load_factor(self):
        hm = HashMap(capacity=10)
        for i in range(5):
            hm.put(f"k{i}", i)
        self.assertAlmostEqual(hm.load_factor(), 0.5)


# --- Prerequisite enrollment tests ---
class TestPrerequisites(unittest.TestCase):

    def test_no_prereq_enrolls_fine(self):
        c = make_course()
        s = make_student(1)
        c.request_enroll(s, "2026-01-15")
        self.assertEqual(c.enrollment_count(), 1)

    def test_prereq_met_enrolls(self):
        c = make_course()
        c.set_prerequisite("CSE1010")
        s = make_student(1)
        s.complete_course("CSE1010")
        c.request_enroll(s, "2026-01-15")
        self.assertEqual(c.enrollment_count(), 1)

    def test_prereq_not_met_raises(self):
        c = make_course()
        c.set_prerequisite("CSE1010")
        s = make_student(2)
        with self.assertRaises(PrerequisiteError):
            c.request_enroll(s, "2026-01-15")

    def test_prereq_not_met_waitlist_also_raises(self):
        c = make_course(capacity=1)
        c.set_prerequisite("CSE1010")
        s1 = make_student(1)
        s1.complete_course("CSE1010")
        c.request_enroll(s1, "2026-01-15")  # fills seat
        s2 = make_student(2)  # no prereq
        with self.assertRaises(PrerequisiteError):
            c.request_enroll(s2, "2026-01-15")

    def test_none_prereq_ignored(self):
        c = make_course()
        c.set_prerequisite("NONE")
        self.assertFalse(c.has_prerequisite())

    def test_complete_course_tracks_taken(self):
        s = make_student(1)
        s.complete_course("CSE1010")
        self.assertTrue(s.has_taken("CSE1010"))
        self.assertFalse(s.has_taken("CSE2050"))

    def test_multiple_prereqs_all_required(self):
        c = make_course()
        c.set_prerequisite("CSE1010")
        c.set_prerequisite("CSE2050")
        s = make_student(1)
        s.complete_course("CSE1010")
        # Only completed one -- should fail
        with self.assertRaises(PrerequisiteError):
            c.request_enroll(s, "2026-01-15")
        s.complete_course("CSE2050")
        # Now both done -- should pass
        c.request_enroll(s, "2026-01-15")
        self.assertEqual(c.enrollment_count(), 1)


# --- Merge sort tests ---
class TestMergeSort(unittest.TestCase):

    def test_sort_by_id(self):
        r = build_roster()
        r = merge_sort(r, 'id')
        ids = [rec.student.student_id for rec in r]
        self.assertEqual(ids, sorted(ids))

    def test_sort_by_name(self):
        r = build_roster()
        r = merge_sort(r, 'name')
        names = [rec.student.name for rec in r]
        self.assertEqual(names, sorted(names, key=str.lower))

    def test_sort_by_date(self):
        r = build_roster()
        r = merge_sort(r, 'date')
        dates = [rec.enroll_date for rec in r]
        self.assertEqual(dates, sorted(dates))

    def test_empty_list(self):
        self.assertEqual(merge_sort([], 'id'), [])

    def test_single_element(self):
        r = [make_record(1)]
        self.assertEqual(merge_sort(r, 'id'), r)


# --- Quick sort tests ---
class TestQuickSort(unittest.TestCase):

    def test_sort_by_id(self):
        r = build_roster()
        quick_sort(r, 'id', 0, len(r) - 1)
        ids = [rec.student.student_id for rec in r]
        self.assertEqual(ids, sorted(ids))

    def test_sort_by_name(self):
        r = build_roster()
        quick_sort(r, 'name', 0, len(r) - 1)
        names = [rec.student.name for rec in r]
        self.assertEqual(names, sorted(names, key=str.lower))

    def test_sort_by_date(self):
        r = build_roster()
        quick_sort(r, 'date', 0, len(r) - 1)
        dates = [rec.enroll_date for rec in r]
        self.assertEqual(dates, sorted(dates))

    def test_single_element(self):
        r = [make_record(1)]
        quick_sort(r, 'id', 0, 0)  # should not crash
        self.assertEqual(len(r), 1)


# --- Course sort_enrolled with new algorithms ---
class TestCourseSortEnrolled(unittest.TestCase):

    def _filled_course(self):
        c = make_course(5)
        data = [(5,"Zara"),(2,"Alice"),(4,"Mina"),(1,"Bob"),(3,"Charlie")]
        for n, name in data:
            s = Student(f"STU{n:05d}", name)
            c.request_enroll(s, f"2026-0{n}-01")
        return c

    def test_merge_sort_by_id(self):
        c = self._filled_course()
        c.sort_enrolled('id', 'merge')
        ids = [r.student.student_id for r in c.enrolled_roster]
        self.assertEqual(ids, sorted(ids))

    def test_quick_sort_by_name(self):
        c = self._filled_course()
        c.sort_enrolled('name', 'quick')
        names = [r.student.name for r in c.enrolled_roster]
        self.assertEqual(names, sorted(names, key=str.lower))

    def test_invalid_algorithm_raises(self):
        c = self._filled_course()
        with self.assertRaises(ValueError):
            c.sort_enrolled('id', 'bubble')


if __name__ == '__main__':
    unittest.main(verbosity=2)
