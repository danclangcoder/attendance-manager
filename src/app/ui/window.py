from tkinter import messagebox

import customtkinter as ctk

from app.config.app_settings import Settings

from .pages import AttendancePage, ClassesPage, LoginPage, SettingsPage, SetupPage, StudentsPage

WINDOW_ICON = f"{Settings.ICON_PATH}/calendar.ico"


class Window(ctk.CTk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.iconbitmap(WINDOW_ICON)
        self.title("Attendance Manager")
        # self.geometry("1280x720")
        self.minsize(640, 640)
        self.center_window(1280, 720)

        self.page_classes = {"attendance": AttendancePage, "classes": ClassesPage, "students": StudentsPage, "settings": SettingsPage, "login": LoginPage, "setup": SetupPage}

        self.pages: dict[str, ctk.CTkFrame] = {}

        on_startup = controller.run_startup()
        self.show_page(on_startup)

        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # if event.widget == self:
        #     print(f"Width: {event.width}\nHeight: {event.width}")
        pass

    def center_window(self, width, height):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def get_page(self, page_name: str):
        if page_name not in self.pages:
            if page_name == "setup":
                self.center_window(800, 600)
                self.resizable(False, False)

            elif page_name == "login":
                self.minsize(800, 600)
                self.center_window(1280, 720)

            else:
                self.resizable(True, True)
            page = self.page_classes[page_name](self, controller=self.controller)
            page.place(relwidth=1, relheight=1)
            self.pages[page_name] = page

        return self.pages[page_name]

    def show_page(self, page_name):
        page = self.get_page(page_name)
        page.lift()

        if hasattr(page, "refresh"):
            page.refresh()  # type: ignore

        if hasattr(page, "on_hide"):
            page.on_hide()  # type: ignore

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_info(self, title, message):
        messagebox.showinfo(title, message)

    def ask_yes_no(self, title, message, parent):
        messagebox.askyesno(title, message, parent=parent)
