from googleapiclient.discovery import build


class GoogleDriveService:
    def __init__(self, oauth):
        self.oauth = oauth

    @property
    def service(self):
        return build("drive", "v3", credentials=self.oauth.credentials)

    def create_folder(self, name: str):
        file_metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
        return self.service.files().create(body=file_metadata, fields="id,name").execute()

    def upload_file(self, filepath: str, parent_id: str | None = None):
        from googleapiclient.http import MediaFileUpload

        file_metadata: dict[str, object] = {"name": filepath.split("/")[-1]}
        if parent_id:
            file_metadata["parents"] = [parent_id]
        media = MediaFileUpload(filepath, resumable=True)
        return self.service.files().create(body=file_metadata, media_body=media, fields="id,name").execute()

    def download_file(self, file_id: str, destination: str):
        request = self.service.files().get_media(fileId=file_id)
        with open(destination, "wb") as handle:
            handle.write(request.execute())
        return destination

    def list_files(self, query: str = ""):
        return self.service.files().list(q=query, spaces="drive", fields="files(id,name,mimeType)").execute()

    def delete_file(self, file_id: str):
        return self.service.files().delete(fileId=file_id).execute()

    def list_folders(self):
        query = "mimeType='application/vnd.google-apps.folder' and trashed=false"

        return self.service.files().list(q=query, spaces="drive", fields="files(id,name)", orderBy="name").execute().get("files", [])
