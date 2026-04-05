"""
test_milestone2.py -- unittest suite for Milestone 2.

Covers:
  - LinkedQueue (FIFO, empty dequeue, size)
  - EnrollmentRecord construction
  - Course capacity + waitlist (enroll, overflow, drop-promotes)
  - Sorting by name / id / date using both algorithms
  - Recursive binary search (first / middle / last / not found / unsorted auto-sort)
"""

import unittest
import datetime

from student import Student
from enrollment_record import EnrollmentRecord
from linked_queue import LinkedQueue
from course import Course
from sorting import insertion_sort, selection_sort, recursive_binary_search


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_student(n):
    """Return Student with zero-padded id and a name."""
    return Student(f"STU{n:05d}", f"Student_{n}")

def make_record(n, date_str="2026-01-15"):
    return EnrollmentRecord(make_student(n), date_str)

def make_course(capacity=3):
    return Course("CSE9999", "Test Course", 3, "CSE", capacity)


# ---------------------------------------------------------------------------
# 1. LinkedQueue
# ---------------------------------------------------------------------------

class TestLinkedQueue(unittest.TestCase):

    def test_enqueue_dequeue_fifo(self):
        q = LinkedQueue()
        q.enqueue("A")
        q.enqueue("B")
        q.enqueue("C")
        self.assertEqual(q.dequeue(), "A")
        self.assertEqual(q.dequeue(), "B")
        self.assertEqual(q.dequeue(), "C")

    def test_is_empty_initially(self):
        q = LinkedQueue()
        self.assertTrue(q.is_empty())

    def test_is_empty_after_dequeue_all(self):
        q = LinkedQueue()
        q.enqueue(1)
        q.dequeue()
        self.assertTrue(q.is_empty())

    def test_len_tracking(self):
        q = LinkedQueue()
        self.assertEqual(len(q), 0)
        q.enqueue("x")
        q.enqueue("y")
        self.assertEqual(len(q), 2)
        q.dequeue()
        self.assertEqual(len(q), 1)

    def test_dequeue_empty_raises(self):
        q = LinkedQueue()
        with self.assertRaises(ValueError):
            q.dequeue()

    def test_dequeue_empty_after_draining_raises(self):
        q = LinkedQueue()
        q.enqueue(42)
        q.dequeue()
        with self.assertRaises(ValueError):
            q.dequeue()

    def test_single_item_round_trip(self):
        q = LinkedQueue()
        q.enqueue("only")
        self.assertFalse(q.is_empty())
        self.assertEqual(q.dequeue(), "only")
        self.assertTrue(q.is_empty())

    def test_peek_does_not_remove(self):
        q = LinkedQueue()
        q.enqueue("front")
        self.assertEqual(q.peek(), "front")
        self.assertEqual(len(q), 1)


# ---------------------------------------------------------------------------
# 2. EnrollmentRecord
# ---------------------------------------------------------------------------

class TestEnrollmentRecord(unittest.TestCase):

    def test_string_date_parsed(self):
        rec = make_record(1, "2026-03-10")
        self.assertIsInstance(rec.enroll_date, datetime.date)
        self.assertEqual(rec.enroll_date.year, 2026)

    def test_date_object_accepted(self):
        s = make_student(2)
        d = datetime.date(2026, 2, 1)
        rec = EnrollmentRecord(s, d)
        self.assertEqual(rec.enroll_date, d)

    def test_invalid_type_raises(self):
        s = make_student(3)
        with self.assertRaises(TypeError):
            EnrollmentRecord(s, 20260101)  # int is not valid


# ---------------------------------------------------------------------------
# 3. Course capacity + waitlist
# ---------------------------------------------------------------------------

class TestCourseEnrollment(unittest.TestCase):

    def test_enroll_within_capacity(self):
        c = make_course(capacity=3)
        for i in range(1, 4):
            c.request_enroll(make_student(i), "2026-01-15")
        self.assertEqual(c.enrollment_count(), 3)
        self.assertEqual(c.waitlist_count(), 0)

    def test_overflow_goes_to_waitlist(self):
        c = make_course(capacity=2)
        for i in range(1, 5):
            c.request_enroll(make_student(i), "2026-01-15")
        self.assertEqual(c.enrollment_count(), 2)
        self.assertEqual(c.waitlist_count(), 2)

    def test_waitlist_is_fifo(self):
        c = make_course(capacity=1)
        c.request_enroll(make_student(1), "2026-01-15")  # fills seat
        c.request_enroll(make_student(2), "2026-01-15")  # waitlist pos 0
        c.request_enroll(make_student(3), "2026-01-15")  # waitlist pos 1
        # Peek at front of waitlist
        front = c.waitlist.peek()
        self.assertEqual(front.student_id, "STU00002")

    def test_drop_promotes_waitlisted_student(self):
        c = make_course(capacity=2)
        s1, s2, s3 = make_student(1), make_student(2), make_student(3)
        c.request_enroll(s1, "2026-01-15")
        c.request_enroll(s2, "2026-01-15")
        c.request_enroll(s3, "2026-01-15")  # goes to waitlist
        self.assertEqual(c.waitlist_count(), 1)

        c.drop("STU00001", enroll_date_for_replacement=datetime.date(2026, 2, 1))

        self.assertEqual(c.enrollment_count(), 2)
        self.assertEqual(c.waitlist_count(), 0)
        enrolled_ids = {r.student.student_id for r in c.enrolled_roster}
        self.assertIn("STU00003", enrolled_ids)

    def test_duplicate_enroll_ignored(self):
        c = make_course(capacity=5)
        s = make_student(1)
        c.request_enroll(s, "2026-01-15")
        c.request_enroll(s, "2026-01-15")  # duplicate -- should be ignored
        self.assertEqual(c.enrollment_count(), 1)

    def test_drop_nonexistent_raises(self):
        c = make_course(capacity=3)
        c.request_enroll(make_student(1), "2026-01-15")
        with self.assertRaises(ValueError):
            c.drop("STU99999")

    def test_waitlist_order_two_promotions(self):
        """Drop twice and verify the second waitlisted student is promoted second."""
        c = make_course(capacity=1)
        s1, s2, s3 = make_student(1), make_student(2), make_student(3)
        c.request_enroll(s1, "2026-01-15")
        c.request_enroll(s2, "2026-01-15")
        c.request_enroll(s3, "2026-01-15")

        c.drop("STU00001")  # s2 promoted
        enrolled_ids = {r.student.student_id for r in c.enrolled_roster}
        self.assertIn("STU00002", enrolled_ids)

        c.drop("STU00002")  # s3 promoted
        enrolled_ids = {r.student.student_id for r in c.enrolled_roster}
        self.assertIn("STU00003", enrolled_ids)


# ---------------------------------------------------------------------------
# 4. Sorting
# ---------------------------------------------------------------------------

def _build_roster():
    """Return an unsorted list of 5 EnrollmentRecords for sort tests."""
    data = [
        (5, "Zara",    "2026-03-01"),
        (2, "Alice",   "2026-01-20"),
        (4, "Mina",    "2026-02-15"),
        (1, "Bob",     "2026-01-10"),
        (3, "Charlie", "2026-02-01"),
    ]
    records = []
    for n, name, date in data:
        s = Student(f"STU{n:05d}", name)
        records.append(EnrollmentRecord(s, date))
    return records


class TestSortingInsertion(unittest.TestCase):

    def test_sort_by_name(self):
        r = _build_roster()
        insertion_sort(r, 'name')
        names = [rec.student.name for rec in r]
        self.assertEqual(names, sorted(names, key=str.lower))

    def test_sort_by_id(self):
        r = _build_roster()
        insertion_sort(r, 'id')
        ids = [rec.student.student_id for rec in r]
        self.assertEqual(ids, sorted(ids))

    def test_sort_by_date(self):
        r = _build_roster()
        insertion_sort(r, 'date')
        dates = [rec.enroll_date for rec in r]
        self.assertEqual(dates, sorted(dates))

    def test_already_sorted_unchanged(self):
        r = _build_roster()
        insertion_sort(r, 'id')
        ids_first = [rec.student.student_id for rec in r]
        insertion_sort(r, 'id')
        ids_second = [rec.student.student_id for rec in r]
        self.assertEqual(ids_first, ids_second)


class TestSortingSelection(unittest.TestCase):

    def test_sort_by_name(self):
        r = _build_roster()
        selection_sort(r, 'name')
        names = [rec.student.name for rec in r]
        self.assertEqual(names, sorted(names, key=str.lower))

    def test_sort_by_id(self):
        r = _build_roster()
        selection_sort(r, 'id')
        ids = [rec.student.student_id for rec in r]
        self.assertEqual(ids, sorted(ids))

    def test_sort_by_date(self):
        r = _build_roster()
        selection_sort(r, 'date')
        dates = [rec.enroll_date for rec in r]
        self.assertEqual(dates, sorted(dates))


class TestCourseSortMethod(unittest.TestCase):

    def _filled_course(self, capacity=5):
        c = make_course(capacity)
        data = [(5, "Zara"), (2, "Alice"), (4, "Mina"), (1, "Bob"), (3, "Charlie")]
        for n, name in data:
            s = Student(f"STU{n:05d}", name)
            c.request_enroll(s, f"2026-0{n}-01")
        return c

    def test_sort_enrolled_by_id_insertion(self):
        c = self._filled_course()
        c.sort_enrolled('id', 'insertion')
        ids = [r.student.student_id for r in c.enrolled_roster]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(c.enrolled_sorted_by, 'id')

    def test_sort_enrolled_by_name_selection(self):
        c = self._filled_course()
        c.sort_enrolled('name', 'selection')
        names = [r.student.name for r in c.enrolled_roster]
        self.assertEqual(names, sorted(names, key=str.lower))
        self.assertEqual(c.enrolled_sorted_by, 'name')

    def test_invalid_algorithm_raises(self):
        c = self._filled_course()
        with self.assertRaises(ValueError):
            c.sort_enrolled('id', 'bubble')

    def test_invalid_key_raises(self):
        c = self._filled_course()
        with self.assertRaises(ValueError):
            c.sort_enrolled('gpa', 'insertion')


# ---------------------------------------------------------------------------
# 5. Recursive binary search
# ---------------------------------------------------------------------------

class TestBinarySearch(unittest.TestCase):

    def setUp(self):
        """Build a roster of 5 records sorted by ID."""
        self.records = _build_roster()
        insertion_sort(self.records, 'id')
        # IDs in sorted order: STU00001 .. STU00005

    def test_find_first(self):
        idx = recursive_binary_search(self.records, "STU00001", 0, len(self.records) - 1)
        self.assertEqual(idx, 0)

    def test_find_last(self):
        idx = recursive_binary_search(self.records, "STU00005", 0, len(self.records) - 1)
        self.assertEqual(idx, 4)

    def test_find_middle(self):
        idx = recursive_binary_search(self.records, "STU00003", 0, len(self.records) - 1)
        self.assertEqual(idx, 2)

    def test_not_found_returns_minus_one(self):
        idx = recursive_binary_search(self.records, "STU99999", 0, len(self.records) - 1)
        self.assertEqual(idx, -1)

    def test_empty_list_returns_minus_one(self):
        idx = recursive_binary_search([], "STU00001", 0, -1)
        self.assertEqual(idx, -1)

    def test_single_element_found(self):
        idx = recursive_binary_search(self.records, "STU00001", 0, 0)
        self.assertEqual(idx, 0)

    def test_single_element_not_found(self):
        idx = recursive_binary_search(self.records, "STU99999", 0, 0)
        self.assertEqual(idx, -1)


class TestDropUsesBinarySearch(unittest.TestCase):

    def test_drop_when_sorted_by_id(self):
        c = make_course(capacity=5)
        for i in range(1, 6):
            c.request_enroll(make_student(i), "2026-01-15")
        c.sort_enrolled('id', 'insertion')
        c.drop("STU00003")
        ids = {r.student.student_id for r in c.enrolled_roster}
        self.assertNotIn("STU00003", ids)
        self.assertEqual(c.enrollment_count(), 4)

    def test_drop_auto_sorts_when_not_sorted_by_id(self):
        c = make_course(capacity=5)
        for i in range(1, 6):
            c.request_enroll(make_student(i), "2026-01-15")
        c.sort_enrolled('name', 'insertion')  # sorted by name, not id
        c.drop("STU00002")                    # should auto-resort by id internally
        ids = {r.student.student_id for r in c.enrolled_roster}
        self.assertNotIn("STU00002", ids)


# ---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main(verbosity=2)
