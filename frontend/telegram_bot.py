import json

import dotenv
import asyncio
import os
from pathlib import Path
import requests
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import ParseMode

from backend.get_user_data import get_data, save_data
from backend.models import ResultMeas
from backend.trans_audio import trans_audio

project_path = Path.cwd().parent
data_path = project_path / "data"
data_path.mkdir(exist_ok=True)
users_path = project_path / "data" / "users.json"

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_message(message: types.Message):
    await message.answer(
        text="<b>Привет!</b> 👋\nОтправь голосовое сообщение или файл формата .mp3 для распознавания дефектов речи!\nНапиши /profile чтобы узнать время и результат последней проверки!",
        parse_mode=ParseMode.HTML
    )


@dp.message(Command("profile"))
async def profile_message(message: types.Message):
    user_id = str(message.from_user.id)

    result = get_data(users_path, user_id)
    if result:
        result_meas = ResultMeas(
            data_last_meas=result.data_last_meas,
            res_last_meas=result.res_last_meas
        )

        message_res = f"<b>Дата последней проверки:</b> {result_meas.data_last_meas.strftime('%Y-%m-%d %H:%M')}\n<b>Обнаружена ли картавость:</b> {'да' if result_meas.res_last_meas else 'нет'}"
    else:
        message_res = "Вы еще не проверяли есть ли у вас картавость"

    await message.answer(
        text=message_res,
        parse_mode=ParseMode.HTML
    )


@dp.message(lambda message: message.audio or message.voice)
async def audio(message: types.Message):
    user_id = str(message.from_user.id)
    file_id = message.audio.file_id if message.audio else message.voice.file_id

    file = await bot.get_file(file_id)
    file_path = file.file_path
    destination = data_path / f"audio_{user_id}.mp3"

    await bot.download_file(file_path, destination=destination)

    data_last_meas = datetime.now()
    translated_audio, sr = trans_audio(destination)

    data = json.dumps({
        "y": translated_audio,
        "sr": sr
    })

    response = requests.post(url=f"http://127.0.0.1:8000/libr_audio/", data=data)
    print(response.status_code)

    res_last_meas = response.json()["burr"]
    result_meas = ResultMeas(data_last_meas=data_last_meas, res_last_meas=res_last_meas)

    if res_last_meas:
        message_res = "<b>У вас обнаружена картавость</b>❌"
    else:
        message_res = "<b>У вас не обнаружено картавости</b>✅"

    await message.reply(
        text=message_res,
        parse_mode=ParseMode.HTML
    )

    save_data(users_path, user_id, result_meas)

    if destination.exists():
        destination.unlink()


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
