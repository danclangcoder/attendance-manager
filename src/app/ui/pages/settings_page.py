from threading import Thread

import customtkinter as ctk
from customtkinter import CTkButton, CTkFrame, CTkLabel, CTkSwitch
from PIL import Image

from app.config.app_settings import Settings

from .base_page import BasePage

GOOGLE_LOGO = f"{Settings.LOGO_PATH}/google.png"


class SettingsPage(BasePage):
    def __init__(self, master, controller):
        super().__init__(master, title="Settings", sidebar=True)

        self.window = master
        self.controller = controller

        general = CTkFrame(master=self.wrapper, width=500, height=200)
        self.after(2, lambda: general.pack(padx=20, pady=20))
        general.pack_propagate(False)
        CTkLabel(master=general, text="General", font=("Arial", 16, "bold")).pack(padx=20, pady=5)
        CTkSwitch(master=general, text="Dark Mode", command=self.set_dark_mode).pack()

        profile = CTkFrame(master=self.wrapper, width=500, height=200)
        self.after(2, lambda: profile.pack(padx=20, pady=20))
        profile.grid_propagate(False)
        profile.grid_columnconfigure(1, weight=1)
        google_logo = ctk.CTkImage(Image.open(GOOGLE_LOGO), size=(16, 16))
        CTkLabel(master=profile, text="Profile", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=20, pady=5, sticky="w")
        self.name = CTkLabel(master=profile, text="", font=("Arial", 12))
        self.gmail = CTkLabel(master=profile, image=google_logo, text="", compound="left")
        self.gmail.grid(row=2, column=0, padx=20, sticky="w")
        self.link_button = CTkButton(profile, text="Link", text_color=("#111111", "#dcdcdc"), fg_color="transparent", hover_color=("#DBDBDB", "#cccccc"), command=self.link)
        self.unlink_button = CTkButton(profile, text="Unlink", text_color=("#111111", "#dcdcdc"), fg_color="transparent", hover_color=("#DBDBDB", "#cccccc"), command=self.unlink)

        self.loading_frame = CTkFrame(self.wrapper, fg_color=("gray90", "gray15"))

        self.loading_label = CTkLabel(
            self.loading_frame,
            text="Connecting to Google...",
            font=("Arial", 16)
        )
        self.loading_label.pack(expand=True)

        # Hidden initially
        self.loading_frame.place_forget()

        self.link_button.bind("<Enter>", lambda widget: self.link_button.configure(text_color="#3B8ED0"))
        self.link_button.bind("<Leave>", lambda widget: self.link_button.configure(text_color="#111111"))
        self.unlink_button.bind("<Enter>", lambda widget: self.unlink_button.configure(text_color="#3B8ED0"))
        self.unlink_button.bind("<Leave>", lambda widget: self.unlink_button.configure(text_color="#111111"))

        self.refresh()

    def refresh(self):
        self.display_user_info()
        self.display_gmail()

    def display_user_info(self):
        if self.controller.current_user:
            user = self.controller.current_user
            self.name.grid(row=1, column=0, padx=20, sticky="w")
            middle_initial = f"{str(user.middle_name)[0].upper()}." if user.middle_name else ""
            self.name.configure(text=f"{user.first_name} {middle_initial} {user.last_name}")

    def display_gmail(self):
        self.link_button.grid_forget()
        self.unlink_button.grid_forget()

        if not self.controller.is_google_linked:
            self.link_button.grid(row=2, column=1, padx=20, pady=20)
            self.gmail.configure(text="\tNot connected")
            return
        
        self.unlink_button.grid(row=2, column=1, padx=20, pady=20)
        thread = Thread(target=self._fetch_gmail, daemon=True)
        thread.start()

    def _fetch_gmail(self):
        try:
            user = self.controller.google_oauth.get_user()
            email = user["email"]
        except Exception as e:
            import traceback
            traceback.print_exc()
            email = str(e)

        self.after(1, lambda: self._update_gmail(email))

    def _update_gmail(self, email):
        self.gmail.configure(text=f"\t{email}")

    def link(self, event=None):
        Thread(target=self._link_google, daemon=True).start()

    def _link_google(self):
        self.controller.link_google_account()

        self.after(0, self._on_linked)

    def _on_linked(self):
        self.display_gmail()

    def unlink(self, event=None):
        Thread(target=self._unlink_google, daemon=True).start()

    def _unlink_google(self):
        self.controller.unlink_google_account()
        self.after(0, self._on_unlinked)

    def _on_unlinked(self):
        self.display_gmail()

    def set_dark_mode(self, event=None):
        mode = ctk.get_appearance_mode()
        if mode == "Light":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")