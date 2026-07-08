from tkinter import messagebox

from src.database import SessionRepository, UserRepository
from src.gui.window import AppWindow
from src.services import Auth


class AppController:
    def __init__(self):
        self.user_repo = UserRepository()
        self.session_repo = SessionRepository()
        self.auth = Auth(user_repo=self.user_repo, session_repo=self.session_repo)
        self.view = AppWindow(controller=self)

    @property
    def current_user(self):
        return self.auth.current_user

    def run(self):
        self.view.mainloop()

    def on_start(self):
        if not self.user_repo.has_users:
            return 'setup'

        if self.auth.restore():
            return 'dashboard'

        return 'login'

    def register(self, name, username, email, password, confirm_password, role=None):
        if role is None:
            role = 'Administrator'

        success, message = self.user_repo.create(name, username, email, password, role)

        if not success:
            messagebox.showerror('Invalid account', message)
            return

        if password != confirm_password:
            messagebox.showerror('Incorrect password', 'Password does not match.')
            return

        print(self.current_user)
        self.view.display('dashboard')

    def authenticate(self, username, password):
        success, message = self.auth.login(username, password)

        if not success:
            messagebox.showerror('Login error', message)
            return False

        self.view.display('dashboard')
        print(self.current_user)
        return True

    def logout(self):
        self.auth.logout()
        self.view.display('login')
