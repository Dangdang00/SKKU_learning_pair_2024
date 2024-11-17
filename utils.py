import os
import csv
import uuid
import datetime

USER_FILE_PATH = "data/user.csv"
DATA_FILE_PATH = "data/data.csv"


def read_csv_user_info():
    user_info = None
    if not os.path.exists(USER_FILE_PATH):
        return user_info

    with open(USER_FILE_PATH, mode="r", encoding="utf-8") as file:
        data = file.read().splitlines()
        if len(data) > 1:
            user_info = {"id": 0, "name": data[1].split(",")[1]}
    return user_info


def read_csv_data_info():
    food_data_list = []

    if not os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "id",
                    "emoji_id",
                    "name",
                    "count",
                    "expiration_date",
                    "registration_date",
                ]
            )
        return food_data_list

    with open(DATA_FILE_PATH, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            food_data_list.append(
                {
                    "id": row.get("id"),
                    "emoji_id": row.get("emoji_id"),
                    "name": row.get("name"),
                    "count": int(row.get("count", 0)),
                    "expiration_date": row.get("expiration_date"),
                    "registration_date": datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
            )

    return food_data_list


def emoji_to_hex(emoji):
    return " ".join(f"0x{ord(char):X}" for char in emoji)


def insert_csv_data_info(emoji_id, name, count, expiration_date):
    with open(DATA_FILE_PATH, mode="a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        # 이모지를 유니코드 코드포인트로 변환
        emoji_hex = emoji_to_hex(emoji_id)

        id = str(uuid.uuid4())
        writer.writerow([id, emoji_hex, name, count, expiration_date])
        writer.writerow([])


def update_csv_data_info(id, emoji_id, name, count, expiration_date):
    temp_file_path = DATA_FILE_PATH + ".tmp"
    with open(
        DATA_FILE_PATH, mode="r", encoding="utf-8", newline=""
    ) as read_file, open(
        temp_file_path, mode="w", encoding="utf-8", newline=""
    ) as write_file:
        reader = csv.DictReader(read_file)

        fieldnames = [
            "id",
            "emoji_id",
            "name",
            "count",
            "expiration_date",
            "registration_date",
        ]
        writer = csv.DictWriter(write_file, fieldnames=fieldnames)

        writer.writeheader()

        for row in reader:
            if row["id"] == id:
                updated_row = {
                    "id": id,
                    "emoji_id": emoji_to_hex(emoji_id),
                    "name": name,
                    "count": count,
                    "expiration_date": expiration_date,
                    "registration_date": row.get("registration_date", ""),
                }
                print(f"[DEBUG] Updated row: {updated_row}")
                writer.writerow(updated_row)
            else:
                print(f"[DEBUG] Existing row: {row}")
                writer.writerow(row)

    os.replace(temp_file_path, DATA_FILE_PATH)


def delete_csv_data_info(id):
    temp_file_path = DATA_FILE_PATH + ".tmp"
    try:
        with open(
            DATA_FILE_PATH, mode="r", encoding="utf-8", newline=""
        ) as read_file, open(
            temp_file_path, mode="w", encoding="utf-8", newline=""
        ) as write_file:
            reader = csv.DictReader(read_file)

            fieldnames = [
                "id",
                "emoji_id",
                "name",
                "count",
                "expiration_date",
                "registration_date",
            ]
            writer = csv.DictWriter(write_file, fieldnames=fieldnames)

            writer.writeheader()

            deleted = False
            for row in reader:
                if row["id"] == id:
                    print(f"[INFO] Deleting row: {row}")
                    deleted = True
                else:
                    writer.writerow(row)

            if not deleted:
                print(f"[WARNING] No row found with ID: {id}")

        os.replace(temp_file_path, DATA_FILE_PATH)
        print(f"[INFO] Row with ID {id} successfully deleted.")
    except Exception as e:
        print(f"[ERROR] Failed to delete row: {e}")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def get_progress_value(expiration_date):
    today = datetime.date.today()
    expiration = datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date()

    # 유통기한 기준 계산
    if expiration >= today:
        # 남은 일수 계산 (D-7 기준으로 비율 계산)
        remaining_days = (expiration - today).days
        progress_value = max(0.0, min(1.0, (7 - remaining_days) / 7))
    else:
        # 유통기한이 지난 경우 진행률은 100%로 설정
        progress_value = 1.0

    return progress_value


def get_d_day(target_date):
    today = datetime.date.today()
    target_date = datetime.datetime.strptime(target_date, "%Y-%m-%d").date()
    delta = (target_date - today).days

    if delta < 0:
        return f"D+{-delta}"
    elif delta == 0:
        return "D-Day"
    else:
        return f"D-{delta}"
