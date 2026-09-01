from threading import Thread
from tkinter import messagebox

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

        self.content = CTkFrame(self.wrapper, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=10, pady=10)

        self.content.grid_columnconfigure(0, weight=1)

        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)

        general = CTkFrame(master=self.content, fg_color=("#d0d0d0", "#343434"), height=60)
        general.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        general.grid_propagate(False)
        general.grid_columnconfigure(0, weight=1)

        CTkLabel(master=general, text="General", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=20, pady=5, sticky="w")

        self.dark_mode_switch = CTkSwitch(master=general, text="Dark Mode", command=self.set_dark_mode)

        self.dark_mode_switch.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        profile = CTkFrame(master=self.content, fg_color=("#d0d0d0", "#343434"))
        profile.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        profile.grid_propagate(False)
        profile.grid_columnconfigure(0, weight=1)

        google_logo = ctk.CTkImage(Image.open(GOOGLE_LOGO), size=(16, 16))

        CTkLabel(master=profile, text="Profile", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=20, pady=5, sticky="w")

        self.name = CTkLabel(master=profile, text="", font=("Arial", 12))
        self.name.grid(row=1, column=0, padx=20, sticky="w")
        self.gmail = CTkLabel(master=profile, image=google_logo, text="", compound="left")
        self.gmail.grid(row=2, column=0, padx=20, sticky="w")

        self.link_button = CTkButton(master=profile, text="Link", text_color=("#111111", "#dcdcdc"), fg_color="transparent", hover_color=("#DBDBDB", "#cccccc"), command=self.link)

        self.unlink_button = CTkButton(master=profile, text="Unlink", text_color=("#111111", "#dcdcdc"), fg_color="transparent", hover_color=("#DBDBDB", "#cccccc"), command=self.unlink)

        self.loading_frame = CTkFrame(self.content, fg_color=("gray90", "gray15"))
        self.loading_frame.grid_rowconfigure(0, weight=1)
        self.loading_frame.grid_columnconfigure(0, weight=1)
        self.loading_label = CTkLabel(self.loading_frame, text="Connecting to Google...", font=("Arial", 16))
        self.loading_label.grid(row=0, column=0, sticky="nsew")
        self.loading_frame.place_forget()

        self.link_button.bind("<Enter>", lambda widget: self.link_button.configure(text_color="#3B8ED0"))

        self.link_button.bind("<Leave>", lambda widget: self.link_button.configure(text_color="#111111"))

        self.unlink_button.bind("<Enter>", lambda widget: self.unlink_button.configure(text_color="#3B8ED0"))

        self.unlink_button.bind("<Leave>", lambda widget: self.unlink_button.configure(text_color="#111111"))

        users = CTkFrame(master=self.content, width=350, height=400, fg_color=("#d0d0d0", "#343434"))
        users.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
        users.grid_propagate(False)
        users.grid_rowconfigure(1, weight=1)
        users.grid_columnconfigure(0, weight=1)

        users_header = CTkFrame(master=users, fg_color="transparent")
        users_header.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="ew")
        users_header.grid_columnconfigure(0, weight=1)

        CTkLabel(master=users_header, text="Users", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w")
        CTkButton(master=users_header, text="Add User", width=100, command=self.open_add_user_popup).grid(row=0, column=1, sticky="e")

        self.user_list = ctk.CTkScrollableFrame(master=users, fg_color="transparent")

        self.user_list.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.user_list.grid_columnconfigure(0, weight=1)

        self.load_dark_mode()

        self.refresh()

    def refresh(self):
        self.display_user_info()
        self.display_gmail()
        self.display_users()

    def display_users(self):
        for widget in self.user_list.winfo_children():
            widget.destroy()

        users = self.controller.get_users()

        for row, user in enumerate(users):
            user_frame = CTkFrame(master=self.user_list)

            user_frame.grid(row=row, column=0, padx=5, pady=5, sticky="ew")

            user_frame.grid_columnconfigure(0, weight=1)
            user_frame.grid_columnconfigure(1, weight=0)

            name = f"{user.first_name}"

            if user.middle_name:
                name += f" {user.middle_name[0]}."

            name += f" {user.last_name}"

            CTkLabel(master=user_frame, text=name, font=("Arial", 13, "bold")).grid(row=0, column=0, padx=15, pady=(10, 2), sticky="w")
            CTkLabel(master=user_frame, text=user.username, font=("Arial", 11)).grid(row=1, column=0, padx=15, pady=(0, 2), sticky="w")
            CTkLabel(master=user_frame, text=user.email, font=("Arial", 11)).grid(row=2, column=0, padx=15, pady=(0, 10), sticky="w")
            CTkButton(
                master=user_frame,
                text="Delete",
                width=70,
                fg_color="transparent",
                text_color=("#D32F2F", "#FF6B6B"),
                hover_color=("#F5D6D6", "#4A2525"),
                command=lambda user_id=user.id: self.delete_user(user_id),
            ).grid(row=0, column=1, rowspan=3, padx=10, pady=10)

    def delete_user(self, user_id):
        if user_id == self.controller.current_user.id:
            self.window.show_error(title="Cannot delete user", message="You cannot delete the currently logged-in user.")
            return

        confirm = messagebox.askyesno(title="Delete User", message="Are you sure you want to delete this user?", parent=self.window)

        if not confirm:
            return

        success, message = self.controller.delete_user(user_id)

        if not success:
            self.window.show_error(title="Delete User", message=message)
            return

        self.display_users()

    def open_add_user_popup(self):
        popup = ctk.CTkToplevel(self.window)

        popup.title("Add User")
        popup.geometry("400x500")
        popup.resizable(False, False)

        popup.transient(self.window)
        popup.grab_set()

        popup.grid_columnconfigure(0, weight=1)

        CTkLabel(master=popup, text="Add User", font=("Arial", 18, "bold")).grid(row=0, column=0, padx=20, pady=(20, 15))

        self.first_name_entry = ctk.CTkEntry(master=popup, placeholder_text="First Name")

        self.first_name_entry.grid(row=1, column=0, padx=30, pady=5, sticky="ew")

        self.middle_name_entry = ctk.CTkEntry(master=popup, placeholder_text="Middle Name")

        self.middle_name_entry.grid(row=2, column=0, padx=30, pady=5, sticky="ew")

        self.last_name_entry = ctk.CTkEntry(master=popup, placeholder_text="Last Name")

        self.last_name_entry.grid(row=3, column=0, padx=30, pady=5, sticky="ew")

        self.username_entry = ctk.CTkEntry(master=popup, placeholder_text="Username")

        self.username_entry.grid(row=4, column=0, padx=30, pady=5, sticky="ew")

        self.email_entry = ctk.CTkEntry(master=popup, placeholder_text="Email")

        self.email_entry.grid(row=5, column=0, padx=30, pady=5, sticky="ew")

        self.password_entry = ctk.CTkEntry(master=popup, placeholder_text="Password", show="*")

        self.password_entry.grid(row=6, column=0, padx=30, pady=5, sticky="ew")

        CTkButton(master=popup, text="Create User", command=lambda: self.create_user(popup)).grid(row=7, column=0, padx=30, pady=(20, 5), sticky="ew")

        CTkButton(master=popup, text="Cancel", fg_color="transparent", border_width=1, command=popup.destroy).grid(row=8, column=0, padx=30, pady=5, sticky="ew")

    def display_user_info(self):
        if self.controller.current_user:
            user = self.controller.current_user

            middle_initial = f"{str(user.middle_name)[0].upper()}." if user.middle_name else ""

            self.name.configure(text=f"{user.first_name} {middle_initial} {user.last_name}")

            self.name.grid(row=1, column=0, padx=20, sticky="w")

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
        self.controller.toggle_dark_mode()

    def load_dark_mode(self):
        enabled = self.controller.is_dark_mode_enabled()

        if enabled:
            self.dark_mode_switch.select()
        else:
            self.dark_mode_switch.deselect()

    def create_user(self, popup):
        first_name = self.first_name_entry.get().strip()
        middle_name = self.middle_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not first_name or not last_name:
            self.window.show_error(title="Invalid user", message="Please provide your complete name.")
            return

        if not username:
            self.window.show_error(title="Invalid user", message="Username is required.")
            return

        if not email:
            self.window.show_error(title="Invalid user", message="Email is required.")
            return

        if not password:
            self.window.show_error(title="Invalid user", message="Password is required.")
            return

        success, message = self.controller.create_user(first_name=first_name, middle_name=middle_name, last_name=last_name, username=username, password=password, email=email)

        self.first_name_entry.delete(0, "end")
        self.middle_name_entry.delete(0, "end")
        self.last_name_entry.delete(0, "end")
        self.username_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")

        if not success:
            print(message)
            return

        popup.destroy()
        self.display_users()
