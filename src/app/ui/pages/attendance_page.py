from customtkinter import CTkButton, CTkFrame, CTkLabel, CTkToplevel, CTkOptionMenu
from CTkTable import CTkTable

from .base_page import BasePage


class AttendancePage(BasePage):
    def __init__(self, master, controller):
        super().__init__(master, title="Attendance", sidebar=True)

        self.window = master
        self.controller = controller

        self.window.center_window(1280, 720)

        card_section = CTkFrame(master=self.wrapper, fg_color="transparent")
        card_section.pack(fill="x")

        card_section.grid_columnconfigure((0, 1, 2), weight=1, uniform="a")
        card_section.grid_rowconfigure(0, weight=0, minsize=100)

        container_1 = CTkFrame(master=card_section, fg_color=("#f6f6f6", "#333333"), border_color="#dddddd")
        container_1.grid(column=0, row=0, sticky="nsew", padx=5)
        container_2 = CTkFrame(master=card_section, fg_color=("#f6f6f6", "#333333"), border_color="#dddddd")
        container_2.grid(column=1, row=0, sticky="nsew", padx=5)
        container_3 = CTkFrame(master=card_section, fg_color=("#f6f6f6", "#333333"), border_color="#dddddd")
        container_3.grid(column=2, row=0, sticky="nsew", padx=5)

        CTkLabel(master=container_1, text="0", text_color=("#464646", "#dcdcdc"), font=("Arial", 32, "bold")).pack(expand=True, pady=(15, 0))
        CTkLabel(master=container_2, text="0", text_color=("#464646", "#dcdcdc"), font=("Arial", 32, "bold")).pack(expand=True, pady=(15, 0))
        CTkLabel(master=container_3, text="0", text_color=("#464646", "#dcdcdc"), font=("Arial", 32, "bold")).pack(expand=True, pady=(15, 0))

        CTkLabel(master=container_1, text="PRESENT", text_color=("#8A8A8A", "#cccccc"), font=("Arial", 12, "bold")).pack(side="bottom")
        CTkLabel(master=container_2, text="ABSENT", text_color=("#8A8A8A", "#cccccc"), font=("Arial", 12, "bold")).pack(side="bottom")
        CTkLabel(master=container_3, text="TOTAL STUDENTS", text_color=("#8A8A8A", "#cccccc"), font=("Arial", 12, "bold")).pack(side="bottom")

        CTkLabel(master=self.wrapper, text="View Attendance", text_color=("#464646", "#dcdcdc"), font=("Arial", 16, "bold")).pack(anchor="w", padx=5, pady=(10, 5))
        buttons = CTkFrame(master=self.wrapper, fg_color="transparent")
        buttons.pack(anchor="w", padx=5, fill="x")
        CTkButton(master=buttons, text="New Attendance", command=lambda: print("Created new attendance.")).pack(side="left", padx=(0, 5))
        CTkButton(master=buttons, text="Select Class", command=self.view_classes).pack(side="left", padx=(0, 5))

        self.content = CTkFrame(master=self.wrapper, fg_color="transparent")
        self.content.pack(fill="both", expand=True)
        self.content.grid_rowconfigure(1, weight=1)
        self.content.grid_columnconfigure(0, weight=1)
        self.table_name = CTkLabel(master=self.content, text="(Select a class)", text_color=("#464646", "#dcdcdc"), font=("Arial", 12, "bold"))
        self.table_name.grid(row=0, column=0)
        treeview = CTkTable(master=self.content, row=10, column=4, values=[["Name", "Student No.", "Section", "Timestamp"]], colors=["white", "white"], header_color="#d6d6d6", )
        treeview.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        footer = CTkFrame(self.wrapper, height=400, corner_radius=10)
        footer.pack(fill="x", padx=10, pady=20)
        footer.pack_propagate(False)
        CTkLabel(master=footer, text="Recent", font=("Firacode Mono", 24)).pack(pady=20)
        
    def refresh(self, event=None):
        # Refresh the page content here
        pass

    def view_classes(self, event=None):
        select_dialog = CTkToplevel(master=self.wrapper)
        select_dialog.geometry("400x400")
        select_dialog.title("Select class")
        select_dialog.transient(master=self.window)
        select_dialog.lift()
        select_dialog.grab_set()

        my_classes = self.controller.get_classes()
        values = [cls.subject.name for cls in my_classes]

        options = CTkOptionMenu(
            select_dialog,
            values=values,
            command=self.select_class,
        )

        options.set("Select")
        options.pack()
        options.focus_set()
        select_dialog.wait_visibility()
        select_dialog.focus_force()

    def select_class(self, subject_name):
        subject = self.controller.get_subject(subject_name)
        print(subject.name)
        
        if subject:
            self.table_name.configure(text="")
            self.table_name.configure(text=subject.name)

    