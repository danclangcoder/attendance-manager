from tkinter import ttk

from customtkinter import CTkButton, CTkFrame, CTkLabel

from .base_page import BasePage


class AttendancePage(BasePage):
    def __init__(self, master):
        super().__init__(master, title="Attendance", sidebar=True)

        card_section = CTkFrame(master=self.wrapper, fg_color="transparent")
        card_section.pack(fill="x")

        card_section.grid_columnconfigure((0, 1, 2), weight=1, uniform="a")
        card_section.grid_rowconfigure(0, weight=0, minsize=100)

        container_1 = CTkFrame(master=card_section, fg_color="#f6f6f6", border_color="#dddddd")
        container_1.grid(column=0, row=0, sticky="nsew", padx=5)
        container_2 = CTkFrame(master=card_section, fg_color="#f6f6f6", border_color="#dddddd")
        container_2.grid(column=1, row=0, sticky="nsew", padx=5)
        container_3 = CTkFrame(master=card_section, fg_color="#f6f6f6", border_color="#dddddd")
        container_3.grid(column=2, row=0, sticky="nsew", padx=5)

        CTkLabel(master=container_1, text="0", text_color="#464646", font=("Arial", 32, "bold")).pack(expand=True, pady=(15, 0))
        CTkLabel(master=container_2, text="0", text_color="#464646", font=("Arial", 32, "bold")).pack(expand=True, pady=(15, 0))
        CTkLabel(master=container_3, text="0", text_color="#464646", font=("Arial", 32, "bold")).pack(expand=True, pady=(15, 0))

        CTkLabel(master=container_1, text="PRESENT", text_color="#8A8A8A", font=("Arial", 12, "bold")).pack(side="bottom")
        CTkLabel(master=container_2, text="ABSENT", text_color="#8A8A8A", font=("Arial", 12, "bold")).pack(side="bottom")
        CTkLabel(master=container_3, text="TOTAL STUDENTS", text_color="#8A8A8A", font=("Arial", 12, "bold")).pack(side="bottom")

        CTkLabel(master=self.wrapper, text="View Attendance", text_color="#464646", font=("Arial", 16, "bold")).pack(anchor="w", padx=5, pady=(10, 5))
        buttons = CTkFrame(master=self.wrapper, fg_color="transparent")
        buttons.pack(anchor="w", padx=5, fill="x")
        CTkButton(master=buttons, text="New Attendance", command=lambda: print("Created new attendance.")).pack(side="left", padx=(0, 5))
        CTkButton(master=buttons, text="Edit Table", command=lambda: print("Edited attendance.")).pack(side="left", padx=(0, 5))

        table = CTkFrame(master=self.wrapper, fg_color="#f6f6f6")
        table.pack(fill="both", padx=5, pady=5)
        treeview = ttk.Treeview(master=table, columns=("default"), show="headings")
        treeview.heading("default", text="(Empty)")
        treeview.pack(fill="both")
