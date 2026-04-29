import datetime
from enrollment_record import EnrollmentRecord
from linked_queue import LinkedQueue
from hashmap import HashMap


def merge_sort(records, by):
    """Merge sort -- O(n log n). Imported from sorting if available, else defined here."""
    if len(records) <= 1:
        return records
    mid = len(records) // 2
    left = merge_sort(records[:mid], by)
    right = merge_sort(records[mid:], by)
    return _merge(left, right, by)

def _merge(left, right, by):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if _get_key(left[i], by) <= _get_key(right[j], by):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def _get_key(record, by):
    if by == 'name':
        return record.student.name.lower()
    elif by == 'id':
        return record.student.student_id
    elif by == 'date':
        return record.enroll_date
    raise ValueError(f"Invalid sort key '{by}'")


class Course:
    """
    Represents a university course with capacity, waitlist, prerequisite checking,
    and merge/quick sort support.

    prerequisite -- HashMap mapping prereq_course_id -> True (or None if no prereq)
    """

    def __init__(self, course_id, title, credits, department, capacity):
        self.course_id = course_id
        self.title = title
        self.credits = credits
        self.department = department
        self.capacity = capacity
        self.enrolled_roster = []
        self.waitlist = LinkedQueue()
        self.enrolled_sorted_by = None
        self.prerequisite = HashMap()   # stores prereq course_id -> True

    def set_prerequisite(self, prereq_course_id):
        """Register a prerequisite course ID in the HashMap."""
        if prereq_course_id and prereq_course_id.strip().upper() != 'NONE':
            self.prerequisite.put(prereq_course_id.strip(), True)

    def has_prerequisite(self):
        """Return True if this course has any prerequisites."""
        return len(self.prerequisite) > 0

    def student_meets_prerequisites(self, student):
        """
        Return True if the student has completed all prerequisites.
        If no prerequisites, always returns True.
        """
        for prereq_id, _ in self.prerequisite.items():
            if not student.has_taken(prereq_id):
                return False
        return True

    def request_enroll(self, student, enroll_date):
        """
        Enroll a student, checking prerequisites first.

        Raises PrerequisiteError if student hasn't met prerequisites.
        Silently ignores duplicate enrollments.
        Adds to waitlist if course is full.
        """
        # Check prerequisites
        if self.has_prerequisite() and not self.student_meets_prerequisites(student):
            missing = [pid for pid, _ in self.prerequisite.items()
                       if not student.has_taken(pid)]
            raise PrerequisiteError(
                f"Student {student.student_id} has not completed prerequisites "
                f"for {self.course_id}: {missing}"
            )

        # Check already enrolled
        for record in self.enrolled_roster:
            if record.student.student_id == student.student_id:
                return

        if len(self.enrolled_roster) < self.capacity:
            self.enrolled_roster.append(EnrollmentRecord(student, enroll_date))
            self.enrolled_sorted_by = None
        else:
            self.waitlist.enqueue(student)

    def drop(self, student_id, enroll_date_for_replacement=None):
        """
        Remove a student by ID using merge sort + linear scan.
        Promotes next waitlisted student if any.
        Raises ValueError if not found.
        """
        idx = None
        for i, rec in enumerate(self.enrolled_roster):
            if rec.student.student_id == student_id:
                idx = i
                break

        if idx is None:
            raise ValueError(f"Student {student_id} is not enrolled in {self.course_id}.")

        self.enrolled_roster.pop(idx)
        self.enrolled_sorted_by = None

        if not self.waitlist.is_empty():
            next_student = self.waitlist.dequeue()
            replacement_date = enroll_date_for_replacement or datetime.date.today()
            self.enrolled_roster.append(EnrollmentRecord(next_student, replacement_date))

    def sort_enrolled(self, by, algorithm='merge'):
        """
        Sort enrolled roster in-place.

        by        -- 'name', 'id', or 'date'
        algorithm -- 'merge' (default) or 'quick'
        """
        if algorithm == 'merge':
            self.enrolled_roster = merge_sort(self.enrolled_roster, by)
        elif algorithm == 'quick':
            try:
                from sorting import quick_sort
                quick_sort(self.enrolled_roster, by, 0, len(self.enrolled_roster) - 1)
            except ImportError:
                _quick_sort(self.enrolled_roster, by, 0, len(self.enrolled_roster) - 1)
        else:
            raise ValueError(f"Unknown algorithm '{algorithm}'. Use 'merge' or 'quick'.")
        self.enrolled_sorted_by = by

    def is_full(self):
        return len(self.enrolled_roster) >= self.capacity

    def enrollment_count(self):
        return len(self.enrolled_roster)

    def waitlist_count(self):
        return len(self.waitlist)

    def __repr__(self):
        return (f"Course({self.course_id}, {self.title!r}, "
                f"enrolled={self.enrollment_count()}/{self.capacity}, "
                f"waitlist={self.waitlist_count()})")


def _quick_sort(records, by, low, high):
    """Fallback quick sort if sorting.py not available."""
    if low < high:
        pi = _partition(records, by, low, high)
        _quick_sort(records, by, low, pi - 1)
        _quick_sort(records, by, pi + 1, high)

def _partition(records, by, low, high):
    pivot = _get_key(records[high], by)
    i = low - 1
    for j in range(low, high):
        if _get_key(records[j], by) <= pivot:
            i += 1
            records[i], records[j] = records[j], records[i]
    records[i + 1], records[high] = records[high], records[i + 1]
    return i + 1


class PrerequisiteError(Exception):
    """Raised when a student attempts to enroll without meeting prerequisites."""
    pass
