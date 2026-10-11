import tkinter as tk
from tkinter import ttk, messagebox
from .branch_catalog import DEFAULT_BRANCHES, fetch_official_branches, OFFICIAL_URLS
from .excel_repository import ExcelStudentRepository
from .student_service import StudentService

class StudentManagementApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TCET B.Voc Student Management System")
        self.root.geometry("1250x760")
        self.root.minsize(960, 620)
        self.service = StudentService(ExcelStudentRepository())
        self.branches = list(DEFAULT_BRANCHES)
        self.vars = {}
        self._build()
        self.refresh_table()

    def _build(self):
        self.root.configure(bg="#eef3fb")
        self.root.option_add("*Font", "Arial 10")

        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("App.TFrame", background="#eef3fb")
        style.configure("Header.TFrame", background="#ffffff")
        style.configure("Accent.TFrame", background="#edf3ff")
        style.configure("Title.TLabel", background="#ffffff", foreground="#1d2b45", font=("Arial", 20, "bold"))
        style.configure("Subtitle.TLabel", background="#ffffff", foreground="#5f6f8f", font=("Arial", 10))
        style.configure("Muted.TLabel", background="#eef3fb", foreground="#58657a", font=("Arial", 9))
        style.configure("Card.TLabelframe", background="#ffffff")
        style.configure("Card.TLabelframe.Label", background="#ffffff", foreground="#1d2b45", font=("Arial", 10, "bold"))
        style.configure("Field.TLabel", background="#ffffff", foreground="#2b3653", font=("Arial", 9, "bold"))
        style.configure("Primary.TButton", foreground="#ffffff", background="#345cff", font=("Arial", 10, "bold"))
        style.map("Primary.TButton",
                  background=[("active", "#294fe6"), ("pressed", "#2345d6")],
                  foreground=[("disabled", "#ffffff")])
        style.configure("Secondary.TButton", background="#edf2ff", foreground="#1d2b45", font=("Arial", 9, "bold"))
        style.map("Secondary.TButton", background=[("active", "#e1e9ff"), ("pressed", "#d8e3ff")])
        style.configure("Table.Treeview", background="#ffffff", foreground="#1c2437", rowheight=28, fieldbackground="#ffffff")
        style.configure("Table.Treeview.Heading", background="#e9eefb", foreground="#1d2b45", font=("Arial", 9, "bold"))
        style.map("Table.Treeview", background=[("selected", "#dfe9ff")], foreground=[("selected", "#0f172a")])

        outer = ttk.Frame(self.root, padding=18, style="App.TFrame")
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer, style="Header.TFrame")
        header.pack(fill="x", pady=(0, 14))
        title = ttk.Label(header, text="TCET B.Voc Student Management", style="Title.TLabel")
        title.pack(anchor="center", padx=18, pady=(18, 18))
        title.bind("<Configure>", lambda e: title.configure(wraplength=max(260, e.width - 30)))

        form = ttk.LabelFrame(outer, text="Student details", padding=12, style="Card.TLabelframe")
        form.pack(fill="x", pady=(0, 12))
        fields = [
            ("Student ID / PRN", "student_id", "entry", ""),
            ("Full name", "full_name", "entry", ""),
            ("B.Voc branch", "branch", "branch", self.branches[0]),
            ("Year", "year", "choice", ["FY", "SY", "TY", "Fourth Year"]),
            ("Semester", "semester", "choice", ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]),
            ("Academic year", "academic_year", "entry", "2026-27"),
            ("Email", "email", "entry", ""),
            ("Phone", "phone", "entry", ""),
            ("Status", "status", "choice", ["Active", "Graduated", "On Hold"]),
        ]
        for i, (label, key, kind, default) in enumerate(fields):
            r, c = divmod(i, 3)
            cell = ttk.Frame(form, padding=6, style="App.TFrame")
            cell.grid(row=r, column=c, sticky="ew", padx=6, pady=4)
            ttk.Label(cell, text=label, style="Field.TLabel").pack(anchor="w")
            var = tk.StringVar(value=default if isinstance(default, str) else default[0])
            self.vars[key] = var
            if kind == "entry":
                widget = ttk.Entry(cell, textvariable=var)
            elif kind == "branch":
                widget = ttk.Combobox(cell, textvariable=var, values=self.branches, state="readonly")
            else:
                widget = ttk.Combobox(cell, textvariable=var, values=default, state="readonly")
            widget.pack(fill="x")
            if key == "branch":
                self.branch_combo = widget
        for c in range(3):
            form.columnconfigure(c, weight=1)

        buttons = ttk.Frame(outer, style="App.TFrame")
        buttons.pack(fill="x", pady=(0, 10))
        ttk.Button(buttons, text="Add / Update Student", command=self.save_student, style="Primary.TButton").pack(side="left")
        ttk.Button(buttons, text="Clear Form", command=self.clear_form, style="Secondary.TButton").pack(side="left", padx=6)
        ttk.Button(buttons, text="Delete Selected", command=self.delete_selected, style="Secondary.TButton").pack(side="left")
        ttk.Button(buttons, text="Refresh Branches", command=self.refresh_branches, style="Secondary.TButton").pack(side="left", padx=6)
        ttk.Button(buttons, text="Refresh Students", command=self.refresh_table, style="Secondary.TButton").pack(side="left")

        filters = ttk.Frame(outer, padding=(0, 0, 0, 8), style="App.TFrame")
        filters.pack(fill="x")
        ttk.Label(filters, text="Search", style="Field.TLabel").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filters, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=6)
        search_entry.bind("<KeyRelease>", lambda event: self.refresh_table())
        ttk.Label(filters, text="Branch filter", style="Field.TLabel").pack(side="left", padx=(12, 0))
        self.filter_var = tk.StringVar(value="All branches")
        self.filter_combo = ttk.Combobox(filters, textvariable=self.filter_var,
                                          values=["All branches"] + self.branches, state="readonly", width=38)
        self.filter_combo.pack(side="left", padx=6)
        self.filter_combo.bind("<<ComboboxSelected>>", lambda event: self.refresh_table())

        columns = ("student_id","full_name","branch","year","semester","academic_year","email","phone","status")
        self.table = ttk.Treeview(outer, columns=columns, show="headings", selectmode="browse", style="Table.Treeview")
        labels = {"student_id":"Student ID / PRN","full_name":"Full Name","branch":"B.Voc Branch",
                  "year":"Year","semester":"Semester","academic_year":"Academic Year",
                  "email":"Email","phone":"Phone","status":"Status"}
        widths = [120,170,285,85,85,110,180,120,90]
        for col, label, width in zip(columns, labels.values(), widths):
            self.table.heading(col, text=label)
            self.table.column(col, width=width, minwidth=70, anchor="w")
        yscroll = ttk.Scrollbar(outer, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=yscroll.set)
        self.table.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")
        self.count_label = ttk.Label(outer, text="0 students", style="Muted.TLabel")
        self.count_label.pack(anchor="w", pady=(8, 0))
        ttk.Label(outer, text="Branch list source: TCET official B.Voc pages. Branch refresh needs internet; student records remain local.",
                  style="Muted.TLabel").pack(anchor="w", pady=(4, 0))

        self.table.bind("<<TreeviewSelect>>", self.load_selected)

    def save_student(self):
        try:
            data = {key: var.get().strip() for key, var in self.vars.items()}
            self.service.save_student(**data)
        except Exception as exc:
            messagebox.showerror("Check student details", str(exc))
            return
        self.refresh_table()
        messagebox.showinfo("Saved", "Student record added or updated in data/students.xlsx.")

    def clear_form(self):
        for key, var in self.vars.items():
            var.set("2026-27" if key == "academic_year" else (self.branches[0] if key == "branch" else
                    ("FY" if key == "year" else "I" if key == "semester" else "Active" if key == "status" else "")))
        self.table.selection_remove(self.table.selection())

    def load_selected(self, _event=None):
        selected = self.table.selection()
        if not selected:
            return
        values = self.table.item(selected[0], "values")
        for key, value in zip(self.vars, values):
            self.vars[key].set(value)

    def delete_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Select student", "Select a student row first.")
            return
        student_id = self.table.item(selected[0], "values")[0]
        if messagebox.askyesno("Confirm deletion", f"Delete student record {student_id}?"):
            self.service.delete_student(student_id)
            self.refresh_table()
            self.clear_form()

    def refresh_branches(self):
        try:
            branches = fetch_official_branches()
        except RuntimeError as exc:
            messagebox.showwarning("TCET branch refresh", str(exc) + "\n\nOfficial pages:\n" + "\n".join(OFFICIAL_URLS))
            return
        self.branches = branches
        self.branch_combo.configure(values=self.branches)
        if self.vars["branch"].get() not in branches:
            self.vars["branch"].set(branches[0])
        self.filter_combo.configure(values=["All branches"] + self.branches)
        messagebox.showinfo("Branches refreshed", f"Loaded {len(branches)} B.Voc branches from the public TCET website.")

    def refresh_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        query = self.search_var.get().casefold().strip()
        branch = self.filter_var.get()
        visible = []
        for student in self.service.list_students():
            if branch != "All branches" and student.branch != branch:
                continue
            searchable = " ".join([student.student_id, student.full_name, student.branch,
                                   student.year, student.semester, student.academic_year,
                                   student.email, student.phone, student.status]).casefold()
            if query and query not in searchable:
                continue
            visible.append(student)
            self.table.insert("", "end", values=(student.student_id, student.full_name, student.branch,
                student.year, student.semester, student.academic_year, student.email, student.phone, student.status))
        self.count_label.config(text=f"{len(visible)} student record(s) shown")

    def run(self):
        self.root.mainloop()
