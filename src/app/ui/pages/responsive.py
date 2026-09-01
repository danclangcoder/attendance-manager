class ResizeHandler:
    def __init__(self, window, breakpoints):
        self.window = window
        self.breakpoints = {key: val for key, val in sorted(breakpoints.items())}
        self.current_breakpoint = None

        # resize event when interacting with the window
        self.window.bind("<Configure>", self.check_size)
        self.window.update()

        min_width = list(self.breakpoints)[0]
        min_height = 640
        self.window.minsize(min_width, min_height)

    def check_size(self, event):
        if event.widget == self.window:
            window_width = event.width
            resize_width = None

            """
            Breakpoints
                S <= 640, 
                M <= 720, 
            """
            for breakpoint in self.breakpoints:
                delta = window_width - breakpoint
                if delta >= 0:
                    resize_width = breakpoint

            if resize_width is not None and resize_width != self.current_breakpoint:
                self.current_breakpoint = resize_width
                self.breakpoints[self.current_breakpoint]()
