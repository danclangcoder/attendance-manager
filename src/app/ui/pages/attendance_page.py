import threading
from datetime import date, datetime, timedelta, timezone
from tkinter import filedialog, messagebox
from zoneinfo import ZoneInfo

from CTkTable import CTkTable
from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkInputDialog, CTkLabel, CTkOptionMenu, CTkScrollableFrame

from app.scanner import QRScanner

from .base_page import BasePage
from .responsive import ResizeHandler


PH_TZ = ZoneInfo("Asia/Manila")
TEST_DATE = date(2026, 8, 25)


class AttendancePage(BasePage):
    def __init__(self, master, controller):
        super().__init__(master, title="Attendance", sidebar=True)

        self.window = master
        self.controller = controller

        ResizeHandler(self.window, {720: self.resize_small, 640: self.resize_medium})

        self.window.center_window(1280, 720)

        self.wrapper.pack_configure(padx=20)

        # ---------------------------------------------------------
        # Filter state
        # ---------------------------------------------------------

        self.classes = []

        self.selected_course = None
        self.selected_section = None
        self.selected_class = None
        self.selected_date = datetime.now(PH_TZ).date()
        self.selected_status = "All Status"

        # ---------------------------------------------------------
        # Attendance counters
        # ---------------------------------------------------------

        card_section = CTkFrame(master=self.wrapper, fg_color="transparent")
        card_section.pack(fill="x")

        card_section.grid_columnconfigure((0, 1, 2), weight=1, uniform="a")

        card_section.grid_rowconfigure(0, weight=0, minsize=100)

        container_1 = CTkFrame(master=card_section, fg_color=("#f6f6f6", "#333333"), border_color="#dddddd")
        container_1.grid(column=0, row=0, sticky="nsew", padx=5)

        container_2 = CTkFrame(master=card_section, fg_color=("#f6f6f6", "#333333"), border_color="#dddddd")
        container_2.grid(column=1, row=0, sticky="nsew", padx=5)

        container_3 = CTkFrame(master=card_section, fg_color=("#f6f6f6", "#333333"), border_color="#dddddd")
        container_3.grid(column=2, row=0, sticky="nsew", padx=5)

        self.present_label = CTkLabel(master=container_1, text="0", text_color=("#464646", "#dcdcdc"), font=("Arial", 32, "bold"))
        self.present_label.pack(expand=True, pady=(15, 0))

        self.absent_label = CTkLabel(master=container_2, text="0", text_color=("#464646", "#dcdcdc"), font=("Arial", 32, "bold"))
        self.absent_label.pack(expand=True, pady=(15, 0))

        self.total_label = CTkLabel(master=container_3, text="0", text_color=("#464646", "#dcdcdc"), font=("Arial", 32, "bold"))
        self.total_label.pack(expand=True, pady=(15, 0))

        CTkLabel(master=container_1, text="PRESENT", text_color=("#8A8A8A", "#cccccc"), font=("Arial", 12, "bold")).pack(side="bottom")

        CTkLabel(master=container_2, text="ABSENT", text_color=("#8A8A8A", "#cccccc"), font=("Arial", 12, "bold")).pack(side="bottom")

        CTkLabel(master=container_3, text="TOTAL STUDENTS", text_color=("#8A8A8A", "#cccccc"), font=("Arial", 12, "bold")).pack(side="bottom")

        CTkLabel(master=self.wrapper, text="View Attendance", text_color=("#464646", "#dcdcdc"), font=("Arial", 16, "bold")).pack(anchor="w", padx=5, pady=(10, 5))

        filters = CTkFrame(master=self.wrapper, fg_color="transparent")
        filters.pack(anchor="w", fill="x", padx=5)
        self.course_options = CTkOptionMenu(master=filters, values=["All Courses"], command=self.select_course)
        self.course_options.pack(side="left", padx=(0, 5))
        self.year_level_options = CTkOptionMenu(master=filters, values=["All Year Levels"], command=self.select_year_level)
        self.year_level_options.pack(side="left", padx=(0, 5))
        self.class_options = CTkOptionMenu(master=filters, values=["Select Class"], command=self.select_class)
        self.class_options.pack(side="left", padx=(0, 5))
        self.date_options = CTkOptionMenu(master=filters, values=[], command=self.select_date)
        self.date_options.pack(side="left", padx=(0, 5))
        self.status_options = CTkOptionMenu(master=filters, values=["All Status", "Present", "Absent"], command=self.select_status)
        self.status_options.pack(side="left", padx=(0, 5))

        buttons = CTkFrame(master=self.wrapper, fg_color="transparent")
        buttons.pack(padx=5, pady=20, anchor="w")

        CTkButton(master=buttons, text="Scan QR", command=self.open_scanner).pack(side="left", padx=(0, 5))
        CTkButton(master=buttons, text="Export Excel", command=self.export_excel).pack(side="left", padx=(0, 5))

        self.scanner_stop = threading.Event()

        # ---------------------------------------------------------
        # Table
        # ---------------------------------------------------------

        self.content = CTkFrame(master=self.wrapper, fg_color="transparent")
        self.content.pack(fill="both", expand=True)

        self.content.grid_rowconfigure(2, weight=1)

        self.content.grid_columnconfigure(0, weight=1)

        self.table_name = CTkLabel(master=self.content, text="(Select a class)", text_color=("#464646", "#dcdcdc"), font=("Arial", 16, "bold"))
        self.table_name.grid(row=0, column=0, pady=20)

        # Fixed header
        self.table_header = CTkFrame(master=self.content, fg_color="transparent", corner_radius=16)
        self.table_header.grid(row=1, column=0, padx=(15, 24), sticky="ew")

        self.table_header.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="table")

        headers = ["Name", "Student No.", "Section", "Timestamp"]

        for column, text in enumerate(headers):
            CTkLabel(master=self.table_header, text=text, fg_color=("#cdcdcd", "#1C1C1C"), text_color=("black", "white"), height=35).grid(row=0, column=column, sticky="ew")

        # Scrollable body
        self.table_container = CTkScrollableFrame(master=self.content, fg_color="transparent")
        self.table_container.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.treeview = CTkTable(
            master=self.table_container,
            row=10,
            column=4,
            values=[["", "", "", ""] for _ in range(10)],
            height=35,
            colors=[("#ffffff", "#373737"), ("#ffffff", "#373737")],
            text_color=("black", "white"),
            corner_radius=6,
        )

        self.treeview.pack(fill="x", expand=True)
        self.refresh()

    def refresh(self, event=None):
        self.classes = self.controller.get_classes() or []
        self.selected_course = None
        self.selected_year_level = None
        self.selected_class = None
        self.selected_date = datetime.now(PH_TZ).date()
        self.selected_status = "All Status"
        self.course_options.set("All Courses")
        self.year_level_options.set("All Year Levels")
        self.status_options.set("All Status")

        if not self.classes:
            self.course_options.configure(values=["All Courses"])
            self.year_level_options.configure(values=["All Year Levels"])
            self.class_options.configure(values=["Select Class"])
            self.class_options.set("Select Class")
            self.date_options.configure(values=[])
            self.clear_table()
            return

        courses = self.controller.get_all_courses() or []
        course_values = sorted(course.name for course in courses)
        self.course_options.configure(values=["All Courses"] + course_values)
        self.course_options.set("All Courses")
        self.update_class_options()

        today = datetime.now(PH_TZ).date()

        dates = [str(today - timedelta(days=i)) for i in range(7)]

        self.date_options.configure(values=dates)
        self.date_options.set(str(today))
        self.selected_date = today

        filtered_classes = self.get_filtered_classes()

        if not filtered_classes:
            self.selected_class = None

            self.class_options.set("Select Class")

            self.table_name.configure(text="(Select a class)")

            self.clear_table()
            return

        self.selected_class = None
        self.class_options.set("Select class")
        self.table_name.configure(text="Select a class")
        self.clear_table()

    def get_class_display_name(self, class_obj):
        return f"{class_obj.subject.name} - {class_obj.section.name}"

    def get_filtered_classes(self):
        filtered = list(self.classes)

        if self.selected_course:
            course = self.controller.get_course(self.selected_course)

            if course:
                course_sections = self.controller.get_sections_by_course(course.id) or []

                section_ids = {section.id for section in course_sections}

                filtered = [cls for cls in filtered if cls.section_id in section_ids]

        if self.selected_year_level:
            filtered = [cls for cls in filtered if str(cls.section.year_level) == str(self.selected_year_level)]

        return filtered

    def update_year_level_options(self):
        if self.selected_course:
            course = self.controller.get_course(self.selected_course)

            if course:
                sections = self.controller.get_sections_by_course(course.id) or []
            else:
                sections = []
        else:
            sections = self.controller.get_sections() or []

        year_level_values = sorted({str(section.year_level) for section in sections if section.year_level is not None})

        self.year_level_options.configure(values=["All Year Levels"] + year_level_values)

        self.year_level_options.set("All Year Levels")

    # =============================================================
    # UPDATE CLASS OPTIONS
    # =============================================================

    def update_class_options(self):
        filtered_classes = self.get_filtered_classes()

        class_values = [self.get_class_display_name(cls) for cls in filtered_classes]

        if not class_values:
            class_values = ["Select Class"]

        self.class_options.configure(values=class_values)

        if self.selected_class not in filtered_classes:
            self.selected_class = None

            self.class_options.set(class_values[0])

    # =============================================================
    # COURSE FILTER
    # =============================================================

    def select_course(self, value):
        if value == "All Courses":
            self.selected_course = None
        else:
            self.selected_course = value

        # Course changes reset section
        self.selected_year_level = None

        self.update_year_level_options()
        self.update_class_options()

        filtered_classes = self.get_filtered_classes()

        if not filtered_classes:
            self.selected_class = None

            self.class_options.set("Select Class")

            self.table_name.configure(text="(Select a class)")

            self.clear_table()
            return

        selected = filtered_classes[0]

        self.selected_class = selected

        self.class_options.set(self.get_class_display_name(selected))

        self.table_name.configure(text=self.get_class_display_name(selected))

        self.load_students(selected.id)

    # =============================================================
    # SECTION FILTER
    # =============================================================

    def select_year_level(self, value):
        if value == "All Year Levels":
            self.selected_year_level = None
        else:
            self.selected_year_level = value

        self.update_class_options()

        filtered_classes = self.get_filtered_classes()

        if not filtered_classes:
            self.selected_class = None

            self.class_options.set("Select Class")

            self.table_name.configure(text="(Select a class)")

            self.clear_table()
            return

        selected = filtered_classes[0]

        self.selected_class = selected

        self.class_options.set(self.get_class_display_name(selected))

        self.table_name.configure(text=self.get_class_display_name(selected))

        self.load_students(selected.id)

    def select_class(self, value):
        if value == "Select Class":
            self.selected_class = None

            self.table_name.configure(text="(Select a class)")

            self.clear_table()
            return

        selected = next((cls for cls in self.get_filtered_classes() if self.get_class_display_name(cls) == value), None)

        if selected is None:
            return

        self.selected_class = selected

        self.table_name.configure(text=self.get_class_display_name(selected))

        self.load_students(selected.id)

    # =============================================================
    # DATE FILTER
    # =============================================================

    def select_date(self, value):
        self.selected_date = date.fromisoformat(value)

        if self.selected_class:
            self.load_students(self.selected_class.id)

    # =============================================================
    # STATUS FILTER
    # =============================================================

    def select_status(self, value):
        self.selected_status = value

        if self.selected_class:
            self.load_students(self.selected_class.id)

    # =============================================================
    # QR SCANNER
    # =============================================================

    def open_scanner(self, event=None):
        if not self.selected_class:
            self.window.show_error(title="No Class Selected", message="Select a class first.")
            return

        QRScanner(master=self.master, controller=self.controller, on_scan=self.record_attendance)

    # =============================================================
    # RECORD ATTENDANCE
    # =============================================================

    def record_attendance(self, qr_hash):
        if not self.selected_class:
            return

        student = self.controller.get_student_by_qr_hash(qr_hash)

        if not student:
            self.window.show_error(title="Attendance Error", message=("QR code is not registered to a student."))
            return

        today = datetime.now(PH_TZ).date()

        existing = self.controller.get_attendance_by_student_and_class_and_date(student.id, self.selected_class.id, today)

        if existing:
            local_time = existing.scanned_at.replace(tzinfo=timezone.utc).astimezone(PH_TZ)

            confirmed = messagebox.askyesno(
                parent=self.window,
                title="Duplicate Attendance",
                message=(
                    f"{student.first_name} {student.last_name} already has attendance recorded for {today}.\n\nScanned at: {local_time.strftime('%I:%M %p')}\n\nRecord another attendance?"
                ),
            )

            if not confirmed:
                return

        record = self.controller.add_attendance(student_id=student.id, class_id=self.selected_class.id, qr_hash=qr_hash)

        if not record:
            return

        self.load_students(self.selected_class.id)

    # =============================================================
    # LOAD STUDENTS
    # =============================================================

    def load_students(self, class_id):
        students = self.controller.get_students_in_class(class_id)

        selected_date = self.selected_date

        rows = []

        present = 0
        absent = 0

        for student in students:
            attendance = self.controller.get_attendance_by_student_and_class_and_date(student.id, class_id, selected_date)

            timestamp = ""
            status = "absent"

            if attendance:
                local_time = attendance.scanned_at.replace(tzinfo=timezone.utc).astimezone(PH_TZ)

                timestamp = local_time.strftime("%Y-%m-%d %I:%M %p")

                status = attendance.status.lower()

            # Counters
            if status == "present":
                present += 1
            else:
                absent += 1

            # Status filter
            if self.selected_status != "All Status" and status != self.selected_status.lower():
                continue

            rows.append([(f"{student.first_name} {student.last_name}"), student.student_number, student.section.name, timestamp])

        rows = self.create_empty_rows(rows)

        self.treeview.destroy()

        self.treeview = CTkTable(
            master=self.table_container,
            row=len(rows),
            column=4,
            values=rows,
            height=35,
            colors=[("#ffffff", "#373737"), ("#ffffff", "#373737")],
            text_color=("black", "white"),
            corner_radius=6,
        )

        self.treeview.pack(padx=0, pady=0, fill="x")
        self.present_label.configure(text=str(present))
        self.absent_label.configure(text=str(absent))
        self.total_label.configure(text=str(len(students)))

    def clear_table(self):
        self.treeview.destroy()

        self.treeview = CTkTable(
            master=self.table_container,
            row=10,
            column=4,
            values=[["", "", "", ""] for _ in range(10)],
            height=35,
            colors=[("#ffffff", "#373737"), ("#ffffff", "#373737")],
            text_color=("black", "white"),
            corner_radius=6,
        )

        self.treeview.pack(padx=0, pady=0, fill="x")

        self.present_label.configure(text="0")
        self.absent_label.configure(text="0")
        self.total_label.configure(text="0")

    def export_excel(self):
        if not self.selected_class:
            self.window.show_error(title="No Class Selected", message="Select a class first.")
            return

        students = self.controller.get_students_in_class(self.selected_class.id)

        if not students:
            self.window.show_error(title="No Students", message=("There are no students enrolled in this class."))
            return

        dialog = CTkInputDialog(text="Enter attendance date (YYYY-MM-DD):", title="Export Attendance")

        value = dialog.get_input()

        if not value:
            return

        try:
            export_date = date.fromisoformat(value)
        except ValueError:
            self.window.show_error(title="Invalid Date", message=("Please enter the date using YYYY-MM-DD format."))
            return

        filename = filedialog.asksaveasfilename(
            title="Export Attendance", defaultextension=".xlsx", filetypes=[("Excel Workbook", "*.xlsx")], initialfile=(f"Attendance_{self.selected_class.section.name}_{export_date}.xlsx")
        )

        if not filename:
            return

        from openpyxl import Workbook

        workbook = Workbook()
        sheet = workbook.active

        assert sheet is not None

        sheet.title = "Attendance"

        sheet.append(["Student No.", "Name", "Section", "Status", "Timestamp"])

        for student in students:
            attendance = self.controller.get_attendance_by_student_and_class_and_date(student.id, self.selected_class.id, export_date)

            status = "Absent"
            timestamp = ""

            if attendance:
                status = attendance.status.capitalize()

                local_time = attendance.scanned_at.replace(tzinfo=timezone.utc).astimezone(PH_TZ)

                timestamp = local_time.strftime("%Y-%m-%d %I:%M %p")

            sheet.append([student.student_number, (f"{student.first_name} {student.last_name}"), student.section.name, status, timestamp])

        workbook.save(filename)

        if not self.controller.google_oauth.is_connected:
            self.window.show_info(
                title="Export Complete", message=(f"Attendance for {export_date} has been exported successfully.\n\nGoogle Drive is not connected, so the file was only saved locally.")
            )
            return

        threading.Thread(target=self.upload_excel_to_drive, args=(filename, export_date), daemon=True).start()

    def upload_excel_to_drive(self, filename, export_date):
        success, result = self.controller.upload_to_google_drive(filename)

        self.window.after(0, self.finish_drive_upload, success, result, export_date)

    def finish_drive_upload(self, success, result, export_date):
        if success:
            self.window.show_info(title="Export Complete", message=(f"Attendance for {export_date} has been exported and uploaded to Google Drive."))
        else:
            self.window.show_error(title="Google Drive Upload Failed", message=(f"The Excel file was saved locally, but the upload to Google Drive failed.\n\n{result}"))

    def create_empty_rows(self, rows):
        while len(rows) < 10:
            rows.append(["", "", "", ""])

        return rows
