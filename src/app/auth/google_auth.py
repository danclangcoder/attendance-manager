import requests
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.config.app_settings import Settings

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/drive.file",
]

CLIENT_SECRET = Settings.CLIENT_SECRET
TOKEN = Settings.TOKEN_PATH


class GoogleOAuth:
    def __init__(self):
        self.credentials = None 

    @property
    def is_connected(self):
        if not TOKEN.exists():
            return False

        creds = Credentials.from_authorized_user_file(
            str(TOKEN),
            SCOPES,
        )

        if creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                return False
            
        self.credentials = creds
            
        return creds.valid

    def login(self):
        if TOKEN.exists():
            self.credentials = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)

        if self.credentials and self.credentials.expired and self.credentials.refresh_token:
            self.credentials.refresh(Request())
            TOKEN.write_text(self.credentials.to_json())

        if not self.credentials or not self.credentials.valid:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)

            self.credentials = flow.run_local_server(port=0, open_browser=True, success_message="You can now return to the application")

            TOKEN.write_text(self.credentials.to_json())

        return self.credentials

    def logout(self):
        if TOKEN.exists():
            TOKEN.unlink()

        self.credentials = None

    def get_user(self):
        if not self.is_connected:
            return None

        oauth2 = build(
            "oauth2",
            "v2",
            credentials=self.credentials,
        )

        return oauth2.userinfo().get().execute()
