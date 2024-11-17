import tkinter as tk
from datetime import datetime
from pages.detail import DetailPage
from utils import read_csv_data_info, get_progress_value, get_d_day


class ListPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sort_key = "registration_date"  # 기본 정렬 기준

        self.canvas = tk.Canvas(self, bg="#FFFFFF", width=393, height=852)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        self.scrollable_frame_id = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        header_container = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
        header_container.grid(row=0, column=0, sticky="ew", padx=16, pady=8)
        header_container.grid_columnconfigure(2, weight=1)

        self.arrow_icon = tk.PhotoImage(file="assets/arrow_left.png")
        arrow_icon_label = tk.Label(
            header_container,
            image=self.arrow_icon,
            width=24,
            height=24,
            bg="#FFFFFF",
            cursor="hand2",
        )
        arrow_icon_label.grid(row=0, column=0, padx=(0, 8))
        arrow_icon_label.bind("<Button-1>", lambda e: controller.go_back())

        header_label = tk.Label(
            header_container,
            text=(
                f"{controller.user_info['name']}님의 냉장고"
                if controller.user_info
                else "냉장고"
            ),
            bg="#FFFFFF",
            font=("Pretendard", 18, "bold"),
        )
        header_label.grid(row=0, column=1)

        self.add_icon = tk.PhotoImage(file="assets/add.png")
        add_icon_label = tk.Label(
            header_container,
            image=self.add_icon,
            width=24,
            height=24,
            bg="#FFFFFF",
            cursor="hand2",
        )
        add_icon_label.grid(row=0, column=2, sticky="se")
        add_icon_label.bind("<Button-1>", lambda e: controller.show_frame(DetailPage))

        self.summary_container = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
        self.summary_container.grid(row=1, column=0, sticky="ew", padx=16)

        self.summary_container.grid_columnconfigure(0, weight=1)
        self.summary_container.grid_columnconfigure(1, weight=0)

        self.total_count_label = tk.Label(
            self.summary_container,
            text="",
            font=("Pretendard", 13),
            bg="#FFFFFF",
        )
        self.total_count_label.grid(row=0, column=0, sticky="w")

        filtered_container = tk.Frame(self.summary_container, bg="#FFFFFF")
        self.register_label = tk.Label(
            filtered_container,
            text="등록순",
            font=("Pretendard", 12),
            bg="#FFFFFF",
            cursor="hand2",
        )
        self.expiration_label = tk.Label(
            filtered_container,
            text="유통기한순",
            font=("Pretendard", 12),
            bg="#FFFFFF",
            cursor="hand2",
        )
        self.register_label.grid(row=0, column=0)
        tk.Label(
            filtered_container,
            text="|",
            font=("Pretendard", 12),
            fg="#757575",
            bg="#FFFFFF",
        ).grid(row=0, column=1)
        self.expiration_label.grid(row=0, column=2)
        filtered_container.grid(row=0, column=1, sticky="e")

        self.register_label.bind(
            "<Button-1>", lambda e: self.sort_by("registration_date")
        )
        self.expiration_label.bind(
            "<Button-1>", lambda e: self.sort_by("expiration_date")
        )

        self.food_list_container = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
        self.food_list_container.grid(row=2, column=0, sticky="ew", padx=16, pady=8)
        self.food_list_container.grid_columnconfigure(0, weight=1)

        self.refresh_page()

    def refresh_page(self):
        food_data_list = read_csv_data_info()
        food_data_list.sort(key=lambda x: x.get(self.sort_key))

        self.total_count_label.config(text=f"전체 {len(food_data_list)}")

        for widget in self.food_list_container.winfo_children():
            widget.destroy()

        for index, item in enumerate(food_data_list):
            item_container = tk.Frame(
                self.food_list_container, bg="#FFFFFF", cursor="hand2"
            )
            item_container.grid(row=index, column=0, sticky="ew", padx=0, pady=8)
            item_container.grid_columnconfigure(1, weight=1)

            item_container.bind(
                "<Button-1>",
                lambda e, data=item: self.controller.show_frame(
                    DetailPage, isAdd=False, data=data
                ),
            )

            canvas = tk.Canvas(
                item_container, width=80, height=80, bg="#FFFFFF", highlightthickness=0
            )
            canvas.create_oval(0, 0, 80, 80, fill="#F5F5F5", outline="#F5F5F5")
            emoji_id = chr(int(item["emoji_id"], 16))
            canvas.create_text(40, 40, text=emoji_id, font=("Pretendard", 36))
            canvas.grid(row=0, column=0, rowspan=3, padx=(0, 16), sticky="w")

            food_label = tk.Label(
                item_container,
                text=item["name"],
                fg="Black",
                bg="#FFFFFF",
                font=("Pretendard", 16, "bold"),
            )
            food_label.grid(row=0, column=1, sticky="w")

            expiration_text = (
                f"~{item['expiration_date']}까지"
                if item.get("expiration_date")
                else "-"
            )
            food_summary = tk.Label(
                item_container,
                text=f"{expiration_text} | {item['count']}개",
                fg="Gray",
                bg="#FFFFFF",
                font=("Pretendard", 12),
            )
            food_summary.grid(row=1, column=1, sticky="w")

            progress_bar_canvas = tk.Canvas(
                item_container, width=200, height=8, bg="#F8F8F8", highlightthickness=0
            )
            progress_bar_canvas.grid(row=2, column=1, sticky="w")
            progress_value = get_progress_value(item["expiration_date"])
            progress_bar_canvas.create_rectangle(
                0, 0, 200 * progress_value, 8, fill="#84DC83", outline=""
            )

            food_d_day = tk.Label(
                item_container,
                text=get_d_day(item["expiration_date"]),
                fg="Gray",
                bg="#FFFFFF",
                font=("Pretendard", 16, "bold"),
            )
            food_d_day.grid(row=0, column=2, rowspan=3, padx=(20, 0), sticky="e")

        self.update_filter_colors()

    def sort_by(self, key):
        self.sort_key = key
        self.refresh_page()

    def update_filter_colors(self):
        if self.sort_key == "registration_date":
            self.register_label.config(fg="Black")
            self.expiration_label.config(fg="#757575")
        elif self.sort_key == "expiration_date":
            self.register_label.config(fg="#757575")
            self.expiration_label.config(fg="Black")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.scrollable_frame_id, width=canvas_width)
