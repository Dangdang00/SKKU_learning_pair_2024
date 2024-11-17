import tkinter as tk
from datetime import datetime
from pages.list import ListPage
from utils import read_csv_data_info, get_progress_value, get_d_day

STATUS = {
    "PLENTY": {
        "value": "여유",
        "message": "아직 여유가 있어요! 안심하고 관리하세요!",
        "emoji": "👍",
    },
    "NEAR": {
        "value": "임박",
        "message": "유통기한 임박! 서둘러 사용하세요.",
        "emoji": "⚠️",
    },
    "EXPIRED": {
        "value": "만료",
        "message": "주의! 유통기한이 지났어요. 확인 후 정리해주세요!",
        "emoji": "🚨",
    },
    "UNREG": {
        "value": "미등록",
        "message": "유통기한이 등록되지 않은 식품이에요.",
        "emoji": "☠️",
    },
}


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        user_name = controller.user_info["name"] if controller.user_info else ""

        root_container = tk.Frame(self, width=393, height=852, bg="#FFFFFF")
        root_container.grid_propagate(False)
        root_container.grid(row=0, column=0)

        header_container = tk.Frame(root_container, bg="#FFFFFF", height=56)
        header_container.grid(row=0, column=0, sticky="ew", padx=16)

        header_container.grid_propagate(False)
        header_container.grid_rowconfigure(0, weight=1)

        header_label = tk.Label(
            header_container,
            text="🍴냉장고를 부탁해!",
            bg="#FFFFFF",
            font=("Pretendard", 18, "bold"),
        )
        header_label.grid(row=0, column=0)

        self.summary_container = tk.Frame(root_container, bg="#F8F8F8")
        self.summary_container.grid(row=1, column=0, padx=16, sticky="ew")

        self.summary_container.grid_rowconfigure(0, weight=1)
        self.summary_container.grid_columnconfigure(0, weight=0)
        self.summary_container.grid_columnconfigure(1, weight=0)

        self.status_emoji_label = tk.Label(
            self.summary_container, text="👍", bg="#F8F8F8", font=("Pretendard", 24)
        )
        self.user_label = tk.Label(
            self.summary_container,
            text=f"{user_name}님의 냉장고,",
            bg="#F8F8F8",
            font=("Pretendard", 14),
        )
        self.status_label = tk.Label(
            self.summary_container,
            text="아직 여유가 있어요! 안심하고 관리하세요!",
            bg="#F8F8F8",
            font=("Pretendard", 14),
        )

        self.status_emoji_label.grid(row=0, column=0, rowspan=2, padx=16, sticky="w")
        self.user_label.grid(row=0, column=1, pady=(10, 0), sticky="w")
        self.status_label.grid(row=1, column=1, pady=(0, 10))

        self.status_button_container = tk.Frame(root_container, bg="#FFFFFF")
        self.status_button_container.grid(
            row=2, column=0, sticky="we", padx=16, pady=12
        )

        for i in range(4):
            self.status_button_container.grid_columnconfigure(i, weight=1)

        self.plenty_button = tk.Label(
            self.status_button_container,
            text="여유",
            fg="#FFFFFF",
            bg="#84DC83",
            height=2,
            font=("Pretendard", 14),
            cursor="hand2",
        )
        self.plenty_button.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        self.plenty_button.bind("<Button-1>", lambda e: self.set_status("PLENTY"))

        self.near_button = tk.Label(
            self.status_button_container,
            text="임박",
            fg="#757575",
            bg="#F5F5F5",
            height=2,
            font=("Pretendard", 14),
            cursor="hand2",
        )
        self.near_button.grid(row=0, column=1, padx=(0, 8), sticky="ew")
        self.near_button.bind("<Button-1>", lambda e: self.set_status("NEAR"))

        self.expired_button = tk.Label(
            self.status_button_container,
            text="만료",
            fg="#757575",
            bg="#F5F5F5",
            height=2,
            font=("Pretendard", 14),
            cursor="hand2",
        )
        self.expired_button.grid(row=0, column=2, padx=(0, 8), sticky="ew")
        self.expired_button.bind("<Button-1>", lambda e: self.set_status("EXPIRED"))

        self.unreg_button = tk.Label(
            self.status_button_container,
            text="미등록",
            fg="#757575",
            bg="#F5F5F5",
            height=2,
            font=("Pretendard", 14),
            cursor="hand2",
        )
        self.unreg_button.grid(row=0, column=3, sticky="ew")
        self.unreg_button.bind("<Button-1>", lambda e: self.set_status("UNREG"))

        self.food_list_container = tk.Frame(root_container, bg="#FFFFFF")
        self.food_list_container.grid(row=3, column=0, sticky="ew", padx=16, pady=8)
        self.food_list_container.grid_columnconfigure(0, weight=1)

        self.refresh_page()
        self.detail_container = tk.Frame(
            root_container, bg="#84DC83", highlightthickness=0, padx=1, pady=1
        )
        self.detail_container.grid(row=8, column=0, padx=16, pady=(4, 16), sticky="ew")

        self.detail_container.grid_columnconfigure(0, weight=1)

        self.detail_button = tk.Label(
            self.detail_container,
            text="냉장고 정리하기",
            height=2,
            fg="#84DC83",
            bg="#FFFFFF",
            cursor="hand2",
        )
        self.detail_button.grid(row=0, column=0, sticky="ew")

        self.detail_button.bind("<Button-1>", lambda e: controller.show_frame(ListPage))

        footer_container = tk.Frame(root_container, bg="#F8F8F8")
        footer_container.grid(row=10, column=0, sticky="ew")

        team_name_label = tk.Label(
            footer_container,
            text="팀 황금조이🌟",
            fg="#8A8A8E",
            bg="#F8F8F8",
            font=("Pretendard", 14, "bold"),
        )
        team_name_label.grid(row=0, column=0, padx=16, pady=(16, 0), sticky="w")

        member_name_label = tk.Label(
            footer_container,
            text="성균관대학교 응용AI융합학부 김예은, 이효정, 조민영, 황다영",
            fg="#8A8A8E",
            bg="#F8F8F8",
            font=("Pretendard", 12),
        )
        member_name_label.grid(row=1, column=0, padx=16, sticky="w")

        copyright_label = tk.Label(
            footer_container,
            text="© 2024 황금조이 All Rights Reserved",
            fg="#8A8A8E",
            bg="#F8F8F8",
            font=("Pretendard", 10),
        )
        copyright_label.grid(row=2, column=0, padx=16, pady=16, sticky="w")

        rows = root_container.grid_size()[1]
        for i in range(rows):
            root_container.grid_rowconfigure(i, weight=0)
        root_container.grid_columnconfigure(0, weight=1)

    def set_status(self, status_key):
        self.status_emoji_label.config(text=STATUS[status_key]["emoji"])
        self.status_label.config(text=STATUS[status_key]["message"])

        status_colors = {
            "PLENTY": "#84DC83",
            "NEAR": "#FFC942",
            "EXPIRED": "#F76464",
            "UNREG": "#757575",
        }
        progress_fill_color = status_colors.get(status_key, "#84DC83")

        buttons = {
            "PLENTY": self.plenty_button,
            "NEAR": self.near_button,
            "EXPIRED": self.expired_button,
            "UNREG": self.unreg_button,
        }

        for key, button in buttons.items():
            if key == status_key:
                button.config(bg=progress_fill_color, fg="#FFFFFF")
                self.detail_container.config(bg=progress_fill_color)
                self.detail_button.config(fg=progress_fill_color)
            else:
                button.config(bg="#F5F5F5", fg="#757575")

        food_data_list = read_csv_data_info()
        filtered_data = self.filter_food_data(food_data_list, status_key)
        self.refresh_page(filtered_data, progress_fill_color)

    def filter_food_data(self, food_data_list, status_key):
        filtered_data = []
        for item in food_data_list:
            d_day_str = get_d_day(item["expiration_date"])
            d_day = None

            # d_day_str을 숫자로 변환
            if d_day_str == "D-Day":
                d_day = 0
            elif d_day_str.startswith("D-"):
                d_day = int(d_day_str[2:])
            elif d_day_str.startswith("D+"):
                d_day = -int(d_day_str[2:])

            # 필터링 조건
            if status_key == "PLENTY" and d_day is not None and d_day > 3:
                filtered_data.append(item)
            elif status_key == "NEAR" and d_day is not None and 0 <= d_day <= 3:
                filtered_data.append(item)
            elif status_key == "EXPIRED" and d_day is not None and d_day < 0:
                filtered_data.append(item)
            elif status_key == "UNREG" and not item.get("expiration_date"):
                filtered_data.append(item)

        return filtered_data

    def refresh_page(self, food_data_list=None, progress_fill_color="#84DC83"):
        if food_data_list is None:
            food_data_list = self.filter_food_data(read_csv_data_info(), "PLENTY")

        food_data_list.sort(
            key=lambda x: (
                datetime.strptime(x["expiration_date"], "%Y-%m-%d")
                if x.get("expiration_date")
                else datetime.max
            )
        )

        for widget in self.food_list_container.winfo_children():
            widget.destroy()

        for index, item in enumerate(food_data_list[:5]):
            item_container = tk.Frame(self.food_list_container, bg="#FFFFFF")
            item_container.grid(row=index, column=0, sticky="ew", padx=0, pady=8)
            item_container.grid_columnconfigure(1, weight=1)

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
                0, 0, 200 * progress_value, 8, fill=progress_fill_color, outline=""
            )

            food_d_day = tk.Label(
                item_container,
                text=get_d_day(item["expiration_date"]),
                fg="Gray",
                bg="#FFFFFF",
                font=("Pretendard", 16, "bold"),
            )
            food_d_day.grid(row=0, column=2, rowspan=3, padx=(20, 0), sticky="e")

        for index in range(len(food_data_list), 5):
            item_container = tk.Frame(self.food_list_container, bg="#FFFFFF", height=80)
            item_container.grid(row=index, column=0, sticky="ew", padx=0, pady=8)
            item_container.grid_columnconfigure(0, weight=1)
