import customtkinter as ctk
from customtkinter import CTk

from src.gui.pages import LoginPage, DashboardPage, SetupPage
from src.core.config import WINDOW_ICON


class AppWindow(CTk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        ctk.set_appearance_mode('light')
        self.minsize(640, 640)
        self.geometry('960x540')
        self.title('Attendance Manager')
        self.iconbitmap(WINDOW_ICON)

        self.pages = {
            'login': LoginPage(self),
            'dashboard': DashboardPage(self),
            'setup': SetupPage(self),
        }

        self.load_pages()
        startup_page = self.controller.on_start()
        self.display(startup_page)

    def load_pages(self):
        for page in self.pages.values():
            page.place(relwidth=1, relheight=1)

    def display(self, page_name):
        if hasattr(self.pages[page_name], 'on_refresh'):
            self.pages[page_name].on_refresh()
        self.pages[page_name].tkraise()
