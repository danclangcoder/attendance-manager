from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel


class SetupPage(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.window = master
        self.controller = controller

        entry_form = CTkFrame(master=self, fg_color=("#f0f0f0", "#333333"), corner_radius=12, width=400, height=600)
        entry_form.pack(expand=True)

        entry_form.grid_propagate(False)
        entry_form.grid_rowconfigure(0, weight=1)
        entry_form.grid_rowconfigure(11, weight=1)
        entry_form.grid_columnconfigure(0, weight=1)
        entry_form.grid_columnconfigure(2, weight=1)

        CTkLabel(master=entry_form, text="Setup", font=("Arial", 20, "bold")).grid(row=1, column=1, pady=20)
        CTkLabel(master=entry_form, text="Personal Information", font=("Arial", 12, "bold")).grid(row=2, column=1, pady=5, sticky="w")
        self.first_name = CTkEntry(master=entry_form, placeholder_text="First Name", width=250, border_width=1, border_color="#888888")
        self.first_name.grid(row=3, column=1, pady=5)
        self.first_name.bind("<Return>", self.focus_next)
        self.middle_name = CTkEntry(master=entry_form, placeholder_text="Middle Name (Optional)", width=250, border_width=1, border_color="#888888")
        self.middle_name.grid(row=4, column=1, pady=5)
        self.middle_name.bind("<Return>", self.focus_next)
        self.last_name = CTkEntry(master=entry_form, placeholder_text="Last Name", width=250, border_width=1, border_color="#888888")
        self.last_name.grid(row=5, column=1, pady=(5, 25))
        self.last_name.bind("<Return>", self.focus_next)
        CTkLabel(master=entry_form, text="Account Information", font=("Arial", 12, "bold")).grid(row=6, column=1, pady=5, sticky="w")
        self.email = CTkEntry(master=entry_form, placeholder_text="📧 Email (Optional)", width=250, border_width=1, border_color="#888888")
        self.email.grid(row=7, column=1, pady=5)
        self.email.bind("<Return>", self.focus_next)
        self.username = CTkEntry(master=entry_form, placeholder_text="👤 Username", width=250, border_width=1, border_color="#888888")
        self.username.grid(row=8, column=1, pady=5)
        self.username.bind("<Return>", self.focus_next)
        self.password = CTkEntry(master=entry_form, placeholder_text="🔒 Password", show="*", width=250, border_width=1, border_color="#888888")
        self.password.grid(row=9, column=1, pady=5)
        self.password.bind("<Return>", self.submit)
        CTkButton(master=entry_form, text="Create Account", command=self.submit).grid(row=10, column=1, pady=20)

    def submit(self, event=None):
        success, message = self.controller.register(
            self.first_name.get(),
            self.middle_name.get(),
            self.last_name.get(),
            self.username.get(),
            self.password.get(),
            self.email.get()
        )
        if not success:
            self.window.show_error(title="Cannot create user", message=message)

    def focus_next(self, event):
        event.widget.tk_focusNext().focus()
        return "break"
