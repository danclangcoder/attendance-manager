import customtkinter as ctk

from .auth import Auth, GoogleOAuth
from .database.repository import (
    AttendanceRepository,
    ClassesRepository,
    CourseRepository,
    EnrollmentRepository,
    GoogleAccountRepository,
    SectionRepository,
    SettingsRepository,
    StudentRepository,
    SubjectRepository,
    UserRepository,
)
from .google_services import GoogleDriveService
from .ui import Window


class App:
    def __init__(self):
        self.user_repo = UserRepository()
        self.student_repo = StudentRepository()
        self.section_repo = SectionRepository()
        self.subject_repo = SubjectRepository()
        self.classes_repo = ClassesRepository()
        self.enrollment_repo = EnrollmentRepository()
        self.course_repo = CourseRepository()
        self.attendance_repo = AttendanceRepository()
        self.settings = SettingsRepository()
        self.google_account_repo = GoogleAccountRepository()
        self.auth = Auth(user_repo=self.user_repo)
        self.google_oauth = GoogleOAuth(google_repo=self.google_account_repo)
        self.google_drive = GoogleDriveService(self.google_oauth)

        courses = [{"name": "BSIT"}, {"name": "BSHM"}, {"name": "BSBA"}, {"name": "BSOA"}]

        for course in courses:
            existing = self.course_repo.get_by_name(course["name"])

            if not existing:
                self.course_repo.create(name=course["name"])

        sections = [
            # BSIT 3rd Year Lagro
            {"name": "LAGBSITM91", "course": "BSIT", "year_level": "3rd Year"},
            {"name": "LAGBSITM81", "course": "BSIT", "year_level": "3rd Year"},
            {"name": "LAGBSITM71", "course": "BSIT", "year_level": "3rd Year"},
            # BSIT 2nd Year Lagro
            {"name": "LAGBSITM61", "course": "BSIT", "year_level": "2nd Year"},
            {"name": "LAGBSITM51", "course": "BSIT", "year_level": "2nd Year"},
            {"name": "LAGBSITM41", "course": "BSIT", "year_level": "2nd Year"},
            # BSIT 1st Year Lagro
            {"name": "LAGBSITM31", "course": "BSIT", "year_level": "1st Year"},
            {"name": "LAGBSITM21", "course": "BSIT", "year_level": "1st Year"},
            {"name": "LAGBSITM11", "course": "BSIT", "year_level": "1st Year"},
            # BSHM 3rd Year Lagro
            {"name": "LAGBSHMM91", "course": "BSHM", "year_level": "3rd Year"},
            {"name": "LAGBSHMM81", "course": "BSHM", "year_level": "3rd Year"},
            {"name": "LAGBSHMM71", "course": "BSHM", "year_level": "3rd Year"},
            # BSHM 2nd Year Lagro
            {"name": "LAGBSHMM61", "course": "BSHM", "year_level": "2nd Year"},
            {"name": "LAGBSHMM51", "course": "BSHM", "year_level": "2nd Year"},
            {"name": "LAGBSHMM41", "course": "BSHM", "year_level": "2nd Year"},
            # BSHM 1st Year Lagro
            {"name": "LAGBSHMM31", "course": "BSHM", "year_level": "1st Year"},
            {"name": "LAGBSHMM21", "course": "BSHM", "year_level": "1st Year"},
            {"name": "LAGBSHMM11", "course": "BSHM", "year_level": "1st Year"},
            # BSBA 3rd Year Lagro
            {"name": "LAGBSBAM91", "course": "BSBA", "year_level": "3rd Year"},
            {"name": "LAGBSBAM81", "course": "BSBA", "year_level": "3rd Year"},
            {"name": "LAGBSBAM71", "course": "BSBA", "year_level": "3rd Year"},
            # BSBA 2nd Year Lagro
            {"name": "LAGBSBAM61", "course": "BSBA", "year_level": "2nd Year"},
            {"name": "LAGBSBAM51", "course": "BSBA", "year_level": "2nd Year"},
            {"name": "LAGBSBAM41", "course": "BSBA", "year_level": "2nd Year"},
            # BSBA 1st Year Lagro
            {"name": "LAGBSBAM31", "course": "BSBA", "year_level": "1st Year"},
            {"name": "LAGBSBAM21", "course": "BSBA", "year_level": "1st Year"},
            {"name": "LAGBSBAM11", "course": "BSBA", "year_level": "1st Year"},
            # BSOA 3rd Year Lagro
            {"name": "LAGBSOAM91", "course": "BSOA", "year_level": "3rd Year"},
            {"name": "LAGBSOAM81", "course": "BSOA", "year_level": "3rd Year"},
            {"name": "LAGBSOAM71", "course": "BSOA", "year_level": "3rd Year"},
            # BSOA 2nd Year Lagro
            {"name": "LAGBSOAM61", "course": "BSOA", "year_level": "2nd Year"},
            {"name": "LAGBSOAM51", "course": "BSOA", "year_level": "2nd Year"},
            {"name": "LAGBSOAM41", "course": "BSOA", "year_level": "2nd Year"},
            # BSOA 1st Year Lagro
            {"name": "LAGBSOAM31", "course": "BSOA", "year_level": "1st Year"},
            {"name": "LAGBSOAM21", "course": "BSOA", "year_level": "1st Year"},
            {"name": "LAGBSOAM11", "course": "BSOA", "year_level": "1st Year"},
            # BSIT 3rd Year Lagro (EVENING)
            {"name": "LAGBSITE91", "course": "BSIT", "year_level": "3rd Year"},
            {"name": "LAGBSITE81", "course": "BSIT", "year_level": "3rd Year"},
            {"name": "LAGBSITE71", "course": "BSIT", "year_level": "3rd Year"},
            # BSIT 2nd Year Lagro (EVENING)
            {"name": "LAGBSITE61", "course": "BSIT", "year_level": "2nd Year"},
            {"name": "LAGBSITE51", "course": "BSIT", "year_level": "2nd Year"},
            {"name": "LAGBSITE41", "course": "BSIT", "year_level": "2nd Year"},
            # BSIT 1st Year Lagro (EVENING)
            {"name": "LAGBSITE31", "course": "BSIT", "year_level": "1st Year"},
            {"name": "LAGBSITE21", "course": "BSIT", "year_level": "1st Year"},
            {"name": "LAGBSITE11", "course": "BSIT", "year_level": "1st Year"},
            # BSHM 3rd Year Lagro (EVENING)
            {"name": "LAGBSHME91", "course": "BSHM", "year_level": "3rd Year"},
            {"name": "LAGBSHME81", "course": "BSHM", "year_level": "3rd Year"},
            {"name": "LAGBSHME71", "course": "BSHM", "year_level": "3rd Year"},
            # BSHM 2nd Year Lagro (EVENING)
            {"name": "LAGBSHME61", "course": "BSHM", "year_level": "2nd Year"},
            {"name": "LAGBSHME51", "course": "BSHM", "year_level": "2nd Year"},
            {"name": "LAGBSHME41", "course": "BSHM", "year_level": "2nd Year"},
            # BSHM 1st Year Lagro (EVENING)
            {"name": "LAGBSHME31", "course": "BSHM", "year_level": "1st Year"},
            {"name": "LAGBSHME21", "course": "BSHM", "year_level": "1st Year"},
            {"name": "LAGBSHME11", "course": "BSHM", "year_level": "1st Year"},
            # BSBA 3rd Year Lagro (EVENING)
            {"name": "LAGBSBAE91", "course": "BSBA", "year_level": "3rd Year"},
            {"name": "LAGBSBAE81", "course": "BSBA", "year_level": "3rd Year"},
            {"name": "LAGBSBAE71", "course": "BSBA", "year_level": "3rd Year"},
            # BSBA 2nd Year Lagro (EVENING)
            {"name": "LAGBSBAE61", "course": "BSBA", "year_level": "2nd Year"},
            {"name": "LAGBSBAE51", "course": "BSBA", "year_level": "2nd Year"},
            {"name": "LAGBSBAE41", "course": "BSBA", "year_level": "2nd Year"},
            # BSBA 1st Year Lagro (EVENING)
            {"name": "LAGBSBAE31", "course": "BSBA", "year_level": "1st Year"},
            {"name": "LAGBSBAE21", "course": "BSBA", "year_level": "1st Year"},
            {"name": "LAGBSBAE11", "course": "BSBA", "year_level": "1st Year"},
            # BSOA 3rd Year Lagro (EVENING)
            {"name": "LAGBSOAE91", "course": "BSOA", "year_level": "3rd Year"},
            {"name": "LAGBSOAE81", "course": "BSOA", "year_level": "3rd Year"},
            {"name": "LAGBSOAE71", "course": "BSOA", "year_level": "3rd Year"},
            # BSOA 2nd Year Lagro (EVENING)
            {"name": "LAGBSOAE61", "course": "BSOA", "year_level": "2nd Year"},
            {"name": "LAGBSOAE51", "course": "BSOA", "year_level": "2nd Year"},
            {"name": "LAGBSOAE41", "course": "BSOA", "year_level": "2nd Year"},
            # BSOA 1st Year Lagro (EVENING)
            {"name": "LAGBSOAE31", "course": "BSOA", "year_level": "1st Year"},
            {"name": "LAGBSOAE21", "course": "BSOA", "year_level": "1st Year"},
            {"name": "LAGBSOAE11", "course": "BSOA", "year_level": "1st Year"},
        ]

        for data in sections:
            course = self.course_repo.get_by_name(data["course"])

            if not course:
                return

            existing_section = self.section_repo.get_by_name(data["name"])

            if not existing_section:
                self.section_repo.create(name=data["name"], course_id=course.id, year_level=data["year_level"])

        logged_in = self.auth.restore_session()

        if logged_in:
            self.google_oauth.initialize(self.current_user)
            self.apply_user_settings()
        else:
            ctk.set_appearance_mode("light")

        self.main_window = Window(self)
        self.main_window.mainloop()

    def run_startup(self):
        if not self.user_repo.has_users:
            return "setup"

        self.google_oauth.refresh()

        return "attendance" if self.current_user else "login"

    # Authentication
    def login(self, username, password):
        success, message = self.auth.login(username, password)
        if success:
            print(f"Logged in as: {self.current_user}")
            self.google_oauth.initialize(self.current_user)
            print(self.is_google_linked)
            print(self.google_oauth.is_connected)
            self.apply_user_settings()
            self.main_window.show_page("attendance")
        return success, message

    def register(self, first_name, middle_name, last_name, username, password, email):
        success, message = self.auth.register(first_name, middle_name, last_name, username, password, email)
        if success:
            self.google_oauth.initialize(self.current_user)
            self.main_window.show_page("attendance")
        return success, message

    def logout(self):
        self.auth.logout()
        print(self.current_user)
        self.google_oauth.reset()
        print(self.is_google_linked)
        print(self.google_oauth.is_connected)
        self.main_window.show_page("login")

    # Google OAuth
    def link_google_account(self):
        if self.current_user is None:
            return
        self.google_oauth.link(self.current_user)

    def unlink_google_account(self):
        self.google_oauth.unlink()

    def set_user_gmail(self):
        if not self.google_oauth.is_connected:
            return None
        account = self.google_oauth.google_account
        return account.email if account else None

    @property
    def is_google_linked(self):
        return self.google_oauth.is_connected

    @property
    def current_user(self):
        return self.auth.active_user

    def toggle_dark_mode(self):
        if self.current_user is None:
            return

        enabled = self.is_dark_mode_enabled()

        new_mode = "light" if enabled else "dark"

        ctk.set_appearance_mode(new_mode)
        self.settings.set(self.current_user.id, "appearance_mode", new_mode)

    def apply_user_settings(self):
        if self.current_user is None:
            ctk.set_appearance_mode("light")
            return

        mode = self.settings.get(self.current_user.id, "appearance_mode", default="light")
        ctk.set_appearance_mode(mode)
        return mode

    def is_dark_mode_enabled(self):
        if self.current_user is None:
            return False
        return self.settings.get(self.current_user.id, "appearance_mode", default="light") == "dark"

    def create_class(self, subject_name, section_name, course_name, year_level):
        user = self.current_user
        if not user:
            return
        course = self.course_repo.get_by_name(course_name)
        section = self.section_repo.get_by_name(section_name)
        subject = self.subject_repo.get_by_name(subject_name)
        if course is None:
            course = self.course_repo.create(name=course_name)
        if section is None:
            section = self.section_repo.create(name=section_name, course_id=course.id, year_level=year_level)
        if subject is None:
            subject = self.subject_repo.create(name=subject_name)
        if self.classes_repo.exists(teacher_id=user.id, subject_id=subject.id, section_id=section.id):
            return False, "Class already exists."
        self.classes_repo.create(subject_id=subject.id, section_id=section.id, teacher_id=user.id)
        return True, None

    def get_classes(self):
        user = self.current_user
        if not user:
            return
        return self.classes_repo.get_by_teacher(user.id)

    def delete_class(self, class_id):
        self.classes_repo.delete(class_id)

    def get_sections(self):
        return self.section_repo.get_all()

    def get_all_sections(self):
        return self.section_repo.get_all_with_students()

    def get_students_in_class(self, class_id: int):
        return self.enrollment_repo.get_students_by_class(class_id)

    def is_student_in_class(self, student_id: int, class_id: int) -> bool:
        return self.enrollment_repo.get_by_student_and_class(student_id, class_id) is not None

    def add_student_to_class(self, student_id: int, class_id: int):
        if self.is_student_in_class(student_id, class_id):
            return False, "Student is already enrolled."
        self.enrollment_repo.create(student_id=student_id, class_id=class_id)
        return True, None

    def remove_student_from_class(self, student_id: int, class_id: int):
        enrollment = self.enrollment_repo.get_by_student_and_class(student_id, class_id)
        if enrollment is None:
            return False, "Student is not enrolled in this class."
        self.enrollment_repo.delete(enrollment.id)
        return True, None

    def add_course(self, course_name):
        course = self.get_course(course_name)
        if course:
            return course
        return self.course_repo.create(name=course_name)

    def get_course(self, course_name):
        return self.course_repo.get_by_name(name=course_name)

    def get_sections_by_course(self, course_id):
        return self.section_repo.get_by_course(course_id)

    def get_all_courses(self):
        return self.course_repo.get_all()

    def add_section(self, **data):
        return self.section_repo.create(**data)

    def get_section_by_course_and_name(self, course_id, section_name):
        return self.section_repo.get_by_course_and_name(course_id=course_id, name=section_name)

    def get_sections_by_course_and_year(self, course_id, year_level):
        return self.section_repo.get_by_course_and_year(course_id, year_level)

    def get_subject(self, subject_name):
        return self.subject_repo.get_by_name(subject_name)

    def add_student(self, **data):
        return self.student_repo.create(**data)

    def get_students(self):
        return self.student_repo.get_all()

    def get_students_by_section(self, section_id: int):
        return self.student_repo.get_by_section(section_id)

    def get_all_students_with_section(self):
        return self.student_repo.get_all_with_section()

    def get_student_by_number(self, student_number: str):
        return self.student_repo.get_by_student_number(student_number)

    def get_student(self, student_id: int):
        return self.student_repo.get_by_id(student_id)

    def configure_qr(self, student_id, qr_hash):
        existing_student = self.student_repo.get_by_qr_hash(qr_hash)

        if existing_student and existing_student.id != student_id:
            return False

        return self.student_repo.register_qr(student_id=student_id, qr_hash=qr_hash)

    def add_attendance(self, student_id: int, class_id: int, status: str = "present", qr_hash: str | None = None):
        user = self.current_user

        if not user:
            return None

        return self.attendance_repo.add_record(student_id=student_id, class_id=class_id, user_id=user.id, status=status, qr_hash=qr_hash)

    def get_recent_attendance(self, limit: int = 20):
        return self.attendance_repo.get_recent(limit)

    def get_attendance(self, attendance_id: int):
        return self.attendance_repo.get_by_id(attendance_id)

    def get_student_attendance(self, student_id: int):
        return self.attendance_repo.get_by_student(student_id)  # type: ignore

    def get_my_attendance(self):
        user = self.current_user

        if not user:
            return []

        return self.attendance_repo.get_by_user(user.id)

    def get_student_attendance_by_user(self, student_id: int):
        user = self.current_user

        if not user:
            return []

        return self.attendance_repo.get_by_student_and_user(student_id=student_id, user_id=user.id)

    def get_attendance_by_student_and_class(self, student_id: int, class_id: int):
        return self.attendance_repo.get_by_student_and_class(student_id, class_id)

    def get_attendance_by_qr(self, qr_hash: str):
        return self.attendance_repo.get_by_qr_hash(qr_hash)

    def enroll_student(self, student_id, class_id):
        return self.enrollment_repo.enroll(student_id=student_id, class_id=class_id)

    def get_students_by_class(self, class_id):
        return self.enrollment_repo.get_students_by_class(class_id)

    def is_student_enrolled(self, student_id, class_id):
        return self.enrollment_repo.is_enrolled(student_id=student_id, class_id=class_id)

    def unenroll_student(self, student_id, class_id):
        return self.enrollment_repo.unenroll(student_id=student_id, class_id=class_id)

    def get_classes_by_section(self, section_id: int):
        if not self.current_user:
            return

        return self.classes_repo.get_by_teacher_and_section(self.current_user.id, section_id)

    def get_student_by_qr_hash(self, qr_hash):
        return self.student_repo.get_by_qr_hash(qr_hash)

    def get_attendance_by_student_and_class_and_date(self, student_id, class_id, attendance_date):
        return self.attendance_repo.get_by_student_and_class_and_date(student_id, class_id, attendance_date)

    def create_user(self, first_name, middle_name, last_name, username, password, email):
        return self.auth.register(first_name, middle_name, last_name, username, password, email)

    def get_users(self):
        return self.user_repo.get_all()

    def upload_to_google_drive(self, filepath: str):
        if not self.google_oauth.is_connected:
            return False, "Google account is not connected."

        try:
            result = self.google_drive.upload_file(filepath)
            return True, result
        except Exception as e:
            return False, str(e)

    def delete_user(self, user_id):
        try:
            self.user_repo.delete(user_id)
            return True, "User deleted successfully."

        except Exception as e:
            return False, str(e)

    def delete_student(self, student_id):
        return self.student_repo.delete(student_id)
