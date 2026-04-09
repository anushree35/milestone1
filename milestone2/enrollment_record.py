import datetime

class EnrollmentRecord:
    
    def __init__(self, student, enroll_date):

        if isinstance(enroll_date, datetime.date.fromisoformat(enroll_date)):
            enroll_date = datetime.fromisoformat(enroll_date)

        self.student = student 
        self.enroll_date = enroll_date

    def __repr__(self):
        return f"EnrollmentRecord(student={self.student}, enroll_date={self.enroll_date})"
