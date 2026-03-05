from university import University
from loader import load_course_catalog, load_students
from stats import mean, median, mode
from student import Student

# main demo script - Anushree & Prudhvi

def main():
    uni = University()
    load_course_catalog("course_catalog.csv", uni)
    load_students("university_data.csv", uni)

    # list of students in a course
    print("Students in CSE2050:")
    for s in uni.get_students_in_course("CSE2050"):
        print(" ", s.name)

    # gpa for one student
    s = uni.get_student("STU00001")
    print(f"\nGPA of {s.name}: {round(s.calculate_gpa(), 2)}")

    # all courses and grades for a student
    print(f"\nCourses for {s.name}:")
    for info in s.get_course_info():
        print(f"  {info['course_code']} - Grade: {info['grade']}, Credits: {info['credits']}")

    # grade stats for CSE2050
    cse2050 = uni.get_course("CSE2050")
    grades = [Student.GRADE_POINTS[s.courses[cse2050]] for s in uni.get_students_in_course("CSE2050")]
    print(f"\nCSE2050 grade stats:")
    print(f"  Mean: {round(mean(grades), 2)}")
    print(f"  Median: {round(median(grades), 2)}")
    print(f"  Mode: {mode(grades)}")

    # gpa stats for whole university
    gpas = [s.calculate_gpa() for s in uni.students.values()]
    print(f"\nUniversity GPA stats:")
    print(f"  Mean GPA: {round(mean(gpas), 2)}")
    print(f"  Median GPA: {round(median(gpas), 2)}")

    # students in both CSE2050 and CSE1010 classes
    set1 = set(s.student_id for s in uni.get_students_in_course("CSE2050"))
    set2 = set(s.student_id for s in uni.get_students_in_course("CSE1010"))
    common = set1 & set2
    print(f"\nCommon students in CSE2050 and CSE1010: {common}")

if __name__ == "__main__":
    main()
