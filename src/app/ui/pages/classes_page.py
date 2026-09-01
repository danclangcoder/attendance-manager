from customtkinter import CTkButton, CTkFrame, CTkLabel

from app.ui.components import ClassCard

from .base_page import BasePage


class ClassesPage(BasePage):
    def __init__(self, master, controller):
        super().__init__(master, title="Classes", sidebar=True)

        self.window = master
        self.controller = controller

        self.cards = []
        self.classes = []
        self.active_card = None

        self.course_values = []
        self.section_values = []

        CTkLabel(master=self.wrapper, text="Manage Classroom", text_color=("#464646", "#dcdcdc"), font=("Arial", 16, "bold")).pack(anchor="w", padx=20, pady=20)

        # Add class button
        buttons = CTkFrame(master=self.wrapper, fg_color="transparent")
        buttons.pack(anchor="w")

        self.add_class = CTkButton(master=buttons, text="Add Class", command=self.create_card)
        self.add_class.pack(side="left", padx=(20, 5), pady=(10, 5))

        # Class container
        self.container = CTkFrame(master=self.wrapper, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=15, pady=5)

        self.default = CTkLabel(master=self.container, text="No classes added yet", text_color=("#464646", "#dcdcdc"), font=("Arial", 16, "bold"))
        self.default.place(relx=0.5, rely=0.5, y=-25, anchor="center")

        self.update_placeholder()

        self.refresh()

    # ---------------------------------------------------------
    # Classes
    # ---------------------------------------------------------

    def refresh(self, event=None):
        if self.active_card:
            self.active_card.destroy()
            self.active_card = None

        for card in self.cards:
            card.destroy()

        self.cards.clear()

        all_classes = self.controller.get_classes()

        self.classes = all_classes

        for cls in self.classes:
            card = ClassCard(
                master=self.container,
                root=self.window,
                controller=self.controller,
                on_save=self.save_card,
                on_discard=self.cancel_edit,
                on_delete=self.delete_card,
                edit_mode=False,
                data=cls,
            )

            card.pack(padx=5, pady=5, side="left", anchor="nw")

            self.cards.append(card)

        self.update_placeholder()

    def create_card(self, event=None):
        self.add_class.configure(state="disabled")

        sections = self.controller.get_sections()

        self.active_card = ClassCard(
            master=self.container,
            root=self.window,
            controller=self.controller,
            on_save=self.save_card,
            on_discard=self.cancel_edit,
            on_delete=self.delete_card,
            edit_mode=True,
            sections=sections,
        )

        self.active_card.pack(padx=10, pady=5, side="left", anchor="nw")

        self.update_placeholder()

    # ---------------------------------------------------------
    # Card actions
    # ---------------------------------------------------------

    def save_card(self, card):
        if self.active_card:
            self.active_card.destroy()
            self.active_card = None

        self.add_class.configure(state="normal")

        self.refresh()

    def cancel_edit(self, card):
        card.destroy()

        if card is self.active_card:
            self.active_card = None

        self.add_class.configure(state="normal")

        self.update_placeholder()

    def delete_card(self, card):
        self.controller.delete_class(card.data.id)

        self.refresh()

        if card in self.cards:
            self.cards.remove(card)

        card.destroy()

        if card is self.active_card:
            self.active_card = None

        self.add_class.configure(state="normal")

        self.update_placeholder()

    # ---------------------------------------------------------
    # Page lifecycle
    # ---------------------------------------------------------

    def on_hide(self):
        if self.active_card:
            self.active_card.destroy()

        self.active_card = None

        self.add_class.configure(state="normal")

        self.update_placeholder()

    def update_placeholder(self):
        if self.cards or self.active_card or self.classes:
            self.default.place_forget()
        else:
            self.default.place(relx=0.5, rely=0.5, y=-25, anchor="center")
