from googleapiclient.discovery import build


class GoogleSheetsService:
    def __init__(self, oauth):
        self.oauth = oauth

    @property
    def service(self):
        return build("sheets", "v4", credentials=self.oauth.credentials)

    def read(self, spreadsheet_id: str, range_name: str = "A1:Z100"):
        return self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()

    def append(self, spreadsheet_id: str, range_name: str, values: list[list[str]]):
        body = {"values": values}
        return self.service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body,
        ).execute()

    def update(self, spreadsheet_id: str, range_name: str, values: list[list[str]]):
        body = {"values": values}
        return self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body,
        ).execute()
