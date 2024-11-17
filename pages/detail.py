import tkinter as tk
import re
import random
from tkinter import messagebox
from datetime import datetime
from utils import insert_csv_data_info, update_csv_data_info, delete_csv_data_info


EMOJI_RANGES = [(0x1F950, 0x1F96F)]


def get_random_emoji():
    start, end = random.choice(EMOJI_RANGES)
    return chr(random.randint(start, end))


class DetailPage(tk.Frame):
    def __init__(self, parent, controller, isAdd=True, data=None):
        super().__init__(parent)
        self.controller = controller
        self.isAdd = isAdd
        self.data = data

        self.init_ui()

    def update_content(self, isAdd=True, data=None):
        self.isAdd = isAdd
        self.data = data

        self.name_field.delete(0, tk.END)
        self.count_field.delete(0, tk.END)
        self.expiration_date_field.delete(0, tk.END)

        if self.data:
            self.populate_fields()
        else:
            self.canvas.itemconfigure(self.emoji_id, text=get_random_emoji())

        self.update_buttons()

    def init_ui(self):
        user_name = (
            self.controller.user_info["name"] if self.controller.user_info else ""
        )

        root_container = tk.Frame(self, width=393, height=852, bg="#FFFFFF")
        root_container.grid_propagate(False)
        root_container.grid(row=0, column=0)

        header_container = tk.Frame(root_container, bg="#FFFFFF", height=56)
        header_container.grid(row=0, column=0, sticky="ew", padx=16)

        header_container.grid_propagate(False)
        header_container.grid_rowconfigure(0, weight=1)
        header_container.grid_columnconfigure(0, weight=0)
        header_container.grid_columnconfigure(1, weight=0)
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
        arrow_icon_label.bind("<Button-1>", lambda e: self.controller.go_back())

        header_label = tk.Label(
            header_container,
            text=f"{user_name}님의 냉장고",
            bg="#FFFFFF",
            font=("Pretendard", 18, "bold"),
        )
        header_label.grid(row=0, column=1)

        self.init_form(root_container)

        self.init_buttons(root_container)

    def init_form(self, root_container):
        form_container = tk.Frame(root_container, bg="#FFFFFF")
        form_container.grid(row=1, column=0, sticky="new")
        root_container.grid_rowconfigure(1, weight=1)
        root_container.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            form_container,
            width=200,
            height=200,
            bg="#FFFFFF",
            highlightthickness=0,
            cursor="hand2",
        )

        x0, y0, x1, y1 = 0, 0, 200, 200
        self.canvas.create_oval(x0, y0, x1, y1, fill="#F5F5F5", outline="#F5F5F5")

        self.emoji_id = self.canvas.create_text(
            (x0 + x1) / 2,
            (y0 + y1) / 2,
            text=get_random_emoji(),
            font=("Pretendard", 56),
        )

        self.canvas.bind("<Button-1>", self.change_emoji)
        self.canvas.grid(row=0, column=0, pady=(16, 32))

        input_outline_container = tk.Frame(form_container, bg="#C4C4C4", bd=1)
        input_outline_container.grid(row=1, column=0)

        input_container = tk.Frame(input_outline_container, bg="#FFFFFF", height=100)
        input_container.grid(row=1, column=0)

        self.name_field = tk.Entry(
            input_container,
            relief="flat",
            highlightthickness=0,
            font=("Pretendard", 16),
        )
        self.name_field.pack(fill="x", padx=4, pady=4)

        line = tk.Frame(form_container, bg="#C4C4C4", width=393, height=1)
        line.grid(row=2, column=0, pady=28, sticky="ew")

        food_info = tk.Label(
            form_container,
            text="식품 정보",
            bg="#FFFFFF",
            font=("Pretendard", 16, "bold"),
        )
        food_info.grid(row=3, column=0, sticky="w", padx=16)

        food_count_container = tk.Frame(form_container, bg="#FFFFFF")
        food_count_container.grid(row=4, column=0, padx=32, pady=16, sticky="ew")
        form_container.grid_columnconfigure(0, weight=1)

        food_count_label = tk.Label(
            food_count_container,
            text="보유 개수*",
            bg="#FFFFFF",
            font=("Pretendard", 14),
        )
        food_count_label.grid(row=1, column=0, pady=(0, 4), sticky="w")

        input_outline_container = tk.Frame(food_count_container, bg="#C4C4C4", bd=1)
        input_outline_container.grid(row=2, column=0, sticky="ew")
        food_count_container.grid_columnconfigure(0, weight=1)
        input_outline_container.grid_columnconfigure(0, weight=1)

        input_container = tk.Frame(input_outline_container, bg="#FFFFFF", height=100)
        input_container.grid(row=2, column=0, sticky="ew")
        input_container.grid_columnconfigure(0, weight=1)

        self.count_field = tk.Entry(
            input_container,
            relief="flat",
            highlightthickness=0,
            font=("Pretendard", 16),
        )
        self.count_field.grid(row=1, column=0, padx=4, pady=4, sticky="ew")
        self.count_error_label = tk.Label(
            food_count_container,
            text="",
            bg="#FFFFFF",
            font=("Pretendard", 12),
            fg="red",
            anchor="w",
        )
        self.count_error_label.grid(row=3, sticky="w", pady=2)

        expiration_date_container = tk.Frame(form_container, bg="#FFFFFF")
        expiration_date_container.grid(row=5, column=0, padx=32, pady=16, sticky="ew")

        expiration_date_label = tk.Label(
            expiration_date_container,
            text="유통기한*",
            bg="#FFFFFF",
            font=("Pretendard", 14),
        )
        expiration_date_label.grid(row=1, column=0, pady=(0, 4), sticky="w")

        input_outline_container = tk.Frame(
            expiration_date_container, bg="#C4C4C4", bd=1
        )
        input_outline_container.grid(row=2, column=0, sticky="ew")
        expiration_date_container.grid_columnconfigure(0, weight=1)
        input_outline_container.grid_columnconfigure(0, weight=1)

        input_container = tk.Frame(input_outline_container, bg="#FFFFFF", height=100)
        input_container.grid(row=2, column=0, sticky="ew")
        input_container.grid_columnconfigure(0, weight=1)

        self.expiration_date_field = tk.Entry(
            input_container,
            relief="flat",
            highlightthickness=0,
            font=("Pretendard", 16),
        )
        self.expiration_date_field.grid(row=1, column=0, padx=4, pady=4, sticky="ew")
        self.expiration_date_error_label = tk.Label(
            expiration_date_container,
            text="",
            bg="#FFFFFF",
            font=("Pretendard", 12),
            fg="red",
            anchor="w",
        )
        self.expiration_date_error_label.grid(row=3, sticky="w", pady=2)

    def init_buttons(self, root_container):
        button_container = tk.Frame(root_container, bg="#FFFFFF")
        button_container.grid(row=2, column=0, sticky="ew", padx=16, pady=12)

        button_container.grid_columnconfigure(0, weight=1)
        button_container.grid_columnconfigure(1, weight=1)

        self.cancel_button = tk.Label(
            button_container,
            text="취소",
            fg="#757575",
            bg="#F5F5F5",
            height=2,
            font=("Pretendard", 14),
            cursor="hand2",
        )
        self.cancel_button.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.submit_button = tk.Label(
            button_container,
            text="추가",
            fg="#FFFFFF",
            bg="#84DC83",
            height=2,
            font=("Pretendard", 14),
            cursor="hand2",
        )
        self.submit_button.grid(row=0, column=1, sticky="ew")

        self.update_buttons()

    def update_buttons(self):
        action_text = "추가" if self.isAdd else "수정"

        self.submit_button.config(text=action_text, bg="#84DC83")
        self.submit_button.bind(
            "<Button-1>",
            lambda e: self.on_submit(),
        )

        if self.isAdd:
            self.cancel_button.config(
                text="취소",
                bg="#F5F5F5",
                fg="#757575",
            )
            self.cancel_button.bind("<Button-1>", lambda e: self.controller.go_back())
        else:
            self.cancel_button.config(
                text="삭제",
                bg="#F5F5F5",
                fg="#757575",
            )
            self.cancel_button.bind("<Button-1>", lambda e: self.on_delete())

    def change_emoji(self, event=None):
        emoji_id = get_random_emoji()
        self.canvas.itemconfigure(self.emoji_id, text=emoji_id)

    def validate_count(self, text):
        if text.isdigit():
            return True
        else:
            self.count_error_label.config(text="숫자만 입력해주세요!")
            return False

    def validate_date(self, text):
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        if re.fullmatch(pattern, text):
            try:
                datetime.strptime(text, "%Y-%m-%d")
                return True
            except ValueError:
                self.expiration_date_error_label.config(
                    text="유효하지 않은 날짜입니다. 올바른 날짜를 입력해주세요!"
                )
                return False
        else:
            self.expiration_date_error_label.config(
                text="yyyy-mm-dd 형식으로 입력해주세요!"
            )
            return False

    def get_input_field(self):
        emoji_id = self.canvas.itemcget(self.emoji_id, "text")
        name = self.name_field.get()
        count = self.count_field.get()
        expiration_date = self.expiration_date_field.get()
        return emoji_id, name, count, expiration_date

    def populate_fields(self):
        if self.data:
            self.name_field.insert(0, self.data.get("name", ""))
            self.count_field.insert(0, self.data.get("count", ""))
            self.expiration_date_field.insert(0, self.data.get("expiration_date", ""))

            emoji_code = self.data.get("emoji_id", "")
            emoji_char = (
                chr(int(emoji_code, 16)) if emoji_code.startswith("0x") else emoji_code
            )
            self.canvas.itemconfigure(self.emoji_id, text=emoji_char)
        else:
            self.canvas.itemconfigure(self.emoji_id, text=get_random_emoji())

    def on_delete(self):
        if not self.data or "id" not in self.data:
            print("[ERROR] 삭제할 데이터가 없습니다.")
            return

        confirm = messagebox.askyesno(
            "삭제 확인", f"이 식품을 정말로 삭제하시겠습니까?"
        )
        if not confirm:
            return

        print(f"[DEBUG] Deleting item: {self.data['id']}")
        delete_csv_data_info(self.data["id"])

        self.controller.go_back()

    def on_submit(self):
        emoji_id, name, count, expiration_date = self.get_input_field()

        if not self.validate_count(count) or not self.validate_date(expiration_date):
            return

        print(emoji_id, name, count, expiration_date)

        if self.isAdd:
            print(
                f"[DEBUG] Adding item: {emoji_id}, {name}, {count}, {expiration_date}"
            )
            insert_csv_data_info(emoji_id, name, count, expiration_date)
        else:
            print(
                f"[DEBUG] Updating item: {emoji_id}, {name}, {count}, {expiration_date}"
            )
            update_csv_data_info(
                self.data["id"], emoji_id, name, count, expiration_date
            )

        self.controller.go_back()
