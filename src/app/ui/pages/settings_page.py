from .base_page import BasePage


class SettingsPage(BasePage):
    def __init__(self, master):
        super().__init__(master, title="Settings", sidebar=True)
