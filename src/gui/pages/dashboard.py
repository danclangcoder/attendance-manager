from customtkinter import CTkFrame, CTkLabel
from src.gui.widgets import Sidebar
from src.gui.responsive_layouts import ResponsivePage, ResponsiveDashboard


class DashboardPage(ResponsivePage):
    layout_handler = ResponsiveDashboard

    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color='#ffffff')

        self.controller = parent.controller

        self.sidebar = Sidebar(parent=self, root=parent)
        self.sidebar.pack(fill='both', side='left')
        self.sidebar.pack_propagate(False)

        self.create_widgets()
        self.create_overlay()
        self.enable_resize()

    def create_widgets(self):
        content_frame = CTkFrame(master=self, corner_radius=0, fg_color='#F8FAFC')
        content_frame.pack(expand=True, fill='both', side='left')

        self.cards_container = CTkFrame(master=content_frame, fg_color='transparent')
        self.cards_container.pack(expand=True, fill='x', side='left', padx=(20, 10), pady=35, anchor='n')

        self.present_card = CTkFrame(
            master=self.cards_container,
            width=160,
            height=100,
            fg_color='#FFFFFF',
            border_color='#E2E8F0',
            border_width=1,
        )
        self.present_card.pack(side='left', padx=10, expand=True, fill='both')
        self.present_card.pack_propagate(False)

        self.present_num = CTkLabel(
            master=self.present_card,
            text='0',
            text_color='#A2A8B4',
            font=('Arial', 24, 'bold'),
        )
        self.present_num.pack(expand=True)

        self.present_label = CTkLabel(
            master=self.present_card,
            text='PRESENT',
            fg_color='transparent',
            text_color='#A2A8B4',
            font=('Arial', 16, 'bold'),
        )
        self.present_label.pack(pady=(0, 10))

        self.absent_card = CTkFrame(
            master=self.cards_container,
            width=160,
            height=100,
            fg_color='#FFFFFF',
            border_color='#E2E8F0',
            border_width=1,
        )
        self.absent_card.pack(side='left', padx=10, expand=True, fill='both')
        self.absent_card.pack_propagate(False)

        self.absent_num = CTkLabel(
            master=self.absent_card,
            text='0',
            text_color='#A2A8B4',
            font=('Arial', 24, 'bold'),
        )
        self.absent_num.pack(expand=True)

        self.absent_label = CTkLabel(
            master=self.absent_card,
            text='ABSENT',
            fg_color='transparent',
            text_color='#A2A8B4',
            font=('Arial', 16, 'bold'),
        )
        self.absent_label.pack(pady=(0, 10))

        self.late_card = CTkFrame(
            master=self.cards_container,
            width=160,
            height=100,
            fg_color='#FFFFFF',
            border_color='#E2E8F0',
            border_width=1,
        )
        self.late_card.pack(side='left', padx=10, expand=True, fill='both')
        self.late_card.pack_propagate(False)

        self.late_num = CTkLabel(
            master=self.late_card,
            text='0',
            text_color='#A2A8B4',
            font=('Arial', 24, 'bold'),
        )
        self.late_num.pack(expand=True)

        self.late_label = CTkLabel(
            master=self.late_card,
            text='LATE',
            fg_color='transparent',
            text_color='#A2A8B4',
            font=('Arial', 16, 'bold'),
        )
        self.late_label.pack(pady=(0, 10))

    def create_overlay(self):
        self.overlay = CTkFrame(self, fg_color=self.cget('fg_color'), corner_radius=0)
        self.sidebar_overlay = CTkFrame(
            self.overlay, fg_color='#3B82F6', width=150, corner_radius=0
        )
        self.sidebar_overlay.pack(fill='both', side='left')
        self.sidebar_overlay.pack_propagate(False)

        content_frame = CTkFrame(master=self.overlay, corner_radius=0, fg_color='#F8FAFC')
        content_frame.pack(expand=True, fill='both', side='left')

        cards_container = CTkFrame(master=content_frame, fg_color='transparent')
        cards_container.pack(fill='x', padx=20, pady=20)

        CTkFrame(
            master=cards_container,
            width=150,
            height=100,
            fg_color='#FFFFFF',
            border_color='#E2E8F0',
            border_width=1,
        ).pack(side='left', expand=True, fill='both', padx=10)
        CTkFrame(
            master=cards_container,
            width=150,
            height=100,
            fg_color='#FFFFFF',
            border_color='#E2E8F0',
            border_width=1,
        ).pack(side='left', expand=True, fill='both', padx=10)
        CTkFrame(
            master=cards_container,
            width=150,
            height=100,
            fg_color='#FFFFFF',
            border_color='#E2E8F0',
            border_width=1,
        ).pack(side='left', expand=True, fill='both', padx=10)

    def update_overlay(self):
        if self.sidebar.toggled:
            self.sidebar_overlay.configure(width=self.sidebar.expanded)
        else:
            self.sidebar_overlay.configure(width=self.sidebar.collapsed)

    def on_refresh(self):
        user = self.current_user

    @property
    def current_user(self):
        return self.controller.current_user
