from customtkinter import CTkButton, CTkFrame


class Sidebar(CTkFrame):
    def __init__(self, master, root, fg_color="#3B8ED0", corner_radius=0, width=250):
        super().__init__(master, fg_color=fg_color, corner_radius=corner_radius)

        self.window = root
        self.controller = root.controller
        self.auth = self.controller.auth

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        CTkButton(master=self, text="📋  Attendance", fg_color="transparent", hover_color="#4752AA", anchor="w", command=lambda: root.show_page("attendance")).grid(
            row=0, column=0, pady=(20, 5)
        )
        CTkButton(master=self, text="👥  Classes", fg_color="transparent", hover_color="#4752AA", anchor="w", command=lambda: root.show_page("classes")).grid(row=1, column=0, pady=(5, 5))
        CTkButton(master=self, text="🎓  Students", fg_color="transparent", hover_color="#4752AA", anchor="w", command=lambda: root.show_page("students")).grid(row=2, column=0, pady=(5, 5))
        CTkButton(master=self, text="🛠  Settings", fg_color="transparent", hover_color="#4752AA", anchor="w", command=lambda: root.show_page("settings")).grid(row=3, column=0, pady=(5, 5))
        CTkButton(master=self, text="⬅️  Logout", fg_color="transparent", hover_color="#4752AA", anchor="w", command=self.logout).grid(row=4, column=0, pady=(5, 20), sticky="s")

        self.grid_propagate(False)

    def logout(self, event=None):
        self.controller.logout()
        self.window.show_page("login")
