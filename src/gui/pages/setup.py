from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from src.gui.responsive_layouts import ResponsivePage, ResponsiveSetup
from src.gui.manager import EventHandler


class SetupPage(ResponsivePage):
    layout_handler = ResponsiveSetup
    """
    BLUE #6166c7
    WHITE #E8E9EB
    """

    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color='#E8E9EB')

        self.controller = parent.controller

        self.create_widgets()
        self.create_layout()
        self.create_overlay()
        self.create_binds()
        self.enable_resize()

    def create_widgets(self):
        self.wrapper = CTkFrame(
            self,
            fg_color='#F2F3F4',
            width=600,
            height=600,
            corner_radius=16,
            border_color='#6166c7',
        )
        self.form_content = CTkFrame(self.wrapper, fg_color='transparent', width=300, height=400)
        self.subtitle = CTkLabel(
            self.wrapper,
            text='Setup your account',
            font=('Arial', 36, 'bold'),
            text_color='#6E6EFF',
        )
        self.name = CTkEntry(
            self.form_content,
            placeholder_text='👤 Complete Name',
            width=240,
            height=34,
            corner_radius=8,
            border_width=1,
            border_color='#CDCDCD',
            fg_color='#EBEBEB',
            font=('Arial', 12),
        )
        self.username = CTkEntry(
            self.form_content,
            placeholder_text='👤 Username',
            width=240,
            height=34,
            corner_radius=8,
            border_width=1,
            border_color='#CDCDCD',
            fg_color='#EBEBEB',
            font=('Arial', 12),
        )
        self.email = CTkEntry(
            self.form_content,
            placeholder_text='✉ Email @gmail.com (Optional)',
            width=240,
            height=34,
            corner_radius=8,
            border_width=1,
            border_color='#CDCDCD',
            fg_color='#EBEBEB',
            font=('Arial', 12),
        )
        self.password = CTkEntry(
            self.form_content,
            placeholder_text='🔒 Password',
            width=240,
            height=34,
            corner_radius=8,
            border_width=1,
            border_color='#CDCDCD',
            fg_color='#EBEBEB',
            font=('Arial', 12),
            show='*',
        )
        self.confirm_password = CTkEntry(
            self.form_content,
            placeholder_text='🔒 Confirm password',
            width=240,
            height=34,
            corner_radius=8,
            border_width=1,
            border_color='#CDCDCD',
            fg_color='#EBEBEB',
            font=('Arial', 12),
            show='*',
        )
        self.submit = CTkButton(
            self.form_content,
            text='Finish Setup',
            text_color='white',
            fg_color='#6E6EFF',
            hover_color='#6E6EFF',
            width=140,
            height=30,
            font=('Arial', 12, 'bold'),
            corner_radius=8,
            command=self.submit_request,
            cursor='hand2',
        )

    def create_layout(self):
        self.wrapper.pack(expand=True, padx=20, pady=20)
        self.wrapper.pack_propagate(False)
        self.subtitle.pack(pady=30)
        self.form_content.pack(expand=True, padx=10)
        for widgets in self.form_content.winfo_children():
            if widgets == self.submit:
                continue
            widgets.pack(pady=(0, 22))
        self.submit.pack(pady=(20,))

    def create_overlay(self):
        self.overlay = CTkFrame(self, fg_color=self.cget('fg_color'))

        wrapper = CTkFrame(
            self.overlay,
            fg_color=self.wrapper.cget('fg_color'),
            width=self.wrapper.cget('width'),
        )
        wrapper.pack(expand=True, padx=20, pady=20)

        form_content = CTkFrame(
            wrapper, fg_color='transparent', height=self.form_content.cget('height')
        )
        form_content.pack(expand=True, padx=10, pady=10)

    def create_binds(self):
        EventHandler.bind_event(self.submit_request, self.submit)
        EventHandler.bind_enter_key(self.submit_request, self.confirm_password)
        EventHandler.bind_enter_key(
            self.focus_next, self.name, self.username, self.email, self.password
        )

    def submit_request(self, event=None):
        self.controller.register(
            name=self.name.get(),
            username=self.username.get(),
            email=self.email.get(),
            password=self.password.get(),
            confirm_password=self.confirm_password.get(),
        )

    def focus_next(self, event):
        event.widget.tk_focusNext().focus()
        return 'break'
