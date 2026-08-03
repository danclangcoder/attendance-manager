from googleapiclient.discovery import build


class GoogleFormsService:
    def __init__(self, oauth):
        self.oauth = oauth

    @property
    def service(self):
        return build("forms", "v1", credentials=self.oauth.credentials)

    def create_form(self, title: str):
        return self.service.forms().create(body={"info": {"title": title}}).execute()

    def add_question(self, form_id: str, question: dict):
        return self.service.forms().responses().list(formId=form_id).execute()

    def publish(self, form_id: str):
        return self.service.forms().publish(formId=form_id).execute()
