from customtkinter import CTkFrame, CTkLabel, CTkScrollableFrame, CTkScrollbar, CTkCanvas

from app.ui.components import Sidebar


class BasePage(CTkFrame):
    def __init__(self, master, *, fg_color=("#e3e3e3", "#242424"), corner_radius=0, title=None, sidebar=False):
        super().__init__(master, fg_color=fg_color, corner_radius=corner_radius)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        if sidebar:
            self.sidebar = Sidebar(self, root=master)
            self.sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")

        if title:
            self.page_title = CTkLabel(
                self,
                text=title,
                font=("Arial", 24, "bold")
            )
            self.page_title.grid(row=0, column=1, pady=20)

        wrapper_container = CTkFrame(self, fg_color="transparent")
        wrapper_container.grid(row=1, column=1, sticky="nsew", padx=10, pady=(0, 10))

        self.wrapper = CTkScrollableFrame(
            wrapper_container,
            fg_color=("#e3e3e3", "#242424")
        )
        self.wrapper.pack(fill="both", expand=True)