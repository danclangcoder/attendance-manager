from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel


class SetupPage(CTkFrame):
    def __init__(self, master, controller, auth):
        super().__init__(master)

        self.window = master
        self.controller = controller
        self.auth = auth

        entry_form = CTkFrame(master=self, corner_radius=0)
        entry_form.pack(fill="both", expand=True)

        entry_form.grid_propagate(False)
        entry_form.grid_rowconfigure(0, weight=1)
        entry_form.grid_rowconfigure(8, weight=1)

        entry_form.grid_columnconfigure(0, weight=1)
        entry_form.grid_columnconfigure(3, weight=1)

        CTkLabel(master=entry_form, text="Setup").grid(row=1, column=1, columnspan=2, pady=20)
        self.first_name = CTkEntry(master=entry_form, placeholder_text="First Name", width=200)
        self.first_name.grid(row=2, column=1, padx=(0, 5), pady=10)
        self.first_name.bind("<Return>", self.focus_next)
        self.last_name = CTkEntry(master=entry_form, placeholder_text="Last Name", width=200)
        self.last_name.grid(row=2, column=2, padx=(5, 0), pady=10)
        self.last_name.bind("<Return>", self.focus_next)
        self.email = CTkEntry(master=entry_form, placeholder_text="Email (Optional)", width=410)
        self.email.grid(row=4, column=1, pady=5, columnspan=2)
        self.email.bind("<Return>", self.focus_next)
        self.username = CTkEntry(master=entry_form, placeholder_text="Username", width=410)
        self.username.grid(row=5, column=1, pady=5, columnspan=2)
        self.username.bind("<Return>", self.focus_next)
        self.password = CTkEntry(master=entry_form, placeholder_text="Password", show="*", width=410)
        self.password.grid(row=6, column=1, pady=5, columnspan=2)
        self.password.bind("<Return>", self.submit)
        CTkButton(master=entry_form, text="Login", command=self.submit).grid(row=7, column=1, pady=20, columnspan=2)

    def submit(self, event=None):
        success, message = self.auth.register(
            self.first_name.get(),
            self.last_name.get(),
            self.username.get(),
            self.password.get(),
            self.email.get()
        )
        if success:
            self.window.show_page("attendance")
        else:
            self.window.show_error(title="Cannot create user", message=message)

    def focus_next(self, event):
        event.widget.tk_focusNext().focus()
        return "break"
