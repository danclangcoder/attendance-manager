from CTkToolTip import CTkToolTip
from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel

from .ctk_date_picker import CTkDatePicker


class ClassCard(CTkFrame):
    def __init__(self, master, on_save, on_discard, on_delete):
        super().__init__(master, fg_color="#f6f6f6", width=400, height=300, corner_radius=15)

        self.on_save = on_save
        self.on_discard = on_discard
        self.on_delete = on_delete

        self.entries = CTkFrame(master=self, fg_color="transparent")
        self.entries.pack(pady=20)
        CTkLabel(master=self.entries, text="Subject").grid(row=0, column=0, sticky="w", padx=5)
        self.subject_entry = CTkEntry(master=self.entries, placeholder_text="Subject Name or Code (e.g., DATALGO)", width=300, height=32, corner_radius=10)
        self.subject_entry.grid(row=1, column=0, padx=5, pady=(0, 10))
        CTkLabel(master=self.entries, text="Section").grid(row=2, column=0, sticky="w", padx=5)
        self.section_entry = CTkEntry(master=self.entries, placeholder_text="Section (e.g., LAGBSITM91)", width=300, height=32, corner_radius=10)
        self.section_entry.grid(row=3, column=0, padx=5, pady=(0, 10))
        self.calendar = CTkDatePicker(master=self)
        self.calendar.set_allow_manual_input(True)
        self.calendar.pack(pady=5)
        self.buttons = CTkFrame(master=self, fg_color="transparent")
        self.buttons.pack(pady=20, side="bottom")
        CTkButton(master=self.buttons, text="Save", command=self.save_widget_state).pack(side="left", padx=5)
        CTkButton(master=self.buttons, text="Discard", command=self.discard_widget_state).pack(side="left", padx=5)

    def create_card_widgets(self):
        delete_button = CTkButton(master=self, text="x", text_color="black", fg_color="transparent", hover_color="#f6f6f6", width=20, height=20, command=self.delete_widget)
        delete_button.pack(side="right", anchor="ne", padx=5, pady=5)
        self.subject_name = CTkLabel(master=self, text="", text_color="#464646", font=("Arial", 16, "bold"))
        self.section_name = CTkLabel(master=self, text="", text_color="#464646", font=("Arial", 12, "bold"))
        self.subject_name.pack(anchor="w", padx=15, pady=(15, 0))
        self.section_name.pack(anchor="w", padx=15, pady=0)
        CTkToolTip(delete_button, message="Delete Class")

    def save_widget_state(self, event=None):
        subject_name = self.subject_entry.get()
        section_name = self.section_entry.get()

        if not subject_name or not section_name:
            return

        self.entries.destroy()
        self.buttons.destroy()

        self.create_card_widgets()
        self.subject_name.configure(text=subject_name.upper())
        self.section_name.configure(text=section_name.upper())
        self.on_save(self)

    def discard_widget_state(self, event=None):
        self.on_discard(self)

    def delete_widget(self, event=None):
        self.on_delete(self)