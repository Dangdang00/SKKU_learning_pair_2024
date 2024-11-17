import tkinter as tk
from tkinter import font
from pages.onboarding import OnBoardingPage
from pages.home import HomePage
from utils import read_csv_user_info


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.page_stack = []
        self.current_frame = None
        self.frames = {}
        self.user_info = read_csv_user_info()
        self.food_data_list = []

        self._initialize_window()
        self._initialize_sidebar()
        self.show_initial_page()

    def _initialize_window(self):
        self.title("냉장고를 부탁해!")
        self.geometry("1080x852")
        self.resizable(False, False)

        icon = tk.PhotoImage(file="assets/favicon.png")
        self.iconphoto(False, icon)

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="ns", padx=(350, 0))

    def _initialize_sidebar(self):
        qr_container = tk.Frame(self, width=200, height=250, bg="#F8F8F8")
        qr_container.grid(row=0, column=1, sticky="s", padx=24, pady=94)
        qr_container.grid_propagate(False)

        qr_img = tk.PhotoImage(file="assets/qr.png")
        image_label = tk.Label(
            qr_container, image=qr_img, width=90, height=90, bg="#F8F8F8"
        )
        image_label.image = qr_img
        image_label.pack(padx=16, pady=16, anchor="w")

        tk.Label(
            qr_container,
            text="냉장고를 부탁해!",
            bg="#F8F8F8",
            font=("Pretendard", 16, "bold"),
        ).pack(padx=16, anchor="w")
        tk.Label(
            qr_container,
            text="QR코드를 스캔하여",
            bg="#F8F8F8",
            font=("Pretendard", 14),
        ).pack(padx=16, anchor="w")
        tk.Label(
            qr_container,
            text="냉장고 정리를 시작해보세요.",
            bg="#F8F8F8",
            font=("Pretendard", 14),
        ).pack(padx=16, pady=(0, 16))

    def show_initial_page(self):
        self.show_frame(OnBoardingPage if self.user_info is None else HomePage)

    def show_frame(self, frame_class, **kwargs):
        if frame_class not in self.frames:
            frame = frame_class(parent=self.container, controller=self, **kwargs)
            self.frames[frame_class] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        else:
            frame = self.frames[frame_class]

        if hasattr(frame, "update_content"):
            frame.update_content(**kwargs)

        if (
            self.current_frame
            and self.current_frame != frame
            and self.current_frame.__class__ != OnBoardingPage
        ):
            self.page_stack.append(self.current_frame)

        if self.current_frame:
            self.current_frame.grid_remove()

        self.current_frame = frame
        self.current_frame.grid()
        self.current_frame.tkraise()

        if hasattr(frame, "refresh_page"):
            frame.refresh_page()

    def go_back(self):
        if self.page_stack:
            self.current_frame.grid_remove()
            self.current_frame = self.page_stack.pop()
            self.current_frame.grid()
            self.current_frame.tkraise()

            if hasattr(self.current_frame, "refresh_page"):
                self.current_frame.refresh_page()


if __name__ == "__main__":
    app = App()
    app.mainloop()
