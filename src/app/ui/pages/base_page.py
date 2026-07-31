from customtkinter import CTkFrame, CTkLabel

from app.ui.components import Sidebar


class BasePage(CTkFrame):
    def __init__(self, master, *, fg_color="#e3e3e3", corner_radius=0, title=None, sidebar=False):
        super().__init__(master, fg_color=fg_color, corner_radius=corner_radius)
        if sidebar:
            self.sidebar = Sidebar(self, root=master)
            self.sidebar.pack(side="left", fill="y")
        if title is not None:
            self.page_title = CTkLabel(master=self, fg_color="#e3e3e3", text=title, text_color="#464646", font=("Arial", 24, "bold"))
            self.page_title.pack(pady=20)

        self.wrapper = CTkFrame(master=self, fg_color="#e3e3e3")
        self.wrapper.pack(fill="both", expand=True, padx=10)
