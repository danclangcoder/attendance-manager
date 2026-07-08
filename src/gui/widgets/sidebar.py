from customtkinter import CTkButton, CTkFrame


class Sidebar(CTkFrame):
    def __init__(self, parent, root):
        super().__init__(parent, corner_radius=0, fg_color='#3B82F6', width=180)

        self.parent = parent
        self.root = root
        self.toggled = True
        self.expanded = 180
        self.collapsed = 50
        self.logout_button_expanded = 100
        self.button_font_expanded = ('Arial', 16)

        self.wrapper = CTkFrame(master=self, fg_color='transparent')
        self.wrapper.place(relx=0.5, rely=0, y=50, anchor='n')

        self.toggle_button = CTkButton(
            master=self,
            text='✖',
            width=20,
            fg_color='transparent',
            hover_color='#2424c4',
            cursor='hand2',
            command=self.toggle_sidebar,
        )
        self.toggle_button.place(relx=1, rely=0, x=-10, y=10, anchor='ne')

        self.create_widgets()

    def create_widgets(self):
        # ✖ collapse | ☰ expand
        self.dashboard_button = CTkButton(
            master=self.wrapper,
            text='🏠 Dashboard',
            font=('Arial', 16),
            width=100,
            height=34,
            fg_color='transparent',
            hover_color='#2424c4',
            anchor='w',
            cursor='hand2',
        )
        self.dashboard_button.pack(pady=5, anchor='w')

        self.attendance_button = CTkButton(
            master=self.wrapper,
            text='📋 Attendance',
            font=('Arial', 16),
            width=100,
            height=34,
            fg_color='transparent',
            hover_color='#2424c4',
            anchor='w',
            cursor='hand2',
        )
        self.attendance_button.pack(pady=5, anchor='w')

        self.students_button = CTkButton(
            master=self.wrapper,
            text='👥 Students',
            font=('Arial', 16),
            width=100,
            height=34,
            fg_color='transparent',
            hover_color='#2424c4',
            anchor='w',
            cursor='hand2',
        )
        self.students_button.pack(pady=5, anchor='w')

        self.logs_button = CTkButton(
            master=self.wrapper,
            text='📄 Logs',
            font=('Arial', 16),
            width=100,
            height=34,
            fg_color='transparent',
            hover_color='#2424c4',
            anchor='w',
            cursor='hand2',
        )
        self.logs_button.pack(pady=5, anchor='w')

        self.profile_button = CTkButton(
            master=self.wrapper,
            text='👤 Profile',
            font=('Arial', 16),
            width=100,
            height=34,
            fg_color='transparent',
            hover_color='#2424c4',
            anchor='w',
            cursor='hand2',
        )
        self.profile_button.pack(pady=5, anchor='w')

        self.settings_button = CTkButton(
            master=self.wrapper,
            text='🛠 Settings',
            font=('Arial', 16),
            width=100,
            height=34,
            fg_color='transparent',
            hover_color='#2424c4',
            anchor='w',
            cursor='hand2',
        )
        self.settings_button.pack(fill='x', pady=5, anchor='w')

        self.logout_button = CTkButton(
            master=self,
            text='⬅️ Logout',
            font=('Arial', 16),
            width=100,
            height=34,
            fg_color='transparent',
            hover_color='#2424c4',
            anchor='center',
            cursor='hand2',
            command=self.logout,
        )
        self.logout_button.place(relwidth=0.7, relx=0.5, rely=1, y=-30, anchor='s')

    def logout(self):
        self.root.controller.logout()

    def toggle_sidebar(self):
        if self.toggled:
            self.collapse()

        else:
            self.expand()

    def collapse(self):
        self.toggled = False
        for widget in self.winfo_children():
            if widget is not self.toggle_button or not self.logout_button:
                widget.place_forget()
        self.configure(width=50)
        self.toggle_button.configure(text='☰')
        self.logout_button.configure(text='⬅️', width=15)
        self.toggle_button.place_configure(relx=0.5, rely=0, x=0, y=10, anchor='n')
        self.logout_button.place_configure(relx=0.5, rely=1, x=0, y=-30, anchor='s')
        self.parent.update_overlay()

    def expand(self):
        self.toggled = True
        self.configure(width=self.expanded)
        self.toggle_button.configure(text='✖')
        self.logout_button.configure(
            text='⬅️ Logout',
            width=self.logout_button_expanded,
            font=self.button_font_expanded,
        )
        self.toggle_button.place_configure(relx=1, rely=0, x=-10, y=10, anchor='ne')
        self.logout_button.place_configure(
            relwidth=0.8, relx=0.5, rely=1, y=-30, anchor='s'
        )
        self.wrapper.place(relx=0.5, rely=0, y=50, anchor='n')
        self.parent.update_overlay()
