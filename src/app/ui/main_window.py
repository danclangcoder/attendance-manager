from tkinter import messagebox

import customtkinter as ctk

from .pages import (
    AttendancePage,
    ClassesPage,
    LoginPage,
    SettingsPage,
    SetupPage,
)


class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        ctk.set_appearance_mode("light")

        self.controller = controller

        self.iconbitmap("assets/icons/calendar.ico")
        self.title("Attendance Manager")
        # self.geometry("1280x720")
        self.minsize(640, 640)
        self.center_window(1280, 720)

        self.pages: dict[str, ctk.CTkFrame] = {
            "attendance": AttendancePage(self),
            "classes": ClassesPage(self),
            "settings": SettingsPage(self),
            "login": LoginPage(self, controller=self.controller, auth=controller.auth),
            "setup": SetupPage(self, controller=self.controller, auth=controller.auth)
        }

        self.load_pages()

        on_startup = self.controller.run_startup()
        self.show_page(on_startup)

    def center_window(self, width, height):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def load_pages(self):
        for page in self.pages.values():
            page.place(relwidth=1, relheight=1)

    def show_page(self, page_name):
        self.pages[page_name].lift()

    def show_error(self, title, message):
        messagebox.showerror(title, message)