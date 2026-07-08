class ResponsiveSetup:
    style = {
        'sm': {
            'subtitle_font': ('Arial', 24, 'bold'),
            'entry_w': 200,
            'box_w': 500,
            'box_h': 500,
        },
        'm': {
            'subtitle_font': ('Arial', 36, 'bold'),
            'entry_w': 240,
            'box_w': 600,
            'box_h': 600,
        },
        'l': {
            'subtitle_font': ('Arial', 40, 'bold'),
            'entry_w': 300,
            'box_w': 700,
            'box_h': 700,
        },
    }

    @classmethod
    def apply_layout(cls, page, breakpoint):
        style = cls.style[breakpoint]

        page.wrapper.configure(width=style['box_w'], height=style['box_h'])
        page.subtitle.configure(font=style['subtitle_font'])
        page.name.configure(width=style['entry_w'])
        page.username.configure(width=style['entry_w'])
        page.email.configure(width=style['entry_w'])
        page.password.configure(width=style['entry_w'])
        page.confirm_password.configure(width=style['entry_w'])
