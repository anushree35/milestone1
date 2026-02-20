from university import University
from loader import load_course_catalog, load_students

def main():
    uni = University()
    load_course_catalog("course_catalog.csv", uni)
    load_students("university_data.csv", uni)

    # test a quick query
    print(uni.get_course_enrollment("CSE2050"))

if __name__ == "__main__":
    main()
