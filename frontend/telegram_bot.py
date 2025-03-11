import dotenv
import asyncio
import os
from pathlib import Path
import requests
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import ParseMode

from backend.get_user_data import get_data
from backend.models import ResultMeas

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
        text="Привет! 👋\nОтправь голосовое сообщение или файл формата .mp3 для распознавания дефектов речи!",
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

        message_res = f"Дата последней проверки: {result_meas.data_last_meas.strftime('%Y-%m-%d %H:%M')}, обнаружена ли картавость: {'да' if result_meas.res_last_meas else 'нет'}"
    else:
        message_res = "Вы еще не проверяли есть ли у вас картавость!"

    await message.answer(
        text=message_res
    )


@dp.message(lambda message: message.audio or message.voice)
async def audio(message: types.Message):
    file_id = message.audio.file_id if message.audio else message.voice.file_id

    file = await bot.get_file(file_id)
    file_path = file.file_path
    destination = data_path / f"audio.mp3"

    await bot.download_file(file_path, destination=destination)

    # Обращение к API
    data_last_meas = datetime.now()
    res_last_meas = ...
    result_meas = ResultMeas(data_last_meas=data_last_meas, res_last_meas=res_last_meas)

    if destination.exists():
        destination.unlink()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
