from university import University
from loader import load_course_catalog, load_students
from stats import mean, median, mode

def main():
    uni = University()
    load_course_catalog("course_catalog.csv", uni)
    load_students("university_data.csv", uni)

    # get students in a course
    print("Students in CSE2050:")
    for s in uni.get_students_in_course("CSE2050"):
        print(" ", s.name)

    # print GPA of a student
    s = uni.get_student("STU00001")
    print(f"\nGPA of {s.name}: {round(s.calculate_gpa(), 2)}")

    # print all courses and info for a student
    print(f"\nCourses for {s.name}:")
    for info in s.get_course_info():
        print(f"  {info['course_code']} - Grade: {info['grade']}, Credits: {info['credits']}")

    # mean, median, mode for a course
    grades = [Student.GRADE_POINTS[s.courses[uni.get_course("CSE2050")]] 
              for s in uni.get_students_in_course("CSE2050")]
    print(f"\nCSE2050 grade stats:")
    print(f"  Mean: {round(mean(grades), 2)}")
    print(f"  Median: {round(median(grades), 2)}")
    print(f"  Mode: {mode(grades)}")

    # mean and median of all student GPAs
    gpas = [s.calculate_gpa() for s in uni.students.values()]
    print(f"\nUniversity GPA stats:")
    print(f"  Mean GPA: {round(mean(gpas), 2)}")
    print(f"  Median GPA: {round(median(gpas), 2)}")

    # common students in two courses
    set1 = set(s.student_id for s in uni.get_students_in_course("CSE2050"))
    set2 = set(s.student_id for s in uni.get_students_in_course("CSE1010"))
    common = set1 & set2
    print(f"\nStudents in both CSE2050 and CSE1010: {common}")

if __name__ == "__main__":
    main()
