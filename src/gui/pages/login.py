import customtkinter as ctk
from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel
from PIL import Image

from src.core.config import APP_LOGO, SCHOOL_LOGO
from src.gui.responsive_layouts import ResponsiveLogin, ResponsivePage
from src.gui.manager import EventHandler


class LoginPage(ResponsivePage):
    layout_handler = ResponsiveLogin

    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color='transparent')

        self.controller = parent.controller

        self.create_widgets()
        self.create_layout()
        self.create_overlay()
        self.create_binds()
        self.enable_resize()

    def create_widgets(self):
        self.wrapper = CTkFrame(master=self, fg_color='#ffffff')
        self.form_container = CTkFrame(master=self.wrapper, fg_color='#ffffff', corner_radius=0)
        self.form_content = CTkFrame(master=self.form_container, fg_color='transparent')
        self.form_label = CTkLabel(
            master=self.form_content,
            text='Login your account',
            font=('Arial', 16, 'bold'),
            text_color='#6E6EFF',
        )
        self.username_entry = CTkEntry(
            master=self.form_content,
            placeholder_text='👤 Username',
            width=240,
            height=36,
            corner_radius=8,
            border_width=1,
            border_color='#e1e1e1',
            fg_color='#fafafa',
            font=('Arial', 12),
        )
        self.password_entry = CTkEntry(
            master=self.form_content,
            placeholder_text='🔒 Password',
            width=240,
            height=36,
            corner_radius=8,
            border_width=1,
            border_color='#e1e1e1',
            fg_color='#fafafa',
            font=('Arial', 12),
            show='*',
        )
        self.login_button = CTkButton(
            master=self.form_content,
            text='Login',
            text_color='white',
            fg_color='#6E6EFF',
            hover_color='#6E6EFF',
            width=140,
            height=30,
            font=('Arial', 12),
            corner_radius=10,
            command=None,
            cursor='hand2',
        )
        self.splash_cover = CTkFrame(
            master=self.wrapper, fg_color='#6E6EFF', width=400, corner_radius=0
        )
        self.text_wrapper = CTkFrame(master=self.splash_cover, fg_color='#6E6EFF')
        self.app_name = CTkLabel(
            master=self.text_wrapper,
            text='Attendance Manager',
            font=('Arial', 24, 'bold'),
            text_color='white',
        )
        self.school_name = CTkLabel(
            master=self.text_wrapper,
            text='Access Computer College\n (Lagro)',
            font=('Arial', 16, 'bold'),
            text_color='white',
        )
        self.img_wrapper = CTkFrame(master=self.splash_cover, fg_color='#6E6EFF')
        self.school_img = ctk.CTkImage(
            light_image=Image.open(SCHOOL_LOGO),
            dark_image=Image.open(SCHOOL_LOGO),
            size=(110, 76),
        )
        self.school_logo = CTkLabel(master=self.img_wrapper, image=self.school_img, text='')
        self.app_img = ctk.CTkImage(
            light_image=Image.open(APP_LOGO),
            dark_image=Image.open(APP_LOGO),
            size=(76, 76),
        )
        self.app_logo = CTkLabel(master=self.img_wrapper, image=self.app_img, text='')

        self.footer = CTkLabel(
            master=self.splash_cover,
            text='Version 1.0\nCopyright © 2026. All Rights Reserved.',
            text_color='white',
        )

    def create_layout(self):
        self.wrapper.pack(expand=True, fill='both')
        self.form_container.pack(expand=True, fill='both', side='right')
        self.form_content.pack(expand=True)
        self.form_label.pack(pady=40)
        self.username_entry.pack(pady=10)
        self.password_entry.pack(pady=10)
        self.login_button.pack(pady=40)
        self.splash_cover.pack(fill='both', side='left')
        self.splash_cover.pack_propagate(False)
        self.text_wrapper.pack(pady=(30, 0))
        self.app_name.pack(pady=(10, 5), side='top')
        self.school_name.pack(pady=(0, 5), side='top')
        self.img_wrapper.pack(expand=True)
        self.school_logo.pack(side='left')
        self.app_logo.pack(side='left')
        self.footer.pack(side='bottom', pady=(0, 20))

    def create_overlay(self):
        self.overlay = CTkFrame(
            self,
            fg_color=self.cget('fg_color'),
            corner_radius=0,
        )

        wrapper = CTkFrame(self.overlay, fg_color='#ffffff')
        wrapper.pack(expand=True, fill='both')

        form = CTkFrame(wrapper, fg_color='#ffffff')
        form.pack(side='right', expand=True, fill='both')

        splash = CTkFrame(wrapper, fg_color='#6E6EFF', corner_radius=0, width=400)
        splash.pack(fill='both', side='left')

        content = CTkFrame(form, fg_color='transparent')
        content.pack(expand=True)

    def create_binds(self):
        EventHandler.bind_event(self.login_request, self.login_button)
        EventHandler.bind_enter_key(self.login_request, self.password_entry)
        EventHandler.bind_enter_key(self.focus_next, self.username_entry)

    def login_request(self, event=None):
        if self.controller.authenticate(
            username=self.username_entry.get(), password=self.password_entry.get()
        ):
            self.clear(self.username_entry, self.password_entry)

    def focus_next(self, event):
        event.widget.tk_focusNext().focus()
        return 'break'

    def clear(self, *widgets, event=None):
        for widget in widgets:
            if isinstance(widget, CTkEntry):
                widget.delete(0, 'end')
