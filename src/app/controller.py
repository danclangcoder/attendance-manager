import customtkinter as ctk

from .auth import Auth, GoogleOAuth
from .database.repository import (
    AttendanceRepository,
    ClassesRepository,
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
        self.attendance_repo = AttendanceRepository()
        self.settings = SettingsRepository()
        self.auth = Auth(user_repo=self.user_repo)
        self.google_oauth = GoogleOAuth()

        if self.auth.is_logged_in:
            self.apply_user_settings()
        else:
            ctk.set_appearance_mode("light")

        self.main_window = MainWindow(self)
        self.main_window.mainloop()

    def run_startup(self):
        if not self.user_repo.has_users:
            return "setup"
        if self.auth.is_logged_in:
            return "attendance"
        return "login"

    # Authentication
    def login(self, username, password):
        success, message = self.auth.login(username, password)
        if success:
            self.main_window.show_page("attendance")
        return success, message

    def register(self, first_name, last_name, username, password, email):
        success, message = self.auth.register(first_name, last_name, username, password, email)
        if success:
            self.main_window.show_page("attendance")
        return success, message

    # Google OAuth
    def link_google_account(self):
        self.google_oauth.login()

    def unlink_google_account(self):
        self.google_oauth.logout()

    def set_user_gmail(self):
        if not self.google_oauth.is_connected:
            return None
        return self.google_oauth.get_user()

    @property
    def is_google_linked(self):
        return self.google_oauth.is_connected

    @property
    def current_user(self):
        return self.auth.active_user


    def toggle_dark_mode(self):
        if self.current_user is None:
            return

        current = ctk.get_appearance_mode()

        new_mode = (
            "dark"
            if current == "Light"
            else "light"
        )

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
        print(mode)
        ctk.set_appearance_mode(mode)
        return mode
    
    def is_dark_mode_enabled(self):
        assert self.current_user is not None
        return self.settings.get(
            self.current_user.id,
            "appearance_mode",
            default="light",
        ) == "dark"
    