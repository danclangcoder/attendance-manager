from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkImage, CTkLabel
from PIL import Image

from app.config.app_settings import Settings

SCHOOL_LOGO = f"{Settings.LOGO_PATH}/access.png"
APP_LOGO = f"{Settings.LOGO_PATH}/qr.png"

TITLE_CAPSTONE = """ATTENDANCE MANAGEMENT SYSTEM OF STUDENTS USING 2D CODE READER FOR
ACCESS COMPUTER AND TECHNICAL COLLEGE LAGRO, QUEZON CITY"""

FOOTER_CREDITS = "Version 1.0\nCopyright © 2026. All Rights Reserved."


class LoginPage(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.window = master
        self.controller = controller

        entry_form = CTkFrame(master=self, fg_color="#e4e4e4", corner_radius=0)
        entry_form.pack(fill="both", side="left", expand=True)

        entry_form.grid_columnconfigure(0, weight=1)
        entry_form.grid_rowconfigure((0, 5), weight=1)

        CTkLabel(master=entry_form, text="Login your account", text_color="#5563CD", font=("Arial", 16, "bold")).grid(row=1, column=0, pady=20)
        self.username = CTkEntry(master=entry_form, placeholder_text="👤 Username", width=300, border_color="#C9C9C9", border_width=1)
        self.username.grid(row=2, column=0, pady=5)
        self.username.bind("<Return>", self.focus_next)
        self.password = CTkEntry(master=entry_form, placeholder_text="🔒 Password", show="*", width=300, border_color="#C9C9C9", border_width=1)
        self.password.grid(row=3, column=0, pady=5)
        self.password.bind("<Return>", self.submit)
        CTkButton(master=entry_form, text="Login", command=self.submit).grid(row=4, column=0, pady=20)

        right_bg = CTkFrame(master=self, fg_color="#5563CD", corner_radius=0)
        right_bg.pack(fill="both", side="left", expand=True)

        right_bg.grid_rowconfigure(1, weight=1)
        right_bg.grid_columnconfigure(0, weight=1)

        logo_1 = CTkImage(Image.open(SCHOOL_LOGO), size=(64, 64))
        logo_2 = CTkImage(Image.open(APP_LOGO), size=(64, 64))

        CTkLabel(master=right_bg, text=TITLE_CAPSTONE, text_color="#ffffff", font=("Times New Roman", 20, "bold"), wraplength=450).grid(row=1, column=0, pady=20)

        logos = CTkFrame(master=right_bg, fg_color="transparent")
        logos.grid(row=2, column=0)

        CTkLabel(master=logos, text="", image=logo_1).pack(side="left")
        CTkLabel(master=logos, text="", image=logo_2).pack(side="left")
        CTkLabel(master=right_bg, text=FOOTER_CREDITS, text_color="#ffffff", font=("Arial", 12)).grid(row=3, column=0, sticky="s", pady=20)

    def submit(self, event=None):
        username = self.username.get()
        password = self.password.get()
        success, message = self.controller.login(username, password)
        if success:
            self.clear_entries(self.username, self.password)
        else:
            self.window.show_error(title="Login Failed", message=message)

    def focus_next(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def clear_entries(self, *widgets, event=None):
        for widget in widgets:
            if isinstance(widget, CTkEntry):
                widget.delete(0, "end")
