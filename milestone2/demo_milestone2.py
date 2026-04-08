import datetime
from university import University
from student import Student


print("Milestone 2 Demo")

#1. Loads the data
uni = University("UConn")
uni.load_course_catalog("course_catalog_CSE10_with_capacity.csv")
uni.load_enrollments("enrollments_CSE10.csv")

print(f"\nLoaded: {len(uni.courses)} courses, and {len(uni.students)} students")

#2. Picks a course and shows its current state
COURSE_ID = "CSE1010"  

uni.print_course_summary(COURSE_ID)

course = uni.courses[COURSE_ID]


#3. Fill the course with new students, adds extras to start the waitlist

print("Enrolling extra students to start waitlist. . .")

# Create students that are definitely not already in the roster
more_students = [
    ("EX001", "Michael Waitlist"),
    ("EX002", "Jim Waitlist"),
    ("EX003", "Dwight Waitlist"),
]

for sid, name in more_students:
    uni.add_student(sid, name)
    uni.enroll_student(sid, COURSE_ID, enroll_date=datetime.date(2026, 1, 20))

print(f"After extra enrollments:")
print(f"Enrolled : {course.enrollment_count()}/{course.capacity}")
print(f"Waitlist : {course.waitlist_count()}")

# This shows who is on the waitlist by printing the queue.
print(f"\nWaitlist contents: {course.waitlist}")


#4. Sort the enrolled roster in three ways

print("Sorting by name (insertion sort)")
course.sort_enrolled(by='name', algorithm='insertion')
for rec in course.enrolled_roster:
    print(f"  {rec.student.name:<25}  id={rec.student.student_id}")

print("Sorting by date (selection sort)")
course.sort_enrolled(by='date', algorithm='selection')
for rec in course.enrolled_roster:
    print(f"  {rec.enroll_date}  {rec.student.name}")

print("Sorting by ID (insertion sort)")
course.sort_enrolled(by='id', algorithm='insertion')
for rec in course.enrolled_roster:
    print(f"  id={rec.student.student_id:<10}  {rec.student.name}")


#5. Drop a student using recursive binary search

print("\n--- Dropping a student (binary search used) ---")

# Pick the first enrolled student to drop
drop_target = course.enrolled_roster[0].student
print(f"Dropping: {drop_target.name}  (id={drop_target.student_id})")
print(f"Waitlist before drop: {course.waitlist_count()}")

uni.drop_student(drop_target.student_id, COURSE_ID)

print(f"\nAfter drop:")
print(f"  Enrolled : {course.enrollment_count()}/{course.capacity}")
print(f"  Waitlist : {course.waitlist_count()}")
print(f"  (next waitlisted student should now be enrolled)")

print("\n--- Final roster ---")
uni.print_course_summary(COURSE_ID)

#6. Show drop raises an error for unknown ID
print("\n--- Dropping a student not in the roster ---")
try:
    uni.drop_student("FAKE999", COURSE_ID)
except ValueError as e:
    print(f"  Caught expected error: {e}")

print("Demo Completed.")
