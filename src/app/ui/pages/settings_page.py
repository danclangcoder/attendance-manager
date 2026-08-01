import customtkinter as ctk
from threading import Thread
from customtkinter import CTkButton, CTkFrame, CTkLabel, CTkSwitch
from PIL import Image

from .base_page import BasePage

from app.config.app_settings import Settings

GOOGLE_LOGO = f"{Settings.LOGO_PATH}/google.png"


class SettingsPage(BasePage):
    def __init__(self, master, auth, controller):
        super().__init__(master, title="Settings", sidebar=True)

        self.view = master
        self.oauth = auth
        self.controller = controller

        general = CTkFrame(master=self.wrapper, width=500, height=200)
        general.pack(padx=20, pady=20)
        general.pack_propagate(False)
        CTkLabel(master=general, text="General", font=("Arial", 16, "bold")).pack(padx=20, pady=5)
        CTkSwitch(master=general, text="Dark Mode", command=self.set_dark_mode).pack()

        profile = CTkFrame(master=self.wrapper, width=500, height=200)
        profile.pack(padx=20, pady=20)
        profile.grid_propagate(False)
        profile.grid_columnconfigure(1, weight=1)
        google_logo = ctk.CTkImage(Image.open(GOOGLE_LOGO), size=(16, 16))
        CTkLabel(master=profile, text="Profile", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=20, pady=5, sticky="w")
        self.gmail = CTkLabel(master=profile, image=google_logo, text="", compound="left")
        self.gmail.grid(row=1, column=0, padx=20, sticky="w")
        self.link_button = CTkButton(profile, text="Link", text_color="#111111", fg_color="transparent", hover_color="#DBDBDB", command=self.redirect_link)
        self.unlink_button = CTkButton(profile, text="Unlink", text_color="#111111", fg_color="transparent", hover_color="#DBDBDB", command=self.unlink)

        self.link_button.bind("<Enter>", lambda widget: self.link_button.configure(text_color="#3B8ED0"))
        self.link_button.bind("<Leave>", lambda widget: self.link_button.configure(text_color="#111111"))
        self.unlink_button.bind("<Enter>", lambda widget: self.unlink_button.configure(text_color="#3B8ED0"))
        self.unlink_button.bind("<Leave>", lambda widget: self.unlink_button.configure(text_color="#111111"))


        if self.oauth.is_connected:
            self.unlink_button.grid(row=1, column=1, padx=20, pady=20)
        else:
            self.link_button.grid(row=1, column=1, padx=20, pady=20)

        self.display_gmail()

    def set_dark_mode(self, event=None):
        mode = ctk.get_appearance_mode()
        if mode == "Light":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def redirect_link(self, event=None):
        Thread(target=self._login_google, daemon=True).start()

    def _login_google(self):
        self.oauth.login()

        self.after(0, self._on_connected)

    def _on_connected(self):
        self.link_button.pack_forget()
        self.unlink_button.grid(row=1, column=1, padx=20, pady=20)
        self.display_gmail()

    def display_gmail(self):
        print("display_gmail called")

        if self.oauth.is_connected:
            user = self.oauth.get_user()
            self.gmail.configure(text=f"\t{user['email']}")
            print("Ok")
        else:
            print("Not ok")
            self.gmail.configure(text="\tLink your Google Account")

    def unlink(self, event=None):
        Thread(target=self._unlink_google, daemon=True).start()

    def _unlink_google(self):
        self.oauth.logout()

        self.after(0, self._on_unlinked)

    def _on_unlinked(self):
        self.unlink_button.pack_forget()
        self.link_button.grid(row=1, column=1, padx=20, pady=20)
        self.display_gmail()