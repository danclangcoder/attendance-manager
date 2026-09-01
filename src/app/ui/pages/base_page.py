from customtkinter import CTkFrame, CTkLabel

from app.ui.components import Sidebar


class BasePage(CTkFrame):
    def __init__(self, master, *, fg_color=("#e3e3e3", "#242424"), corner_radius=0, title=None, sidebar=False):
        super().__init__(master, fg_color=fg_color, corner_radius=corner_radius)

        if sidebar:
            self.sidebar = Sidebar(self, root=master)
            self.sidebar.pack(side="left", fill="y")

        self.wrapper = CTkFrame(self, fg_color=("#e3e3e3", "#242424"))
        self.wrapper.pack(fill="both", expand=True)

        if title:
            self.page_title = CTkLabel(self.wrapper, text=title, font=("Arial", 24, "bold"))
            self.page_title.pack(pady=20)

    def resize_small(self):
        pass

    def resize_medium(self):
        pass
