from CTkToolTip import CTkToolTip
from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel, CTkOptionMenu


class ClassCard(CTkFrame):
    def __init__(self, master, root, controller, on_save, on_discard, on_delete, edit_mode=True, data=None):
        super().__init__(master, fg_color=("#f6f6f6", "#333333"), width=300, height=300, corner_radius=15)

        self.window = root
        self.controller = controller
        self.on_save = on_save
        self.on_discard = on_discard
        self.on_delete = on_delete
        self.data = data

        self.pack_propagate(False)

        if edit_mode:
            self.create_edit_widgets()
        else:
            self.create_display_widgets()

    def create_edit_widgets(self):
        self.entries = CTkFrame(master=self, fg_color="transparent")
        self.entries.pack(fill="x", padx=15, pady=15)
        self.entries.grid_columnconfigure(0, weight=1)

        CTkLabel(master=self.entries, text="Subject").grid(row=0, column=0, sticky="w", padx=5)

        self.subject_entry = CTkEntry(master=self.entries, placeholder_text="Subject Name or Code", height=32, corner_radius=10)
        self.subject_entry.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew", columnspan=2)

        CTkLabel(master=self.entries, text="Section").grid(row=2, column=0, sticky="w", padx=5)

        self.section_entry = CTkEntry(master=self.entries, placeholder_text="Section (e.g., LAGBSITM91)", height=32, corner_radius=10)
        self.section_entry.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew", columnspan=2)

        self.dropdown_widgets = CTkFrame(master=self, fg_color="transparent")
        self.dropdown_widgets.pack(pady=10)

        self.courses = CTkOptionMenu(master=self.dropdown_widgets, values=["BSIT", "BSHM", "BSBA"], width=100, fg_color=("#dddddd", "#444444"), text_color=("black", "white"))
        self.courses.grid(row=0, column=0, padx=5)
        self.year_level = CTkOptionMenu(master=self.dropdown_widgets, values=["1st Year", "2nd Year", "3rd Year"], width=100, fg_color=("#dddddd", "#444444"), text_color=("black", "white"))
        self.year_level.grid(row=0, column=1, padx=5)

        self.buttons = CTkFrame(master=self, fg_color="transparent")
        self.buttons.pack(pady=20, side="bottom")

        CTkButton(master=self.buttons, text="Save", command=self.save_widget_state, width=80, corner_radius=12).pack(side="left", padx=5)
        CTkButton(master=self.buttons, text="Discard", command=self.discard_widget_state, width=80, corner_radius=12).pack(side="left", padx=5)

    def create_display_widgets(self):
        if self.data is None:
            return

        delete_button = CTkButton(
            master=self,
            text="x",
            text_color=("#464646", "#dcdcdc"),
            fg_color="transparent",
            hover_color=("#f6f6f6", "#333333"),
            width=20,
            height=20,
            command=self.delete_widget,
        )
        delete_button.pack(side="right", anchor="ne", padx=5, pady=5)

        self.subject_name = CTkLabel(
            master=self,
            text=self.data.subject.name,
            font=("Arial", 16, "bold"),
        )
        self.subject_name.pack(anchor="w", padx=15, pady=(15, 0))

        self.section_name = CTkLabel(
            master=self,
            text=self.data.section.name,
            font=("Arial", 12, "bold"),
        )
        self.section_name.pack(anchor="w", padx=15)

        self.delete_tooltip = CTkToolTip(delete_button, message="Delete Class")

    def save_widget_state(self, event=None):
        subject = self.subject_entry.get().strip()
        section = self.section_entry.get().strip()
        course = self.courses.get().strip()
        year_level = self.year_level.get().strip()

        if not subject or not section:
            return

        self.save_class_data(subject, section, course, year_level)
        self.on_save(self)

    def save_class_data(self, subject, section, course, year_level):
        success, message = self.controller.create_class(subject, section, course, year_level)
        if not success:
            self.window.show_error(title="Database error", message=message)

    def discard_widget_state(self, event=None):
        self.on_discard(self)

    def delete_widget(self, event=None):
        if hasattr(self, "delete_tooltip"):
            self.delete_tooltip.destroy()

        self.on_delete(self)
