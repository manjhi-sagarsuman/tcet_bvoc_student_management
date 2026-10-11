import unittest
from src.models import Student
from src.branch_catalog import DEFAULT_BRANCHES

class StudentModelTests(unittest.TestCase):
    def test_valid_student(self):
        s = Student("PRN001", "Test Student", DEFAULT_BRANCHES[0], "FY", "I", "2026-27")
        self.assertEqual(s.student_id, "PRN001")

    def test_missing_name_rejected(self):
        with self.assertRaises(ValueError):
            Student("PRN001", "", DEFAULT_BRANCHES[0], "FY", "I", "2026-27")

    def test_bad_email_rejected(self):
        with self.assertRaises(ValueError):
            Student("PRN001", "Test Student", DEFAULT_BRANCHES[0], "FY", "I", "2026-27", email="not-an-email")

if __name__ == "__main__":
    unittest.main()
