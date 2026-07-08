class EventHandler:
    @staticmethod
    def bind_event(callback, widget):
        widget.configure(command=callback)

    @staticmethod
    def bind_enter_key(callback, *entries):
        for entry in entries:
            entry.bind('<Return>', callback)

    @staticmethod
    def bind_esc_key(callback, *entries):
        for entry in entries:
            entry.bind('<Escape>', callback)
