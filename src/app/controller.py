import customtkinter as ctk

from .auth import Auth, GoogleOAuth
from .database.repository import (
    AttendanceRepository,
    ClassesRepository,
    CourseRepository,
    GoogleAccountRepository,
    SectionRepository,
    SettingsRepository,
    StudentRepository,
    SubjectRepository,
    UserRepository,
)
from .ui import MainWindow


class App:
    def __init__(self):
        self.user_repo = UserRepository()
        self.student_repo = StudentRepository()
        self.section_repo = SectionRepository()
        self.subject_repo = SubjectRepository()
        self.classes_repo = ClassesRepository()
        self.course_repo = CourseRepository()
        self.attendance_repo = AttendanceRepository()
        self.settings = SettingsRepository()
        self.google_account_repo = GoogleAccountRepository()
        self.auth = Auth(user_repo=self.user_repo)
        self.google_oauth = GoogleOAuth(google_repo=self.google_account_repo)

        logged_in = self.auth.restore_session()

        if logged_in:
            self.google_oauth.initialize(self.current_user)
            self.apply_user_settings()
        else:
            ctk.set_appearance_mode("light")

        self.main_window = MainWindow(self)
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
        self.settings.set(
            self.current_user.id,
            "appearance_mode",
            new_mode,
        )

    def apply_user_settings(self):
        if self.current_user is None:
            ctk.set_appearance_mode("light")
            return

        mode = self.settings.get(
            self.current_user.id,
            "appearance_mode",
            default="light",
        )
        ctk.set_appearance_mode(mode)
        return mode

    def is_dark_mode_enabled(self):
        if self.current_user is None:
            return False

        return (
            self.settings.get(
                self.current_user.id,
                "appearance_mode",
                default="light",
            )
            == "dark"
        )

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
            section = self.section_repo.create(
                name=section_name,
                course_id=course.id,
                year_level=year_level,
            )
        
        if subject is None:
            subject = self.subject_repo.create(name=subject_name)

        if self.classes_repo.exists(teacher_id=user.id, subject_id=subject.id, section_id=section.id):
            return False, "Class already exists."

        self.classes_repo.create(
            subject_id=subject.id,
            section_id=section.id,
            teacher_id=user.id,
        )

        return True, None

    def get_classes(self):
        user = self.current_user
        if not user:
            return
        return self.classes_repo.get_by_teacher(user.id)

    def get_subject(self, subject_name):
        return self.subject_repo.get_by_name(subject_name)

    def delete_class(self, class_id):
        self.classes_repo.delete(class_id)
