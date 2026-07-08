from customtkinter import CTkFrame
from src.gui.manager import ResizeManager


class ResponsivePage(CTkFrame):
    layout_handler = None

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.current_breakpoint = None

    def enable_resize(self):
        self.bind('<Configure>', self._on_resize)

    def _on_resize(self, event):
        ResizeManager.handle_resize(
            widget=self,
            width=event.width,
            height=event.height,
            callback=self._apply_layout,
        )

    def _apply_layout(self, breakpoint):
        if breakpoint == self.current_breakpoint:
            return

        self.current_breakpoint = breakpoint

        if self.layout_handler:
            self.layout_handler.apply_layout(self, breakpoint)
