from dataclasses import dataclass
from datetime import date
import re

@dataclass
class Student:
    student_id: str
    full_name: str
    branch: str
    year: str
    semester: str
    academic_year: str
    email: str = ""
    phone: str = ""
    status: str = "Active"

    def __post_init__(self):
        self.student_id = self.student_id.strip()
        self.full_name = self.full_name.strip()
        self.branch = self.branch.strip()
        self.year = self.year.strip()
        self.semester = self.semester.strip()
        self.academic_year = self.academic_year.strip()
        self.email = self.email.strip()
        self.phone = self.phone.strip()
        if not self.student_id:
            raise ValueError("Student ID / PRN is required.")
        if not self.full_name:
            raise ValueError("Student name is required.")
        if not self.branch:
            raise ValueError("Select a B.Voc branch.")
        if self.year not in {"FY", "SY", "TY", "Fourth Year"}:
            raise ValueError("Select a valid year.")
        if self.semester not in {"I", "II", "III", "IV", "V", "VI", "VII", "VIII"}:
            raise ValueError("Select a valid semester.")
        if self.email and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", self.email):
            raise ValueError("Enter a valid email address.")
        if self.phone and not re.match(r"^[+\d()\-\s]{7,20}$", self.phone):
            raise ValueError("Enter a valid phone number.")
        if self.status not in {"Active", "Graduated", "On Hold"}:
            raise ValueError("Select a valid student status.")
