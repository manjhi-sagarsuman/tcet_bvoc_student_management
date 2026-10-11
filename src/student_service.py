from .models import Student

class StudentService:
    def __init__(self, repository):
        self.repository = repository

    def list_students(self):
        return sorted(self.repository.all(), key=lambda s: (s.branch.casefold(), s.full_name.casefold()))

    def save_student(self, **fields):
        student = Student(**fields)
        # Student ID is the unique key. Update existing records with the same ID.
        self.repository.save(student)
        return student

    def delete_student(self, student_id):
        return self.repository.delete(student_id)

    def branches(self):
        return sorted({s.branch for s in self.repository.all()})
