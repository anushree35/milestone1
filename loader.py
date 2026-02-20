import csv

def load_course_catalog(csv_path, uni):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            course_code = row["course_code"].strip()
            credits = int(row["credits"])
            uni.add_course(course_code, credits)

def load_students(csv_path, uni):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            student_id = row["student_id"].strip()
            name = row["name"].strip()
            uni.add_student(student_id, name)
            student = uni.get_student(student_id)
            courses_raw = row["courses"].strip().split(";")
            for entry in courses_raw:
                if ":" in entry:
                    parts = entry.split(":")
                    course_code = parts[0].strip()
                    grade = parts[1].strip()
                    course = uni.get_course(course_code)
                    if course:
                        student.enroll(course, grade)
