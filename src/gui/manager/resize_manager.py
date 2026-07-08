class ResizeManager:
    BREAKPOINTS = {'sm': (960, 540), 'm': (1280, 720), 'l': (1920, 1080)}
    resize_state = {}

    @staticmethod
    def get_breakpoint(width, height):
        if width <= 960 or height <= 540:
            return 'sm'
        elif width <= 1280 or height <= 720:
            return 'm'
        return 'l'

    @staticmethod
    def show_overlay(widget):
        widget.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        widget.overlay.lift()

    @staticmethod
    def hide_overlay(widget):
        widget.overlay.place_forget()

    @classmethod
    def apply_resize(cls, widget, width, height, callback):
        cls.resize_state.pop(widget, None)
        breakpoint = cls.get_breakpoint(width, height)
        callback(breakpoint)
        cls.hide_overlay(widget)

    @classmethod
    def handle_resize(cls, widget, width, height, callback):
        cls.show_overlay(widget)
        if widget in cls.resize_state:
            widget.after_cancel(cls.resize_state[widget])
        cls.resize_state[widget] = widget.after(
            300, lambda: cls.apply_resize(widget, width, height, callback)
        )
