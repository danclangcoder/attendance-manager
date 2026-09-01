import customtkinter as ctk


class ScheduleWidget(ctk.CTkFrame):
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    HOURS = [f"{hour:02d}" for hour in range(1, 13)]
    MINUTES = [f"{minute:02d}" for minute in range(0, 60, 5)]
    PERIODS = ["AM", "PM"]

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.day = ctk.CTkOptionMenu(self, values=self.DAYS)

        self.start_hour = ctk.CTkOptionMenu(self, values=self.HOURS)

        self.start_minute = ctk.CTkOptionMenu(self, values=self.MINUTES)

        self.start_period = ctk.CTkOptionMenu(self, values=self.PERIODS)

        self.end_hour = ctk.CTkOptionMenu(self, values=self.HOURS)

        self.end_minute = ctk.CTkOptionMenu(self, values=self.MINUTES)

        self.end_period = ctk.CTkOptionMenu(self, values=self.PERIODS)

        self._layout()

    def _layout(self):
        self.day.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        ctk.CTkLabel(self, text="Start").grid(row=1, column=0, padx=5)

        self.start_hour.grid(row=1, column=1, padx=2)
        self.start_minute.grid(row=1, column=2, padx=2)
        self.start_period.grid(row=1, column=3, padx=2)

        ctk.CTkLabel(self, text="End").grid(row=2, column=0, padx=5)

        self.end_hour.grid(row=2, column=1, padx=2)
        self.end_minute.grid(row=2, column=2, padx=2)
        self.end_period.grid(row=2, column=3, padx=2)

    def get_value(self):
        return {
            "day": self.day.get(),
            "start_time": self._get_time(self.start_hour, self.start_minute, self.start_period),
            "end_time": self._get_time(self.end_hour, self.end_minute, self.end_period),
        }

    @staticmethod
    def _get_time(hour, minute, period):
        return f"{hour.get()}:{minute.get()} {period.get()}"
