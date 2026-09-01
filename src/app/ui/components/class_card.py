from CTkToolTip import CTkToolTip
from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel, CTkOptionMenu


class ClassCard(CTkFrame):
    def __init__(self, master, root, controller, on_save, on_discard, on_delete, edit_mode=True, data=None, sections=None):
        super().__init__(master, fg_color=("#f6f6f6", "#333333"), corner_radius=15, width=200, height=360)

        self.window = root
        self.controller = controller
        self.on_save = on_save
        self.on_discard = on_discard
        self.on_delete = on_delete
        self.data = data
        self.sections = sections or []

        self.grid_propagate(False)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)

        if edit_mode:
            self.create_edit_widgets()
        else:
            self.create_display_widgets()

    def create_edit_widgets(self):
        # Course
        CTkLabel(self, text="Course").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

        courses = self.controller.get_all_courses()
        self.courses = courses

        course_names = [course.name for course in courses]

        self.course_options = CTkOptionMenu(self, values=course_names or ["Select course"], width=200, command=self.on_course_change)
        self.course_options.grid(row=1, column=0, padx=10, pady=(0, 10), columnspan=2)

        # Year Level
        CTkLabel(self, text="Year Level").grid(row=2, column=0, sticky="w", padx=10, pady=(0, 5))

        self.year_options = CTkOptionMenu(self, values=["Select year level"], width=200, command=self.on_year_change)
        self.year_options.grid(row=3, column=0, padx=10, pady=(0, 10), columnspan=2)

        # Section
        CTkLabel(self, text="Section").grid(row=4, column=0, sticky="w", padx=10, pady=(0, 5))

        self.section_options = CTkOptionMenu(self, values=["Select section"], width=200)
        self.section_options.grid(row=5, column=0, padx=10, pady=(0, 10), columnspan=2)

        # Subject
        CTkLabel(self, text="Subject").grid(row=6, column=0, sticky="w", padx=10, pady=(0, 5))

        self.subject_entry = CTkEntry(self, placeholder_text="Subject Name or Code", height=32, corner_radius=10, width=220)
        self.subject_entry.grid(row=7, column=0, padx=10, pady=(0, 10), columnspan=2)

        # Buttons
        CTkButton(self, text="Save", command=self.save_widget_state, width=80, corner_radius=12).grid(row=8, column=0, padx=(10, 5), pady=20, sticky="nsew")

        CTkButton(self, text="Discard", command=self.discard_widget_state, width=80, corner_radius=12).grid(row=8, column=1, padx=(0, 10), pady=20, sticky="nsew")

        # Defaults
        if courses:
            self.course_options.set(courses[0].name)
            self.on_course_change(courses[0].name)

    def on_course_change(self, course_name):
        course = next((course for course in self.courses if course.name == course_name), None)

        if course is None:
            return

        self.selected_course = course

        year_levels = sorted({section.year_level for section in self.sections if section.course_id == course.id})

        self.year_options.configure(values=year_levels or ["Select year level"])

        if year_levels:
            self.year_options.set(year_levels[0])
            self.on_year_change(year_levels[0])
        else:
            self.year_options.set("Select year level")
            self.section_options.configure(values=["Select section"])
            self.section_options.set("Select section")

    def on_year_change(self, year_level):
        if not hasattr(self, "selected_course"):
            return

        sections = [section for section in self.sections if (section.course_id == self.selected_course.id and section.year_level == year_level)]

        section_names = [section.name for section in sections]

        self.filtered_sections = sections

        self.section_options.configure(values=section_names or ["Select section"])

        if section_names:
            self.section_options.set(section_names[0])
        else:
            self.section_options.set("Select section")

    def create_display_widgets(self):
        if self.data is None:
            return

        delete_button = CTkButton(
            master=self, text="x", text_color=("#464646", "#dcdcdc"), fg_color="transparent", hover_color=("#f6f6f6", "#333333"), width=20, height=20, command=self.delete_widget
        )
        delete_button.pack(side="right", anchor="ne", padx=5, pady=5)

        self.subject_name = CTkLabel(master=self, text=self.data.subject.name, font=("Arial", 16, "bold"))
        self.subject_name.pack(anchor="w", padx=15, pady=(15, 0))

        self.section_name = CTkLabel(master=self, text=self.data.section.name, font=("Arial", 12, "bold"))
        self.section_name.pack(anchor="w", padx=15, pady=(0, 15))

        self.delete_tooltip = CTkToolTip(delete_button, message="Delete Class")

    def save_widget_state(self, event=None):
        subject = self.subject_entry.get().strip().upper()
        section_name = self.section_options.get().strip()

        if not subject or not section_name or section_name == "Select section" or not hasattr(self, "filtered_sections"):
            return

        section = next((section for section in self.filtered_sections if section.name == section_name), None)

        if section is None:
            return

        self.save_class_data(subject, section.name, self.selected_course.name, section.year_level)

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
