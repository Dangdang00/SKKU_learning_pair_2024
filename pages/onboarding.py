import tkinter as tk
import csv
import os
from pages.home import HomePage

USER_FILE_PATH = "data/user.csv"


class OnBoardingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        root_container = tk.Frame(self, width=393, height=852, bg="#FFFFFF")
        root_container.pack_propagate(False)
        root_container.pack(fill="both", expand=True)

        onboarding_container = tk.Frame(root_container, bg="#FFFFFF")
        onboarding_container.pack(expand=True)

        header_label = tk.Label(
            onboarding_container,
            text="🍴냉장고를 부탁해!",
            bg="#FFFFFF",
            font=("Pretendard", 18, "bold"),
        )
        header_label.pack(pady=(0, 24))

        input_label = tk.Label(
            onboarding_container,
            text="이름",
            bg="#FFFFFF",
            font=("Pretendard", 14),
            anchor="w",
        )
        input_label.pack(fill="x", pady=(0, 2))

        input_outline_container = tk.Frame(onboarding_container, bg="#757575", bd=1)
        input_outline_container.pack()

        input_container = tk.Frame(input_outline_container, bg="#FFFFFF", height=100)
        input_container.pack()
        self.input_field = tk.Entry(
            input_container,
            relief="flat",
            highlightthickness=0,
            font=("Pretendard", 16),
        )
        self.input_field.pack(fill="x", padx=4, pady=4)

        self.error_label = tk.Label(
            onboarding_container,
            text="",
            bg="#FFFFFF",
            font=("Pretendard", 12),
            fg="red",
            anchor="w",
        )
        self.error_label.pack(fill="x", pady=2)

        self.unreg_button = tk.Label(
            onboarding_container,
            text="시작하기!",
            fg="#FFFFFF",
            bg="#84DC83",
            height=2,
            font=("Pretendard", 14),
        )
        self.unreg_button.pack(fill="x", pady=16)
        self.unreg_button.bind("<Button-1>", lambda e: self.on_button_click(e))

    def on_button_click(self, event):
        user_input = self.input_field.get()

        if not len(user_input.replace(" ", "")):
            self.error_label.config(text="이름을 입력해주세요!")
            return

        self.error_label.config(text="")

        is_file_empty = (
            not os.path.exists(USER_FILE_PATH) or os.path.getsize(USER_FILE_PATH) == 0
        )

        with open(USER_FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if is_file_empty:
                writer.writerow(["id", "name"])

            writer.writerow([0, user_input])

        self.controller.user_info = {"id": 0, "name": user_input}
        self.controller.show_frame(HomePage)
