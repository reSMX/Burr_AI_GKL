import json
from pathlib import Path

from backend.   models import ResultMeas


def get_data(users_path: Path, user_id: str):
    with open(users_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if user_id in data:
        return ResultMeas(
            data_last_meas=data[user_id]['data_last_meas'],
            res_last_meas=data[user_id]['res_last_meas']
        )
    else:
        return None


def save_data(users_path: Path, user_id: str):
    with open(users_path, "r", encoding="utf-8") as file:
        data = json.load(file)
