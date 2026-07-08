class ResponsiveDashboard:
    style = {
        'sm': {
            'sidebar_width': 120,
            'card_width': 100,
            'card_number_font': ('Arial', 24, 'bold'),
            'card_label_font': ('Arial', 12, 'bold'),
            'button_width': 50,
            'button_height': 30,
            'button_font': ('Arial', 12),
            'button_padding': (0, 5),
            'cards_container_padding': 25,
        },
        'm': {
            'sidebar_width': 180,
            'card_width': 200,
            'card_number_font': ('Arial', 24, 'bold'),
            'card_label_font': ('Arial', 16, 'bold'),
            'cards_container_padding': 35,
            'button_width': 100,
            'button_height': 34,
            'button_font': ('Arial', 16),
            'button_padding': 10,
        },
        'l': {
            'sidebar_width': 220,
            'card_width': 250,
            'card_number_font': ('Arial', 32, 'bold'),
            'card_label_font': ('Arial', 24, 'bold'),
            'cards_container_padding': 40,
            'button_width': 150,
            'button_height':  36,
            'button_font': ('Arial', 20, 'bold'),
            'button_padding': 15,
        },
    }

    @classmethod
    def apply_layout(cls, page, breakpoint):
        style = cls.style[breakpoint]

        page.sidebar.expanded = style['sidebar_width']
        page.sidebar.button_width = style['button_width']
        page.sidebar.button_height = style['button_height']
        page.sidebar.button_font_expanded = style['button_font']

        if page.sidebar.toggled:
            page.sidebar.configure(width=page.sidebar.expanded)
            for widget in page.sidebar.winfo_children():
                if hasattr(widget, 'CTkButton'):
                    widget.configure(
                        width=page.sidebar.button_width,
                        height=page.sidebar.button_height,
                        font=page.sidebar.button_font_expanded
                    )
            

        page.sidebar.dashboard_button.configure(
            width=style['button_width'], font=style['button_font']
        )
        page.sidebar.attendance_button.configure(
            width=style['button_width'], font=style['button_font']
        )
        page.sidebar.students_button.configure(
            width=style['button_width'], font=style['button_font']
        )
        page.sidebar.logs_button.configure(
            width=style['button_width'], font=style['button_font']
        )
        page.sidebar.profile_button.configure(
            width=style['button_width'], font=style['button_font']
        )
        page.sidebar.settings_button.configure(
            width=style['button_width'], font=style['button_font']
        )
        page.sidebar.logout_button.configure(
            width=style['button_width'], font=style['button_font']
        )

        page.sidebar.dashboard_button.pack_configure(pady=style['button_padding'])
        page.sidebar.attendance_button.pack_configure(pady=style['button_padding'])
        page.sidebar.students_button.pack_configure(pady=style['button_padding'])
        page.sidebar.logs_button.pack_configure(pady=style['button_padding'])
        page.sidebar.profile_button.pack_configure(pady=style['button_padding'])
        page.sidebar.settings_button.pack_configure(pady=style['button_padding'])

        page.present_card.configure(width=style['card_width'])
        page.absent_card.configure(width=style['card_width'])
        page.late_card.configure(width=style['card_width'])

        page.present_num.configure(font=style['card_number_font'])
        page.absent_num.configure(font=style['card_number_font'])
        page.late_num.configure(font=style['card_number_font'])

        page.present_label.configure(font=style['card_label_font'])
        page.absent_label.configure(font=style['card_label_font'])
        page.late_label.configure(font=style['card_label_font'])

        page.cards_container.pack_configure(pady=style['cards_container_padding'])
