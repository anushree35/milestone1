import datetime

class EnrollmentRecord:
    
    def __init__(self, student, enrollment_date):

        if isinstance(enrollment_date, datetime.date):
            enroll_date = datetime.fromisoformat(enrollment_date)

        self.student = student 
        self.enrollment_date = enroll_date

    def __repr__(self):
        return f"EnrollmentRecord(student={self.student}, enrollment_date={self.enrollment_date})"
