# File structure

```text
tcet_bvoc_student_management/
├── main.py
├── requirements.txt
├── README.md
├── src/
│   ├── models.py              # Student model and validation
│   ├── branch_catalog.py      # Public TCET branch list + refresh
│   ├── excel_repository.py    # Excel CRUD
│   ├── student_service.py     # Business logic
│   └── student_app.py         # Tkinter UI
├── data/
│   └── students.xlsx          # Created automatically
├── diagrams/
│   ├── architecture.png
│   └── workflow.png
└── tests/
    └── test_models.py
```

The Student ID / PRN is the unique key. Saving another record with the same ID updates the existing record.
