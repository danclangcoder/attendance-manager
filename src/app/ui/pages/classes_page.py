from customtkinter import CTkButton, CTkFrame, CTkLabel

from app.ui.components import ClassCard

from .base_page import BasePage


class ClassesPage(BasePage):
    def __init__(self, master):
        super().__init__(master, title="Classes", sidebar=True)

        self.classes = []
        self.active_card = None

        CTkLabel(master=self.wrapper, text="Manage Classroom", text_color="#464646", font=("Arial", 16, "bold")).pack(anchor="w", padx=5, pady=20)
        self.add_button = CTkButton(master=self.wrapper, text="Add Class", command=self.create_card)
        self.add_button.pack(anchor="w", padx=5, pady=5)
        self.container = CTkFrame(master=self.wrapper, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=5, pady=5)
        self.default = CTkLabel(master=self.container, text="No classes added yet", text_color="#464646", font=("Arial", 16, "bold"))
        self.default.place(relx=0.5, rely=0.5, y=-25, anchor="center")

    def create_card(self, event=None):
        self.add_button.configure(state="disabled")
        self.active_card = ClassCard(
            master=self.container, 
            on_save=self.save_card,
            on_discard=self.cancel_edit,
            on_delete=self.delete_card,
        )
        self.active_card.pack(side="left", anchor="n", padx=(0, 10), pady=5)
        self.active_card.pack_propagate(False)
        self.update_placeholder()

    def save_card(self, card):
        if card not in self.classes:
            self.classes.append(card)
        self.add_button.configure(state="normal")
        self.update_placeholder()
        self.active_card = None

    def cancel_edit(self, card):
        card.destroy()
        if card is self.active_card:
            self.active_card = None
        self.add_button.configure(state="normal")
        self.update_placeholder()

    def delete_card(self, card):
        if card in self.classes:
            self.classes.remove(card)
        card.destroy()
        if card is self.active_card:
            self.active_card = None
        self.add_button.configure(state="normal")
        self.update_placeholder()

    def update_placeholder(self):
        if self.classes or self.active_card is not None:
            self.default.place_forget()
        else:
            self.default.place(relx=0.5, rely=0.5, y=-25, anchor="center")