import datetime
from enrollment_record import EnrollmentRecord
from linked_queue import LinkedQueue
from sorting import insertion_sort, selection_sort, recursive_binary_search


class Course:
    """
    Represents a university course with enrollment capacity and a waitlist.

    enrolled_roster -- list of EnrollmentRecord objects
    waitlist        -- LinkedQueue of Student objects (FIFO)
    enrolled_sorted_by -- tracks the current sort key, or None if unsorted
    """

    SORT_ALGORITHMS = {
        'insertion': insertion_sort,
        'selection': selection_sort,
    }

    def __init__(self, course_id, title, credits, department, capacity):
        self.course_id = course_id
        self.title = title
        self.credits = credits
        self.department = department
        self.capacity = capacity
        self.enrolled_roster = []       # list of EnrollmentRecord
        self.waitlist = LinkedQueue()   # LinkedQueue of Student
        self.enrolled_sorted_by = None  # 'name', 'id', 'date', or None

    # --- Enrollment ---

    def request_enroll(self, student, enroll_date):
        """
        Enroll a student in this course.

        If already enrolled: silently ignore (documented choice -- avoids
        duplicate records without crashing the loader).
        If space is available: add an EnrollmentRecord to enrolled_roster.
        If full: add the student to the waitlist queue.
        """
        # Check already enrolled
        for record in self.enrolled_roster:
            if record.student.student_id == student.student_id:
                return  # already enrolled, ignore

        if len(self.enrolled_roster) < self.capacity:
            self.enrolled_roster.append(EnrollmentRecord(student, enroll_date))
            self.enrolled_sorted_by = None  # roster order changed
        else:
            self.waitlist.enqueue(student)

    # --- Drop ---

    def drop(self, student_id, enroll_date_for_replacement=None):
        """
        Remove a student from the enrolled roster by student_id.

        If the roster is currently sorted by 'id', uses recursive binary search.
        Otherwise, re-sorts by 'id' automatically before searching.

        After removal, promotes the next waitlisted student (if any).
        Raises ValueError if the student is not found.
        """
        # Ensure sorted by id so binary search works
        if self.enrolled_sorted_by != 'id':
            insertion_sort(self.enrolled_roster, 'id')
            self.enrolled_sorted_by = 'id'

        idx = recursive_binary_search(
            self.enrolled_roster, student_id, 0, len(self.enrolled_roster) - 1
        )

        if idx == -1:
            raise ValueError(f"Student {student_id} is not enrolled in {self.course_id}.")

        self.enrolled_roster.pop(idx)
        self.enrolled_sorted_by = 'id'  # still sorted after removal

        # Promote next waitlisted student
        if not self.waitlist.is_empty():
            next_student = self.waitlist.dequeue()
            replacement_date = enroll_date_for_replacement or datetime.date.today()
            self.enrolled_roster.append(EnrollmentRecord(next_student, replacement_date))
            self.enrolled_sorted_by = None  # new record appended at end, order broken

    # --- Sorting ---

    def sort_enrolled(self, by, algorithm='insertion'):
        """
        Sort the enrolled roster in-place.

        by        -- 'name', 'id', or 'date'
        algorithm -- 'insertion' (default) or 'selection'
        """
        if algorithm not in self.SORT_ALGORITHMS:
            raise ValueError(f"Unknown algorithm '{algorithm}'. Choose from: {list(self.SORT_ALGORITHMS)}.")
        self.SORT_ALGORITHMS[algorithm](self.enrolled_roster, by)
        self.enrolled_sorted_by = by

    # --- Utility ---

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
