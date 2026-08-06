from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.config.app_settings import Settings

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/forms",
]

CLIENT_SECRET = Settings.CLIENT_SECRET


class GoogleOAuth:
    def __init__(self, google_repo):
        self.google_repo = google_repo
        self.credentials = None
        self.google_account = None

    def initialize(self, user):
        if user is None:
            return

        self.google_account = self.google_repo.get_by_user_id(user.id)

        if self.google_account is None:
            return
        
        self.credentials = self.google_repo.get_credentials(user.id)

        self.refresh()

    def link(self, user):
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET,
            SCOPES,
        )

        self.credentials = flow.run_local_server(
            port=0,
            open_browser=True,
            success_message="You can now return to the application",
        )

        profile = self.get_user()

        if profile is None:
            self.reset()
            return

        self.google_account = self.google_repo.save(
            user_id=user.id,
            google_id=profile["id"],
            email=profile["email"],
            name=profile["name"],
            credentials=self.credentials,
        )

    def unlink(self):
        if self.google_account is None:
            return

        # Optional:
        # requests.post(
        #     "https://oauth2.googleapis.com/revoke",
        #     params={"token": self.credentials.token},
        # )

        self.google_repo.unlink(self.google_account.user_id)
        self.reset()

    def refresh(self):
        if self.credentials is None:
            return

        if self.google_account is None:
            return

        if self.credentials.valid:
            return

        if self.credentials.expired:
            if not self.credentials.refresh_token:
                return

            self.credentials.refresh(Request())

            self.google_repo.update_credentials(
                self.google_account.user_id,
                self.credentials,
            )

    def get_user(self):
        if not self.is_connected:
            return None

        oauth2 = build(
            "oauth2",
            "v2",
            credentials=self.credentials,
        )

        return oauth2.userinfo().get().execute()

    def get_drive_service(self):
        if not self.is_connected:
            return None

        return build(
            "drive",
            "v3",
            credentials=self.credentials,
        )

    def reset(self):
        self.credentials = None
        self.google_account = None

    @property
    def is_linked(self):
        return self.google_account is not None

    @property
    def is_connected(self):
        return (
            self.credentials is not None
            and self.credentials.valid
        )