
from .auth import Auth, GoogleOAuth
from .database.repository import UserRepository
from .ui import MainWindow


class AppInstance:
    def __init__(self):
        print(__file__)
        self.user_repo = UserRepository()
        self.oauth = GoogleOAuth()
        self.auth = Auth()
        self.window = MainWindow(self)
        self.window.mainloop()

    def run_startup(self):
        if not self.user_repo.has_users:
            return "setup"
        if self.auth.is_logged_in:
            return "attendance"
        return "login"
        