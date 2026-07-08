class ResponsiveLogin:
    style = {
        'sm': {
            'title_font': ('Arial', 16, 'bold'),
            'entry_width': 220,
            'button_font': ('Arial', 12),
            'button_height': 30,
            'app_font': ('Arial', 16, 'bold'),
            'school_font': ('Arial', 12, 'bold'),
            'logo_size': (110, 76),
            'qr_size': (76, 76),
            'school_name': 'Access Computer College\n(Lagro)',
            'box_w': 300
        },
        'm': {
            'title_font': ('Arial', 24, 'bold'),
            'entry_width': 260,
            'button_font': ('Arial', 14),
            'button_height': 32,
            'app_font': ('Arial', 24, 'bold'),
            'school_font': ('Arial', 16, 'bold'),
            'logo_size': (110, 76),
            'qr_size': (76, 76),
            'school_name': 'Access Computer College (Lagro)',
            'box_w': 400
        },
        'l': {
            'title_font': ('Arial', 32, 'bold'),
            'entry_width': 320,
            'button_font': ('Arial', 16),
            'button_height': 34,
            'app_font': ('Arial', 36, 'bold'),
            'school_font': ('Arial', 24, 'bold'),
            'logo_size': (165, 114),
            'qr_size': (114, 114),
            'school_name': 'Access Computer College (Lagro)',
            'box_w': 500
        },
    }

    @classmethod
    def apply_layout(cls, page, breakpoint):
        style = cls.style[breakpoint]

        page.form_label.configure(font=style['title_font'])
        page.username_entry.configure(width=style['entry_width'])
        page.password_entry.configure(width=style['entry_width'])
        page.login_button.configure(
            width=140, height=style['button_height'], font=style['button_font']
        )
        page.app_name.configure(font=style['app_font'])
        page.school_name.configure(font=style['school_font'], text=style['school_name'])
        page.school_img.configure(size=style['logo_size'])
        page.app_img.configure(size=style['qr_size'])

        page.splash_cover.configure(width=style['box_w'])
