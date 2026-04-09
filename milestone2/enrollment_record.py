import datetime
 
class EnrollmentRecord:
    
    def __init__(self, student, enroll_date):
        if isinstance(enroll_date, str):
            self.enroll_date = datetime.date.fromisoformat(enroll_date)
        elif isinstance(enroll_date, datetime.date):
            self.enroll_date = enroll_date
        else:
            raise TypeError(f"enroll_date must be a date or YYYY-MM-DD string, got {type(enroll_date)}")
 
        self.student = student
 
    def __repr__(self):
        return f"EnrollmentRecord(student={self.student}, enroll_date={self.enroll_date})"
